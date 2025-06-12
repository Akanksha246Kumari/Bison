import os
import azure.cognitiveservices.speech as speechsdk
import config

def text_to_speech(text, session_id, turn_id):
    """Converts text to speech using Azure AI Speech and saves it as an MP3 file.

    Args:
        text (str): The text to be converted to speech.
        session_id (str): The unique identifier for the call session.
        turn_id (int): The current turn in the conversation.

    Returns:
        str: The path to the generated audio file.
    """
    # Configure the speech synthesis
    speech_config = speechsdk.SpeechConfig(subscription=config.AZURE_SPEECH_KEY, region=config.AZURE_SPEECH_REGION)
    # Use a natural, conversational voice
    speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'

    # Define the audio output path
    audio_dir = os.path.join('static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    audio_filepath = os.path.join(audio_dir, f"{session_id}_{turn_id}.mp3")
    
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_filepath)

    # Create a speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Synthesize the text
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text '{text}' and saved to '{audio_filepath}'")
        return audio_filepath
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
        return None
