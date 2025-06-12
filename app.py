import streamlit as st
import uuid
import database
from ai_assistant import AIAssistant
from speech_to_text import transcribe_audio
from text_to_speech import text_to_speech
from custom_audio_recorder import custom_audio_recorder
import base64

def display_reports():
    """Fetches and displays all maintenance reports from the database."""
    st.header("View Maintenance Reports")
    reports = database.get_all_reports()
    if not reports:
        st.info("No reports have been submitted yet.")
        return
    
    for report in reports:
        try:
            report_data = report.get('report_data', {})
            site_name = report_data.get('site_name', 'N/A')
            report_id = report.get('id', 'N/A')
            timestamp = report.get('timestamp', 'N/A')

            with st.expander(f"Report ID: {report_id} - {site_name} on {timestamp}"):
                st.json(report_data)
        except Exception as e:
            st.error(f"Failed to display report {report.get('id', 'N/A')}: {e}")

def live_chat():
    """Renders a live chat interface with voice capabilities."""
    st.header("Live Chat with Fieldwise AI")

    # Initialize chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ai_assistant" not in st.session_state:
        session_id = f"streamlit-session-{uuid.uuid4()}"
        st.session_state.session_id = session_id
        st.session_state.turn_id = 0
        st.session_state.ai_assistant = AIAssistant(session_id)
        initial_response = st.session_state.ai_assistant.get_ai_response(None)
        st.session_state.messages.append({"role": "assistant", "content": initial_response})
        audio_file = text_to_speech(initial_response, st.session_state.session_id, st.session_state.turn_id)
        st.session_state.audio_file = audio_file

    # Auto-play audio if available
    if 'audio_file' in st.session_state and st.session_state.audio_file:
        st.audio(st.session_state.audio_file, autoplay=True)
        st.session_state.audio_file = None # Clear after playing

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Voice recorder and text input
    audio_data_url = custom_audio_recorder()
    prompt = st.chat_input("Or type your response:")

    if audio_data_url and isinstance(audio_data_url, str):
        # Decode the base64 data URL
        header, encoded = audio_data_url.split(",", 1)
        audio_bytes = base64.b64decode(encoded)

        # Transcribe audio to text
        prompt = transcribe_audio(audio_bytes)
        if not prompt:
            st.warning("Could not understand audio. Please try again or type your response.")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            ai_response = st.session_state.ai_assistant.get_ai_response(prompt)

            if "CONVERSATION_COMPLETE" in ai_response:
                message_placeholder.markdown("Okay, I have all the details. Generating the final report now...")
                final_summary_json = st.session_state.ai_assistant.generate_json_summary()
                database.save_report(final_summary_json)
                st.success("Report saved! You can view it in the 'View Reports' tab.")
                final_message = "Report saved! How can I help with the next report?"
                st.session_state.messages.append({"role": "assistant", "content": final_message})
                st.session_state.turn_id += 1
                st.session_state.audio_file = text_to_speech(final_message, st.session_state.session_id, st.session_state.turn_id)
            else:
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.turn_id += 1
                st.session_state.audio_file = text_to_speech(ai_response, st.session_state.session_id, st.session_state.turn_id)
        st.rerun()

def main():
    st.title("Fieldwise AI Maintenance Dashboard")

    # Initialize database
    database.create_table()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Live Chat", "View Reports"])

    if page == "Live Chat":
        live_chat()
    elif page == "View Reports":
        display_reports()

if __name__ == "__main__":
    main()

