import collections
import wave

import sounddevice as sd
import webrtcvad


SAMPLE_RATE = 16000
FRAME_DURATION_MS = 30
CHANNELS = 1
VAD_MODE = 2
OUTPUT_FILE = "vad_recording.wav"


def record_until_silence():
    vad = webrtcvad.Vad(VAD_MODE)

    frame_size = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)

    ring_buffer = collections.deque(maxlen=20)
    voiced_frames = []

    print("Listening... speak now.")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=frame_size,
        dtype="int16",
        channels=CHANNELS,
    ) as stream:
        triggered = False

        while True:
            frame, overflowed = stream.read(frame_size)

            if overflowed:
                print("Audio buffer overflowed.")

            is_speech = vad.is_speech(frame, SAMPLE_RATE)

            if is_speech:
                print("Speech detected.")
            else:
                print("Silence.")

            if not triggered:
                ring_buffer.append((frame, is_speech))

                num_voiced = len([f for f, speech in ring_buffer if speech])

                if num_voiced > 0.7 * ring_buffer.maxlen:
                    triggered = True
                    print("Recording started.")

                    for f, speech in ring_buffer:
                        voiced_frames.append(f)

                    ring_buffer.clear()

            else:
                voiced_frames.append(frame)
                ring_buffer.append((frame, is_speech))

                num_unvoiced = len([f for f, speech in ring_buffer if not speech])

                if num_unvoiced > 0.8 * ring_buffer.maxlen:
                    print("Recording stopped.")
                    break

    save_wav(OUTPUT_FILE, voiced_frames)
    print(f"Saved speech audio to {OUTPUT_FILE}")


def save_wav(path, frames):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))


if __name__ == "__main__":
    record_until_silence()

"""
Open microphone stream
        ↓
Read 30 ms audio chunk
        ↓
Ask VAD: speech or silence?
        ↓
If enough recent chunks are speech:
        start recording
        ↓
Keep saving speech chunks
        ↓
If enough recent chunks are silence:
        stop recording
        ↓
Save final speech as vad_recording.wavf
"""