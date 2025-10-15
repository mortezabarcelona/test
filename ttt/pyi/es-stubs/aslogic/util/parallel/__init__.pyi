import es
import es.aslogic.util
import es.aslogic.util.logging
import java.io
import java.lang
import java.util
import java.util.concurrent
import java.util.concurrent.locks
import java.util.function
import typing

_AsyncResult__T = typing.TypeVar('_AsyncResult__T')  # <T>

class AsyncResult(typing.Generic[_AsyncResult__T]):

    def fail(self, t: java.lang.Throwable) -> None:
        """
        """
        ...

    @typing.overload
    def success(self, object: _AsyncResult__T) -> None:
        """
        """
        ...

    @typing.overload
    def success(self) -> None:
        """
        """
        ...

_AsyncTask__IN = typing.TypeVar('_AsyncTask__IN')  # <IN>

_AsyncTask__OUT = typing.TypeVar('_AsyncTask__OUT')  # <OUT>

class AsyncTask(typing.Generic[_AsyncTask__IN, _AsyncTask__OUT]):

    _of__IN = typing.TypeVar('_of__IN')  # <IN>

    _of__OUT = typing.TypeVar('_of__OUT')  # <OUT>

    @classmethod
    def of(cls, runnable: typing.Union[java.lang.Runnable, typing.Callable]) -> 'AsyncTask'[_of__IN, _of__OUT]:
        """
        """
        ...

    def run(self, in_: _AsyncTask__IN, result: AsyncResult[_AsyncTask__OUT]) -> None:
        """
        """
        ...

class AsyncTasksRunner:

    @typing.overload
    def __init__(self):
        """
        """
        ...

    @typing.overload
    def __init__(self, name: typing.Union[java.lang.String, str]):
        """
        """
        ...

    @typing.overload
    def add(self, task: typing.Union[AsyncTask[typing.Any, typing.Any], typing.Callable[[typing.Any], typing.Any]]) -> None:
        """
        """
        ...

    @typing.overload
    def add(self, task: 'AsyncTasksRunner') -> None:
        """
        """
        ...

    @typing.overload
    def add(self, task: typing.Union[java.lang.Runnable, typing.Callable]) -> None:
        """
        """
        ...

    @typing.overload
    def addFinish(self, onFinish: typing.Union[java.lang.Runnable, typing.Callable]) -> None:
        """
        """
        ...

    @typing.overload
    def addFinish(self, onFinish: typing.Union[java.lang.Runnable, typing.Callable], runOnSuccess: bool, runOnFailure: bool) -> None:
        """
        """
        ...

    def getFailed(self) -> java.lang.Throwable:
        """
        """
        ...

    def getSuccess(self) -> typing.Any:
        """
        """
        ...

    def run(self, in_: typing.Any) -> None:
        """
        """
        ...

    def setAutoRun(self, autoRun: bool) -> None:
        """
        """
        ...

    def setRunner(self, runner: typing.Union[java.util.function.Consumer[typing.Union[java.lang.Runnable, typing.Callable]], typing.Callable[[], typing.Union[java.lang.Runnable, typing.Callable]]]) -> None:
        """
        """
        ...

    class Task:

        @typing.overload
        def __init__(self, this$0: 'AsyncTasksRunner', task: typing.Union[AsyncTask[typing.Any, typing.Any], typing.Callable[[typing.Any], typing.Any]], runOnSuccess: bool, runOnFail: bool):
            """
            """
            ...

        @typing.overload
        def __init__(self, this$0: 'AsyncTasksRunner', task: 'AsyncTasksRunner', runOnSuccess: bool, runOnFail: bool):
            """
            """
            ...

        @typing.overload
        def __init__(self, this$0: 'AsyncTasksRunner', task: typing.Union[java.lang.Runnable, typing.Callable], runOnSuccess: bool, runOnFail: bool):
            """
            """
            ...

        def canRun(self) -> bool:
            """
            """
            ...

class CurrentThreadReadWriteLocker:

    def __init__(self, lock: 'MonitorReentrantReadWriteLock'):
        """
        """
        ...

    def lockRead(self) -> java.io.Closeable:
        """
        """
        ...

    def lockWrite(self) -> java.io.Closeable:
        """
        """
        ...

