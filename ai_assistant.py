import os
from openai import AzureOpenAI
import config

class AIAssistant:
    """Manages the conversation logic using Azure OpenAI."""

    def __init__(self, session_id):
        """Initializes the AI assistant.

        Args:
            session_id (str): A unique identifier for the current call session.
        """
        self.session_id = session_id
        self.client = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version="2023-12-01-preview",
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT
        )
        self.deployment_name = config.AZURE_OPENAI_DEPLOYMENT_NAME
        self.history = [self._get_system_prompt()]

    def _get_system_prompt(self):
        """Defines the role and instructions for the AI model based on detailed requirements."""
        return {
            "role": "system",
            "content": """
            You are a friendly and efficient AI assistant named 'Fieldwise' for a salt water disposal company. 
            Your purpose is to help field technicians verbally submit maintenance reports.
            You are conversational, clear, and concise. Your goal is to guide the user to provide all necessary information.

            GUIDING SCRIPT:
            Your conversation should follow this structure. Be natural and adapt to the user's responses.
            1.  **Greeting & Identify User:** Start with a friendly greeting. Ask for the technician's name.
            2.  **Identify Site:** Ask what site they are visiting.
            3.  **Identify Problem:** Ask what problem they are addressing or what type of maintenance they are performing.
            4.  **Gather Symptoms:** Ask about the symptoms they noticed (e.g., strange noises, leaks, power loss, vibrations).
            5.  **Symptom Duration:** Ask how long they have been tracking the symptoms.
            6.  **Parts Replacement:** Ask what parts they are replacing.
            7.  **Part Model Numbers:** Ask if the new parts have the same model number. If not, ask for the new model number.
            8.  **Maintenance Time:** Ask roughly what time they started the maintenance.
            9.  **Final Confirmation:** Once you have gathered all the details, confirm with the user. Say something like, "Okay, I think I have all the details. Shall I write up the report?"

            IMPORTANT:
            - Ask one question at a time.
            - Keep your responses short and to the point.
            - When you have all the information and the user has confirmed, and ONLY then, end your response with the exact keyword: **CONVERSATION_COMPLETE**
            """
        }

    def get_ai_response(self, user_text):
        """Gets a conversational response from the AI."""
        if user_text:
            self.history.append({"role": "user", "content": user_text})

        # If this is the first turn, the history only has the system prompt.
        # We add an empty user message to kickstart the conversation from the AI.
        if len(self.history) == 1:
             self.history.append({"role": "user", "content": ""})

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=self.history,
            temperature=0.7,
            max_tokens=200
        )

        ai_response_text = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": ai_response_text})
        return ai_response_text

    def generate_json_summary(self):
        """After the conversation is complete, this generates a final JSON summary."""
        summary_prompt = {
            "role": "user",
            "content": "The user has confirmed the report is ready. Based on our entire conversation history, please summarize all the collected information into a single, clean JSON object. Do not include any other text, just the JSON."
        }

        summary_history = self.history + [summary_prompt]

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=summary_history,
            temperature=0.2, # Lower temperature for more deterministic JSON output
            max_tokens=500
        )

        json_summary = response.choices[0].message.content.strip()
        return json_summary
