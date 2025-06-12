#!/usr/bin/env python3
import os
import wave
import signal
import sys
from io import BytesIO

import pyaudio
from elevenlabs.client import ElevenLabs

# ---- Config ----
ELEVEN_API_KEY = "<YOUR_API_KEY_HERE>"
MODEL_ID = "scribe_v1"

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Duration control
stop_recording = False
def signal_handler(sig, frame):
    global stop_recording
    stop_recording = True
    print("\nStopping recording...")

signal.signal(signal.SIGINT, signal_handler)

# ---- Record audio from mic ----
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
print("🎙️ Recording... Press Ctrl+C to stop.")

frames = []
while not stop_recording:
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)

stream.stop_stream()
stream.close()
audio.terminate()
print("Recording complete.")

# ---- Write to WAV in memory ----
buf = BytesIO()
wf = wave.open(buf, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
buf.seek(0)

# ---- Transcribe via API ----
eleven = ElevenLabs(api_key="sk_19e377061a7da6bf99183cddce1cd3090526d35ed0813b00")
result = eleven.speech_to_text.convert(
    file=buf,
    model_id=MODEL_ID,
    tag_audio_events=True,
    diarize=True,
    language_code="eng"  # Auto-detect
)

# ---- Show transcription ----
import json
print(result.model_dump_json(indent=2))

