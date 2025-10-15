import es
import es.aslogic.geom
import java.lang
import java.util
import java.util.function
import typing

class LapInACell:

    def getAirblock(self) -> es.aslogic.geom.Airblock:
        """
        """
        ...

    def getEntryTime(self, cell: es.aslogic.geom.Cell) -> int:
        """
        """
        ...

    def getExitTime(self, cell: es.aslogic.geom.Cell) -> int:
        """
        """
        ...

    def getLap(self) -> 'PartakeMission.Lap':
        """
        """
        ...

    def getMaxAlt(self) -> float:
        """
        """
        ...

    def getMinAlt(self) -> float:
        """
        """
        ...

    def getMinimumHorizontalSeparation(self) -> float:
        """
        """
        ...

    def getMinimumVerticalSeparation(self) -> float:
        """
        """
        ...

    def getMission(self) -> 'PartakeMission.PartakeMissionDetection':
        """
        """
        ...

    def getSubTrajectory(self) -> es.aslogic.geom.Trajectory:
        """
        """
        ...

    def isActive(self) -> bool:
        """
        """
        ...

    def isAirblock(self) -> bool:
        """
        """
        ...

    def isAirblockFullyInside(self, cell: es.aslogic.geom.Cell) -> bool:
        """
        """
        ...

    def isTrajectory(self) -> bool:
        """
        """
        ...

class PartakeConflict:
    """
    Represents all the .... between a pair of A/Cs
    
    """

    userObject: typing.Any = ...
    """
    """

    mission1: 'PartakeMission' = ...
    """
    """

    mission2: 'PartakeMission' = ...
    """
    """

    forbiddenIntervals: java.util.List = ...
    """
    Intervals of relative time distances gaps w.r.t ??????? where the missions are in real conflict.
         0 means that the missions are not moved, 1: the mission2 is 1 second to the right (or mission1, 1 second to the left), and so on...
        
        
        
    """

    timeIntervals: java.util.List = ...
    """
    Intervals of ABSOLUTE EPOCHS where the missions are in conflict.
         It includes potencial conflicts, because it takes in account launch windows.
        
        
        
    """

    worstClearence: int = ...
    """
    From all the pairwise conflicts between these two missions. The clearance of the most conflictive (largest overlapping).
         If clearance is positive, they are in a real conflict, otherwise, in a potential conflict.
        
        
        
    """

    @typing.overload
    def __init__(self, mission1: 'PartakeMission', mission2: 'PartakeMission', forbiddenIntervals: java.util.List['PartakeConflict.Interval'], worstClearence: int, timeIntervals: java.util.List['PartakeConflict.Interval']):
        """
        """
        ...

    @typing.overload
    def __init__(self, mission1: 'PartakeMission', mission2: 'PartakeMission', forbiddenIntervals: java.util.List['PartakeConflict.Interval'], worstClearence: int, timeIntervals: java.util.List['PartakeConflict.Interval'], userObject: typing.Any):
        """
        """
        ...

    def getUserObject(self) -> typing.Any:
        """
        """
        ...

    def toString(self) -> java.lang.String:
        """
        """
        ...

    class Interval:

        def __init__(self, begin: int, end: int):
            """
            """
            ...

        def getBegin(self) -> int:
            """
            """
            ...

        def getEnd(self) -> int:
            """
            """
            ...

        def toString(self) -> java.lang.String:
            """
            """
            ...

