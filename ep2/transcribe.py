# imports
import os
import pydub
import torch

import numpy as np

from pydub.playback import play

from transformers import WhisperProcessor, WhisperForConditionalGeneration

## local imports
from args import args

# setup output
os.makedirs(args.output_dir, exist_ok=True)
output_path = os.path.join(args.output_dir, args.output)
try:
    os.remove(output_path)
except FileNotFoundError:
    pass

# try to use mps GPU
device = (
    torch.device(args.device)
    if torch.backends.mps.is_available()
    else torch.device("cpu")
)
print(f"using device: {device}")

# load model and processor
print("loading model...")
processor = WhisperProcessor.from_pretrained(f"openai/whisper-{args.size}")
model = WhisperForConditionalGeneration.from_pretrained(
    f"openai/whisper-{args.size}"
).to(device)
model.config.forced_decoder_ids = None

# extract audio
print("extracting audio from video...")
data = pydub.AudioSegment.from_file(args.input, "mp4")
data = data.set_frame_rate(args.sampling_rate)
data = data.set_channels(1)

# split data on silence
print("splitting audio on silence...")
audio_chunks = pydub.silence.split_on_silence(
    data,
    min_silence_len=args.silence_len,
    keep_silence=True,
    silence_thresh=args.silence_thresh,
)
assert len(audio_chunks) > 0, "no audio chunks found!"
print(f"found {len(audio_chunks)} chunks!")

MAX_LEN = 600_000 #250_000

transcriptions = []
print("transcribing...")
for audio_chunk in audio_chunks:
    print(f"processing chunk {len(transcriptions)+1} of {len(audio_chunks)}")
    audio_array = np.array(audio_chunk.get_array_of_samples(), dtype=np.float32)
    audio_array /= np.max(np.abs(audio_array))

    # split audio into chunks
    if len(audio_array) > MAX_LEN:
        print(f"splitting into {len(audio_array) // MAX_LEN + 1} subchunks ")
        audio_array = np.array_split(audio_array, len(audio_array) // MAX_LEN + 1)
    else:
        audio_array = [audio_array]

    for audio_array_chunk in audio_array:
        input_features = processor(
            audio_array_chunk,
            sampling_rate=args.sampling_rate,
            return_tensors="pt",
        ).input_features.to(device)

        # generate token ids
        predicted_ids = model.generate(input_features)

        # decode token ids to text
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

        print(f"writing chunk to {output_path}...")
        with open(output_path, "a") as f:
            f.write(" ".join(transcription) + "\n")

        transcriptions.extend(transcription)

full_transcription = "\n".join(transcriptions)
