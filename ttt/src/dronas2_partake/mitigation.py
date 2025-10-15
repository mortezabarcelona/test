import logging
from typing import Optional, Iterable

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel, IntVar, Domain, CpSolver, LinearExpr

from dronas2_partake.model import PartakeMission, PartakeConflict
from dronas2_partake.utils.cpmodels import Solution, State, SingleRunner_Abstract, Model, MultipleRunner_Abstract, Objective


class MitigationSolution(Solution):

    def __init__(self):
        self.delays: Optional[dict[PartakeMission, int | None]] = None
        self._objective_value: Optional[int] = None

        self._state: Optional[State] = None

    def is_solved(self):
        return self._state in [State.SOLVED_OPTIMAL, State.SOLVED_FEASIBLE]

    def get_presence_count(self):
        count = 0
        for m, v in self.delays.keys():
            if v is not None:
                count += 1
        return count

    def get_result_delay(self, mission: PartakeMission):
        if mission not in self.delays.keys():
            raise Exception("Mission not in the problem")
        return self.delays[mission]

    def get_objective_value(self):
        return self._objective_value


class SingleRunner(MitigationSolution, SingleRunner_Abstract):

    def __init__(self, algorithm: 'MitigationAlgorithm_Abstract', max_compute_time=10):
        MitigationSolution.__init__(self)
        SingleRunner_Abstract.__init__(self, algorithm, max_compute_time)


class MultipleRunner(MitigationSolution, MultipleRunner_Abstract):

    def __init__(self, algorithm: 'MitigationAlgorithm_Abstract', max_compute_time=10):
        MitigationSolution.__init__(self)
        MultipleRunner_Abstract.__init__(self, algorithm, max_compute_time)


