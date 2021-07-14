import asyncio
import hashlib
import json
import logging
import os
from http import HTTPStatus

from fastapi import FastAPI, Query, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from websockets.exceptions import ConnectionClosedOK

from mdpreview.templates import render_template
from mdpreview.util import share

PATH = "/tmp/mdpreview.md".encode()
METADATA_PATH = "/tmp/mdpreview.json"

static = os.path.join(share, "static")

app = FastAPI()
logger = logging.getLogger(__name__)

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
    app.mount("/static", StaticFiles(directory=static), name="static")
    running = True


@app.on_event("shutdown")
async def app_shutdown():
    global running
    running = False


@app.get("/")
async def markdown(request: Request, scrollTop: int = Query(default=0)):
    markdown_path = "/tmp/mdpreview.md"
    if not os.path.exists(markdown_path):
        return Response(status_code=int(HTTPStatus.NOT_FOUND))

    try:
        with open(markdown_path) as f:
            markdown = f.read()
    except OSError as exc:
        logger.error(str(exc))
        return Response(status_code=int(HTTPStatus.UNAUTHORIZED))

    metadata = get_metadata()

    logger.debug("Loaded markdown.")
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


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    global running
    await websocket.accept()
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
        pass

    await websocket.close()
