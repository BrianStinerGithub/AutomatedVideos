from xmlrpc.client import DateTime
import moviepy.editor as mpy
import os
from datetime import date, datetime

# slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "slow"
vcodec =   "libx264"
videoquality = "24"

txt_dir, png_dir, music_dir, video_name = "description.txt", "picture", "music", "Title"



def edit_video(description_dir, image_dir, music_dir, video_name):

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


    # load image
    still = mpy.ImageClip(os.path.join(image_dir, "image.png"))

    # merge audio
    audio = mpy.concatenate_audioclips(songs)

    # still image with audio creates video
    still.resize(width=1920, height=1080)
    still = still.set_duration(audio.duration)
    still = still.set_audio(audio)

    # No ImageMagick, so we need to use ffmpeg
    
    video = mpy.CompositeVideoClip([still])
    # save file
    video.write_videofile(video_name+".mp4", threads=4, fps=24,
                               codec=vcodec,
                               preset=compression,
                               ffmpeg_params=["-crf",videoquality])

    video.close()


if __name__ == '__main__':
    edit_video(txt_dir, png_dir, music_dir, video_name)