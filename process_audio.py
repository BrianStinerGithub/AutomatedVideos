import moviepy.editor as mpy
import os
import time
import gizeh as gz
import numpy as np
import librosa as lr

# global variables
songs = []
txt_dir, audio_dir = "description/tracklist.txt", "audio"
# ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "ultrafast"
vcodec =   "libx264"
videoquality = "24"
W,H = 128,128 # 128x128 pixel
duration = 2  # 2 seconds
ncircles = 20 # Number of circles


def preload():
    # load description
    tracklist = open(txt_dir, "w")
    tracklist.write("\nTracklist  • • • \n")

    # load songs and add tracklist to description
    duration, i = 0, 1
    for file in os.listdir(audio_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3") or filename.endswith(".m4a"):
            current_song = mpy.AudioFileClip(os.path.join(audio_dir, filename))
            songs.append(current_song)
            result = time.gmtime(duration)
            tracklist.write(f'{result.tm_hour}:{result.tm_min}:{result.tm_sec} • {filename.split(".")[0]} \n')
            current_song.close()
            duration += current_song.duration

def setup():
    print(songs)

def make_frame(t):

    surface = gz.Surface(W,H)

    for i in range(ncircles):
        angle = 2*np.pi*(1.0*i/ncircles+t/duration)
        center = W*( 0.5+ gz.polar2cart(0.1,angle))
        circle = gz.circle(r= W*(1.0-1.0*i/ncircles),
                              xy= center, fill= (i%2,i%2,i%2))
        circle.draw(surface)

    return surface.get_npimage()

def process_audio():
    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_gif("circles.gif",fps=15, opt="OptimizePlus", fuzz=10)



if __name__ == '__main__':
    preload()
    setup()
    process_audio()