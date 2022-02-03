from __future__ import unicode_literals
import moviepy.editor as mpy
import os
import time

# ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "ultrafast"
vcodec =   "libx264"
videoquality = "24"

txt_dir, audio_dir = "description/tracklist.txt", "audio"

def process_audio(description_dir, audio_dir):

    # load description
    tracklist = open(description_dir, "w")
    tracklist.write("\nTracklist  • • • \n")

    # load songs and add tracklist to description
    duration, i = 0, 1
    for file in os.listdir(audio_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3") or filename.endswith(".m4a"):
            current_song = mpy.AudioFileClip(os.path.join(audio_dir, filename))
            result = time.gmtime(duration)
            tracklist.write(f'{result.tm_hour}:{result.tm_min}:{result.tm_sec} • {filename.split(".")[0]} \n')
            current_song.close()
            os.rename(os.path.join(audio_dir, filename), os.path.join(audio_dir, "audio"+str(i)+".mp3"))
            i=i+1
            duration += current_song.duration


if __name__ == '__main__':
    process_audio(txt_dir, audio_dir)