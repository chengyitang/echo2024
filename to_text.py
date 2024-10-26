import subprocess
import ffmpeg
import speech_recognition as sr
from pydub import AudioSegment

def to_text(file_input):
    # use SpeechRecognition to put audio to text
    def audio_to_text(file_input):
        recognizer = sr.Recognizer()
        with file_input as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text

    # if the file has an ".mp3" extension
    if file_input.lower().endswith(".mp3"):
        # tranfer mp3 to wav
        def _mp3_to_wav(mp3_input, wav_path):
            song = AudioSegment.from_mp3(mp3_input)
            song.export(wav_path, format="wav")

        _mp3_to_wav(file_input, "audio.wav")
        return audio_to_text('audio.wav')

    #if the file has an ".mp4" extension
    elif file_input.lower().endswith(".mp4"):
        ffmpeg.input(file_input).output('audio.wav').run()   # video to audio
        return audio_to_text('audio.wav')
        
    elif file_input.lower().endswith(".pdf"):
        # extract text from pdf
        def extract_text_from_pdf(pdf_path):
            text = ''
            try:
                text = subprocess.check_output(['pdftotext', pdf_path, '-']).decode('utf-8')
            except Exception as e:
                print(f'Error extracting text from PDF: {e}')
            return text

        text = extract_text_from_pdf(file_input)
        return text

