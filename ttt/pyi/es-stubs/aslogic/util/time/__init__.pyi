import datetime
import es.aslogic.util.logging
import java.lang
import java.sql
import java.time
import java.time.format
import java.time.temporal
import java.util
import java.util.regex
import typing

class Chrono:
    """
    This class holds a time and makes substractions to get the elapsed times.
    
    """

    instance: typing.ClassVar['Chrono'] = ...
    """
    """

    def __init__(self):
        """
        """
        ...

    def millis(self) -> float:
        """
        """
        ...

    def millisResetStart(self) -> float:
        """
        """
        ...

    def millisRestart(self) -> float:
        """
        """
        ...

    @classmethod
    def newStart(cls) -> 'Chrono':
        """
        """
        ...

    def pause(self) -> float:
        """
        """
        ...

    def reset(self) -> None:
        """
        """
        ...

    def secs(self) -> float:
        """
        """
        ...

    def secsResetStart(self) -> float:
        """
        """
        ...

    def secsRestart(self) -> float:
        """
        """
        ...

    def start(self) -> None:
        """
        """
        ...

    def toString(self) -> java.lang.String:
        """
        """
        ...

class ProgressChrono:
    """
    This class holds a time and makes substractions to get the elapsed times.
    
    """

    FORMAT_SECS: typing.ClassVar[int] = ...
    """
    """

    FORMAT_COLON: typing.ClassVar[int] = ...
    """
    """

    FORMAT_COMP: typing.ClassVar[int] = ...
    """
    """

    log: es.aslogic.util.logging.Log = ...
    """
    """

    maskOnes: int = ...
    """
    """

    processName: java.lang.String = ...
    """
    """

    progressStartName: java.lang.String = ...
    """
    """

    progressRunName: java.lang.String = ...
    """
    """

    progressStopName: java.lang.String = ...
    """
    """

    showProgress: bool = ...
    """
    """

    showPercent: bool = ...
    """
    """

    showAccTime: bool = ...
    """
    """

    showAccTimeFormat: int = ...
    """
    """

    showSpeed: bool = ...
    """
    """

    showSpeedUnit: java.lang.String = ...
    """
    """

    def __init__(self):
        """
        """
        ...

    def finish(self) -> None:
        """
        """
        ...

    @typing.overload
    def increment(self) -> None:
        """
        """
        ...

    @typing.overload
    def increment(self, many: int) -> None:
        """
        """
        ...

    def notSyncIncrement(self) -> None:
        """
        """
        ...

    @classmethod
    def of(cls, total: int, step: int, log: es.aslogic.util.logging.Log) -> 'ProgressChrono':
        """
        """
        ...

    def setPrintAproxGap(self, total: int) -> 'ProgressChrono':
        """
        """
        ...

    def setTotal(self, total: int) -> 'ProgressChrono':
        """
        """
        ...

    def start(self) -> 'ProgressChrono':
        """
        """
        ...
