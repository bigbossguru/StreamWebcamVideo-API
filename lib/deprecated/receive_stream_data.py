import requests  # type: ignore
import ffmpeg
import cv2


def general_render_raw_bytes2video(video_name: str = "general_video") -> None:
    ffmpeg_process = (
        ffmpeg.input("pipe:", framerate=30)
        .output(f"./{video_name}.mp4", vcodec="libx264")
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    try:
        # Don't forget to change the correct source URL
        responce = requests.get(..., stream=True)

        for chunk in responce.iter_content(chunk_size=1024 * 1024):
            if chunk:
                # Remove static meta info about received data
                # like that b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                chunk = chunk[37:]
                ffmpeg_process.stdin.write(chunk)

    except:
        ffmpeg_process.stdin.close()
        ffmpeg_process.wait()


def opencv_render_raw_bytes2video(video_name: str = "opencv_video") -> None:
    # Don't forget to change the correct source URL
    video_stream = cv2.VideoCapture(...)

    if not video_stream.isOpened():
        raise Exception("Error video capture is already opens")

    width = int(video_stream.get(3))
    height = int(video_stream.get(4))
    fps = video_stream.get(5)
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    video_writer = cv2.VideoWriter(f"{video_name}.mp4", fourcc, fps, frame_size)

    try:
        while True:
            ret, frame = video_stream.read()
            if not ret:
                break

            video_writer.write(frame)

            # These two methods you can use for debugging or showing frames in realtime
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
    except:
        video_stream.release()
        cv2.destroyAllWindows()
