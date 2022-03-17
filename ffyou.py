#!/usr/local/bin/python3
import os, sys
from subprocess import PIPE, run
from retrying import retry

YOUTUBE_URL='https://youtu.be/'
VIDEO_LINK_QUALITY = 'best'
VIDEO_FILE_EXTENSION = '.mp4'
# TMP_DIR = os.path.join('/', 'tmp')
TMP_DIR = os.path.join('/', 'secrets')

try:
    PLAYLIST = os.environ['PLAYLIST']
except:
    print("Playlist not found")
    exit(1)

print("===============================================")
print("===============================================")
print(PLAYLIST)
print("===============================================")
print("===============================================")

def main():
    PL = PLAYLIST.split(',')
    for i in PL:
        video_title = run('youtube-dl --skip-download --get-title --no-warnings {youtube}{yt_video_path}'.format(yt_video_path=i, youtube=YOUTUBE_URL), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.strip()
        file_video_link = run('youtube-dl -f {video_link_quality} -g {youtube}{yt_video_path}'.format(video_link_quality=VIDEO_LINK_QUALITY, yt_video_path=i, youtube=YOUTUBE_URL), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout

        file_input = os.path.join(TMP_DIR, i+VIDEO_FILE_EXTENSION)
        file_output = os.path.join(TMP_DIR, video_title+VIDEO_FILE_EXTENSION)

        print("Downloading video from YouTube")
        os.system('aria2c -k 1M -s 128 -x 128 -o "..{output}" "{url}"'.format(url=file_video_link, output=file_input))

        print("Converting video from YouTube")
        os.system('ffmpeg -i {file_input} -crf 15 -vf scale=1920x1080:flags=lanczos -aspect 16:9 {file_output}'.format(file_input=file_input, file_output=file_output))

        os.system('rm -rf {}'.format(file_input))
        # print("Uploading to YouTube")
        # cmd = os.system('youtube-upload --file="{file_output}" --title="{video_title}" --description="{video_title}" --category="22" --privacyStatus="private"'.format(file_output=file_input, video_title=video_title))

        # os.system('rm -rf {} {}'.format(file_input,file_output))
        # exit_code = os.WEXITSTATUS(cmd)
        # if int(exit_code) != 0:
        #     exit(1)

def get_playlist(YOUTUBE_PLAYLIST):
    videos_list = run('youtube-dl --get-id https://www.youtube.com/playlist?list={} -i'.format(YOUTUBE_PLAYLIST), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.strip().split('\n')
    my_string = ','.join(videos_list)
    print()
    print()
    print(my_string)
    print()
    print()

if "playlist" in str(sys.argv):
    get_playlist(os.environ['YOUTUBE_PLAYLIST'])
else:
    main()
