import azure.cognitiveservices.speech as speechsdk
import config

def transcribe_audio(audio_bytes):
    """
    Transcribes audio data to text using Azure Speech Service.

    Args:
        audio_bytes (bytes): The audio data in WAV format from streamlit-audiorecorder.

    Returns:
        str: The transcribed text, or an empty string if transcription fails.
    """
    speech_config = speechsdk.SpeechConfig(
        subscription=config.AZURE_SPEECH_KEY, 
        region=config.AZURE_SPEECH_REGION
    )
    
    # The streamlit-audiorecorder provides WAV bytes. We can use an in-memory stream.
    stream = speechsdk.audio.PushAudioInputStream()
    stream.write(audio_bytes)
    stream.close()

    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )

    print("Recognizing speech from audio stream...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
        return ""
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
        return ""
    
    return ""
