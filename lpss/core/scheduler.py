from concurrent.futures.thread import ThreadPoolExecutor
from typing import Callable, List
from collections import deque

from PySide2.QtCore import QObject, Signal, QTimer

from lpss.settings import settings


class Schedule(QObject):
    index = 0

    def __init__(self, parent=None):
        super(Schedule, self).__init__(parent=parent)
        self.interval: int = 0      # the schedule interval in milliseconds
        self.nextFireUp: int = 0      # when is this schedule going to be fired up? in milliseconds
        self.fun: Callable or None = None
        self.i = Schedule.index
        self.args = None
        self.description = ""
        self.oneShot = False
        Schedule.index += 1

    def __str__(self):
        return f"Schedule {self.i} with interval {self.interval}ms"


class _SchedulerSingleton(QObject):
    onTick = Signal()
    instance = None

    def __init__(self, parent):
        super(_SchedulerSingleton, self).__init__(parent=parent)

        self.ms: int = 0     # milliseconds counter

        self.timeOrderedSchedules: deque = deque()  # the most important data structure

        self._toBeRescheduled: List[Schedule] = []

        self._running: bool = False

        self.threadPool = ThreadPoolExecutor(1)

        self.timer: QTimer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timerGranularity: int = settings().get("timer_granularity")
        self.timer.start(self.timerGranularity)

    def _tick(self):
        if self._running:
            self.onTick.emit()
            self.ms += self.timerGranularity
            # check in the timeOrderedSchedules for the next schedules to be run
            # remove them from the timeOrderedSchedules
            self._checkSchedule()
            # reschedule them
            self._reschedule()
            # run them
            self._runScheduled()
            # clear the list of schedules to be rescheduled and run
            self._toBeRescheduled.clear()

    def _checkSchedule(self):
        while True:
            try:
                currentSchedule: Schedule = self.timeOrderedSchedules[0]     # O(1)
            except IndexError:      # the timeOrderedSchedules is empty, there are no more schedules to extract
                return
            if self.ms >= currentSchedule.nextFireUp:
                self._toBeRescheduled.append(self.timeOrderedSchedules.popleft())   # O(1)
            else:
                return

    def _reschedule(self):
        for schedule in self._toBeRescheduled:
            schedule.nextFireUp = self.ms + schedule.interval
            if not schedule.oneShot:
                self._insertSchedule(schedule)

    def _insertSchedule(self, schedule: Schedule):
        try:
            firstSchedule = self.timeOrderedSchedules[0]
        except IndexError:  # deque length is 0, let's just append the schedule
            self.timeOrderedSchedules.append(schedule)
            return

        # Now that we know the timeOrderedSchedules is not empty, iterate it to find the place for the schedule to be
        # re-inserted
        index = 0
        while True:
            try:
                iterSchedule = self.timeOrderedSchedules[index]
            except IndexError:  # reached the length of the deque let's just append the schedule
                self.timeOrderedSchedules.append(schedule)
                return

            if iterSchedule.nextFireUp > schedule.nextFireUp:
                self.timeOrderedSchedules.insert(index, schedule)
                return
            index += 1

    def _runScheduled(self):
        for schedule in self._toBeRescheduled:
            self.threadPool.submit(schedule.fun, schedule.args)

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    def appendSchedule(self, intervalMs: int, fun: Callable, description="", args=None) -> Schedule:
        s = Schedule()
        s.interval = intervalMs
        s.fun = fun
        s.description = description
        s.args = args
        s.nextFireUp = self.ms + intervalMs
        self._insertSchedule(s)
        return s

    def oneShot(self, fun: Callable, description="", args=None, interval=1):
        s = Schedule()
        s.oneShot = True
        s.fun = fun
        s.description = description
        s.args = args
        s.nextFireUp = self.ms + interval
        self._insertSchedule(s)
        return s

    def removeSchedule(self, schedule: Schedule):
        self.timeOrderedSchedules.remove(schedule)
        try:
            self._toBeRescheduled.remove(schedule)
        except ValueError:
            return


def scheduler() -> _SchedulerSingleton:
    if _SchedulerSingleton.instance is None:
        _SchedulerSingleton.instance = _SchedulerSingleton(None)
    return _SchedulerSingleton.instance
