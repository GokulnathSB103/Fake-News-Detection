import speech_recognition as sr
from moviepy import VideoFileClip
import os
import tempfile
from pydub import AudioSegment

def convert_audio_to_text(file):
    """
    Extracts audio from video (if necessary) and transcribes it to text.
    Supports: .mp4, .mov, .avi, .wav, .mp3, and Streamlit Mic input.
    """
    r = sr.Recognizer()
    
    # 1. Get the file extension
    # Streamlit Mic input usually has no .name attribute or is named 'audio.wav'
    file_name = getattr(file, 'name', 'recorded_audio.wav')
    suffix = os.path.splitext(file_name)[1].lower()
    
    # 2. Save the uploaded bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_media:
        temp_media.write(file.getbuffer() if hasattr(file, 'getbuffer') else file.read())
        temp_path = temp_media.name

    temp_wav_path = None

    try:
        # 3. Handle Video Files (Extract Audio)
        if suffix in ['.mp4', '.mov', '.avi', '.mkv']:
            video = VideoFileClip(temp_path)
            temp_wav_path = temp_path.replace(suffix, "_extracted.wav")
            # Extract only the audio track as a WAV file
            video.audio.write_audiofile(temp_wav_path, codec='pcm_s16le', verbose=False, logger=None)
            path_to_process = temp_wav_path
            video.close() # Close file handle to allow deletion later

        # 4. Handle Compressed Audio (MP3/OGG to WAV)
        elif suffix in ['.mp3', '.ogg', '.flv']:
            audio = AudioSegment.from_file(temp_path)
            temp_wav_path = temp_path.replace(suffix, "_converted.wav")
            audio.export(temp_wav_path, format="wav")
            path_to_process = temp_wav_path

        else:
            # Already a WAV file (standard for SpeechRecognition)
            path_to_process = temp_path

        # 5. Transcribe using Google Speech Recognition
        with sr.AudioFile(path_to_process) as source:
            # Adjust for ambient noise for better accuracy
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text

    except sr.UnknownValueError:
        return "System Error: Audio was not clear enough to transcribe."
    except sr.RequestError:
        return "System Error: Could not reach the Speech Recognition service."
    except Exception as e:
        return f"Processing Error: {str(e)}"
    
    finally:
        # 6. Clean up all temporary files
        if os.path.exists(temp_path):
            try: os.remove(temp_path)
            except: pass
        if temp_wav_path and os.path.exists(temp_wav_path):
            try: os.remove(temp_wav_path)
            except: pass