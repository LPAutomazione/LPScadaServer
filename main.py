import sys

from PySide2.QtGui import QGuiApplication

import logging

from lpss.core.server import Server

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    app = QGuiApplication(sys.argv)
    logger.info("Starting scada")

    server = Server()
    sys.exit(app.exec_())