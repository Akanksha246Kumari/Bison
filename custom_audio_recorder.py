import streamlit as st
import streamlit.components.v1 as components

def custom_audio_recorder():
    # Define the HTML and JavaScript for the custom audio recorder
    html_code = """
    <div id="root"></div>
    <script>
    const root = document.getElementById('root');
    const button = document.createElement('button');
    button.textContent = 'Record';
    root.appendChild(button);

    let recorder;
    let chunks = [];
    let isRecording = false;

    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream);
        recorder.ondataavailable = e => chunks.push(e.data);
        recorder.onstop = () => {
            const blob = new Blob(chunks, { 'type' : 'audio/wav' });
            chunks = []; // Clear chunks for next recording
            const reader = new FileReader();
            reader.onload = () => {
                const dataUrl = reader.result;
                // Send data to Streamlit
                window.parent.postMessage({ type: 'streamlit:setComponentValue', value: dataUrl }, '*');
            };
            reader.readAsDataURL(blob);
        };
        recorder.start();
        isRecording = true;
        button.textContent = 'Stop';
    }

    function stopRecording() {
        recorder.stop();
        isRecording = false;
        button.textContent = 'Record';
    }

    button.onclick = () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    };
    </script>
    """
    # Use Streamlit's components API to render the HTML/JS
    # Add a key to preserve state across reruns
    audio_data_url = components.html(html_code, height=50)
    return audio_data_url

