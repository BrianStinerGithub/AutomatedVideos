import moviepy.editor as mpy
import os
import time
import gizeh as gz
import numpy as np
import librosa as lr

# global variables
songs = []

txt_dir, audio_dir, video_dir = "description/tracklist.txt", "audio", "videos"

W,H = 1920,1080
animationfps = 18

# ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "ultrafast"
vcodec =   "libx264"
videoquality = "24"

def preload():
    # load tracklist file
    tracklist = open(txt_dir, "w")
    tracklist.write("\nTracklist  • • • \n")
    keepable_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -,.~$%^&*#@+"

    # load all songs in folder and add tracklist to text file
    duration = 0
    for file in os.listdir(audio_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"):
            current_song = mpy.AudioFileClip(os.path.join(audio_dir, filename))
            songs.append(current_song)
            result = time.gmtime(duration)
            print(filename)
            tracklist.write(f'{result.tm_hour}:{result.tm_min}:{result.tm_sec} • {filename.split(".")[0]} \n')
            current_song.close()
            duration += current_song.duration

def setup():
    print(list(map(lambda x: x.duration, songs)))

def make_frame(t):

    surface = gz.Surface(W,H)

    for i in range(20):
        angle = 2*np.pi*(1.0*i/20+t/2)
        center = W*( 0.5+ gz.polar2cart(0.1,angle))
        circle = gz.circle(r= W*(1.0-1.0*i/20),
                              xy= center, fill= (i%2,i%2,i%2))
        circle.draw(surface)

    return surface.get_npimage()

def create_video():
    # for song in songs:
    #     clip = mpy.VideoClip(make_frame, duration=60) # song.duration
    #     clip = clip.set_audio(song)
    #     print("\n"+song.filename)
    #     clip.write_videofile(f"videos/{song.filename.split('.')[0]}.mp4",
    #         fps=animationfps, codec='mpeg4', audio_codec="aac", 
    #         audio_bitrate="192k", preset="ultrafast", threads=4, 
    #         verbose=False, logger=None)

    clip = mpy.VideoClip(make_frame, duration=60)
    clip.set_fps(24).set_duration(60).write_videofile("test.mp4")
    



if __name__ == '__main__':
    preload()
    setup()
    create_video()