from typing import Generator, Optional
import cv2
import numpy as np

from .singleton import Singleton


class BaseWebCamera:
    def __init__(self, cam_id: int = 0) -> None:
        self.cam_id = cam_id
        self.cam = cv2.VideoCapture(self.cam_id)
        self.width = int(self.cam.get(3))
        self.height = int(self.cam.get(4))
        self.fps = int(self.cam.get(5))

    def get_metadata(self) -> dict:
        frame_transform = ",".join(map(str, (self.height, self.width, 3)))
        return {
            "Frame-Transform": frame_transform,
            "Chunk-Size": "1024,1024",
            "FPS": str(self.fps),
        }

    def get_frame(self) -> np.ndarray:
        _, frame = self.cam.read()
        frame = cv2.flip(frame, 1)
        return frame


class WebCameraStream(BaseWebCamera, metaclass=Singleton):
    def stream_frame_bytes(self) -> Generator[bytes, None, None]:
        while self.cam.isOpened():
            yield self.get_frame().tobytes()

    def stream_img_bytes(self) -> Generator[bytes, None, None]:
        while self.cam.isOpened():
            _, buffer = cv2.imencode(".jpg", self.get_frame())
            img_frame = buffer.tobytes()
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + img_frame + b"\r\n"


class WebCameraRecoder(BaseWebCamera, metaclass=Singleton):
    def __init__(self, video_name: Optional[str] = None, cam_id: int = 0):
        self.video_name = video_name
        super().__init__(cam_id)

    def record_video(self) -> None:
        fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
        self.video_writer = cv2.VideoWriter(f"{self.video_name}.mp4", fourcc, self.fps, (self.width, self.height))

        while self.cam.isOpened():
            self.video_writer.write(self.get_frame())
