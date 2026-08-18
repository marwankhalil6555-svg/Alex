import os
import time
import numpy as np
import keyboard
import psutil
import sounddevice as sd
from faster_whisper import WhisperModel

# Pin process to lower priority to cap CPU impact
process = psutil.Process(os.getpid())
try:
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
except Exception:
    pass

# Initialize Whisper with fastest single-thread configuration
model = WhisperModel(
    "tiny.en", 
    device="cpu", 
    compute_type="int8", 
    cpu_threads=1,
    num_workers=1,
)

SAMPLE_RATE = 16000
CHUNK_SAMPLES = int(0.6 * SAMPLE_RATE)  # Reduced to 600ms for faster response time
SILENCE_THRESHOLD = 0.015               # Slightly raised to skip low-level background noise
TARGET_WORDS = {"alex", "alex."}

print("⚡ Fast & Low-CPU Stream Active...")

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", blocksize=CHUNK_SAMPLES) as stream:
    while True:
        audio, overflowed = stream.read(CHUNK_SAMPLES)
        audio = audio.flatten()

        # Fast RMS-based Voice Activity Detection check
        rms = np.sqrt(np.mean(audio**2))
        if rms < SILENCE_THRESHOLD:
            time.sleep(0.01)
            continue

        # Fast transcribe: greedy search (beam_size=1) minimizes CPU usage
        segments, _ = model.transcribe(
            audio, 
            language="en", 
            beam_size=3, 
            temperature=0,
        )

        text = "".join(segment.text for segment in segments).strip().lower()

        if text:
            print(f"Heard: '{text}'")

            # Rapid exact match and boundary clean-up
            clean_text = text.rstrip(".")
            if clean_text in TARGET_WORDS or "alex" in clean_text.split():
                keyboard.press_and_release("f9")
                print("🎯 Alex Detected -> F9 Triggered!")
                # Brief pause to prevent double-triggering on the same word
                time.sleep(0.3)

        time.sleep(0.01)
