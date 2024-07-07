import io
from functools import cache
from pathlib import Path

from PIL import Image
from ffmpeg import FFmpeg


@cache
def get_first_frame(video_path: Path) -> Image:
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(video_path)
        .output(
            'pipe:1',
            f='image2',
            vframes=1,
            vcodec="png"
        )
    )

    res = ffmpeg.execute()

    out_buffer = io.BytesIO(res)
    out_buffer.seek(0)
    return Image.open(out_buffer)


if __name__ == '__main__':
    target_bpm = 77.99
    frame = get_first_frame(
        video_path=Path(
            'bot/bpm_gifs/generator/templates/floppa.mp4'),
    )
    with open(f'frame.png', 'wb') as f:
        f.write(frame.read())