class PartakeDetection(java.lang.Runnable):

    def getGroupedConflicts(self) -> java.util.List[PartakeConflict]:
        """
        """
        ...

    def getState(self) -> 'PartakeDetection.State':
        """
        """
        ...

    class Filter:

        def test(self, algorithm: 'PartakeDetection.Handle', cell1: es.aslogic.geom.Cell, cell2: es.aslogic.geom.Cell, lap1: LapInACell, lap2: LapInACell) -> bool:
            """
            """
            ...

    class Handle:

        def getWorld(self) -> es.aslogic.geom.World_Spherical:
            """
            """
            ...

        def getWorldRadius(self) -> float:
            """
            """
            ...

    class Hint(java.lang.Enum['PartakeDetection.Hint']):

        PARALLELIZE: typing.ClassVar['PartakeDetection.Hint'] = ...
        """
        """

        TRAJECTORY_CONFLICT_REFINING: typing.ClassVar['PartakeDetection.Hint'] = ...
        """
        """

        @classmethod
        @typing.overload
        def valueOf(cls, name: typing.Union[java.lang.String, str]) -> 'PartakeDetection.Hint':
            """
            """
            ...

        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>

        @classmethod
        @typing.overload
        def valueOf(cls, class_: typing.Type[_valueOf_1__T], string: typing.Union[java.lang.String, str]) -> _valueOf_1__T:
            """
            """
            ...

        @classmethod
        def values(cls) -> typing.List['PartakeDetection.Hint']:
            """
            """
            ...

    class State(java.lang.Enum['PartakeDetection.State']):

        IDLE: typing.ClassVar['PartakeDetection.State'] = ...
        """
        """

        RUNNING: typing.ClassVar['PartakeDetection.State'] = ...
        """
        """

        DONE: typing.ClassVar['PartakeDetection.State'] = ...
        """
        """

        ERROR: typing.ClassVar['PartakeDetection.State'] = ...
        """
        """

        @classmethod
        @typing.overload
        def valueOf(cls, name: typing.Union[java.lang.String, str]) -> 'PartakeDetection.State':
            """
            """
            ...

        _valueOf_1__T = typing.TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>

        @classmethod
        @typing.overload
        def valueOf(cls, class_: typing.Type[_valueOf_1__T], string: typing.Union[java.lang.String, str]) -> _valueOf_1__T:
            """
            """
            ...

        @classmethod
        def values(cls) -> typing.List['PartakeDetection.State']:
            """
            """
            ...

class PartakeDetectionBuilder:

    getCellChrono: typing.ClassVar[float] = ...
    """
    """

    getCellFindChrono: typing.ClassVar[float] = ...
    """
    """

    getCellAddCellsChrono: typing.ClassVar[float] = ...
    """
    """

    getCellTimelineChrono: typing.ClassVar[float] = ...
    """
    """

    def __init__(self, world: es.aslogic.geom.World_Spherical):
        """
        """
        ...

    def addHint(self, hint: PartakeDetection.Hint) -> 'PartakeDetectionBuilder':
        """
        """
        ...

    def addMission(self, mission: 'PartakeMission.PartakeMissionDetection') -> None:
        """
        """
        ...

    def addMissions(self, missions: typing.Union[java.lang.Iterable['PartakeMission.PartakeMissionDetection'], typing.Sequence['PartakeMission.PartakeMissionDetection'], typing.Set['PartakeMission.PartakeMissionDetection'], typing.Callable[[], 'PartakeMission.PartakeMissionDetection']]) -> None:
        """
        """
        ...

    def build(self) -> PartakeDetection:
        """
        """
        ...

    def buildDummy(self) -> PartakeDetection:
        """
        """
        ...

    def build_v1(self) -> PartakeDetection:
        """
        """
        ...

    def configureDefaultStack(self) -> 'PartakeDetectionBuilder':
        """
        """
        ...

    def setClearanceFilter(self, clearanceFilter: typing.Union[PartakeDetection.Filter, typing.Callable]) -> None:
        """
        """
        ...

    def setDistanceGrouping(self, distanceGrouping: float) -> None:
        """
        """
        ...

    def setHorizontalFilter(self, horizontalFilter: typing.Union[PartakeDetection.Filter, typing.Callable]) -> None:
        """
        """
        ...

    def setMinimumDistance(self, minimumDistanceGrouping: float) -> None:
        """
        """
        ...

    def setTrajectoryFilter(self, trajectoryFilter: typing.Union[PartakeDetection.Filter, typing.Callable]) -> None:
        """
        """
        ...

    def setVerticalFilter(self, verticalFilter: typing.Union[PartakeDetection.Filter, typing.Callable]) -> None:
        """
        """
        ...