class DelayedUpdater:

    @typing.overload
    def __init__(self):
        """
        """
        ...

    @typing.overload
    def __init__(self, delayMillis: int, maxDelay: int):
        """
        """
        ...

    def notifyUpdate(self, runnable: typing.Union[java.lang.Runnable, typing.Callable]) -> None:
        """
        """
        ...

    def onApply(self) -> None:
        """
        """
        ...

    def start(self) -> None:
        """
        """
        ...

    def stop(self) -> None:
        """
        """
        ...

class FifoPriorityThreadPoolExecutor(java.util.concurrent.ThreadPoolExecutor):
    """
    A FIFO priority `ThreadPoolExecutor` that prioritizes submitted `Runnable`s by assuming they implement
     `FifoPriorityThreadPoolExecutor.Prioritized`. `FifoPriorityThreadPoolExecutor.Prioritized` runnables that return lower values for `FifoPriorityThreadPoolExecutor.Prioritized.getPriority()`
     will be executed before those that return higher values. Priorities only apply when multiple items are queued at the
     same time. Runnables with the same priority will be executed in FIFO order.
    
    """

    @typing.overload
    def __init__(self, poolSize: int):
        """
        """
        ...

    @typing.overload
    def __init__(self, corePoolSize: int, maximumPoolSize: int, keepAlive: int, timeUnit: java.util.concurrent.TimeUnit):
        """
        """
        ...

    @typing.overload
    def __init__(self, corePoolSize: int, maximumPoolSize: int, keepAlive: int, timeUnit: java.util.concurrent.TimeUnit, threadFactory: typing.Union[java.util.concurrent.ThreadFactory, typing.Callable]):
        """
        """
        ...

    class DefaultThreadFactory(java.util.concurrent.ThreadFactory):

        def __init__(self):
            """
            """
            ...

        def newThread(self, runnable: typing.Union[java.lang.Runnable, typing.Callable]) -> java.lang.Thread:
            """
            """
            ...

    class Prioritized:

        def getPriority(self) -> int:
            """
            """
            ...

class FlushableThreadPoolExecutor(java.util.concurrent.ThreadPoolExecutor):

    @typing.overload
    def __init__(self, corePoolSize: int, maximumPoolSize: int, keepAliveTime: int, unit: java.util.concurrent.TimeUnit, workQueue: java.util.concurrent.BlockingQueue[typing.Union[java.lang.Runnable, typing.Callable]]):
        """
        """
        ...

    @typing.overload
    def __init__(self, corePoolSize: int, maximumPoolSize: int, keepAliveTime: int, unit: java.util.concurrent.TimeUnit, workQueue: java.util.concurrent.BlockingQueue[typing.Union[java.lang.Runnable, typing.Callable]], handler: typing.Union[java.util.concurrent.RejectedExecutionHandler, typing.Callable]):
        """
        """
        ...

    @typing.overload
    def __init__(self, corePoolSize: int, maximumPoolSize: int, keepAliveTime: int, unit: java.util.concurrent.TimeUnit, workQueue: java.util.concurrent.BlockingQueue[typing.Union[java.lang.Runnable, typing.Callable]], threadFactory: typing.Union[java.util.concurrent.ThreadFactory, typing.Callable]):
        """
        """
        ...

    @typing.overload
    def __init__(self, corePoolSize: int, maximumPoolSize: int, keepAliveTime: int, unit: java.util.concurrent.TimeUnit, workQueue: java.util.concurrent.BlockingQueue[typing.Union[java.lang.Runnable, typing.Callable]], threadFactory: typing.Union[java.util.concurrent.ThreadFactory, typing.Callable], handler: typing.Union[java.util.concurrent.RejectedExecutionHandler, typing.Callable]):
        """
        """
        ...

    def execute(self, runnable: typing.Union[java.lang.Runnable, typing.Callable]) -> None:
        """
        """
        ...

    def flush(self) -> None:
        """
        """
        ...

    def shutdownNow(self) -> java.util.List[java.lang.Runnable]:
        """
        """
        ...

    @typing.overload
    def submit(self, runnable: typing.Union[java.lang.Runnable, typing.Callable]) -> java.util.concurrent.Future[typing.Any]:
        """
        """
        ...

    _submit_1__T = typing.TypeVar('_submit_1__T')  # <T>

    @typing.overload
    def submit(self, runnable: typing.Union[java.lang.Runnable, typing.Callable], t: _submit_1__T) -> java.util.concurrent.Future[_submit_1__T]:
        """
        """
        ...

    _submit_2__T = typing.TypeVar('_submit_2__T')  # <T>

    @typing.overload
    def submit(self, callable: typing.Union[java.util.concurrent.Callable[_submit_2__T], typing.Callable[[], _submit_2__T]]) -> java.util.concurrent.Future[_submit_2__T]:
        """
        """
        ...

