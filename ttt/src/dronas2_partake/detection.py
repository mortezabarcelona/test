from math import radians
from typing import Union, Iterable

from dronas2.api.broker import GeometryAirblock, GeometryTrajectory
from dronas2_partake.model import PartakeConflict, PartakeMissionDetection

# HashSet = jpype.JClass("java.util.HashSet")

from java.lang import Double, Long
from java.util import HashSet
from es.aslogic.geom import Airblock as PartakeAirblock, Trajectory as PartakeTrajectory, LinearRing, Point, \
    Earth
from es.aslogic.partake import PartakeDetectionBuilder, Filter_Trajectory_Mission
from es.aslogic.partake import PartakeMissionBuilder

def execute_detection(
        missions: Iterable[PartakeMissionDetection],
        detect_collection: Union[set[PartakeMissionDetection], None] = None
) -> list[PartakeConflict]:
    """
    Run Partake Detection algorithm and retrieve pairwise conflicts
    :param missions: list of missions to detect conflicts
    :param detect_collection: if supplied, only conflicts involving these mission will be computed
    :return: a list of the conflicts found in the scenario
    """

    builder = PartakeDetectionBuilder(Earth.getWorldS2Rad3D()) # Bug in partake, radians is mandatory
    # builder.addHint(PartakeDetection.Hint.TRAJECTORY_CONFLICT_REFINING)

    java_detect_collection = HashSet() if detect_collection is not None else None

    for i, md in enumerate(missions):
        pmb = PartakeMissionBuilder()
        pmb.setUserObject(i) # Assign index as user object to reference it later
        pmb.setCancellable(md.cancellable)
        pmb.setConstantMitigatedDelay(Long(md.constant_mitigation_delay) if md.constant_mitigation_delay is not None else None)
        pmb.setLaunchWindow(md.launch_window_lower, md.launch_window_upper)
        pmb.setTolerance(md.tolerance_lower, md.tolerance_upper)
        for g in md.geometry:
            if isinstance(g, GeometryAirblock):
                a = PartakeAirblock.create(
                    LinearRing.create(
                        (Point.create2D(radians(lon), radians(lat)) for lon, lat in g.coordinates)
                    ),
                    g.bottom,
                    g.top,
                )
                pmb.addLap(
                    a,
                    g.time_begin + md.relative_added_time_to_geometry,
                    g.time_end + md.relative_added_time_to_geometry,
                    Double(g.minimum_separation_horizontal),
                    Double(g.minimum_separation_vertical)
                )
            elif isinstance(g, GeometryTrajectory):
                a = PartakeTrajectory.builder()
                for lon, lat, alt, time in g.coordinates:
                    a.add3DM(radians(lon), radians(lat), alt, time + md.relative_added_time_to_geometry)
                pmb.addLap(
                    a.build(),
                    Double(g.minimum_separation_horizontal),
                    Double(g.minimum_separation_vertical)
                )

        pm = pmb.buildForDetection()

        if java_detect_collection is not None and md in detect_collection:
            java_detect_collection.add(pm)

        builder.addMission(pm)

    builder.configureDefaultStack()

    if java_detect_collection is not None:
        builder.setTrajectoryFilter(Filter_Trajectory_Mission().setDetectCollection(java_detect_collection))

    pd_algorithm = builder.build()
    pd_algorithm.run()

    partake_conflicts: list[PartakeConflict] = []
    for gc in pd_algorithm.getGroupedConflicts():
        partake_conflicts.append(PartakeConflict(
            mission1 = missions[gc.mission1.getUserObject()],
            mission2 = missions[gc.mission2.getUserObject()],
            forbidden_intervals=[(interval.getBegin(), interval.getEnd()) for interval in gc.forbiddenIntervals],
            worst_clearance=gc.worstClearence
        ))

    return partake_conflicts

