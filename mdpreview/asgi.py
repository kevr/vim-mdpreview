import asyncio
import logging
import os

from http import HTTPStatus

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from websockets.exceptions import ConnectionClosedOK

from mdpreview.templates import render_template

curdir = os.path.dirname(__file__)
rootdir = '/'.join([curdir, ".."])

app = FastAPI()
logger = logging.getLogger(__name__)

running = True


@app.on_event("startup")
async def app_startup():
    global running
    static_dir = "/usr/share/mdpreview/static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    running = True


@app.on_event("shutdown")
async def app_shutdown():
    global running
    running = False


@app.get("/")
async def markdown(request: Request):
    markdown_path = "/tmp/mdpreview.md"
    if not os.path.exists(markdown_path):
        return Response(status_code=int(HTTPStatus.NOT_FOUND))

    try:
        with open(markdown_path) as f:
            markdown = f.read()
    except OSError as exc:
        logger.error(str(exc))
        return Response(status_code=int(HTTPStatus.UNAUTHORIZED))

    logger.debug("Loaded markdown.")
    template = render_template("index.html", markdown=markdown)
    return HTMLResponse(template)


def update_cache():
    path = "/tmp/mdpreview.md"
    cache_path = "/tmp/mdpreview.md.cache"
    with open(path) as original:
        with open(cache_path, "w") as cache:
            cache.write(original.read())


async def compare():
    path = "/tmp/mdpreview.md"
    cache_path = "/tmp/mdpreview.md.cache"
    with open(path) as mod:
        modified = mod.read()
    with open(cache_path) as cache:
        cached = cache.read()
    return modified == cached


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    global running
    await websocket.accept()
    update_cache()

    try:
        while running:
            if not await compare():
                await websocket.send_json({"message": "reload"})
            await asyncio.sleep(0.5)
    except (WebSocketDisconnect, ConnectionClosedOK):
        pass

    await websocket.close()
