"""
import uvicorn
from fastapi.responses import StreamingResponse
from fastapi.responses import Response as FastResponse

from flask import Response as FlaskResponse

from server import server_fastapi, server_flaskapi
from lib import camera

MIMETYPE: str = "multipart/x-mixed-replace; boundary=frame"

fastapi_app = server_fastapi.fastapi_app()


@fastapi_app.api_route("/", methods=["GET", "HEAD"])
def raw():
    stream = camera.WebCameraStream()
    return StreamingResponse(stream.stream_frame_bytes(), headers=stream.get_metadata(), media_type=MIMETYPE)


flask_app = server_flaskapi.flask_app()


@flask_app.route("/")
def video():
    stream = camera.WebCameraStream()
    return FlaskResponse(stream.stream_img_bytes(), headers=stream.get_metadata(), mimetype=MIMETYPE)


if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
    flask_app.run(host="0.0.0.0", port=8000, threaded=True)
"""
