import datetime
import logging
from math import floor
from typing import Optional, Iterable, Union
from enum import Enum, auto

from pqdict import pqdict

from dronas2.api.broker import Geometry
from dronas2.api.models.dcb_analysis_traffic_set_model import Mission
from dronas2_partake import detection, mitigation, analysis
from dronas2_partake.analysis import Cluster
from dronas2_partake.io import missions
from dronas2_partake.model import PartakeMissionDetection, PartakeConflict, PartakeMission


class DcbSimulatorPartakeMissionDetection(PartakeMissionDetection):

    def __init__(self, geometry: list[Geometry], tolerance_upper: int, tolerance_lower: int,
                 launch_window_upper: int = 0, launch_window_lower: int = 0,
                 constant_mitigation_delay: Optional[int] = None, cancellable: bool = False, priority: int = 0,
                 relative_added_time_to_geometry: int = 0, user_object=None):
        super().__init__(geometry, tolerance_upper, tolerance_lower, launch_window_upper, launch_window_lower,
                         constant_mitigation_delay, cancellable, priority, relative_added_time_to_geometry, user_object)

        self.cluster: Optional[MyCluster] = None
        self.current_number_of_conflicts: int = 0

        self.temporal_mitigated_delay: Optional[int] = None
        self.submitted: bool = False
        self.confirmed: bool = False

        self.test_confirmed_time: Optional[datetime.datetime] = None

    def __repr__(self):
        m: Mission = self.user_object
        return m.callsign

    def __lt__(self, other):
        return _compute_submission_from(self) < _compute_submission_from(other)

class MyCluster(Cluster):
    def __init__(self):
        super().__init__()

    def check(self):

        m_dict: dict[DcbSimulatorPartakeMissionDetection, int] = {}

        for conflict in self.conflicts:
            m1: DcbSimulatorPartakeMissionDetection = conflict.mission1
            m2: DcbSimulatorPartakeMissionDetection = conflict.mission2

            if m1 in m_dict.keys():
                m_dict[m1] = m_dict[m1] + 1
            else:
                m_dict[m1] = 1

            if m2 in m_dict.keys():
                m_dict[m2] = m_dict[m2] + 1
            else:
                m_dict[m2] = 1

        assert len(m_dict) == len(self.missions)

        for mission in self.missions:
            m: DcbSimulatorPartakeMissionDetection = mission
            assert m.cluster is self
            assert m in m_dict.keys()
            assert m.current_number_of_conflicts == m_dict[m]


def _compute_submission_from(partake_mission: DcbSimulatorPartakeMissionDetection):
    m: Mission = partake_mission.user_object
    return m.compute_submission_time()

def _compute_confirmation_from(partake_mission: DcbSimulatorPartakeMissionDetection):
    m: Mission = partake_mission.user_object
    computed = m.compute_confirmation_time()

    # TODO comment this when changed in steps
    if partake_mission.test_confirmed_time is not None:
        if partake_mission.test_confirmed_time != computed:
            raise Exception("BUG: Confirmation time has changed")
    else:
        partake_mission.test_confirmed_time = computed

    return computed


class EmptyBatchTimeIntervalPolicy(Enum):
    RETURN_EMPTY_ITERATION = auto()
    """
    The run_step() will return without submitting any mission. Only time is advanced.
    """

    DILATE_TIME_TO_FIT_AT_LEAST_ONE = auto()
    """
    Time will advance until the next non-empty second. Next iteration will go from that second.
    """

    DILATE_TIME_PROPORTIONALLY_UNTIL_NON_EMPTY_BATCH = auto()
    """
    Time advances proportionally to the batch size until at least one mission is submitted. This policy keeps
    the length of the batches (to make proper charts).
    """


