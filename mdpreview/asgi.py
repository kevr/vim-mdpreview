import asyncio
import hashlib
import json
import logging
import os
from http import HTTPStatus
from typing import List

from fastapi import FastAPI, Query, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from websockets.exceptions import ConnectionClosedOK

from mdpreview.templates import render_template
from mdpreview.util import share

HOME = os.environ.get("HOME", "/root")
PATH = os.path.join(HOME, ".mdpreview.md")
METADATA_PATH = os.path.join(HOME, ".mdpreview.json")
STATIC = os.path.join(share, "static")

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

cache_hash = ''

running = True


def get_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH) as fd:
            return json.load(fd)
    return {
        # Default values.
        "x": 0,
        "y": 0
    }


@app.on_event("startup")
async def app_startup():
    global running
    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    running = True


@app.on_event("shutdown")
async def app_shutdown():
    global running
    running = False


@app.get("/")
async def markdown(request: Request, scrollTop: int = Query(default=0)):
    if not os.path.exists(PATH):
        return Response(status_code=int(HTTPStatus.NOT_FOUND))

    try:
        with open(PATH) as f:
            markdown = f.read()
    except OSError as exc:
        logger.error(str(exc))
        return Response(status_code=int(HTTPStatus.UNAUTHORIZED))

    logger.info("Loaded markdown.")
    template = render_template("index.html", markdown=markdown,
                               scrollTop=scrollTop)
    return HTMLResponse(template)


def get_hash():
    with open(PATH, "rb") as f:
        md5 = hashlib.md5()
        md5.update(f.read())
        return md5.hexdigest()


def update_cache():
    global cache_hash
    cache_hash = get_hash()


async def compare():
    return get_hash() == cache_hash


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    global running
    await manager.connect(websocket)
    update_cache()

    try:
        while running:
            if not await compare():
                metadata = get_metadata()
                data = {"message": "reload"}
                data.update(metadata)
                await websocket.send_json(data)
                update_cache()
            await asyncio.sleep(0.2)
    except (WebSocketDisconnect, ConnectionClosedOK):
        manager.disconnect(websocket)
