import es.aslogic.util.time
import java.io
import java.lang
import java.time
import java.util
import java.util.function
import typing

class Formatter:

    DEFAULT_FORMAT: typing.ClassVar['Formatter'] = ...
    """
    """

    ONLY_MESSAGE_FORMAT: typing.ClassVar['Formatter'] = ...
    """
    """

    @classmethod
    def defaultFormat(cls) -> 'Formatter':
        """
        """
        ...

    def format(self, owner: 'Log', instant: java.time.LocalDateTime, level: 'Log.Level', message: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> java.lang.String:
        """
        """
        ...

    @classmethod
    def onlyMessageFormat(cls) -> 'Formatter':
        """
        """
        ...

    @classmethod
    def withName(cls, name: typing.Union[java.lang.String, str]) -> 'Formatter':
        """
        """
        ...

class L:

    loud: typing.ClassVar['Log'] = ...
    """
    """

    mute: typing.ClassVar['Log'] = ...
    """
    """

    @classmethod
    def d(cls, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs a debug message.
        
        """
        ...

    @classmethod
    def e(cls, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs an error message (by the System.err stream).
        
        """
        ...

    @classmethod
    def i(cls, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs an info message.
        
        """
        ...

    @classmethod
    def lazy(cls, o: typing.Union[java.util.function.Supplier[typing.Any], typing.Callable[[], typing.Any]]) -> typing.Any:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, traces: typing.List[java.lang.StackTraceElement], skip: int) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, th: java.lang.Throwable) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, th: java.lang.Throwable, skip: int) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, th: java.lang.Throwable, skip: int, logWriter: java.io.PrintStream) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, th: java.lang.Throwable, skip: int, logWriter: java.io.PrintWriter) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, th: java.lang.Throwable, skip: int, logWriter: typing.Union[java.util.function.Consumer[typing.Union[java.lang.String, str]], typing.Callable[[], typing.Union[java.lang.String, str]]]) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, th: java.lang.Throwable, logWriter: java.io.PrintStream) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, th: java.lang.Throwable, logWriter: java.io.PrintWriter) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def printStackTrace(cls, th: java.lang.Throwable, logWriter: typing.Union[java.util.function.Consumer[typing.Union[java.lang.String, str]], typing.Callable[[], typing.Union[java.lang.String, str]]]) -> None:
        """
        """
        ...

    @classmethod
    def printStackTraceToString(cls, th: java.lang.Throwable) -> java.lang.String:
        """
        """
        ...

    @classmethod
    def t(cls, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs a trace message.
        
        """
        ...

    @classmethod
    def to(cls, printer: typing.Union['Printer', typing.Callable]) -> 'Log_Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def toStdOut(cls) -> 'Log_Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def toStdOut(cls, name: typing.Union[java.lang.String, str]) -> 'Log_Printer':
        """
        """
        ...

    @classmethod
    def w(cls, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs a warning message.
        
        """
        ...

    class LazyParam:

        def get(self) -> typing.Any:
            """
            """
            ...

class Log:

    def child(self, childName: typing.Union[java.lang.String, str]) -> 'Log':
        """
        """
        ...

    def d(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs a debug message.
        
        """
        ...

    @typing.overload
    def e(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs an error message (by default in the System.err stream).
        
        """
        ...

    @typing.overload
    def e(self, throwable: java.lang.Throwable, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs an error message with an exception. (by default in the System.err stream).
        
        """
        ...

    def i(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs an info message.
        
        """
        ...

    def name(self) -> java.lang.String:
        """
        """
        ...

    def t(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs a trace message.
        
        """
        ...

    def v(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs a verbose message.
        
        """
        ...

    @typing.overload
    def w(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs a warning message.
        
        """
        ...

    @typing.overload
    def w(self, throwable: java.lang.Throwable, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        Logs a warning message with an exception.
        
        """
        ...

    class Level(java.lang.Enum['Log.Level']):

        MUTE: typing.ClassVar['Log.Level'] = ...
        """
        """

        ERROR: typing.ClassVar['Log.Level'] = ...
        """
        """

        WARN: typing.ClassVar['Log.Level'] = ...
        """
        """

        INFO: typing.ClassVar['Log.Level'] = ...
        """
        """

        DEBUG: typing.ClassVar['Log.Level'] = ...
        """
        """

        VERBOSE: typing.ClassVar['Log.Level'] = ...
        """
        """

        TRACE: typing.ClassVar['Log.Level'] = ...
        """
        """

        @classmethod
        @typing.overload
        def valueOf(cls, name: typing.Union[java.lang.String, str]) -> 'Log.Level':
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
        def values(cls) -> typing.List['Log.Level']:
            """
            """
            ...

class Printer:

    @classmethod
    @typing.overload
    def of(cls, formatter: typing.Union[Formatter, typing.Callable], appendable: typing.Union[java.util.function.Consumer[typing.Union[java.lang.String, str]], typing.Callable[[], typing.Union[java.lang.String, str]]]) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def of(cls, appendable: typing.Union[java.util.function.Consumer[typing.Union[java.lang.String, str]], typing.Callable[[], typing.Union[java.lang.String, str]]]) -> 'Printer':
        """
        """
        ...

    @classmethod
    def ofFilterLevel(cls, level: Log.Level, printer: typing.Union['Printer', typing.Callable]) -> 'Printer':
        """
        """
        ...

    @classmethod
    def ofFork(cls, errorPrinter: typing.Union['Printer', typing.Callable], warningPrinter: typing.Union['Printer', typing.Callable], infoPrinter: typing.Union['Printer', typing.Callable], verbosePrinter: typing.Union['Printer', typing.Callable], debugPrinter: typing.Union['Printer', typing.Callable], tracePrinter: typing.Union['Printer', typing.Callable]) -> 'Printer':
        """
        """
        ...

    @classmethod
    def ofForkError(cls, errorPrinter: typing.Union['Printer', typing.Callable], theRest: typing.Union['Printer', typing.Callable]) -> 'Printer':
        """
        """
        ...

    @classmethod
    def ofNull(cls) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofPrintStream(cls, formatter: typing.Union[Formatter, typing.Callable], appendable: java.io.PrintStream) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofPrintStream(cls, appendable: java.io.PrintStream) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofPrintWriter(cls, formatter: typing.Union[Formatter, typing.Callable], appendable: java.io.PrintWriter) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofPrintWriter(cls, appendable: java.io.PrintWriter) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofStdErr(cls) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofStdErr(cls, formatter: typing.Union[Formatter, typing.Callable]) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofStdOut(cls) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofStdOut(cls, formatter: typing.Union[Formatter, typing.Callable]) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofStringBuilder(cls, formatter: typing.Union[Formatter, typing.Callable], changed: typing.Union[java.util.function.Consumer[java.lang.StringBuilder], typing.Callable[[], java.lang.StringBuilder]]) -> 'Printer':
        """
        """
        ...

    @classmethod
    @typing.overload
    def ofStringBuilder(cls, changed: typing.Union[java.util.function.Consumer[java.lang.StringBuilder], typing.Callable[[], java.lang.StringBuilder]]) -> 'Printer':
        """
        """
        ...

    @classmethod
    def ofTee(cls, printer1: typing.Union['Printer', typing.Callable], printer2: typing.Union['Printer', typing.Callable]) -> 'Printer':
        """
        """
        ...

class Log_Delegator(Log):

    @typing.overload
    def __init__(self):
        """
        """
        ...

    @typing.overload
    def __init__(self, log: Log):
        """
        """
        ...

    def child(self, childName: typing.Union[java.lang.String, str]) -> Log:
        """
        """
        ...

    def d(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def e(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def e(self, throwable: java.lang.Throwable, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def i(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def name(self) -> java.lang.String:
        """
        """
        ...

    def setDelegate(self, delegate: Log) -> 'Log_Delegator':
        """
        """
        ...

    def t(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def v(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def w(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def w(self, throwable: java.lang.Throwable, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

class Log_Printer(Log):

    def __init__(self, name: typing.Union[java.lang.String, str], clock: typing.Union[es.aslogic.util.time.ITimeClock, typing.Callable], printer: typing.Union[Printer, typing.Callable]):
        """
        """
        ...

    def child(self, childName: typing.Union[java.lang.String, str]) -> Log:
        """
        """
        ...

    def d(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def e(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def e(self, throwable: java.lang.Throwable, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def i(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def name(self) -> java.lang.String:
        """
        """
        ...

    def t(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def v(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def w(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def w(self, throwable: java.lang.Throwable, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

class Printer_Filter_ContentContains(Printer):

    def __init__(self, substring: typing.Union[java.lang.String, str], printer: typing.Union[Printer, typing.Callable]):
        """
        """
        ...

class Printer_Filter_ContentStartsWith(Printer):

    def __init__(self, substring: typing.Union[java.lang.String, str], printer: typing.Union[Printer, typing.Callable]):
        """
        """
        ...

class Printer_Filter_Level(Printer):

    def __init__(self, level: Log.Level, printer: typing.Union[Printer, typing.Callable]):
        """
        """
        ...

class Printer_Filter_Pattern(Printer):

    @typing.overload
    def __init__(self, node: 'Printer_Filter_Pattern.Node', defaultInclude: bool, printer: typing.Union[Printer, typing.Callable]):
        """
        """
        ...

    @typing.overload
    def __init__(self, node: java.util.List['Printer_Filter_Pattern.Node'], defaultInclude: bool, printer: typing.Union[Printer, typing.Callable]):
        """
        """
        ...

    class Node:

        def __init__(self, include: bool, pattern: 'Printer_Filter_Pattern.PathPattern', level: Log.Level, printer: typing.Union[Printer, typing.Callable]):
            """
            """
            ...

        def add(self, node: 'Printer_Filter_Pattern.Node') -> 'Printer_Filter_Pattern.Node':
            """
            """
            ...

        @classmethod
        @typing.overload
        def exclude(cls, pattern: typing.Union[java.lang.String, str], level: Log.Level, childs: typing.List['Printer_Filter_Pattern.Node']) -> 'Printer_Filter_Pattern.Node':
            """
            """
            ...

        @classmethod
        @typing.overload
        def exclude(cls, pattern: typing.Union[java.lang.String, str], childs: typing.List['Printer_Filter_Pattern.Node']) -> 'Printer_Filter_Pattern.Node':
            """
            """
            ...

        def findPrinter(self) -> Printer:
            """
            """
            ...

        @classmethod
        @typing.overload
        def include(cls, pattern: typing.Union[java.lang.String, str], level: Log.Level, childs: typing.List['Printer_Filter_Pattern.Node']) -> 'Printer_Filter_Pattern.Node':
            """
            """
            ...

        @classmethod
        @typing.overload
        def include(cls, pattern: typing.Union[java.lang.String, str], childs: typing.List['Printer_Filter_Pattern.Node']) -> 'Printer_Filter_Pattern.Node':
            """
            """
            ...

        def isExcluded(self, value: 'Printer_Filter_Pattern.PathPattern', level: Log.Level) -> 'Printer_Filter_Pattern.Node':
            """
            """
            ...

        @classmethod
        def of(cls, include: bool, pattern: typing.Union[java.lang.String, str], level: Log.Level, printer: typing.Union[Printer, typing.Callable], childs: typing.List['Printer_Filter_Pattern.Node']) -> 'Printer_Filter_Pattern.Node':
            """
            """
            ...

    class PathPattern:

        def matches(self, valuePath: 'Printer_Filter_Pattern.PathPattern') -> bool:
            """
            """
            ...

        @classmethod
        def ofPattern(cls, pattern: typing.Union[java.lang.String, str]) -> 'Printer_Filter_Pattern.PathPattern':
            """
            """
            ...

        @classmethod
        def ofValue(cls, value: typing.Union[java.lang.String, str]) -> 'Printer_Filter_Pattern.PathPattern':
            """
            """
            ...

class Printer_Fork(Printer):

    def __init__(self, errorPrinter: typing.Union[Printer, typing.Callable], warningPrinter: typing.Union[Printer, typing.Callable], infoPrinter: typing.Union[Printer, typing.Callable], verbosePrinter: typing.Union[Printer, typing.Callable], debugPrinter: typing.Union[Printer, typing.Callable], tracePrinter: typing.Union[Printer, typing.Callable]):
        """
        """
        ...

class Printer_Tee(Printer):

    def __init__(self, printer1: typing.Union[Printer, typing.Callable], printer2: typing.Union[Printer, typing.Callable]):
        """
        """
        ...

class TaskLog(Log):

    def subtask(self, taskName: typing.Union[java.lang.String, str], value: float) -> 'TaskLog':
        """
        """
        ...

    def taskEnd(self) -> None:
        """
        """
        ...

    def taskStart(self, maxValue: float) -> None:
        """
        """
        ...

    def taskUpdate(self, incrementValue: float) -> None:
        """
        """
        ...

class Log_Task_Abstract(TaskLog):

    def __init__(self, taskName: typing.Union[java.lang.String, str], parent: TaskLog, valueInParent: float):
        """
        """
        ...

    def d(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def e(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def e(self, throwable: java.lang.Throwable, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def i(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def subtask(self, taskName: typing.Union[java.lang.String, str], value: float) -> TaskLog:
        """
        """
        ...

    def t(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    def taskEnd(self) -> None:
        """
        """
        ...

    def taskStart(self, maxValue: float) -> None:
        """
        """
        ...

    def taskUpdate(self, incrementValue: float) -> None:
        """
        """
        ...

    def v(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def w(self, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

    @typing.overload
    def w(self, throwable: java.lang.Throwable, what: typing.Union[java.lang.String, str], params: typing.List[typing.Any]) -> None:
        """
        """
        ...

class Log_Task_Printer(Log_Task_Abstract):

    def __init__(self, log: Log, taskName: typing.Union[java.lang.String, str], parent: TaskLog, valueInParent: float):
        """
        """
        ...

    def subtask(self, taskName: typing.Union[java.lang.String, str], value: float) -> TaskLog:
        """
        """
        ...
