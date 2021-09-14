from PySide2.QtCore import QObject

import logging

from lpss.core.scheduler import scheduler

logger = logging.getLogger(__name__)


class Server(QObject):
    instance = None

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self.scheduler = scheduler()
        self.scheduler.onTick.connect(self.onSchedulerTick)
        self.scheduler.running = True

    def onSchedulerTick(self):
        #logger.info("Tick!")
        pass
