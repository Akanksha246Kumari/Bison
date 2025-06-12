# Fieldwise AI - Voice-Powered Maintenance Reporting Bot

Fieldwise AI is an intelligent, voice-powered chatbot designed to allow field technicians to submit detailed maintenance reports over a simple phone call. The assistant engages the user in a natural, human-like conversation to gather all necessary information and automatically saves the structured report to a database.

This project leverages a powerful combination of telephony services and cloud-based AI to create a seamless and efficient reporting experience, moving beyond simple scripts to a truly conversational AI.

## Project Architecture

The system is composed of several key services that work in concert:

- **Twilio (Telephony Gateway):** Provides the phone number and handles the call connection. When a technician calls, Twilio connects to our Flask application.

- **Flask Web Server (`voice_app.py`):** The central hub of the application. It receives instructions from Twilio, orchestrates the AI conversation, and serves the generated audio files.

- **Azure OpenAI (`ai_assistant.py`):** The "brain" of the operation. It uses a powerful language model (like GPT-3.5 Turbo) to understand the user's speech and decide what to say next, making the conversation dynamic and intelligent.

- **Azure AI Speech (`text_to_speech.py`):** The "voice" of the bot. It converts the AI's text responses into high-quality, natural-sounding speech, which is then played back to the user over the phone.

- **SQLite Database (`database.py`):** Stores the final, structured maintenance reports submitted by the technicians.

- **Streamlit Dashboard (`app.py`):** A simple web interface for viewing and managing the reports stored in the database.

 *(Placeholder for a future architecture diagram)*

---

## Setup and Configuration Guide

This is a detailed guide to get the project running. You will need accounts for Twilio and Microsoft Azure.

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd fieldwise_chatbot
```
4.  Once all questions are answered, a summary of the report is displayed.
5.  Upon confirmation, the report is saved to the `maintenance_reports.db` SQLite database.

This setup provides a solid foundation for the project. It can be extended to include more complex features, such as voice input/output, integration with cloud services like Azure, and more detailed reporting.

## 🎤 Voice Integration (Telephony)

### Features
- **Twilio Voice Call Handling** 
  - Endpoint: `/voice`
  - Processes incoming voice calls
- **Real-time Speech Processing**
  - Converts speech to text using Azure Speech Services
  - Generates AI responses with Azure OpenAI
  - Converts text responses to audio
- **Conversation Management**
  - Maintains session state with Flask
  - Tracks conversation turns

### Setup
1. **Twilio Configuration**
   ```bash
   export TWILIO_ACCOUNT_SID=your_sid
   export TWILIO_AUTH_TOKEN=your_token
   ```

2. **Run Flask Server**
   ```bash
   python voice_app.py
   ```

3. **Webhook Configuration**
   Set Twilio voice webhook to:
   `https://your-domain.com/voice`