class PartakeMissionBuilder:

    def __init__(self):
        """
        """
        ...

    @typing.overload
    def addLap(self, airblock: es.aslogic.geom.Airblock, begin: int, end: int) -> 'PartakeMissionBuilder':
        """
        """
        ...

    @typing.overload
    def addLap(self, airblock: es.aslogic.geom.Airblock, begin: int, end: int, minimumHorizontalSeparation: float, minimumVerticalSeparation: float) -> 'PartakeMissionBuilder':
        """
        """
        ...

    @typing.overload
    def addLap(self, trajectory: es.aslogic.geom.Trajectory) -> 'PartakeMissionBuilder':
        """
        """
        ...

    @typing.overload
    def addLap(self, trajectory: es.aslogic.geom.Trajectory, minimumHorizontalSeparation: float, minimumVerticalSeparation: float) -> 'PartakeMissionBuilder':
        """
        """
        ...

    def buildForDetection(self) -> 'PartakeMission.PartakeMissionDetection':
        """
        """
        ...

    def buildSimple(self) -> 'PartakeMission':
        """
        """
        ...

    def setCancellable(self, cancellable: bool) -> 'PartakeMissionBuilder':
        """
        """
        ...

    def setConstantMitigatedDelay(self, constantMitigatedDelay: int) -> 'PartakeMissionBuilder':
        """
        """
        ...

    def setLaunchWindow(self, launchWindowLowerBound: int, launchWindowUpperBound: int) -> 'PartakeMissionBuilder':
        """
        """
        ...

    def setTolerance(self, toleranceLowerBound: int, toleranceUpperBound: int) -> 'PartakeMissionBuilder':
        """
        """
        ...

    def setUserObject(self, userObject: typing.Any) -> 'PartakeMissionBuilder':
        """
        """
        ...

    def toString(self) -> java.lang.String:
        """
        """
        ...

class Filter_Clearance(PartakeDetection.Filter):

    def __init__(self):
        """
        """
        ...

    def test(self, algorithm: PartakeDetection.Handle, cel1: es.aslogic.geom.Cell, cell2: es.aslogic.geom.Cell, lap1: LapInACell, lap2: LapInACell) -> bool:
        """
        """
        ...

class Filter_Horizontal_DistancePlanes(PartakeDetection.Filter):

    def __init__(self):
        """
        """
        ...

    @typing.overload
    def distancePlane(self, airblock1: es.aslogic.geom.Airblock, airblock2: es.aslogic.geom.Airblock, minDist: float, radius: float) -> bool:
        """
        Computes the distance a trajectory and an airblock and returns true if they are closer than minDist.
        
        """
        ...

    @typing.overload
    def distancePlane(self, segment1: es.aslogic.geom.Trajectory, airblock: es.aslogic.geom.Airblock, minDist: float, radius: float) -> bool:
        """
        """
        ...

    @typing.overload
    def distancePlane(self, segment1: es.aslogic.geom.Trajectory, segment2: es.aslogic.geom.Trajectory, minDist: float, radius: float) -> bool:
        """
        """
        ...

    def distanceUsingPlanes(self, c1r: es.aslogic.geom.Coordinate, c2r: es.aslogic.geom.Coordinate, c3r: es.aslogic.geom.Coordinate, minDist: float, radius: float) -> bool:
        """
        Computes the distance between a segment and a point and returns true if they are closer than minDist.
        
        """
        ...

    def setFast(self, fast: bool) -> 'Filter_Horizontal_DistancePlanes':
        """
        """
        ...

    def setOverrideHorizontalDistance(self, overrideHorizontalDistance: float) -> 'Filter_Horizontal_DistancePlanes':
        """
        """
        ...

    def test(self, algorithm: PartakeDetection.Handle, cell1: es.aslogic.geom.Cell, cell2: es.aslogic.geom.Cell, lap1: LapInACell, lap2: LapInACell) -> bool:
        """
        """
        ...

class Filter_Horizontal_RealConflictsSampled(PartakeDetection.Filter):

    def __init__(self):
        """
        """
        ...

    def test(self, algorithm: PartakeDetection.Handle, cell1: es.aslogic.geom.Cell, cell2: es.aslogic.geom.Cell, lap1: LapInACell, lap2: LapInACell) -> bool:
        """
        """
        ...

