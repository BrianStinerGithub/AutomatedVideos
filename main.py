import math
from re import S
import moviepy.editor as mpy
import os
import time
import gizeh as gz
import numpy as np
import librosa as lr
from pyparsing import White
from scipy.fft import fft
import soundfile as sf
from PIL import Image
import random as r

# global variables
songs = []

title = "Playlist"

txt_dir, audio_dir, video_dir = "description/tracklist.txt", "audio", "videos"

W,H= 1920,1080

# ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "ultrafast"
vcodec =   "libx264"
videoquality = "24"

def time_to_frames(t, sr=22500, h_l=1024):
    return lr.time_to_frames(t, sr=sr, hop_length=h_l)

def calc_fps():
    return len(fourier[1])/music.duration

def next_power_of_2(x):
    return 2**(math.ceil(math.log(x, 2)))

def params_for_fps(fps=30, sr=22500):
    frame_seconds=1.0/fps
    frame_hop = round(frame_seconds*sr) # in samples
    frame_fft = next_power_of_2(2*frame_hop)
    rel_error = (frame_hop-(frame_seconds*sr))/frame_hop
    
    return frame_hop, frame_fft, rel_error

#This ball class is responsible for acceleration and velocity of the ball
class Ball:
    def __init__(self):
        self.angle = r.randint(0,360)
        self.x = W/2 + np.cos(self.angle)*100
        self.y = H/2 + np.sin(self.angle)*100
        self.speed = r.randint(1,3)
        self.acceleration = r.randint(1,3)
        self.radius = r.randint(1,5)
        self.color = (200,200,200,1)
        self.blurry = r.choice([True, False])


    def update(self, condition):
        zoomzoom = .1
        if(condition):
            zoomzoom = .5
        self.x += self.speed * np.cos(self.angle) * zoomzoom
        self.y += self.speed * np.sin(self.angle) * zoomzoom
        self.speed += self.acceleration

    def off_screen(self):
        if(self.x < 0 or self.x > W or self.y < 0 or self.y > H):
            return True
        else:
            return False

    def draw(self, surface):
        circle = gz.circle(self.radius, xy=[self.x, self.y], fill=self.color, stroke=self.color, stroke_width=2)
        if(self.blurry):
            circle2 = gz.circle(self.radius+2, xy=[self.x, self.y], fill=(180,180,180,.5), stroke=(180,180,180,.5), stroke_width=2)
            circle2.draw(surface)
        circle.draw(surface)

def testing_preload():
    pass

def setup():
    global balls, frequencies, fourier, mel, beats, background, music, harmonic, percussive, h_l, sr
    music = mpy.AudioFileClip(f"{title}.wav")
    balls = []
    print(f"expiriment: {np.geomspace(1,1024, num=11, endpoint=True)}")

    print("Loading in audio...")
    y, sr = lr.load(f"{title}.wav")

    h_l, nfft, r_error = params_for_fps(fps=30, sr=sr)
    print(f"hop length: {h_l} nfft: {nfft} rel error: {r_error}")
    print("\nCalculating fourier transform...")
    fourier = np.abs(lr.stft(y, hop_length=h_l, n_fft=nfft, center=True))
    print(f"fourier.shape: {fourier.shape}")
    print(f"frames per second: {calc_fps()} ")

    print("\nCalculating harmonic and percussive transforms...")
    harmonic, percussive = lr.decompose.hpss(S=fourier)
    print("harmonic.shape: ",harmonic.shape)
    print("percussive.shape: ",percussive.shape)

    print("\nCalculating mel spectrogram...")
    mel = np.abs(lr.feature.melspectrogram(S=fourier, n_mels=256, fmax=8000))
    print(f"mel.shape[0]: {mel.shape[0]}")

    print("\nCalculating rhythm...")
    beats = lr.beat.plp(y,sr=sr, hop_length=h_l)
    print(f"beats: {len(beats)}")

    print("\nLoading image...")
    background = Image.open("image.jpg")
    background.load()
    print("background.size: ", background.size)
    background = background.resize((W,H))
    print("background.size: ", background.size)


def make_frame(t):
    

    surface = gz.Surface(W,H, bg_color=(0,0,0,0))

    frame = time_to_frames(t, sr=sr, h_l=h_l)

    angle = range(0,180,1)
    for i in [-1,1]:
            
        x1 = (W/2) + np.cos(angle)*100*i + np.cos([*harmonic[20:380:2, frame]])*100
        y1 = (H/2) + np.sin(angle)*100   - np.sin([*harmonic[20:380:2, frame]])*100
        points  = list(zip(x1,y1))
        line  = gz.polyline(points,  stroke=(.8,.8,.8,1), stroke_width=2)
        line.draw(surface)

    if(beats[frame]>0.3):
        circle = gz.circle(10, xy=[W/2, H/2], fill=(.8,.8,.8,1), stroke=(.8,.8,.8,1), stroke_width=1)
        circle.draw(surface)

    b = Ball() 
    balls.append(b)
    for ball in balls:
        if(ball.off_screen()):
            balls.remove(ball)
        ball.update(beats[frame]>0.3)
        ball.draw(surface)


    

    # All finished drawing, now put background under the animation
    # animation = Image.fromarray(surface.get_npimage(), 'RGB')    
    # print(f"frame: {frame}")
    # print(f"t: {t}")

    # return np.asarray(Image.alpha_composite(animation, background))

    return surface.get_npimage()

def make_video():
    clip = mpy.VideoClip(make_frame)
    clip = clip.set_audio(music).set_fps(30).set_duration(30).write_videofile(f"videos\{title}.mp4", #delete .set_duration when testing is over
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

    
    global music, frequencies, fourier, mel, beats, background
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
    beats = lr.beat.plp(y, sr, hop_length=512)
    print(f"rhythm: {len(beats)} beats\n")
    print("Calculating frequencies...")
    frequencies = lr.core.mel_to_hz(mel)

    # load background image
    background = Image.open("image.jpg")
    background = background.resize((W,H))
    
