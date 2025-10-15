import typing
from datetime import datetime
from math import floor
from typing import Optional

from dronas2.api.broker import GeometryTrajectory, Operation
from dronas2.api.models.dcb_analysis_traffic_set_model import Mission, Trajectory
from dronas2_partake.model import PartakeMissionDetection

_T = typing.TypeVar('_T', bound=PartakeMissionDetection)

def convert_dcbmission_into_partake(
        dcbmission: Mission,
        *, # From here, only parameters referenced by name
        constant_mitigation_delay: Optional[int] = None,
        cancellable: bool = False,
        instanceable_class: type[_T] = PartakeMissionDetection
) -> _T:
    """
    Converts a `dronas2.api.models.dcb_analysis_traffic_set_model.Mission` into a `dronas2_partake.model.PartakeMissionDetection`.
    :param dcbmission: Mission from dcb model
    :param constant_mitigation_delay: If set, mitigation algorithm will set this mission to a fixed delay
    :param cancellable: If set, mitigation algorithm can cancel out this mission in order to solve the problem
    :param instanceable_class:
    :return: the PartakeMissionDetection
    """

    geometry = []
    for t in dcbmission.geometry:
        gt = GeometryTrajectory()
        gt.coordinates = t.coordinates
        gt.minimum_separation_vertical = t.min_vertical_separation
        gt.minimum_separation_horizontal = t.min_horizontal_separation
        geometry.append(gt)

    return instanceable_class(
        geometry=geometry,
        tolerance_upper=dcbmission.tolerance_upper,
        tolerance_lower=dcbmission.tolerance_lower,
        launch_window_lower=dcbmission.launch_window_lower,
        launch_window_upper=dcbmission.launch_window_upper,
        constant_mitigation_delay=constant_mitigation_delay,
        cancellable=cancellable,
        relative_added_time_to_geometry=floor(datetime.timestamp(dcbmission.request)),
        user_object=dcbmission
    )


def convert_dcbmission_into_operation(
        dcbmission: Mission
) -> Operation:

    geometry = []
    for t in dcbmission.geometry:
        gt = GeometryTrajectory()
        gt.coordinates = t.coordinates
        gt.minimum_separation_vertical = t.min_vertical_separation
        gt.minimum_separation_horizontal = t.min_horizontal_separation
        geometry.append(gt)

    op = Operation()
    op.callsign=dcbmission.callsign
    op.request=dcbmission.request
    op.geometry=geometry
    op.tolerance_upper=dcbmission.tolerance_upper
    op.tolerance_lower=dcbmission.tolerance_lower
    op.launch_window_lower=dcbmission.launch_window_lower
    op.launch_window_upper=dcbmission.launch_window_upper

    return op

def convert_operation_into_dcbmission(
        operation: Operation,
        /,*,
        overwrite_minimum_separation_horizontal: int=None, fill_minimum_separation_horizontal: int=None,
        overwrite_minimum_separation_vertical: int=None, fill_minimum_separation_vertical: int=None,
        overwrite_tolerance_lower: int=None, fill_tolerance_lower: int=None,
        overwrite_tolerance_upper: int=None, fill_tolerance_upper: int=None,
        overwrite_launch_window_lower: int=None, fill_launch_window_lower: int=None,
        overwrite_launch_window_upper: int=None, fill_launch_window_upper: int=None,
        overwrite_submission_window: int=None, fill_submission_window: int=None,
        overwrite_confirmation_window: int=None, fill_confirmation_window: int=None
) -> Mission:

    geometry = []
    for t in operation.geometry:
        if isinstance(t, GeometryTrajectory):
            gt = Trajectory()
            gt.coordinates = t.coordinates
            gt.min_vertical_separation=(
                overwrite_minimum_separation_horizontal if overwrite_minimum_separation_horizontal is not None
                else t.minimum_separation_horizontal if t.minimum_separation_horizontal is not None else fill_minimum_separation_horizontal
            )
            gt.min_horizontal_separation=(
                overwrite_minimum_separation_vertical if overwrite_minimum_separation_vertical is not None
                else t.minimum_separation_vertical if t.minimum_separation_vertical is not None else fill_minimum_separation_vertical
            )
            # gt.minimum_separation_vertical = t.minimum_separation_vertical
            # gt.minimum_separation_horizontal = t.minimum_separation_horizontal
            geometry.append(gt)

    m = Mission()
    m.callsign=operation.callsign
    m.request=operation.request
    m.geometry=geometry
    m.tolerance_lower=(
        overwrite_tolerance_lower if overwrite_tolerance_lower is not None
        else operation.tolerance_lower if operation.tolerance_lower is not None else fill_tolerance_lower
    )
    m.tolerance_upper=(
        overwrite_tolerance_upper if overwrite_tolerance_upper is not None
        else operation.tolerance_upper if operation.tolerance_upper is not None else fill_tolerance_upper
    )
    m.launch_window_lower=(
        overwrite_launch_window_lower if overwrite_launch_window_lower is not None
        else operation.launch_window_lower if operation.launch_window_lower is not None else fill_launch_window_lower
    )
    m.launch_window_upper=(
        overwrite_launch_window_upper if overwrite_launch_window_upper is not None
        else operation.launch_window_upper if operation.launch_window_upper is not None else fill_launch_window_upper
    )
    m.submission_window=(
        overwrite_submission_window if overwrite_submission_window is not None
        else operation.minimum_submission if operation.minimum_submission is not None else fill_submission_window
    )
    m.confirmation_window=(
        overwrite_confirmation_window if overwrite_confirmation_window is not None
        else operation.confirmation_window if operation.confirmation_window is not None else fill_confirmation_window
    )
    m.user_object = operation

    return m
