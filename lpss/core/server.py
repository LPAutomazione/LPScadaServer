from PySide2.QtCore import QObject

import logging

from lpss.core.scheduler import scheduler
from lpss.ws.ws_server import WsServer

logger = logging.getLogger(__name__)


class Server(QObject):
    instance = None

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)

        # Initialize the task scheduler which is in charge of polling through all the devices
        self.scheduler = scheduler()
        self.scheduler.onTick.connect(self.onSchedulerTick)
        self.scheduler.running = True

        # Initialize the WebSocket server which is in charge of communicating with the clients
        self.wsServer = WsServer()

    def onSchedulerTick(self):
        #logger.info("Tick!")
        pass

    def cleanup(self) -> None:
        """
        To be called before program exit
        """
        logger.info("Cleaning up...")
        self.scheduler.running = False
        self.wsServer.close()
        logger.info("Shutting down.")

