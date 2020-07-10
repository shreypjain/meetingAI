from resemblyzer import preprocess_wav, VoiceEncoder
from resemblyzer.hparams import sampling_rate 
from pathlib import Path
from spectralcluster import SpectralClusterer
from pydub import AudioSegment
import speech_recognition as sr
import warnings
from flask import Flask, render_template

warnings.filterwarnings("ignore")

#give the file path to your audio file
audio_file_path = 'audio_files/test.wav' #we'll put a recording right here, of a file
wav_fpath = Path(audio_file_path)

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':    
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

mp3_to_wav(audio_file_path)

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
#read data from the wave file
print(labelling)
def split_audio(file_path):
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

n = split_audio('audio_files/test.wav')