import speech_recognition as sr

r = sr.Recognizer()

harvard = sr.AudioFile('audio_files/ambient_noise.wav')
with harvard as source:
    r.adjust_for_ambient_noise(source)
    r.enable_separate_recognition_per_channel=True
    
    audio = r.record(source)
    text = r.recognize_google(audio, language = 'en-IN')

print(text)