class Filter_Trajectory_Lap(PartakeDetection.Filter):

    def __init__(self):
        """
        """
        ...

    def setDetectCollection(self, detectCollection: typing.Union[java.util.Collection['PartakeMission.Lap'], typing.Sequence['PartakeMission.Lap'], typing.Set['PartakeMission.Lap']]) -> 'Filter_Trajectory_Lap':
        """
        Conflicts where none of the missions is present in this collection, will be filtered out.
        
        """
        ...

    def setRegulatedCollection(self, regulatedCollection: typing.Union[java.util.Collection['PartakeMission.Lap'], typing.Sequence['PartakeMission.Lap'], typing.Set['PartakeMission.Lap']]) -> 'Filter_Trajectory_Lap':
        """
        If both missions in conflict appear in this collection, it will be filtered out.
        
        """
        ...

    def test(self, algorithm: PartakeDetection.Handle, cell1: es.aslogic.geom.Cell, cell2: es.aslogic.geom.Cell, lap1: LapInACell, lap2: LapInACell) -> bool:
        """
        """
        ...

class Filter_Trajectory_Mission(PartakeDetection.Filter):

    def __init__(self):
        """
        """
        ...

    def setDetectCollection(self, detectCollection: typing.Union[java.util.Collection['PartakeMission.PartakeMissionDetection'], typing.Sequence['PartakeMission.PartakeMissionDetection'], typing.Set['PartakeMission.PartakeMissionDetection']]) -> 'Filter_Trajectory_Mission':
        """
        Conflicts where none of the missions is present in this collection, will be filtered out.
        
        """
        ...

    @typing.overload
    def setRegulatedCollection(self, regulatedCollection: typing.Union[java.util.Collection['PartakeMission.PartakeMissionDetection'], typing.Sequence['PartakeMission.PartakeMissionDetection'], typing.Set['PartakeMission.PartakeMissionDetection']]) -> 'Filter_Trajectory_Mission':
        """
        If both missions in conflict appear in this collection, it will be filtered out.
        
        """
        ...

    @typing.overload
    def setRegulatedCollection(self, regulatedCollection: typing.Union[java.util.function.Predicate['PartakeMission.PartakeMissionDetection'], typing.Callable[[], 'PartakeMission.PartakeMissionDetection']]) -> 'Filter_Trajectory_Mission':
        """
        """
        ...

    def test(self, algorithm: PartakeDetection.Handle, cell1: es.aslogic.geom.Cell, cell2: es.aslogic.geom.Cell, lap1: LapInACell, lap2: LapInACell) -> bool:
        """
        """
        ...

class Filter_Vertical(PartakeDetection.Filter):

    def __init__(self):
        """
        """
        ...

    def test(self, algorithm: PartakeDetection.Handle, cel1: es.aslogic.geom.Cell, cell2: es.aslogic.geom.Cell, lap1: LapInACell, lap2: LapInACell) -> bool:
        """
        """
        ...

class PartakeMission:

    def getConstantMitigatedDelay(self) -> int:
        """
        If NOT null, this mission is steady at a specific delay.
        
        """
        ...

    def getLaunchWindowLowerBound(self) -> int:
        """
        """
        ...

    def getLaunchWindowUpperBound(self) -> int:
        """
        """
        ...

    def getPriority(self) -> int:
        """
        Greater priority, more difficult to be cancelled
         Greater than 0
        
        """
        ...

    def getToleranceLowerBound(self) -> int:
        """
        """
        ...

    def getToleranceUpperBound(self) -> int:
        """
        """
        ...

    def getUserObject(self) -> typing.Any:
        """
        """
        ...

    def isCancellable(self) -> bool:
        """
        """
        ...

    class Lap:

        def getBegin(self) -> int:
            """
            """
            ...

        def getEnd(self) -> int:
            """
            """
            ...

        def getMinimumHorizontalSeparation(self) -> float:
            """
            """
            ...

        def getMinimumVerticalSeparation(self) -> float:
            """
            """
            ...

        def getMission(self) -> 'PartakeMission.PartakeMissionDetection':
            """
            """
            ...

        def isActive(self) -> bool:
            """
            """
            ...

    class LapAirblock(es.aslogic.partake.PartakeMission.Lap):

        def getAirblock(self) -> es.aslogic.geom.Airblock:
            """
            """
            ...

    class LapTrajectory(es.aslogic.partake.PartakeMission.Lap):

        def getTrajectory(self) -> es.aslogic.geom.Trajectory:
            """
            """
            ...

    class PartakeMissionDetection(es.aslogic.partake.PartakeMission):

        def computeBegin(self) -> int:
            """
            """
            ...

        def computeEnd(self) -> int:
            """
            """
            ...

        def getLaps(self) -> java.util.List['PartakeMission.Lap']:
            """
            """
            ...
