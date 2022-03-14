import os
from subprocess import PIPE, run

YOUTUBE_URL='https://youtu.be/'
VIDEO_LINK_QUALITY = 'best'
VIDEO_FILE_EXTENSION = '.mp4'
TMP_DIR = os.path.join('/', 'tmp')

try:
    # PLAYLIST = os.environ['PLAYLIST']
    PLAYLIST = 'PLSV_wtTonUmR-s0obXZn2OsNeota6TMxt'
except:
    print("Playlist not found")

videos_list = run('youtube-dl --get-id https://www.youtube.com/playlist?list={} -i'.format(PLAYLIST), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.strip().split('\n')

for i in videos_list:
    # os.system('')
    file_input = os.path.join(TMP_DIR, i+VIDEO_FILE_EXTENSION)
    file_output = os.path.join(TMP_DIR, i+'_output'+VIDEO_FILE_EXTENSION)
    video_title = run('youtube-dl --skip-download --get-title --no-warnings {youtube}{yt_video_path}'.format(yt_video_path=i, youtube=YOUTUBE_URL), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.strip()
    file_video_link = run('youtube-dl -f {video_link_quality} -g {youtube}{yt_video_path}'.format(video_link_quality=VIDEO_LINK_QUALITY, yt_video_path=i, youtube=YOUTUBE_URL), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout

    os.system('aria2c -k 1M -s 128 -x 128 -o "..{output}" "{url}"'.format(url=file_video_link, output=file_input))
    os.system('ffmpeg -i {file_input} -crf 15 -vf scale=1920x1080:flags=lanczos -aspect 16:9 {file_output}'.format(file_input=file_input, file_output=file_output))

    cmd = os.system('youtube-upload --file={file_output} --title={video_title} --category="22" --privacyStatus="private"'.format(file_output=file_input, video_title=video_title))

    os.system('rm -rf {} {}'.format(file_input,file_output))
    exit_code = os.WEXITSTATUS(cmd)
    if int(exit_code) != 0:
        exit(1)
