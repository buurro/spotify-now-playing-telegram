import logging

from ffmpeg import FFmpeg
from pathlib import Path

from bot.utils.config import tmp_gifs_dir

logger = logging.getLogger(__name__)


def adjust_video_tempo(video_path: Path, video_bpm: float, target_bpm: float) -> bytes:
    current_interval_sec = 60.0 / video_bpm
    target_interval_sec = 60.0 / target_bpm

    speed_factor = current_interval_sec / target_interval_sec

    output_file = tmp_gifs_dir / f"{video_path.stem}_{int(target_bpm)}.mp4"

    if output_file.exists():
        logger.info(f"Using cached video: {output_file}")
        with open(output_file, 'rb') as f:
            content = f.read()

        return content

    logger.info(f"Adjusting tempo from {video_bpm} -> {output_file}")

    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(video_path)
        .output(
            output_file,
            # there was pipe:1 before but mp4 not support streaming
            f='mp4',
            vf=f"setpts=(PTS-STARTPTS)/{speed_factor}",
            af=f"atempo={speed_factor}",
            vcodec="libx264",
            preset="slow",
            crf=24,

        )
    )

    try:
        ffmpeg.execute()
        with open(output_file, 'rb') as f:
            content = f.read()
    finally:
        output_file.unlink(missing_ok=True)

    logger.info(f"Video adjusted: {output_file}")
    return content


if __name__ == '__main__':
    target_bpm = 77.99
    new_video_content = adjust_video_tempo(
        video_path=Path(
            'bot/bpm_gifs/generator/templates/100_floppa.mp4'),
        video_bpm=600,
        target_bpm=target_bpm,
    )
    with open(f'adjusted_{target_bpm}.mp4', 'wb') as f:
        f.write(new_video_content)