class MitigationAlgorithm_Abstract(Model):

    def __init__(
            self,
            missions: Iterable[PartakeMission],
            conflicts: list[PartakeConflict],
            objective: Objective,
            precision_seconds: int,
            logger: logging.Logger
     ):

        self.logger = logger
        self.objective: Objective = objective
        self.resolution_seconds: int = precision_seconds

        self._missions: Iterable[PartakeMission] = missions
        self._conflicts: list[PartakeConflict] = conflicts
        self._model: Optional[CpModel] = None

        self._built: bool = False

        self._dvDelays: dict[PartakeMission, IntVar] = {}
        self._dvDelayDifferences: dict[PartakeConflict, IntVar] = {}

    def _make_populate(self):
        self._make_populate_delays()
        self._make_populate_conflicts()

    def _make_populate_delays(self):
        for m in self._missions:
            self._make_populate_delays_mission(m)

    def _make_populate_delays_mission(self, m):
        if m.constant_mitigation_delay is not None:
            # Regulated traffic
            self._dvDelays[m] = self._model.new_constant(m.constant_mitigation_delay)
        else:
            # Normal traffic
            if self.resolution_seconds == 1:
                self._dvDelays[m] = self._model.new_int_var(
                    -m.launch_window_lower,
                    m.launch_window_upper,
                    f"Delay for {m}"
                )

            else:
                self._dvDelays[m] = self._model.new_int_var_from_domain(
                    # Need to split the domain in two parts to ensure the 0 is in the domain
                    Domain.FromValues([
                        *(-v for v in range(self.resolution_seconds, m.launch_window_lower+1)), # negative domain
                        *(v for v in range(0, m.launch_window_upper+1)) # positive domain
                    ]),
                    #     list(range(
                    #     -m.launch_window_lower,
                    #     m.launch_window_upper + 1,
                    #     self.resolution_seconds
                    # ))),
                    f"Delay for {m}"
                )

            if m.constant_mitigation_delay_hint is not None:
                self._model.add_hint(self._dvDelays[m], m.constant_mitigation_delay_hint)

    def _make_populate_conflicts(self):
        for c in self._conflicts:
            self._make_populate_conflicts_conflict(c)

    def _make_populate_conflicts_conflict(self, c):
        # Each conflict must be solved by moving the missions, so the diffs in the conflicts are already restricted,
        # but we compute the bounds of each difference to guide the algorithm.

        # In this method we only populate the variables with a maximum and minimum.
        # The equality (difference = delay1 - delay2), and the forbidden intervals are computed in constraints()

        min_domain_diff = (-c.mission1.launch_window_lower) - c.mission2.launch_window_upper
        max_domain_diff = c.mission1.launch_window_upper - (-c.mission2.launch_window_lower)

        if min_domain_diff > max_domain_diff:
            min_domain_diff, max_domain_diff = max_domain_diff, min_domain_diff

        if self.resolution_seconds == 1:
            self._dvDelayDifferences[c] = self._model.new_int_var(
                min_domain_diff,
                max_domain_diff,
                f"DelayDifference for {c}"
            )
        else:
            self._dvDelayDifferences[c] = self._model.new_int_var_from_domain(
                # Need to split the domain in two parts to ensure the 0 is in the domain
                Domain.FromValues([
                    *(-v for v in range(self.resolution_seconds, -min_domain_diff+1)), # negative domain
                    *(v for v in range(0, max_domain_diff+1)) # positive domain
                ]),
                # Domain.FromValues(list(range(
                #     min_domain_diff,
                #     max_domain_diff + 1,
                #     self.resolution_seconds
                # ))),
                f"DelayDifference for {c}"
            )

    # noinspection PyMethodMayBeStatic
    def _check_if_need_to_execute(self) -> bool:
        """
        The algorithm is needed to be executed if any real conflicts
        :return:
        """

        return True

        # The code below is commented because there is a bug when missions are fixed at a specified delay.
        # Conflict might not be real, but at that delay, they are.
        # if self.objective != Objective.FEASIBILITY:
        #     return True
        #
        # for c in self._conflicts:
        #     if c.worst_clearance > 0:
        #         return True
        # return False

    def _make_constraints(self):
        for c in self._conflicts:
            self._make_constraints_conflict(c)

    def _make_constraints_conflict(self, c: PartakeConflict):

        d1 = self._dvDelays[c.mission1]
        d2 = self._dvDelays[c.mission2]
        diff = self._dvDelayDifferences[c]

        self._model.add(diff == d1 - d2)

        self._make_constraints_conflict_differenceNotZero(diff, c)

        for begin, end in c.forbidden_intervals:
            self._make_constraints_conflict_forbidden_interval(diff, c, begin, end)

    def _make_constraints_conflict_differenceNotZero(self, diff: IntVar, c: PartakeConflict):

        # worstClearance have tolerances included.
        # So greater than worstClearance > 0, means conflict, and has to be resolved (diff != 0)
        if c.worst_clearance > 0:
            self._model.add(diff != 0)

    def _make_constraints_conflict_forbidden_interval(self, diff: IntVar, c: PartakeConflict, begin: int, end: int):
        # // Add NO OVERLAP restriction of this interval.
        # // This boolean tells if the current value (of difference) is before or after the interval.
        # BoolVar AC1AC2 = model.newBoolVar(
        #     dvNameCorrector.apply(
        #         "Conflict between: " + delays.indexOf(conf.mission1) + " -> " + delays.indexOf(conf.mission2)
        #     )
        # );
        # model.addLessThan(difference, interval.getBegin()).onlyEnforceIf(AC1AC2);
        # model.addGreaterOrEqual(difference, interval.getEnd()).onlyEnforceIf(AC1AC2.not());

        before_or_after = self._model.new_bool_var(f"Conflict between {c.mission1} and {c.mission2} at forbidden interval {begin} -> {end}")

        self._model.add(diff < begin).only_enforce_if(before_or_after)
        self._model.add(diff >= end).only_enforce_if(before_or_after.negated())

    def _make_objective(self):
        pass

    def run_single(self, max_compute_time=10) -> SingleRunner:

        if self._model is None:
            self._build()

        return SingleRunner(self, max_compute_time=max_compute_time)

    def run_multiple(self, max_compute_time=10) -> MultipleRunner:

        if self._model is None:
            self._build()

        return MultipleRunner(self, max_compute_time=max_compute_time)

    def _build(self):

        self._model = cp_model.CpModel()
        if self._check_if_need_to_execute():
            self._make_populate()
            self._make_constraints()
            if self.objective == Objective.OPTIMALITY:
                self._make_objective()

    def extract_solution(self, solution: MitigationSolution, extractor):
        solution.delays = {}
        for m, dv in self._dvDelays.items():
            value = extractor.value(dv)
            solution.delays[m] = value

    # @property
    def get_model(self):
        return self._model


