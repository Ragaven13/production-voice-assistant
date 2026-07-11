import sounddevice as sd
from scipy.io.wavfile import write


SAMPLE_RATE = 16000
DURATION = 5
OUTPUT_FILE = "recording.wav";

def record_audio():
    print("Recording... ")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"

    ) # NumPy Array (80000 × 1)
    sd.wait()

    write(OUTPUT_FILE,SAMPLE_RATE,audio)
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    record_audio()