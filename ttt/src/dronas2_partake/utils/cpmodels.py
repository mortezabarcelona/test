import threading
from abc import abstractmethod, ABC
from enum import Enum, auto

from ortools.sat.cp_model_pb2 import CpSolverStatus
from ortools.sat.python.cp_model import CpModel, CpSolverSolutionCallback, CpSolver

import multiprocessing

class State(Enum):
    IDLE = auto()
    RUNNING = auto()
    SOLVED_OPTIMAL = auto()
    SOLVED_FEASIBLE = auto()
    NOT_SOLVED_UNKNOWN = auto()
    NOT_SOLVED_INFEASIBLE = auto()
    NOT_SOLVED_INVALID = auto()
    ERROR = auto()


class Objective(Enum):
    FEASIBILITY = auto()
    OPTIMALITY = auto()


class Solution:

    @abstractmethod
    def is_solved(self):
        pass


class Model:

    @abstractmethod
    def get_model(self) -> CpModel:
        pass

    @abstractmethod
    def extract_solution(self, solution: 'Solution', extractor):
        pass


class SingleRunner_Abstract(Solution, ABC):
    max_compute_time: int

    _algorithm: Model

    def __init__(self, algorithm: Model, max_compute_time=10):
        super().__init__()
        self.max_compute_time = max_compute_time
        self._algorithm = algorithm

    def __enter__(self):

        if self._state == State.RUNNING:
            raise Exception(f"Already running")

        self._state = State.RUNNING

        try:

            self._solver = CpSolver()
            self._solver.parameters.max_time_in_seconds = float(self.max_compute_time*multiprocessing.cpu_count())
            self._solver.parameters.num_search_workers = multiprocessing.cpu_count()

            status = self._solver.solve(self._algorithm.get_model())

            match status:
                case CpSolverStatus.FEASIBLE:
                    self._state = State.SOLVED_FEASIBLE
                    self._algorithm.extract_solution(self, self._solver)
                case CpSolverStatus.OPTIMAL:
                    self._state = State.SOLVED_OPTIMAL
                    self._algorithm.extract_solution(self, self._solver)
                case CpSolverStatus.MODEL_INVALID:
                    self._state = State.NOT_SOLVED_INVALID
                case CpSolverStatus.INFEASIBLE:
                    self._state = State.NOT_SOLVED_INFEASIBLE
                case CpSolverStatus.UNKNOWN:
                    self._state = State.NOT_SOLVED_UNKNOWN

        finally:
            if self._state == State.RUNNING:
                self._state = State.ERROR

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._state = State.IDLE
        pass


class MultipleRunner_Abstract(Solution, CpSolverSolutionCallback):

    _solver: CpSolver
    max_compute_time: int

    _algorithm: Model

    def __init__(self, algorithm: Model, max_compute_time=10):
        CpSolverSolutionCallback.__init__(self)

        self._state = None
        self._waiting_for_solution = False
        self.is_computing = False
        self.__solution_count = 0
        self._running = False
        self.max_compute_time = max_compute_time
        self._algorithm = algorithm
        self._objective_value = None

    def thread_function(self):
        self._state = State.RUNNING

        self._solver = CpSolver()
        self._solver.parameters.max_time_in_seconds = float(self.max_compute_time)
        self._solver.parameters.enumerate_all_solutions = True

        self._solver.solve(self._algorithm.get_model(), self)

        self._state = State.IDLE
        with self.get_result_condition:
            self._waiting_for_solution = False
            self._state = State.NOT_SOLVED_INFEASIBLE
            self.get_result_condition.notify()

    def on_solution_callback(self):
        """Called on each new solution."""

        self._algorithm.extract_solution(self, self)

        self.__solution_count += 1

        with self.processing_condition:
            with self.get_result_condition:
                self._waiting_for_solution = False
                self._state = State.SOLVED_FEASIBLE
                self.get_result_condition.notify()

            while not self._waiting_for_solution:
                self.processing_condition.wait()

            self._state = State.RUNNING
            # self.delays = None
            self._objective_value = None

    def solution_count(self):
        """Returns the number of solutions found."""
        return self.__solution_count

    def __iter__(self):

        self.thread = threading.Thread(target=self.thread_function)
        self.get_result_condition = threading.Condition()
        self.processing_condition = threading.Condition()

        if self._state == State.RUNNING:
            raise Exception(f"Already running")

        self._state = State.RUNNING

        self._solver = CpSolver()
        self._solver.parameters.max_time_in_seconds = float(self.max_compute_time)

        self.is_computing = True
        self.thread.start()

        return self

    def __next__(self) -> 'MultipleRunner_Abstract':

        with self.processing_condition:
            self._waiting_for_solution = True
            self.processing_condition.notify()

        with self.get_result_condition:
            while self._waiting_for_solution:
                self.get_result_condition.wait()

        if self.is_solved():
            return self
        else:
            raise StopIteration()

    @abstractmethod
    def is_solved(self):
        pass