class Locker:

    def __init__(self, lock: java.util.concurrent.locks.Lock):
        """
        """
        ...

    def lock(self) -> java.io.Closeable:
        """
        """
        ...

class MonitorLock:

    def lock(self, monitor: typing.Any) -> None:
        """
        """
        ...

    @typing.overload
    def tryLock(self, monitor: typing.Any) -> bool:
        """
        """
        ...

    @typing.overload
    def tryLock(self, monitor: typing.Any, time: int, unit: java.util.concurrent.TimeUnit) -> bool:
        """
        """
        ...

    def unlock(self, monitor: typing.Any) -> None:
        """
        """
        ...

    @classmethod
    def wrap(cls, lock: java.util.concurrent.locks.Lock) -> 'MonitorLock':
        """
        """
        ...

_Parallel__LoopBody__T = typing.TypeVar('_Parallel__LoopBody__T')  # <T>

class Parallel:
    """
    COPY\-PASTE: TODO Revisar
    
    """

    iCPU: typing.ClassVar[int] = ...
    """
    """

    def __init__(self):
        """
        """
        ...

    _For_0__T = typing.TypeVar('_For_0__T')  # <T>

    @classmethod
    @typing.overload
    def For(cls, start: int, stop: int, loopBody: typing.Union['Parallel.LoopBody'[int], typing.Callable[[], int]]) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def For(cls, nCpus: int, start: int, stop: int, loopBody: typing.Union['Parallel.LoopBody'[int], typing.Callable[[], int]]) -> None:
        """
        """
        ...

    _ForEach_0__T = typing.TypeVar('_ForEach_0__T')  # <T>

    @classmethod
    @typing.overload
    def ForEach(cls, nCpus: int, parameters: typing.Union[java.lang.Iterable[_ForEach_0__T], typing.Sequence[_ForEach_0__T], typing.Set[_ForEach_0__T], typing.Callable[[], _ForEach_0__T]], loopBody: typing.Union['Parallel.LoopBody'[_ForEach_0__T], typing.Callable[[], _ForEach_0__T]]) -> None:
        """
        """
        ...

    _ForEach_1__T = typing.TypeVar('_ForEach_1__T')  # <T>

    @classmethod
    @typing.overload
    def ForEach(cls, parameters: typing.Union[java.lang.Iterable[_ForEach_1__T], typing.Sequence[_ForEach_1__T], typing.Set[_ForEach_1__T], typing.Callable[[], _ForEach_1__T]], loopBody: typing.Union['Parallel.LoopBody'[_ForEach_1__T], typing.Callable[[], _ForEach_1__T]]) -> None:
        """
        """
        ...

    @classmethod
    def Fork(cls, nCpus: int, tasks: typing.List[java.lang.Runnable]) -> None:
        """
        """
        ...

    @classmethod
    def main(cls, argv: typing.List[java.lang.String]) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def runAsync(cls, run: typing.Union[java.lang.Runnable, typing.Callable]) -> java.util.concurrent.Future[typing.Any]:
        """
        """
        ...

    _runAsync_1__T = typing.TypeVar('_runAsync_1__T')  # <T>

    @classmethod
    @typing.overload
    def runAsync(cls, run: typing.Union[java.util.concurrent.Callable[_runAsync_1__T], typing.Callable[[], _runAsync_1__T]]) -> java.util.concurrent.Future[_runAsync_1__T]:
        """
        """
        ...

    class LoopBody(typing.Generic[_Parallel__LoopBody__T]):

        def run(self, i: _Parallel__LoopBody__T) -> None:
            """
            """
            ...

    class ParallelTest:

        def __init__(self):
            """
            """
            ...

