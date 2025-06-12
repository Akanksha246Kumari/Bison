import os
from flask import Flask, request, session, url_for
from twilio.twiml.voice_response import VoiceResponse
from ai_assistant import AIAssistant
from text_to_speech import text_to_speech
import database

app = Flask(__name__)
# A secret key is needed for Flask session management
app.secret_key = os.urandom(24)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Handle incoming and ongoing voice calls with the AI assistant."""
    response = VoiceResponse()
    session_id = request.values.get('CallSid', 'default_session')

    # Initialize turn counter in Flask's session object
    if 'turn_id' not in session:
        session['turn_id'] = 0

    # Get the user's speech from Twilio's request
    user_speech = request.values.get('SpeechResult', None)

    # Initialize our AI assistant for this specific call session
    ai_assistant = AIAssistant(session_id)

    # Get the AI's response.
    # On the first turn, user_speech will be None, and the assistant will give its greeting.
    ai_response_text = ai_assistant.get_ai_response(user_speech)

    # Special keyword to end the call and save the report
    if "CONVERSATION_COMPLETE" in ai_response_text:
        final_summary = ai_assistant.get_conversation_summary()
        database.save_report(final_summary)
        # Use <Say> for the final message for simplicity
        response.say("Thank you. Your maintenance report has been filed. Goodbye.", voice='alice')
        response.hangup()
        return str(response)

    # Convert the AI's text response to a spoken audio file
    audio_filename = text_to_speech(ai_response_text, session_id, session['turn_id'])
    
    # Generate a public URL for the audio file that Twilio can access
    audio_url = url_for('static', filename=f'audio/{os.path.basename(audio_filename)}', _external=True)

    # Tell Twilio to play the generated audio file
    response.play(audio_url)

    # Listen for the user's next response and send it back to this same /voice endpoint
    response.gather(input='speech', action='/voice', speechTimeout='auto', speechModel='experimental_conversational')

    # If the user doesn't say anything, Twilio re-calls /voice. We can redirect to repeat the process.
    response.redirect('/voice')

    # Increment the turn counter for unique audio filenames
    session['turn_id'] += 1

    return str(response)

if __name__ == "__main__":
    # Make sure the app is run from the correct directory so it can find the 'static' folder
    app.run(port=5001, debug=True)
