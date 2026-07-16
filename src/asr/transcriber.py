from pathlib import Path

from faster_whisper import WhisperModel


MODEL_SIZE = "base"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"
DEFAULT_AUDIO_FILE = "vad_recording.wav"


def load_model():
    print(f"Loading Whisper model: {MODEL_SIZE}")

    model = WhisperModel(
        MODEL_SIZE,
        device=DEVICE,
        compute_type=COMPUTE_TYPE,
    )

    print("Whisper model loaded.")
    return model


def transcribe_audio(model, audio_path):
    audio_file = Path(audio_path)

    if not audio_file.exists():
        raise FileNotFoundError(
            f"Audio file was not found: {audio_file}"
        )

    print(f"Transcribing: {audio_file}")

    segments, info = model.transcribe(
        str(audio_file),
        beam_size=5,
        vad_filter=False,
    )

    print(
        f"Detected language: {info.language} "
        f"with probability {info.language_probability:.2f}"
    )

    transcript_parts = []

    for segment in segments:
        text = segment.text.strip()

        if text:
            transcript_parts.append(text)

            print(
                f"[{segment.start:.2f}s → "
                f"{segment.end:.2f}s] {text}"
            )

    transcript = " ".join(transcript_parts)

    return transcript


if __name__ == "__main__":
    whisper_model = load_model()

    final_text = transcribe_audio(
        whisper_model,
        DEFAULT_AUDIO_FILE,
    )

    print("\nFinal transcript:")
    print(final_text)