import logging
from typing import List

from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtNetwork import QHostAddress
from PySide2.QtWebSockets import QWebSocketServer, QWebSocket

from lpss.settings import settings

logger = logging.getLogger(__name__)


class ClientWrapper(QObject):
    """
    A wrapper around the QWebSocket class
    """

    disconnected = Signal(object)

    def __init__(self, client: QWebSocket, parent=None):
        super(ClientWrapper, self).__init__(parent=parent)
        self.wsClient: QWebSocket = client
        self.wsClient.textMessageReceived.connect(self.onTextMessageReceived)
        self.wsClient.disconnected.connect(self.onDisconnected)

    @Slot(str)
    def sendTextMessage(self, msg: str):
        self.wsClient.sendTextMessage(msg)

    @Slot(str)
    def onTextMessageReceived(self, msg: str):
        logger.info(f"Received: {msg} from {self.sender()}")
        #self.client.sendTextMessage("Welcome")

    @Slot()
    def onDisconnected(self):
        logger.info(f"Client disconnected")
        self.disconnected.emit(self)


class WsServer(QObject):
    """
    A Websocket server that keeps track of the connected clients
    """

    clients: List[ClientWrapper] = []   # the list of currently connected clients

    def __init__(self, parent=None):
        super(WsServer, self).__init__(parent=parent)
        self.srv = QWebSocketServer("LpaServer", QWebSocketServer.NonSecureMode)
        self.srv.newConnection.connect(self.onNewConnection)
        self.srv.closed.connect(self.onClosed)
        if not self.srv.listen(QHostAddress.LocalHost, settings().get("wss_port")):
            logger.error("Failed to open web socket server.")

    def close(self) -> None:
        """
        Gracefully disconnect all the clients if any, and terminates the WebSocket server
        """
        for client in self.clients:
            client.wsClient.close()
        self.srv.close()

    @Slot()
    def onNewConnection(self):
        """
        When a websocket client connects, we wrap it into a ClientWrapper and store it into the list
        of connected clients
        """
        conn: QWebSocket = self.srv.nextPendingConnection()
        client = ClientWrapper(conn)
        client.disconnected.connect(self.onDisconnected)
        self.clients.append(client)
        logger.info(f"New connection, clients num: {len(self.clients)}")

    @Slot(object)
    def onDisconnected(self, obj: ClientWrapper) -> None:
        """
        When a client disconnects itself we remove it from the list of connected clients
        """
        self.clients.remove(obj)
        logger.info(f"Current number of clients connected: {len(self.clients)}")

    def onClosed(self):
        logger.info("Websocket Server closed")