class DcbSimulator:

    def __init__(
            self,
            initial_traffic_set: Iterable[Mission],
            *,
            logger: logging.Logger
    ):
        """
        Construct dcb simulator.
        :param initial_traffic_set: list of missions that will conform the initial traffic set
        """

        self.logger = logger

        self.missions_detection_map: dict[Mission, DcbSimulatorPartakeMissionDetection] = dict()

        self.pending_traffic_priority_queue = pqdict(data=[])

        for initial_mission in initial_traffic_set:
            partake = missions.convert_dcbmission_into_partake(
                initial_mission,
                cancellable=True,
                instanceable_class=DcbSimulatorPartakeMissionDetection
            )
            self.missions_detection_map[initial_mission] = partake
            self.pending_traffic_priority_queue.additem(partake, partake)

        if len(self.pending_traffic_priority_queue) == 0:
            raise Exception("Parameter `initial_traffic_set' cannot be empty.")

        if len(self.missions_detection_map.keys()) != len(self.pending_traffic_priority_queue):
            raise Exception("There are multiple references to the same Mission inside the `initial_traffic_set'.")


        self.current_simulation_datetime = _compute_submission_from(self.pending_traffic_priority_queue.top())

        self.accepted_partake_missions: set[DcbSimulatorPartakeMissionDetection] = set()
        self.rejected_partake_missions: set[DcbSimulatorPartakeMissionDetection] = set()

        self.__last_accepted_missions = None

    def get_mission_delay(self, m: Mission) -> Optional[int]:
        # This will throw if mission does not exist
        pm = self.missions_detection_map[m]
        if pm.constant_mitigation_delay is not None:
            return pm.constant_mitigation_delay
        if pm.temporal_mitigated_delay is not None:
            return pm.temporal_mitigated_delay
        return None

    def apply_parameters_to_not_submitted_missions(
            self,
            missions_filter: Optional[Union[Mission, Iterable[Mission]]] = None,
            new_submission_window: Optional[int] = None,
            new_confirmation_window: Optional[int] = None,
            new_launch_window_lower: Optional[int] = None,
            new_launch_window_upper: Optional[int] = None,
            new_tolerance_lower: Optional[int] = None,
            new_tolerance_upper: Optional[int] = None,
    ):
        """
        Updates Missions' attributes inside the simulator. Only for non-submitted yet missions, this method throws an exception if a mission in the filter is already submitted.

        ATTENTION: Use this method instead of changing the values directly in the Mission. The behavior of doing that is undefined.
        :param missions_filter:
        :param new_submission_window:
        :param new_confirmation_window:
        :param new_launch_window_lower:
        :param new_launch_window_upper:
        :param new_tolerance_lower:
        :param new_tolerance_upper:
        :return:
        """

        pt_missions: list[DcbSimulatorPartakeMissionDetection] = []

        if missions_filter is None:
            pt_missions = list(self.pending_traffic_priority_queue)
            self.pending_traffic_priority_queue.clear()
        elif isinstance(missions_filter, list):
            for m in missions_filter:
                pt = self.missions_detection_map.get(m)
                if pt is None:
                    raise Exception(f"Mission in missions_filter was not in the simulation: {m}")
                elif pt.submitted:
                    raise Exception(f"Mission in missions_filter was already submitted: {m}")
                pt_missions.append(pt)

            for pt in pt_missions:
                self.pending_traffic_priority_queue.pop(pt)

        elif isinstance(missions_filter, Mission):
            pt = self.missions_detection_map.get(missions_filter)
            if pt is None:
                raise Exception(f"Mission in missions_filter was not in the simulation: {missions_filter}")
            elif pt.submitted:
                raise Exception(f"Mission in missions_filter was already submitted: {missions_filter}")

            self.pending_traffic_priority_queue.pop(pt)

        if new_submission_window is not None:
            if new_submission_window < 0:
                raise Exception(f"Invalid value for new_submission_window {new_submission_window}")
            for pt in pt_missions:
                m: Mission = pt.user_object
                m.submission_window = new_submission_window
                pt.constant_mitigation_delay_hint = None

        if new_confirmation_window is not None:
            if new_confirmation_window < 0:
                raise Exception(f"Invalid value for new_confirmation_window {new_confirmation_window}")
            for pt in pt_missions:
                m: Mission = pt.user_object
                m.confirmation_window = new_confirmation_window
                pt.constant_mitigation_delay_hint = None

        if new_launch_window_lower is not None:
            if new_launch_window_lower < 0:
                raise Exception(f"Invalid value for new_launch_window_lower {new_launch_window_lower}")
            for pt in pt_missions:
                m: Mission = pt.user_object
                m.launch_window_lower = new_launch_window_lower
                pt.launch_window_lower = new_launch_window_lower
                pt.constant_mitigation_delay_hint = None

        if new_launch_window_upper is not None:
            if new_launch_window_upper < 0:
                raise Exception(f"Invalid value for new_launch_window_upper {new_launch_window_upper}")
            for pt in pt_missions:
                m: Mission = pt.user_object
                m.launch_window_upper = new_launch_window_upper
                pt.launch_window_upper = new_launch_window_upper

        if new_tolerance_lower is not None:
            if new_tolerance_lower < 0:
                raise Exception(f"Invalid value for new_tolerance_lower {new_tolerance_lower}")
            for pt in pt_missions:
                m: Mission = pt.user_object
                m.tolerance_lower = new_tolerance_lower
                pt.tolerance_lower = new_tolerance_lower

        if new_tolerance_upper is not None:
            if new_tolerance_upper < 0:
                raise Exception(f"Invalid value for new_tolerance_upper {new_tolerance_upper}")
            for pt in pt_missions:
                m: Mission = pt.user_object
                m.tolerance_upper = new_tolerance_upper
                pt.tolerance_lower = new_tolerance_upper

        for pt in pt_missions:
            self.pending_traffic_priority_queue.additem(pt, pt)


    def append_missions(self, new_missions: Union[Mission, Iterable[Mission]]):
        """
        Tries to append new missions into the simulation. If a Mission is already in, no effect.

        Note that if a submission time falls before the current simulation time, then it will be submitted on the next simulator iteration.
        :param new_missions:
        :return:
        """

        for m in new_missions if isinstance(new_missions, Iterable) else new_missions,:
            if m not in self.missions_detection_map.keys():
                partake = missions.convert_dcbmission_into_partake(
                    m,
                    cancellable=True,
                    instanceable_class=DcbSimulatorPartakeMissionDetection
                )
                self.missions_detection_map[m] = partake
                self.pending_traffic_priority_queue.additem(partake, partake)

    def remove_missions(self, old_missions: Union[Mission, Iterable[Mission]]):
        """
        Tries to remove missions from the simulation. If a Mission is not in the simulator, no effect.

        Note that if the mission is already accepted, all conflicts will be gone along with the mission, then clusters may change as well.
        :param old_missions:
        :return:
        """
        recently_rejected_missions = []
        if isinstance(old_missions, list):
            for m in old_missions:
                pt = self.missions_detection_map.get(m)
                if pt is None:
                    continue
                if pt.submitted:
                    if pt in self.accepted_partake_missions:
                        recently_rejected_missions.append(pt)
                    else:
                        self.rejected_partake_missions.remove(pt)
                else:
                    self.pending_traffic_priority_queue.pop(pt)
        elif isinstance(old_missions, Mission):
            pt = self.missions_detection_map.get(old_missions)
            if pt is None:
                return
            if pt.submitted:
                if pt in self.accepted_partake_missions:
                    recently_rejected_missions.append(pt)
                else:
                    self.rejected_partake_missions.remove(pt)
            else:
                self.pending_traffic_priority_queue.pop(pt)

            self.pending_traffic_priority_queue.pop(pt)

        self.accepted_partake_missions.difference_update(recently_rejected_missions)
        self.__5_remove_rejected_missions_and_optimize_clusters(recently_rejected_missions)

    @property
    def accepted_missions_count(self) -> int:
        return len(self.accepted_partake_missions)

    @property
    def accepted_missions_iterable(self) -> Iterable[Mission]:
        return (pt.user_object for pt in self.accepted_partake_missions)

    @property
    def rejected_missions_count(self) -> int:
        return len(self.rejected_partake_missions)

    @property
    def rejected_missions_iterable(self) -> Iterable[Mission]:
        return (pt.user_object for pt in self.rejected_partake_missions)

    @property
    def pending_missions_count(self) -> int:
        return len(self.pending_traffic_priority_queue)

    @property
    def pending_missions_iterable(self) -> Iterable[Mission]:
        return (pt.user_object for pt in self.pending_traffic_priority_queue)

    def get_recently_submitted_missions(self) -> set[Mission]:
        # TODO make this method more efficient
        if self.__last_accepted_missions is None:
            self.__last_accepted_missions = set(self.accepted_missions_iterable)
            return self.__last_accepted_missions
        else:
            current_accepted_missions = set(self.accepted_missions_iterable)
            recently_submitted_missions = current_accepted_missions.difference(self.__last_accepted_missions)
            self.__last_accepted_missions = current_accepted_missions
            return recently_submitted_missions

    def get_next_submitted_missions(
            self,
            batch_time_interval_seconds: int = 1,
            empty_batch_time_interval_policy: EmptyBatchTimeIntervalPolicy = EmptyBatchTimeIntervalPolicy.DILATE_TIME_PROPORTIONALLY_UNTIL_NON_EMPTY_BATCH,
    ) -> set[Mission]:
        # TODO make this method more efficient

        if len(self.pending_traffic_priority_queue) == 0:
            return set()

        multiplier = self.__1_1_compute_future_datetime(batch_time_interval_seconds)

        # If batches are strict, don't multipy
        if multiplier > 0:
            if empty_batch_time_interval_policy == EmptyBatchTimeIntervalPolicy.RETURN_EMPTY_ITERATION:
                future_simulation_datetime = self.current_simulation_datetime + datetime.timedelta(seconds=batch_time_interval_seconds)
            elif empty_batch_time_interval_policy == EmptyBatchTimeIntervalPolicy.DILATE_TIME_TO_FIT_AT_LEAST_ONE and multiplier > 0:
                future_simulation_datetime = _compute_submission_from(self.pending_traffic_priority_queue.top())
            else:
                future_simulation_datetime = self.current_simulation_datetime + datetime.timedelta(seconds=batch_time_interval_seconds * (multiplier + 1))
        else:
            future_simulation_datetime = self.current_simulation_datetime + datetime.timedelta(seconds=batch_time_interval_seconds)

        new_submitted_missions_partake = self.__1_2_accumulate_missions_until(future_simulation_datetime)

        for pt in new_submitted_missions_partake:
            self.pending_traffic_priority_queue.additem(pt, pt)

        return set((pt.user_object for pt in new_submitted_missions_partake))


    def run_step(
            self,
            *,
            batch_time_interval_seconds: int = 1,
            precision_seconds: int = 1,
            max_compute_time_seconds: int = 10,
            empty_batch_time_interval_policy: EmptyBatchTimeIntervalPolicy = EmptyBatchTimeIntervalPolicy.DILATE_TIME_PROPORTIONALLY_UNTIL_NON_EMPTY_BATCH
    ) -> bool:
        """
        Run simulation step. User can perform changes in between. It's meant to be called inside a while loop.

        while dcb_simulation.run_step():
            pass

        :param precision_seconds: mitigation algorithm precision
        :param max_compute_time_seconds: mitigation algorithm timeout
        :param batch_time_interval_seconds: How many seconds submitted missions before running mitigation and reject some of them.
        :param empty_batch_time_interval_policy: Policy in case the next batch is empty
        :return: if simulation is not done yet
        """

        if len(self.pending_traffic_priority_queue) == 0:
            logging.debug(f"Pending traffic set became empty. Exiting simulation.")
            return False

        if batch_time_interval_seconds < 1:
            raise Exception(f"`batch_time_interval_seconds` must be greater than 0. Received: {batch_time_interval_seconds}")

        if precision_seconds < 1:
            raise Exception(f"`precision_seconds` must be greater than 0. Received: {precision_seconds}")

        if max_compute_time_seconds < 1:
            raise Exception(f"`max_compute_time_seconds` must be greater than 0. Received: {max_compute_time_seconds}")

        # 1. Collect new missions

        # 1.1. Analyze the next mission to see if it has to skip some intervals
        multiplier = self.__1_1_compute_future_datetime(batch_time_interval_seconds)

        # If batches are strict, don't multipy
        if multiplier > 0:
            if empty_batch_time_interval_policy == EmptyBatchTimeIntervalPolicy.RETURN_EMPTY_ITERATION:
                future_simulation_datetime = self.current_simulation_datetime + datetime.timedelta(seconds=batch_time_interval_seconds)
                self.current_simulation_datetime = future_simulation_datetime
                return True
            elif empty_batch_time_interval_policy == EmptyBatchTimeIntervalPolicy.DILATE_TIME_TO_FIT_AT_LEAST_ONE and multiplier > 0:
                future_simulation_datetime = _compute_submission_from(self.pending_traffic_priority_queue.top())
            else:
                future_simulation_datetime = self.current_simulation_datetime + datetime.timedelta(seconds=batch_time_interval_seconds * (multiplier + 1))
        else:
            future_simulation_datetime = self.current_simulation_datetime + datetime.timedelta(seconds=batch_time_interval_seconds)

        logging.debug(f"Begin step. current={self.current_simulation_datetime} future={future_simulation_datetime} accepted={len(self.accepted_partake_missions)} rejected={len(self.rejected_partake_missions)}")

        # 1.2. Accumulate missions until the future datetime
        new_submitted_missions_partake = self.__1_2_accumulate_missions_until(future_simulation_datetime)

        # 1.3. Advance time, algorithm is executing in the new future
        self.current_simulation_datetime = future_simulation_datetime

        # 2. Run detection
        missions_to_detection = [*self.accepted_partake_missions, *new_submitted_missions_partake]

        logging.debug(f"Detection. missions_to_detection={len(missions_to_detection)} detect_collection={[repr(m) for m in new_submitted_missions_partake]}={len(new_submitted_missions_partake)}.")

        new_conflicts = detection.execute_detection(
            missions_to_detection,
            detect_collection=new_submitted_missions_partake
        )

        i = 0
        for c in new_conflicts:
            logging.debug(f"    Conflict {i}. mission1={repr(c.mission1)} mission2={repr(c.mission2)}")
            i += 1

        # 3. Run analysis
        logging.debug(f"Analysis. new_conflicts={len(new_conflicts)}.")

        # 3.1. Execute clustering
        changed_clusters = self.__3_1_clusterize_new_conflicts(new_conflicts)

        # 3.2. Insta-accept people without conflict
        insta_accepted = self.__3_2_insta_accept_without_conflict_return_debug(new_submitted_missions_partake)

        # 4. Run mitigation

        # 4.1. Fix confirmed missions to its current delay
        insta_confirmed = self.__4_1_confirm_missions_until_now_return_debug()

        logging.debug(f"Mitigation. insta_accepted={insta_accepted}={len(insta_accepted)} confirmed={insta_confirmed} changed_clusters={len(changed_clusters)}.")

        # 4.2[cluster]. Iterate changed clusters to mitigate them
        recently_rejected_missions: list[DcbSimulatorPartakeMissionDetection] = []
        for i, changed_cluster in enumerate(changed_clusters):

            # 4.2[cluster].1. Remove confirmed conflicts between confirmed missions in this cluster
            removed_conflicts = self.__4_2_1_remove_confirmed_conflicts_from_cluster_return_debug(changed_cluster)

            logging.debug(f"    Cluster {i}. missions={len(changed_cluster.missions)} conflicts={len(changed_cluster.conflicts)} removed={len(removed_conflicts)}.")

            # 4.2[cluster].2. Execute algorithm
            mitigation_algorithm: mitigation.MitigationAlgorithm_Abstract = mitigation.MitigationAlgorithm_Batch(
                changed_cluster.missions,
                changed_cluster.conflicts,
                precision_seconds=precision_seconds
            )

            with mitigation_algorithm.run_single(max_compute_time=max_compute_time_seconds) as result:

                if not result.is_solved():
                    raise Exception(f"BUG: Mitigation algorithm should have been solved the problem. Maybe a timeout occurred without any solution found. State: {result._state}")

                # 4.2[cluster].3. Accept/Reject missions
                self.__4_2_3_apply_mitigation_result(changed_cluster, result.delays, recently_rejected_missions)


        # 5. Remove just rejected missions and optimize clusters
        # Need to be here because it may split clusters
        if len(recently_rejected_missions) > 0:
            self.__5_remove_rejected_missions_and_optimize_clusters(recently_rejected_missions)

        return True # Go inside the while until next step

    def __1_1_compute_future_datetime(self, batch_time_interval_seconds: int) -> int:
        next_mission_submission = _compute_submission_from(self.pending_traffic_priority_queue.top())
        multiplier = floor(((next_mission_submission - self.current_simulation_datetime) / batch_time_interval_seconds).total_seconds())
        return multiplier

    def __1_2_accumulate_missions_until(self, future_simulation_datetime: datetime.datetime) -> set[DcbSimulatorPartakeMissionDetection]:
        new_submitted_missions_partake: set[DcbSimulatorPartakeMissionDetection] = set()
        while len(new_submitted_missions_partake) < len(self.pending_traffic_priority_queue):
            mission_to_simulate = self.pending_traffic_priority_queue.top()

            if _compute_submission_from(mission_to_simulate) <= future_simulation_datetime:
                self.pending_traffic_priority_queue.pop()
                new_submitted_missions_partake.add(mission_to_simulate)
                mission_to_simulate.submitted = True
            else:
                break
        return new_submitted_missions_partake

    def __3_1_clusterize_new_conflicts(
            self,
            conflicts: list[PartakeConflict],
    ) -> set[MyCluster]:

        changed_clusters: set[MyCluster] = set()

        for conflict in conflicts:
            # noinspection PyTypeChecker
            mission1: DcbSimulatorPartakeMissionDetection = conflict.mission1
            # noinspection PyTypeChecker
            mission2: DcbSimulatorPartakeMissionDetection = conflict.mission2

            cluster1 = mission1.cluster
            cluster2 = mission2.cluster

            if cluster1 is not None:
                if cluster2 is not None:
                    if cluster1 is not cluster2:
                        # Merge
                        cluster1.missions.update(cluster2.missions)
                        cluster1.conflicts.extend(cluster2.conflicts)
                        for m in cluster2.missions:
                            m: DcbSimulatorPartakeMissionDetection = m
                            m.cluster = cluster1

                        # Cluster 2 disappears, so removed from changed clusters
                        changed_clusters.discard(cluster2)
                    # else, they already are in the same cluster

                    cluster1.conflicts.append(conflict)

                    mission1.current_number_of_conflicts += 1
                    mission2.current_number_of_conflicts += 1

                    cluster1.check()

                else:
                    # cluster1 exists, cluster2 not
                    cluster1.missions.add(conflict.mission2)
                    cluster1.conflicts.append(conflict)

                    mission2.cluster = cluster1
                    mission2.current_number_of_conflicts = 1

                    mission1.current_number_of_conflicts += 1

                    cluster1.check()

                changed_clusters.add(cluster1)

            else:
                if cluster2 is not None:
                    # cluster2 exists, cluster1 not
                    cluster2.missions.add(conflict.mission1)
                    cluster2.conflicts.append(conflict)

                    mission1.cluster = cluster2
                    mission1.current_number_of_conflicts = 1

                    mission2.current_number_of_conflicts += 1

                    changed_clusters.add(cluster2)

                    cluster2.check()

                else:
                    # none of them exists, create a cluster with them
                    cluster1 = MyCluster()
                    cluster1.missions.add(conflict.mission1)
                    cluster1.missions.add(conflict.mission2)
                    cluster1.conflicts.append(conflict)

                    mission1.cluster = cluster1
                    mission1.current_number_of_conflicts = 1

                    mission2.cluster = cluster1
                    mission2.current_number_of_conflicts = 1

                    changed_clusters.add(cluster1)

                    cluster1.check()

        return changed_clusters

    def __3_2_insta_accept_without_conflict_return_debug(self, new_submitted_missions_partake: Iterable[DcbSimulatorPartakeMissionDetection]) -> list[str]:
        insta_accepted_debug: list[str] = []
        for new_submitted_mission_partake in new_submitted_missions_partake:
            # Check people without cluster (previous step filled this map) and insta-accept
            if new_submitted_mission_partake.cluster is None: # not in self.missions_clusters.keys():

                new_submitted_mission_partake.cancellable = False
                new_submitted_mission_partake.temporal_mitigated_delay = 0
                self.accepted_partake_missions.add(new_submitted_mission_partake)

                insta_accepted_debug.append(repr(new_submitted_mission_partake))
        return insta_accepted_debug

    def __4_1_confirm_missions_until_now_return_debug(self) -> int:
        insta_confirmed = 0
        for accepted_partake_mission in self.accepted_partake_missions:

            confirmation_time = _compute_confirmation_from(accepted_partake_mission)
            if not accepted_partake_mission.confirmed and confirmation_time <= self.current_simulation_datetime:
                # Set constant mitigated delay and remove it from constant
                if accepted_partake_mission.temporal_mitigated_delay is not None:
                    accepted_partake_mission.constant_mitigation_delay = accepted_partake_mission.temporal_mitigated_delay
                    accepted_partake_mission.temporal_mitigated_delay = None
                    accepted_partake_mission.confirmed = True
                    self.logger.debug(f"    Confirmed {insta_confirmed}: {repr(accepted_partake_mission)}")
                else:
                    raise Exception("BUG: expected 'temporal_mitigated_delay' to be set on an accepted and not confirmed Mission.")
                insta_confirmed += 1
        return insta_confirmed

    def __4_2_1_remove_confirmed_conflicts_from_cluster_return_debug(self, changed_cluster: MyCluster) -> list[PartakeConflict]:

        to_remove_conflicts: list[PartakeConflict] = []
        for conflict in changed_cluster.conflicts:
            # noinspection PyTypeChecker
            m1: DcbSimulatorPartakeMissionDetection = conflict.mission1
            # noinspection PyTypeChecker
            m2: DcbSimulatorPartakeMissionDetection = conflict.mission2
            if m1.confirmed and m2.confirmed:
                to_remove_conflicts.append(conflict)

        for to_remove_conflict in to_remove_conflicts:
            # noinspection PyTypeChecker
            m1: DcbSimulatorPartakeMissionDetection = to_remove_conflict.mission1
            # noinspection PyTypeChecker
            m2: DcbSimulatorPartakeMissionDetection = to_remove_conflict.mission2

            changed_cluster.conflicts.remove(to_remove_conflict)

            if m1.current_number_of_conflicts <= 0:
                raise Exception(f"BUG: m1.current_number_of_conflicts should be grater than 0, found {m1.current_number_of_conflicts}")
            m1.current_number_of_conflicts -= 1
            if m1.current_number_of_conflicts == 0:
                changed_cluster.missions.remove(m1)
                m1.cluster = None

            if m2.current_number_of_conflicts <= 0:
                raise Exception(f"BUG: m2.current_number_of_conflicts should be grater than 0, found {m2.current_number_of_conflicts}")
            m2.current_number_of_conflicts -= 1
            if m2.current_number_of_conflicts == 0:
                changed_cluster.missions.remove(m2)
                m2.cluster = None

        return to_remove_conflicts

    def __4_2_3_apply_mitigation_result(
            self,
            changed_cluster: MyCluster,
            delays: dict[PartakeMission, int|None],
            out_recently_rejected_missions: list[DcbSimulatorPartakeMissionDetection]
    ):
        for processed_partake_mission in changed_cluster.missions:
            processed_partake_mission: DcbSimulatorPartakeMissionDetection = processed_partake_mission

            delay = delays.get(processed_partake_mission)
            if delay is not None:

                processed_partake_mission.cancellable = False
                processed_partake_mission.temporal_mitigated_delay = delay
                processed_partake_mission.constant_mitigation_delay_hint = delay
                if processed_partake_mission not in self.accepted_partake_missions:
                    self.accepted_partake_missions.add(processed_partake_mission)
                    self.logger.debug(f"    Accepted: {repr(processed_partake_mission)}")
                elif processed_partake_mission in self.rejected_partake_missions:
                    raise Exception("BUG: A rejected mission is now accepted?")

            else:
                out_recently_rejected_missions.append(processed_partake_mission)

                if processed_partake_mission not in self.rejected_partake_missions:
                    self.rejected_partake_missions.add(processed_partake_mission)
                    self.logger.debug(f"    Rejected: {repr(processed_partake_mission)}")
                elif processed_partake_mission in self.accepted_partake_missions:
                    raise Exception("BUG: An accepted mission is now rejected?")

    def __5_remove_rejected_missions_and_optimize_clusters(
            self,
            recently_rejected_missions: list[DcbSimulatorPartakeMissionDetection]
    ):

        check_clusters_for_split = set()

        for m in recently_rejected_missions:
            cluster = m.cluster
            if cluster is not None:
                cluster.missions.remove(m)
                m.cluster = None

                keep_conflicts = []
                for old_conflict in cluster.conflicts:
                    # noinspection PyTypeChecker
                    mission1: DcbSimulatorPartakeMissionDetection = old_conflict.mission1
                    # noinspection PyTypeChecker
                    mission2: DcbSimulatorPartakeMissionDetection = old_conflict.mission2

                    if mission1 is m:
                        mission2.current_number_of_conflicts -= 1

                        if mission2.current_number_of_conflicts == 0:
                            mission2.cluster = None
                            cluster.missions.remove(mission2)

                    elif mission2 is m:
                        mission1.current_number_of_conflicts -= 1

                        if mission1.current_number_of_conflicts == 0:
                            mission1.cluster = None
                            cluster.missions.remove(mission1)

                    else:
                        keep_conflicts.append(old_conflict)

                cluster.conflicts[:] = keep_conflicts

                if len(cluster.missions) > 1:
                    check_clusters_for_split.add(cluster)

        for cluster in check_clusters_for_split:

            new_clusters = analysis.execute_analysis(cluster.conflicts, MyCluster)

            if len(new_clusters) > 1:
                # Reassign everyone to their new cluster
                total_missions = 0
                for new_cluster in new_clusters:
                    total_missions += len(new_cluster.missions)
                    for m in new_cluster.missions:
                        m: DcbSimulatorPartakeMissionDetection = m
                        m.cluster = new_cluster

                if total_missions != len(cluster.missions):
                    raise Exception("BUG: Expected no orphan missions when splitting clusters")
            elif len(new_clusters) == 1:
                if len([*new_clusters][0].missions) != len(cluster.missions):
                    raise Exception("BUG: Expected no orphan missions when splitting clusters")
