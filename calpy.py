import sys
import time
import keyboard
import numpy as np
import pyaudio
import pyttsx3

# ==========================================
# Audio & Sensitivity Configuration
# ==========================================
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 256  # ~16ms frame size

# Adjust Sensitivity: "VERY_LOW", "LOW", "MEDIUM_LOW", "MEDIUM", "HIGH"
# Set to "MEDIUM_LOW" for a little bit more sensitivity than "LOW".
SENSITIVITY = "MEDIUM_LOW"

if SENSITIVITY == "VERY_LOW":
    PEAK_FLOOR = 700.0   # Must be very loud
    SNR_THRESH = 6.5
    CREST_THRESH = 4.5
elif SENSITIVITY == "LOW":
    PEAK_FLOOR = 500.0
    SNR_THRESH = 5.5
    CREST_THRESH = 4.0
elif SENSITIVITY == "MEDIUM_LOW":  # Slightly easier to trigger than LOW
    PEAK_FLOOR = 420.0
    SNR_THRESH = 5.0
    CREST_THRESH = 3.7
elif SENSITIVITY == "HIGH":
    PEAK_FLOOR = 250.0
    SNR_THRESH = 3.5
    CREST_THRESH = 2.8
else:  # "MEDIUM"
    PEAK_FLOOR = 350.0
    SNR_THRESH = 4.5
    CREST_THRESH = 3.4

# Timing Parameters
MIN_GAP = 0.12  # Prevents rapid chatter from counting as consecutive claps
MAX_GAP = 0.60

# Dynamic Tracking
ambient_rms = 50.0
clap_count = 0
last_clap_time = 0.0
cooldown_until = 0.0


def stop_script(reason="Three claps detected"):
    print(f"\n🛑 EXIT: {reason}")
    try:
        agent = pyttsx3.init()
        agent.say("closing clapy")
        agent.runAndWait()
    except Exception:
        pass
    sys.exit()


p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
)

print(f"=== Clap Detector Active (Sensitivity: {SENSITIVITY}) ===")
print("💡 Press 'F7' on your keyboard anytime to exit.\n")

try:
    while True:
        if keyboard.is_pressed("f7"):
            stop_script("Manual 'f7' key pressed")

        raw_data = stream.read(CHUNK, exception_on_overflow=False)
        audio = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32)

        rms = np.sqrt(np.mean(audio**2))
        peak = np.max(np.abs(audio))
        current_time = time.time()

        # Dynamic baseline update
        if rms < (ambient_rms * 1.4):
            ambient_rms = (ambient_rms * 0.95) + (rms * 0.05)

        # Ignore audio during cooldown
        if current_time < cooldown_until:
            continue

        # Feature Extraction
        crest_factor = peak / (rms + 1e-5)
        snr_ratio = rms / (ambient_rms + 1e-5)
        zero_crossings = np.sum(np.diff(np.signbit(audio)) != 0) / len(audio)

        # Sensitivity-controlled clap evaluation
        is_clap = (
            peak > max(ambient_rms * 2.8, PEAK_FLOOR)
            and snr_ratio > SNR_THRESH
            and crest_factor > CREST_THRESH
            and (0.09 <= zero_crossings <= 0.32)
        )

        if is_clap:
            time_since_last = current_time - last_clap_time

            if time_since_last >= MIN_GAP:
                if clap_count == 0 or time_since_last <= MAX_GAP:
                    clap_count += 1
                else:
                    clap_count = 1

                last_clap_time = current_time
                cooldown_until = current_time + 0.10  # 100ms cooldown
                print(f"👏 Clap {clap_count}...", end="\r", flush=True)

        # Trigger logic
        if clap_count > 0 and (current_time - last_clap_time) > MAX_GAP:
            if clap_count >= 2:
                keyboard.press_and_release("f9")
                print("\n👏 👏 Double Clap -> F9 Pressed!")

            clap_count = 0
            print(" " * 40, end="\r", flush=True)

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