class PausableThreadPoolExecutor(java.util.concurrent.ScheduledThreadPoolExecutor):

    def __init__(self, corePoolSize: int):
        """
        """
        ...

    def isPaused(self) -> bool:
        """
        """
        ...

    def isRunning(self) -> bool:
        """
        """
        ...

    def pause(self) -> None:
        """
        Pause the execution
        
        """
        ...

    def resume(self) -> None:
        """
        Resume pool execution
        
        """
        ...

class ReadWriteLock:

    def readLock(self) -> MonitorLock:
        """
        """
        ...

    def writeLock(self) -> MonitorLock:
        """
        """
        ...

_Sync__ThrowingRunnable__T = typing.TypeVar('_Sync__ThrowingRunnable__T', bound=java.lang.Exception)  # <T>

class Sync:

    def __init__(self):
        """
        """
        ...

    @classmethod
    @typing.overload
    def i11e(cls, monitor: java.util.concurrent.locks.Lock) -> java.lang.AutoCloseable:
        """
        """
        ...

    @classmethod
    @typing.overload
    def i11e(cls, monitor: java.util.concurrent.locks.Lock, block: typing.Union[java.lang.Runnable, typing.Callable]) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def of(cls, monitor: java.util.concurrent.locks.Lock) -> java.lang.AutoCloseable:
        """
        """
        ...

    _of_1__T = typing.TypeVar('_of_1__T')  # <T>

    @classmethod
    @typing.overload
    def of(cls, monitor: java.util.concurrent.locks.Lock, ticker: typing.Union[es.aslogic.util.Ticker, typing.Callable], block: typing.Union[java.util.function.Supplier[_of_1__T], typing.Callable[[], _of_1__T]]) -> _of_1__T:
        """
        """
        ...

    _of_2__T = typing.TypeVar('_of_2__T')  # <T>

    @classmethod
    @typing.overload
    def of(cls, monitor: java.util.concurrent.locks.Lock, block: typing.Union[java.util.function.Supplier[_of_2__T], typing.Callable[[], _of_2__T]]) -> _of_2__T:
        """
        """
        ...

    @classmethod
    @typing.overload
    def of(cls, monitor: java.util.concurrent.locks.Lock, ticker: typing.Union[es.aslogic.util.Ticker, typing.Callable], block: typing.Union[java.lang.Runnable, typing.Callable]) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def of(cls, monitor: java.util.concurrent.locks.Lock, block: typing.Union[java.lang.Runnable, typing.Callable]) -> None:
        """
        """
        ...

    _ofThrowing__T = typing.TypeVar('_ofThrowing__T', bound=java.lang.Exception)  # <T>

    @classmethod
    def ofThrowing(cls, monitor: java.util.concurrent.locks.Lock, ticker: typing.Union[es.aslogic.util.Ticker, typing.Callable], block: typing.Union['Sync.ThrowingRunnable'[_ofThrowing__T], typing.Callable[[], _ofThrowing__T]]) -> None:
        """
        """
        ...

    @classmethod
    @typing.overload
    def sneakyI11e(cls, monitor: java.util.concurrent.locks.Lock) -> java.lang.AutoCloseable:
        """
        """
        ...

    @classmethod
    @typing.overload
    def sneakyI11e(cls, monitor: java.util.concurrent.locks.Lock, block: typing.Union[java.lang.Runnable, typing.Callable]) -> None:
        """
        """
        ...

    class ThrowingRunnable(typing.Generic[_Sync__ThrowingRunnable__T]):

        def run(self) -> None:
            """
            """
            ...

class MonitorReentrantReadWriteLock(ReadWriteLock):

    def __init__(self):
        """
        """
        ...

    def dump(self, sb: java.lang.StringBuilder) -> java.lang.StringBuilder:
        """
        """
        ...

    def readLock(self) -> MonitorLock:
        """
        """
        ...

    def writeLock(self) -> MonitorLock:
        """
        """
        ...

