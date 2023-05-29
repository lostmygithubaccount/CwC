import subprocess
import soundfile as sf
import torch
from transformers import Speech2Text2Processor, SpeechEncoderDecoderModel
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Check if MPS is available
# device = torch.device('mps') if torch.backends.mps.is_available() else torch.device('cpu')

video_path = "temp.mp4"
audio_path = "temp.wav"


# Extract audio from the video file using ffmpeg
print("extracting audio from video...")
command = f"ffmpeg -y -i {video_path} -ab 160k -ac 1 -ar 16000 -vn {audio_path}"
subprocess.call(command, shell=True)


# Load the speech-to-text model and processor
# model = SpeechEncoderDecoderModel.from_pretrained("facebook/s2t-wav2vec2-large-en-de")#.to(device)
# processor = Speech2Text2Processor.from_pretrained("facebook/s2t-wav2vec2-large-en-de")
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")


# Read the audio file
speech, _ = sf.read("temp.wav")

# Process the audio file
inputs = processor(speech, sampling_rate=16_000, return_tensors="pt")  # .to(device)

# Generate transcription
generated_ids = model.generate(
    inputs=inputs["input_values"], attention_mask=inputs["attention_mask"]
)

# Decode the transcription
transcription = processor.batch_decode(generated_ids)

# Print the transcription
print(transcription)


"""
import subprocess
import torch
from transformers import Speech2Text2Processor, SpeechEncoderDecoderModel
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import soundfile as sf

# Use MPS if available
# device = torch.device('mps') if torch.backends.mps.is_available() else torch.device('cpu')
# print(f"Using device: {device}")

# First, we'll need to extract the audio from the video using ffmpeg
video_path = "temp.mp4"
audio_path = "temp.wav"

print("extracting audio from video...")
command = f"ffmpeg -i {video_path} -ab 160k -ac 1 -ar 16000 -vn {audio_path}"
subprocess.call(command, shell=True)

# Load pretrained model and processor
print("loading model and processor...")
model = "facebook/s2t-wav2vec2-large-en-de"
#model = Wav2Vec2ForCTC.from_pretrained(model)  # .to(device)
#processor = Wav2Vec2Processor.from_pretrained(model)
model = SpeechEncoderDecoderModel.from_pretrained(model)
processor = Speech2Text2Processor.from_pretrained(model)
#model = SpeechEncoderDecoderModel.from_pretrained(model)  # .to(device)
#processor = Speech2Text2Processor.from_pretrained(model)

# Read the audio file
print("reading audio file...")
speech, _ = sf.read(audio_path)

# Process the audio
print("processing audio...")
inputs = processor(speech, sampling_rate=16_000, return_tensors="pt")  # .to(device)

# Generate the transcription
print("generating transcription...")
generated_ids = model.generate(
    inputs=inputs["input_values"], attention_mask=inputs["attention_mask"]
)
transcription = processor.batch_decode(generated_ids)

# Write the transcription to a text file
print("writing transcription to file...")
with open("transcription.txt", "w") as f:
    f.write("\n".join(transcription))
    """
