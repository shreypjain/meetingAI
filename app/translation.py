from resemblyzer import preprocess_wav, VoiceEncoder
from resemblyzer.hparams import sampling_rate 
from pathlib import Path
from spectralcluster import SpectralClusterer
from pydub import AudioSegment
import speech_recognition as sr
import warnings
from flask import Flask, render_template

warnings.filterwarnings("ignore")

def get_full_translation(audio_file_name):
    def mp3_to_wav(file):
        if audio_file_name.split('.')[1] == 'mp3':    
            sound = AudioSegment.from_mp3(audio_file_name)
            sound.export(f"{audio_file_name.split('.')[0]}.wav", format="wav")
        else:
            pass
        
    wav_fpath = (f"{audio_file_name.split('.')[0]}.wav")

    #preprocesses the wave file to turn it into a file without sounds
    wav = preprocess_wav(wav_fpath)
    encoder = VoiceEncoder("cpu") #Creates a voice encoder object so we can process audio with the cpu
    _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)

    #create a cluster object 
    clusterer = SpectralClusterer(
        min_clusters=2,
        max_clusters=100,
        p_percentile=0.90,
        gaussian_blur_sigma=1)

    #label the speaker that is speaking at certain time
    labels = clusterer.predict(cont_embeds)

    def create_labelling(labels,wav_splits):
        times = [((s.start + s.stop) / 2) / sampling_rate for s in wav_splits]
        labelling = []
        start_time = 0

        for i,time in enumerate(times):
            if i>0 and labels[i]!=labels[i-1]:
                temp = [str(labels[i-1]),start_time,time]
                labelling.append(tuple(temp))
                start_time = time
            if i==len(times)-1:
                temp = [str(labels[i]),start_time,time]
                labelling.append(tuple(temp))

        return labelling
    
    labelling = create_labelling(labels,wav_splits)
    print(labelling)
    #read data from the wave file

    def split_audio(file_path):
        thisList = []
        n = 0
        for i in labelling:
            n =+ 1
            #changes the values in the tuple to ints and milliseconds
            start= int(i[1])*1000 
            end=int(i[2])*1000
            #finds the audio file as a wav
            newAud = AudioSegment.from_wav(file_path)
            #creates a new audio based on the values given by seconds
            newAudio = newAud[start:end]
            newAudio.export(f'audio_files/split/SplitAudio_{n}.wav', format="wav") #Exports to a wav file in the current path.
            
        return n

    n = split_audio(audio_file_name)

    def get_translation():
        entire_text = []
        for num in range(n):
            r = sr.Recognizer()

            harvard = sr.AudioFile(f'audio_files/split/SplitAudio_{num+1}.wav')
            with harvard as source:
                r.adjust_for_ambient_noise(source)
                r.enable_separate_recognition_per_channel=True
                
                audio = r.record(source)
                text = r.recognize_google(audio, language='en-US')
                
                text = f'Speaker {n}: ' + str(text)
                entire_text.append(text)
        return entire_text

    translation = get_translation()

    return render_template('translation.html', translation = translation)