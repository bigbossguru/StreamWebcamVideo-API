from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from lib import camera

MEDIA_TYPE: str = "multipart/x-mixed-replace; boundary=frame"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route("/", methods=["GET", "HEAD"])
def stream_webcam():
    stream = camera.WebCameraStream()
    return StreamingResponse(stream.stream_img_bytes(), headers=stream.get_metadata(), media_type=MEDIA_TYPE)
