import subprocess
import ffmpeg
import speech_recognition as sr
from pydub import AudioSegment

file_path = (r"C:\Users\aaa.mp4")  # Replace with the actual file path

# use SpeechRecognition to put audio to text
def audio_to_text(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(text)

# if the file has an ".mp3" extension
if file_path.lower().endswith(".mp3"):
    # tranfer mp3 to wav
    def _mp3_to_wav(mp3_path, wav_path):
        song = AudioSegment.from_mp3(mp3_path)
        song.export(wav_path, format="wav")

    _mp3_to_wav(file_path, "audio.wav")
    audio_to_text('audio.wav')

#if the file has an ".mp4" extension
elif file_path.lower().endswith(".mp4"):
    ffmpeg.input(file_path).output('audio.wav').run()   # video to audio
    audio_to_text('audio.wav')



