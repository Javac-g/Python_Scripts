from moviepy import VideoFileClip

def mp4_to_mp3(mp4_path, mp3_path):
    video = VideoFileClip(mp4_path)
    audio = video.audio
    audio.write_audiofile(mp3_path)
    audio.close()
    video.close()

if __name__ == "__main__":
    input_mp4 = "Adele - Rolling in the Deep (Official Music Video).mp4"   # Replace with your MP4 file path
    output_mp3 = "Adele - Rolling in the Deep (Official Music Video).mp3" # Replace with desired MP3 output path
    mp4_to_mp3(input_mp4, output_mp3)
    print(f"Converted {input_mp4} to {output_mp3}")
