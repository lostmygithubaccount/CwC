# imports
import argparse

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--size",
    type=str,
    default="large-v2",
    help="model size to use. must be one of 'tiny', 'small', 'medium', 'large', or 'large-v2'",
)
parser.add_argument(
    "--input",
    type=str,
    default="temp.mp4",
    help="path to input video file",
)
parser.add_argument(
    "--audio",
    type=str,
    default="temp.wav",
    help="path to output audio file",
)
parser.add_argument(
    "--output-dir",
    type=str,
    default="outputs",
    help="path to output directory",
)
parser.add_argument(
    "--output",
    type=str,
    default="output.txt",
    help="path to output text file",
)
parser.add_argument(
    "--sampling-rate",
    type=int,
    default=16000,
    help="sampling rate of the audio",
)
parser.add_argument(
    "--device",
    type=str,
    default="mps",
    help="device to use. must be one of 'cpu' or 'mps'",
)
parser.add_argument(
    "--silence-len",
    type=int,
    default=1200,
    help="number of frames to miliseconds as silence",
)
parser.add_argument(
    "--silence-thresh",
    type=float,
    default=-30,
    help="threshold for silence",
)
args = parser.parse_args()
