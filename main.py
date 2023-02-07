from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from lib import camera

MIMETYPE: str = "multipart/x-mixed-replace; boundary=frame"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route("/", methods=["GET", "HEAD"])
def raw():
    stream = camera.WebCameraStream(cam_id="V4L2:/dev/video0")
    return StreamingResponse(stream.stream_frame_bytes(), headers=stream.get_metadata(), media_type=MIMETYPE)
