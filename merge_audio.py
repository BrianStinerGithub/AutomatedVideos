import moviepy.editor as mpy
import os
import time

# slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "ultrafast"
vcodec =   "libx264"
videoquality = "24"

txt_dir, music_dir = "description.txt", "music/Input"

def merge_audio(description_dir, music_dir):

    songs = []

    # load description
    description = open(description_dir, "a+") 
    description.write(u'\uFEFF'.encode('UTF-8'))
    description.write("\n")
    description.write("Tracklist  • • • ")
    description.write("\n")


    # load songs and add tracklist to description
    duration = 0
    for file in os.listdir(music_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"):
            current_song = mpy.AudioFileClip(os.path.join(music_dir, filename))
            songs.append(current_song)
            result = time.gmtime(duration)
            description.write(f'{result.tm_hour}:{result.tm_min}:{result.tm_sec} • {filename.split(".")[0]}')
            duration += current_song.duration

    # merge audio
    audio = mpy.concatenate_audioclips(songs)
    audio.write_audiofile("music/Output/audio.mp3", codec="libmp3lame", bitrate="320k", ffmpeg_params=["-q:a", "5"])

if __name__ == '__main__':
    merge_audio(txt_dir, music_dir)