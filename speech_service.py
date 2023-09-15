from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

def transcribe_audio(project_id: str, audio_content: bytes) -> cloud_speech.RecognizeResponse:
    client = SpeechClient()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        content=audio_content,
    )

    response = client.recognize(request=request)
    return response
