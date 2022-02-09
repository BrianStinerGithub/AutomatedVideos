import moviepy.editor as mpy
import os
import time
import gizeh as gz
import numpy as np
import librosa as lr
import soundfile as sf
from PIL import Image

# global variables
songs = []

title = "Playlist"

txt_dir, audio_dir, video_dir = "description/tracklist.txt", "audio", "videos"

W,H = 1920,1080

# ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "ultrafast"
vcodec =   "libx264"
videoquality = "24"
def testing_preload():
    
    global music, frequencies, fourier, mel, rhythm, background
    music = mpy.AudioFileClip(f"{title}.wav")
    
    print("Loading in audio...")
    y, sr = lr.load(f"{title}.wav")
    print(f"{sr} Hz, {len(y)} samples\n")
    print("Calculating fourier transform...")
    fourier = lr.stft(y, n_fft=2048, hop_length=512, center=True)
    print(f"fourier.shape: {fourier.shape}\n")
    print("Calculating mel spectrogram...")
    mel = lr.feature.melspectrogram(S=fourier, sr=sr, n_fft=2048, hop_length=128, n_mels=64)
    print(f"mel.shape: {mel.shape}\n")
    print("Calculating rhythm...")
    rhythm = lr.beat.plp(y, sr, hop_length=512)
    print(f"rhythm: {len(rhythm)} beats\n")
    print("Calculating frequencies...")
    frequencies = lr.core.mel_to_hz(mel)

    # load background image
    background = Image.open("image.jpg")
    background = background.resize((W,H))


def setup():
    pass

def make_frame(t):
    surface = gz.Surface(W,H, bg_color=(0,0,0))

    x1 = list(range(100,W-100,(W-200)/len(mel)))
    y1 = list([*mel[:, lr.time_to_frames(t)]*20 + (H/3)])
    x2 = list(range(100,W-100,(W-200)/len(fourier)))
    y2 = np.abs(list([*fourier[:, lr.time_to_frames(t)] + (2*H/3)]))

    points = list(zip(x1,y1))
    line = gz.polyline(points, stroke=(.8,.8,.8), stroke_width=2)
    points3 = list(zip(x2,y2))
    line3 = gz.polyline(points3, stroke=(.8,.8,.8), stroke_width=2)

    if(rhythm[lr.time_to_frames(t)]>0.4):
        circle = gz.circle(10, xy=[W/2, H/2], fill=(.8,.8,.8), stroke=(.8,.8,.8), stroke_width=1)
        circle.draw(surface)


    line.draw(surface)
    line3.draw(surface)
    return surface.get_npimage()+background #numpy.ndarray

def make_video():
    clip = mpy.VideoClip(make_frame)
    print(lr.time_to_frames(1))
    clip = clip.set_audio(music).set_fps(lr.time_to_frames(1)).set_duration(60).write_videofile(f"videos\{title}.mp4", #music.duration
            codec='mpeg4', audio_codec="aac",
            audio_bitrate="192k", preset="ultrafast", threads=4, 
            verbose=False, logger=None)


if __name__ == '__main__':
    testing_preload()
    setup()
    make_video()













def preload():
    # load tracklist file
    tracklist = open(txt_dir, "w")
    tracklist.write("\nTracklist  • • • \n")

    # load all songs in folder and add tracklist to text file
    duration = 0
    for file in os.listdir(audio_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".wav"):
            current_song = mpy.AudioFileClip(os.path.join(audio_dir, filename))
            print(f"{os.path.join(audio_dir, filename)} loaded. {current_song.duration/60} minutes.")
            current_song.filename = filename
            songs.append(current_song)
            result = time.gmtime(duration)
            tracklist.write(f'{result.tm_hour}:{result.tm_min}:{result.tm_sec} • {filename.split(".")[0]} \n')
            current_song.close()
            duration += current_song.duration

    
    global music, frequencies, fourier, mel, rhythm, background
    #if file already exists, skip writing
    music = mpy.concatenate_audioclips(songs)
    print(music.duration)
    if(os.path.isfile(f"{title}.wav")):
        print("Audio already exists. Skipping write...")
    else:
        music.write_audiofile(f"{title}.wav")


    
    print("Loading in audio...")
    y, sr = lr.load(f"{title}.wav")
    print(f"{sr} Hz, {len(y)} samples\n")
    print("Calculating fourier transform...")
    fourier = lr.stft(y, n_fft=2048, hop_length=512, center=True)
    print(f"fourier.shape: {fourier.shape}\n")
    print("Calculating mel spectrogram...")
    mel = lr.feature.melspectrogram(S=fourier, sr=sr, n_fft=2048, hop_length=128, n_mels=64)
    print(f"mel.shape: {mel.shape}\n")
    print("Calculating rhythm...")
    rhythm = lr.beat.plp(y, sr, hop_length=512)
    print(f"rhythm: {len(rhythm)} beats\n")
    print("Calculating frequencies...")
    frequencies = lr.core.mel_to_hz(mel)

    # load background image
    background = Image.open("image.jpg")
    background = background.resize((W,H))
    
