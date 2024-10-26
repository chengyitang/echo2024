# to_text.py

import subprocess
import ffmpeg
import speech_recognition as sr
from pydub import AudioSegment
import os

def to_text(file_input_path):
    # Check the file extension
    file_extension = os.path.splitext(file_input_path)[1].lower()
    
    if file_extension == ".mp3":
        # Convert MP3 to WAV
        wav_path = os.path.join('uploads', 'audio.wav')
        song = AudioSegment.from_mp3(file_input_path)
        song.export(wav_path, format="wav")
        return audio_to_text(wav_path)

    elif file_extension == ".mp4":
        # Extract audio from MP4
        wav_path = os.path.join('uploads', 'audio.wav')
        ffmpeg.input(file_input_path).output(wav_path).run()
        return audio_to_text(wav_path)

    elif file_extension == ".pdf":
        # Extract text from PDF
        return extract_text_from_pdf(file_input_path)

    else:
        return None

def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

def extract_text_from_pdf(pdf_path):
    text = ''
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f'Error extracting text from PDF: {e}')
    return text