class MitigationAlgorithm_Enumeration(MitigationAlgorithm_Abstract):

    def __init__(
            self,
            missions: list[PartakeMission],
            conflicts: list[PartakeConflict],
            objective: Objective=Objective.OPTIMALITY,
            precision_seconds=60,
            logger: logging.Logger=logging.getLogger('MitigationAlgorithm_Enumeration')
    ):
        super().__init__(missions, conflicts, objective, precision_seconds, logger)

        self._objective_expr: Optional[LinearExpr] = None

    def _make_objective(self):
        def add_abs_equality_return_dv(dv: IntVar, expr: LinearExpr) -> IntVar:
            self._model.add_abs_equality(dv, expr)
            return dv

        self._objective_expr = LinearExpr.Sum([
            add_abs_equality_return_dv(
                # Variable that represents the absolute value of 'dv'
                self._model.new_int_var(0, max(m.launch_window_lower, m.launch_window_upper), f"Inverse of: {dv}"),
                dv
            )
            for m, dv in self._dvDelays.items()
        ])

        self._model.minimize(self._objective_expr)

    def extract_solution(self, solution: MitigationSolution, extractor: CpSolver):
        super().extract_solution(solution, extractor)
        if self._objective_expr is not None:
            solution._objective_value = extractor.value(self._objective_expr)


