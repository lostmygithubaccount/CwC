# imports
import os

# setup
#video: str = "videos/ted-godot.mp4"
video: str = "videos/mount-godot.mp4"
#video: str = "videos/shirky-love.mp4"
output_prefix: str = video.split("/")[-1].split("-")[0]
sizes: list[str] = ["tiny", "small", "medium", "large", "large-v2"]

# args
silence_len = 1200
if "shirky" in video:
    silence_len = 1000
elif "mount" in video:
    silence_len = 3000
silence_thresh: float = -40 if "shirky" in video else -30

# run
for size in sizes:
    output = f"{output_prefix}_{size.replace('-', '_')}.txt"
    os.system(
        f"python transcribe.py --size {size} --input {video} --output {output} --silence-len {silence_len} --silence-thresh {silence_thresh}"
    )
