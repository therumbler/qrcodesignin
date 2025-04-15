from datetime import datetime
import json
import logging
import os


logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.root_path = "./.db"
        self._create_directory(self.root_path)

    def _create_directory(self, path):
        """create the root path if it does not exist"""
        if not os.path.exists(path):
            logger.info("creating root path: %s", path)
            os.makedirs(path)
        uuids_path = os.path.join(path, "uuids")
        if not os.path.exists(uuids_path):
            logger.info("creating uuids path: %s", uuids_path)
            os.makedirs(uuids_path)

    def _get_path(self, uuid: str):
        return f"{self.root_path}/uuids/{uuid}.json"

    def get_uuid(self, uuid: str):
        path = self._get_path(uuid)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return None

    def create_uuid(self, uuid: str):
        """create a new uuid"""
        path = self._get_path(uuid)
        if os.path.exists(path):
            logger.error("trying to create uuid that already exists: %s", uuid)
            return False

        with open(path, "w", encoding="utf-8") as file:
            data = {
                "uuid": uuid,
                "ts_created": int(datetime.now().timestamp()),
            }
            file.write(json.dumps(data))
