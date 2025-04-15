"""create a web app using FastAPI"""

import logging
import os
import sys


from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket


from qrcodesignin.service import Service
import settings

logger = logging.getLogger(__name__)


def make_app():
    """create a web app using FastAPI"""
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logger.info("creating web app")
    service = Service(base_url=settings.BASE_URL)

    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/")
    async def index():
        """index path"""
        return FileResponse("./static/index.html")

    @app.get("/auth/{identifier}")
    async def get_auth(identifier: str):
        logger.info("get_auth: %s", identifier)
        resp = await service.get_uuid(identifier)
        if not resp:
            raise HTTPException(status_code=404, detail="UUID not found")
        return resp

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """Handle WebSocket connections"""
        await websocket.accept()
        try:
            while True:
                message = await websocket.receive_json()
                logger.info("got message: %r", message)
                response = await service.process(message, ws_connection=websocket)
                logger.info("response: %r", response)
                if response:
                    await websocket.send_json(response)
        except Exception as ex:
            logger.exception("WebSocket error: %s", ex)

    @app.get("/{filepath:path}")
    async def serve_file(filepath: str):
        """Serve files from the static directory or return a 404 if not found."""
        file_path = os.path.join("./static", filepath)

        # Check if the file exists
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="File not found error")

    return app
