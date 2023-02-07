from typing import Generator
import cv2
import numpy as np
import requests  # type: ignore
import math
import ffmpeg

from .singleton import Singleton


class ClientReceiver(metaclass=Singleton):
    def __init__(self, url: str = "http://localhost:8000") -> None:
        self.url = url
        self.metadata = self._metadata()

    def display_video(self):
        for chunk in self._get_bytes():
            try:
                frame = np.frombuffer(chunk, dtype=np.uint8).reshape(*self.metadata["screen_size"])  # or 480, 640, 3)
            except:
                buffer = np.frombuffer(chunk[37:], dtype=np.uint8)
                frame = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
            cv2.imshow("", frame)
            cv2.waitKey(1)

    def record_video(self, video_name: str = "output"):
        ffmpeg_process = (
            ffmpeg.input("pipe:", framerate=self.metadata["fps"] or 30)
            .output(f"./{video_name}.mp4", vcodec="libx264")
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

        for chunk in self._get_bytes():
            try:
                ffmpeg_process.stdin.write(chunk)
            except:
                ffmpeg_process.stdin.close()
                ffmpeg_process.wait()

    def _get_bytes(self) -> Generator[bytes, None, None]:
        with requests.get(url=self.url, stream=True) as res:
            res.raise_for_status()
            for chunk in res.iter_content(chunk_size=self.metadata["chunk_size"] or 1024 * 1024):
                yield chunk

    def _metadata(self) -> dict:
        try:
            res = requests.head(self.url)
            return dict(
                screen_size=list(map(int, res.headers["frame-transform"].split(","))),
                chunk_size=math.prod(list(map(int, res.headers["chunk-size"].split(",")))),
                fps=int(res.headers["fps"]),
            )
        except:
            return {}
