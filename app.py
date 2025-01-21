from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from pydub import AudioSegment
import os

app = Flask(__name__)
CORS(app)

client_gen = Groq(api_key='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')

def split_audio(file_path, chunk_length_ms=5 * 60 * 1000):
    audio = AudioSegment.from_file(file_path)
    return [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

def transcribe_and_diarize(audio_file_path, client=client_gen):
    with open(audio_file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_file_path, file.read()),
            model="whisper-large-v3-turbo",
            prompt="Specify context or spelling",
            language="uk",
            temperature=0.0
        )
        return transcription.text

def transcribe_audio_chunks(file_path, transcription_func):
    chunks = split_audio(file_path)
    transcriptions = []
    for i, chunk in enumerate(chunks):
        temp_file_path = f"temp_chunk_{i}.wav"
        chunk.export(temp_file_path, format="wav")
        transcription = transcription_func(temp_file_path)
        transcriptions.append(transcription)
        os.remove(temp_file_path)
    return " ".join(transcriptions)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Сохранение временного файла
        temp_file_path = f"temp_audio_{file.filename}"
        file.save(temp_file_path)

        # Запуск транскрипции
        transcription = transcribe_audio_chunks(temp_file_path, transcribe_and_diarize)

        # Удаление временного файла
        os.remove(temp_file_path)

        return jsonify({'transcription': transcription})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
