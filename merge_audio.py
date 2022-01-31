import moviepy.editor as mpy
import os
import datetime

# slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "ultrafast"
vcodec =   "libx264"
videoquality = "24"

txt_dir, music_dir = "description.txt", "music"

def merge_audio(description_dir, music_dir):

    songs = []

    # load description
    description = open(description_dir, "a+") 
    description.write("\n")
    description.write("Tracklist  • • • ")
    description.write("\n")


    # load songs and add tracklist to description
    videotime = 0
    track_time = datetime.min
    for file in os.listdir(music_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"):
            current_song = mpy.AudioFileClip(os.path.join(music_dir, filename))
            songs.append(current_song)
            description.write(track_time.strftime("%H:%M:%S")+" • "+filename.split('.')[0]+"\n")
            videotime += current_song.duration
            track_time = datetime.fromtimestamp(videotime)

    # merge audio
    audio = mpy.concatenate_audioclips(songs)
    audio.write_audiofile("audio.mp3")

if __name__ == '__main__':
    merge_audio(txt_dir, music_dir)