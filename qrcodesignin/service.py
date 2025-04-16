import logging
from uuid import uuid4

from qrcodesignin.database import Database


logger = logging.getLogger(__name__)


class Service:

    def __init__(self, base_url):
        self._connections = {}
        self.base_url = base_url
        self._database = Database()
        logger.info("Service initialized with base_url: %s", base_url)

    def _create_image_url(self, data):
        """create a qr code for a url"""
        return f"https://api.qrserver.com/v1/create-qr-code/?data={data}&size=200x200"

    def create_new_qr_code(self, ws_connection):
        """create a new qr code"""
        uuid = self.new_uuid()
        url = f"{self.base_url}/auth/{uuid}"
        image_url = self._create_image_url(url)
        data = {
            "image_url": image_url,
            "uuid": uuid,
        }
        self._connections[uuid] = ws_connection

        self._database.create_uuid(uuid)
        return data

    def new_uuid(self):
        """create a new uuid"""

        return str(uuid4())

    async def process(self, message, ws_connection):
        """process a message from the websocket"""
        if message.get("action") == "create_qr_code":
            return self.create_new_qr_code(ws_connection)
        elif message.get("action") == "get_uuid":
            uuid = message.get("uuid")

            resp = self._database.get_uuid(uuid)
            logger.info("resp: %s", resp)
            return resp
        else:
            raise ValueError(f"Unknown action: {message.get('action')}")

    async def get_uuid(self, uuid: str):
        """get a uuid from the database"""
        logger.info("get_uuid: %s", uuid)
        if self._connections.get(uuid):
            await self._connections[uuid].send_json({"auth": True})
        return self._database.get_uuid(uuid)

    async def websocket_disconnected(self, ws_connection):
        """handle websocket disconnection"""
        logger.info("websocket disconnected")
        for uuid, connection in self._connections.items():
            if connection == ws_connection:
                logger.info("removing connection for uuid: %s", uuid)
                del self._connections[uuid]
                break
