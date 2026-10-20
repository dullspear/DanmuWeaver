import socket
import threading
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).parent / "static"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def launch(long_video_path: str, result_data: dict):
    app = FastAPI()

    @app.get("/media")
    def media():
        return FileResponse(long_video_path)

    @app.get("/result")
    def result():
        return JSONResponse(result_data)

    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

    port = _find_free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    webbrowser.open(f"http://127.0.0.1:{port}/")
    return port
