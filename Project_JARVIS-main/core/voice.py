import os
import sys
import pyttsx3
import speech_recognition as sr

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

# Set voice to deep male voice
def set_deep_male_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        # Prefer "Daniel" for deep male voice on Mac
        if "Daniel" in voice.name:
            engine.setProperty('voice', voice.id)
            return
    # Fallback to any male voice if Daniel not found
    for voice in voices:
        if "male" in voice.name.lower() or "male" in str(voice.gender).lower():
             engine.setProperty('voice', voice.id)
             return

set_deep_male_voice()

def speak(text):
    import re
    
    if "{" in text and "}" in text and "status" in text:
        text = "Task completed."
        
    # Remove markdown like asterisks to prevent TTS spelling it out
    text = re.sub(r'\*+', '', text)
    
    # Print first so user sees it even if audio fails
    print(f"JARVIS: {text}")

    # On macOS with a GUI/Threading environment, pyttsx3's loop often conflicts 
    # with the main thread event loop (PyQt). Default to system 'say' command on macOS
    # to avoid hangs/crashes unless we are strictly in a non-GUI text mode.
    if sys.platform == "darwin":
        try:
            # Escape quotes to prevent shell injection/errors
            clean_text = text.replace('"', '\\"').replace("'", "")
            os.system(f'say "{clean_text}"')
            return
        except Exception as e2:
            print(f"TTS Fallback Error: {e2}")
            # Fall through to pyttsx3 if 'say' fails (unlikely)

    # Use PowerShell for more robust TTS on Windows background threads
    if sys.platform == 'win32':
        try:
            import subprocess
            clean_text = text.replace('"', '\\"').replace("'", "''")
            ps_cmd = f'powershell -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{clean_text}\')"'
            subprocess.Popen(ps_cmd, shell=True)
            return
        except Exception as e:
            print(f"PowerShell TTS Error: {e}")

    # Fallback to pyttsx3
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile

def listen():
    r = sr.Recognizer()
    try:
        print("Listening...")
        
        # Audio recording parameters
        duration = 7  # Increased from 5 to 7 seconds to give more time
        fs = 16000    # Sample rate
        channels = 1
        
        # Record audio using sounddevice
        print("Recording...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='float32')
        sd.wait() # Wait until recording is finished
        
        # Save to a temporary wav file
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "temp_audio.wav")
        sf.write(temp_path, recording, fs)
        
        # Process the recorded file with speech_recognition
        with sr.AudioFile(temp_path) as source:
            print("Recognizing...")
            # Skip adjust_for_ambient_noise because it consumes the first 1 second 
            # of the recorded audio, which often cuts off the start of the command!
            audio = r.record(source)
            query = r.recognize_google(audio)
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
                
            return query.lower()
            
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "none"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "none"
    except Exception as mic_error:
        print(f"Mic Error: {mic_error}")
        # Microphone failed, fall back to text input
        # Silently continue to text mode
        try:
            return input("YOU (text fallback): ").lower()
        except Exception:
            return "none"
