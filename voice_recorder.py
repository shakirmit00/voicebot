#import speech_recognition as sr

#def record_voice():
#    recognizer = sr.Recognizer()
#    with sr.Microphone() as source:
#        try:
#            print("🟡 Speak now...")
#            audio = recognizer.listen(source)
#            print("🔵 Processing...")
#            text = recognizer.recognize_google(audio)
#            return text
#        except sr.UnknownValueError:
#            return "Could not understand audio"
#        except sr.RequestError as e:
#            return f"Could not request results; {e}"

#import speech_recognition as sr

#def record_voice():
#    recognizer = sr.Recognizer()
#    mic = sr.Microphone()

#    with mic as source:
#        print("🟡 Speak now...")
#        recognizer.adjust_for_ambient_noise(source, duration=1)
#        recognizer.pause_threshold = 2.0  # 👈 Increase this (default is 0.8)

#        try:
#            audio = recognizer.listen(source)
#            print("🔵 Processing...")
#            return recognizer.recognize_google(audio)
#        except sr.WaitTimeoutError:
#            print("⏳ Timeout: No speech detected.")
#            return None
#        except sr.UnknownValueError:
#            print("❌ Could not understand audio.")
#            return None
#        except sr.RequestError as e:
#            print(f"❌ API error: {e}")
#            return None
            
#import speech_recognition as sr

#def record_voice(timeout=5, phrase_time_limit=10):
#    r = sr.Recognizer()
#    with sr.Microphone() as source:
#        print("🟡 Speak now...")
#        r.adjust_for_ambient_noise(source, duration=0.5)
#        try:
#            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#            print("🔵 Processing...")
#            return r.recognize_google(audio)
#        except sr.WaitTimeoutError:
#            print("⌛ Timeout. No speech detected.")
#        except sr.UnknownValueError:
#            print("❌ Could not understand audio.")
#        except sr.RequestError as e:
#            print(f"⚠️ Speech recognition service error: {e}")
#        return None

# voice_recorder.py
#import speech_recognition as sr

#recognizer = sr.Recognizer()

#def record_voice(timeout=5, phrase_time_limit=10):
#    with sr.Microphone() as source:
#        print("🟡 Speak now...")
#        try:
#            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#            print("🔵 Processing...")
#            return recognizer.recognize_google(audio)
#        except sr.WaitTimeoutError:
#            print("⌛ Timeout. No speech detected.")
#        except sr.UnknownValueError:
#            print("❌ Could not understand audio.")
#        except sr.RequestError as e:
#            print("❌ Could not request results:", e)
#    return None

# voice_recorder.py
import speech_recognition as sr

def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🟡 Speak now...")
        audio = recognizer.listen(source, phrase_time_limit=5)

    try:
        print("🔵 Processing...")
        command = recognizer.recognize_google(audio)
        return command
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"❌ Speech Recognition error; {e}")
        return None