class MitigationAlgorithm_Batch(MitigationAlgorithm_Abstract):

    def __init__(
            self,
            missions: Iterable[PartakeMission], conflicts: list[PartakeConflict],
            precision_seconds=1,
            minimum_approved=None,
            logger: logging.Logger=logging.getLogger('MitigationAlgorithm_Batch')
    ):
        super().__init__(
            missions,
            conflicts,
            Objective.OPTIMALITY if minimum_approved is None else Objective.FEASIBILITY,
            precision_seconds,
            logger
        )
        self.minimum_approved: Optional[int] = minimum_approved
        self._dvMissionPresence: dict[PartakeMission, IntVar] = {}
        self._objective_expr: Optional[LinearExpr] = None  # Initialize objective_expr as None

    def extract_solution(self, solution: MitigationSolution, extractor: CpSolver):

        solution.delays = {}
        for m, dv in self._dvDelays.items():

            if m in self._dvMissionPresence.keys():
                present = extractor.value(self._dvMissionPresence[m])
                if not present:
                    solution.delays[m] = None
                    continue

            value = extractor.value(dv)
            solution.delays[m] = value

        if self._objective_expr is not None:
            solution._objective_value = extractor.value(self._objective_expr)
            self.logger.debug("self.objective_expr is not None")
        else:
            ## changed for counting mission numbers in feasiblity case
            self._objective_expr = LinearExpr.Sum([
                dv for dv in self._dvMissionPresence.values()
            ])
            self.logger.debug("self.objective_expr is None")
        # Extract the presence of each mission
        # solution._presence_result = {m: cp_solver.value(dv) for m, dv in self._dvMissionPresence.items()}

    def _make_constraints(self):
        super()._make_constraints()

        if self.minimum_approved is not None:
            # Add the constraint for minimum number of approved missions
            self._model.add(
                LinearExpr.Sum([dv for dv in self._dvMissionPresence.values()]) >= self.minimum_approved
            )
            pass

    def _make_populate_delays_mission(self, m):
        super()._make_populate_delays_mission(m)

        if m.cancellable:
            self._dvMissionPresence[m] = self._model.new_bool_var(f"Presence of {m}")
            self._model.add_hint(self._dvMissionPresence[m], 0)

    def _make_constraints_conflict_differenceNotZero(self, diff: IntVar, c: PartakeConflict):

        if c.worst_clearance > 0:

            diff = self._dvDelayDifferences[c]

            ac1_present = self._dvMissionPresence.get(c.mission1, None)
            ac2_present = self._dvMissionPresence.get(c.mission2, None)

            if ac1_present is None and ac2_present is None:
                # No one is cancellable, the restriction is enforced
                self._model.add(diff != 0)
            elif ac1_present is None:
                # // AC2 is cancellable, the restriction is enforced only if AC2 is present
                # getModel().addDifferent(difference, 0).onlyEnforceIf(ac2IsPresentVar.getBoolVar());
                self._model.add(diff != 0).only_enforce_if(ac2_present)
                pass
            elif ac2_present is None:
                # // AC1 is cancellable, the restriction is enforced only if AC1 is present
                # getModel().addDifferent(difference, 0).onlyEnforceIf(ac1IsPresentVar.getBoolVar());
                self._model.add(diff != 0).only_enforce_if(ac1_present)
                pass
            else:
                # // Both are cancellable, the restriction is enforced only if AC1 and AC2 are present
                # Literal[] cond = new Literal[]{ac1IsPresentVar.getBoolVar(), ac2IsPresentVar.getBoolVar()};
                # getModel().addDifferent(difference, 0).onlyEnforceIf(cond);
                self._model.add(diff != 0).only_enforce_if(ac1_present, ac2_present)





    def _make_constraints_conflict_forbidden_interval(self, diff: IntVar, c: PartakeConflict, begin: int, end: int):

        ac1_present = self._dvMissionPresence.get(c.mission1, None)
        ac2_present = self._dvMissionPresence.get(c.mission2, None)

        if ac1_present is None and ac2_present is None:
            # No one is cancellable, the restriction is enforced
            super()._make_constraints_conflict_forbidden_interval(diff, c, begin, end)
        else:
            before_or_after = self._model.new_bool_var(f"Conflict between {c.mission1} and {c.mission2} at forbidden interval {begin} -> {end}")

            if ac1_present is None:
                # // AC2 is cancellable, the restriction is enforced only if AC2 is present
                # getModel().addDifferent(difference, 0).onlyEnforceIf(ac2IsPresentVar.getBoolVar());

                self._model.add(diff < begin).only_enforce_if(before_or_after, ac2_present)
                self._model.add(diff >= end).only_enforce_if(before_or_after.negated(), ac2_present)

            elif ac2_present is None:
                # // AC1 is cancellable, the restriction is enforced only if AC1 is present
                # getModel().addDifferent(difference, 0).onlyEnforceIf(ac1IsPresentVar.getBoolVar());

                self._model.add(diff < begin).only_enforce_if(before_or_after, ac1_present)
                self._model.add(diff >= end).only_enforce_if(before_or_after.negated(), ac1_present)

            else:
                # // Both are cancellable, the restriction is enforced only if AC1 and AC2 are present
                # Literal[] cond = new Literal[]{ac1IsPresentVar.getBoolVar(), ac2IsPresentVar.getBoolVar()};
                # getModel().addDifferent(difference, 0).onlyEnforceIf(cond);

                self._model.add(diff < begin).only_enforce_if(before_or_after, ac1_present, ac2_present)
                self._model.add(diff >= end).only_enforce_if(before_or_after.negated(), ac1_present, ac2_present)


    def _make_objective(self):

        # Maximize the number of accepted missions
        # TODO minimize delays
        if len(self._dvMissionPresence) > 0:
            self._objective_expr = LinearExpr.Sum([
                dv for dv in self._dvMissionPresence.values()
            ])
            self._model.maximize(self._objective_expr)
