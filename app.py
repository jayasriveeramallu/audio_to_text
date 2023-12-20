from flask import Flask, request, jsonify
import assemblyai as aai
import tempfile
import os 

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()

# Set your AssemblyAI API key
aai.settings.api_key = os.getenv('API_KEY')

transcriber = aai.Transcriber()

@app.route('/', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        # Get raw audio data from the POST request
        audio_data = request.data

        # Set up audio stream parameters
        fs = 44100  # Sample rate

        # Save audio data to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            audio_path = temp_audio_file.name
            with open(audio_path, 'wb') as af:
                af.write(audio_data)

        # Transcribe audio from the temporary file
        transcript = transcriber.transcribe(audio_path)

        # Return the transcription as JSON
        return jsonify({'transcription': transcript.text})

if __name__ == '__main__':
    app.run(debug=True)
