from typing import Optional

from dronas2.api.broker import Geometry


class PartakeMission:

    def __init__(
            self,
            launch_window_upper: int = 0,
            launch_window_lower: int = 0,
            constant_mitigation_delay: Optional[int] = None,
            cancellable: bool = False,
            priority: int = 0,
            user_object = None
    ):

        self.launch_window_upper: int = launch_window_upper
        self.launch_window_lower: int = launch_window_lower
        self.constant_mitigation_delay: Optional[int] = constant_mitigation_delay
        self.constant_mitigation_delay_hint: Optional[int] = None
        self.cancellable: bool = cancellable
        self.priority: int = priority
        """
        Not used for now. It will prioritize the missions to be cancelled.
        """

        self.user_object = user_object

        # tolerance_upper: int
        # tolerance_lower: int

    def __str__(self):
        if self.user_object is not None:
            return "PartakeMission[" + str(self.user_object) + "]"
        else:
            return "PartakeMission[]"


class PartakeMissionDetection(PartakeMission):

    def __init__(
            self,
            geometry: list[Geometry],
            tolerance_upper: int,
            tolerance_lower: int,
            launch_window_upper: int = 0,
            launch_window_lower: int = 0,
            constant_mitigation_delay: Optional[int] = None,
            cancellable: bool = False,
            priority: int = 0,
            relative_added_time_to_geometry: int = 0,
            user_object=None
    ):

        super().__init__(
            launch_window_upper, launch_window_lower, constant_mitigation_delay, cancellable, priority, user_object
        )

        self.relative_added_time_to_geometry: int = relative_added_time_to_geometry
        self.geometry = geometry
        self.tolerance_upper: int = tolerance_upper
        self.tolerance_lower: int = tolerance_lower

    def __str__(self):
        if self.user_object is not None:
            return "PartakeMissionDetection[" + str(self.user_object) + "]"
        else:
            return "PartakeMissionDetection[]"


class PartakeConflict:

    def __init__(
            self,
            mission1: PartakeMission,
            mission2: PartakeMission,
            forbidden_intervals: list[tuple[int, int]],
            worst_clearance: int
    ):
        self.mission1 = mission1
        self.mission2 = mission2
        self.forbidden_intervals = forbidden_intervals
        self.worst_clearance = worst_clearance

    def __str__(self):
        return f"PartakeConflict[{self.mission1} -> {self.mission2}]"
