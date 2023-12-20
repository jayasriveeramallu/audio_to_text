from flask import Flask, request, jsonify

import assemblyai as aai
import sounddevice as sd
import numpy as np
import io
import wave
import tempfile

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
import os 
# Set your AssemblyAI API key
aai.settings.api_key=os.getenv('API_KEY')
# Set your AssemblyAI API key

transcriber = aai.Transcriber()

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        # Get raw audio data from the POST request
        audio_data = request.data

        # Set up audio stream parameters
        fs = 44100  # Sample rate

        # Save audio data to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            audio_path = temp_audio_file.name
            with wave.open(audio_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(fs)
                wf.writeframes(audio_data)

        # Transcribe audio from the temporary file
        transcript = transcriber.transcribe(audio_path)

        # Return the transcription as JSON
        return jsonify({'transcription': transcript.text})

if __name__ == '__main__':
    app.run(debug=True)

