from typing import Generator
import numpy as np
import cv2


def common_webcam_func(
    cam_id: int, to_file: bool = False, video_name: str = "output"
) -> Generator[np.ndarray, None, None]:
    cap = cv2.VideoCapture(cam_id)

    if not cap.isOpened():
        raise Exception("Error video capture is already opens")

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(5)
    frame_size = (width, height)

    if to_file:
        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        video_writer = cv2.VideoWriter(f"{video_name}.mp4", fourcc, fps, frame_size)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        if to_file:
            video_writer.write(frame)
        yield frame


def stream_video_bytes(cam_id: int = 0) -> Generator[bytes, None, None]:
    for frame in common_webcam_func(cam_id=cam_id):
        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"


def general_live_stream_webcam(cam_id: int = 0) -> None:
    for frame in common_webcam_func(cam_id=cam_id, to_file=True):
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