class ReadWriteUpdateLock(ReadWriteLock):

    def updateLock(self) -> MonitorLock:
        """
        """
        ...

class MonitorNonReentrantReadWriteUpdateLock(ReadWriteUpdateLock):

    def __init__(self):
        """
        """
        ...

    def dump(self, sb: java.lang.StringBuilder) -> java.lang.StringBuilder:
        """
        """
        ...

    @typing.overload
    def readLock(self) -> MonitorLock:
        """
        """
        ...

    @typing.overload
    def readLock(self, debugLog: es.aslogic.util.logging.Log) -> MonitorLock:
        """
        """
        ...

    @typing.overload
    def updateLock(self) -> MonitorLock:
        """
        """
        ...

    @typing.overload
    def updateLock(self, debugLog: es.aslogic.util.logging.Log) -> MonitorLock:
        """
        """
        ...

    @typing.overload
    def writeLock(self) -> MonitorLock:
        """
        """
        ...

    @typing.overload
    def writeLock(self, debugLog: es.aslogic.util.logging.Log) -> MonitorLock:
        """
        """
        ...

_AsyncCallback__AsyncTaskHelper__T = typing.TypeVar('_AsyncCallback__AsyncTaskHelper__T')  # <T>

_AsyncCallback__T = typing.TypeVar('_AsyncCallback__T')  # <T>

class AsyncCallback(typing.Generic[_AsyncCallback__T]):

    EMPTY: typing.ClassVar['AsyncCallback'] = ...
    """
    """

    _empty__V = typing.TypeVar('_empty__V')  # <V>

    @classmethod
    def empty(cls) -> 'AsyncCallback'[_empty__V]:
        """
        """
        ...

    _onFail__V = typing.TypeVar('_onFail__V')  # <V>

    @classmethod
    def onFail(cls, t: typing.Union[java.util.function.Consumer[java.lang.Throwable], typing.Callable[[], java.lang.Throwable]]) -> 'AsyncCallback.AsyncTaskHelper'[_onFail__V]:
        """
        """
        ...

    def onFailure(self, caught: java.lang.Throwable) -> None:
        """
        """
        ...

    @typing.overload
    def onSuccess(self, result: _AsyncCallback__T) -> None:
        """
        """
        ...

    _onSuccess_1__V = typing.TypeVar('_onSuccess_1__V')  # <V>

    @classmethod
    @typing.overload
    def onSuccess(cls, t: typing.Union[java.util.function.Consumer[_onSuccess_1__V], typing.Callable[[], _onSuccess_1__V]]) -> 'AsyncCallback.AsyncTaskHelper'[_onSuccess_1__V]:
        """
        """
        ...

    _single__V = typing.TypeVar('_single__V')  # <V>

    @classmethod
    def single(cls, callback: typing.Union[java.util.function.Consumer[bool], typing.Callable[[], bool]]) -> 'AsyncCallback'[_single__V]:
        """
        """
        ...

    _to__V = typing.TypeVar('_to__V')  # <V>

    @classmethod
    def to(cls, result: AsyncResult[_to__V]) -> 'AsyncCallback'[_to__V]:
        """
        """
        ...

    class AsyncTaskHelper(es.aslogic.util.parallel.AsyncCallback[_AsyncCallback__AsyncTaskHelper__T], typing.Generic[_AsyncCallback__AsyncTaskHelper__T]):

        def __init__(self):
            """
            """
            ...

        def onFailure(self, caught: java.lang.Throwable) -> None:
            """
            """
            ...

        def onSuccess(self, result: _AsyncCallback__AsyncTaskHelper__T) -> None:
            """
            """
            ...

_AsyncCallbackWithInput__IN = typing.TypeVar('_AsyncCallbackWithInput__IN')  # <IN>

_AsyncCallbackWithInput__OUT = typing.TypeVar('_AsyncCallbackWithInput__OUT')  # <OUT>

class AsyncCallbackWithInput(AsyncCallback[_AsyncCallbackWithInput__OUT], typing.Generic[_AsyncCallbackWithInput__IN, _AsyncCallbackWithInput__OUT]):

    def getIn(self) -> _AsyncCallbackWithInput__IN:
        """
        """
        ...
