import json
import yt_dlp


class MyLogger:
    def debug(self, msg):
        # For compatability with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            logWriter = open (pwd+"/logs/"+datumHeute+"_downloader.log", "a+")
            logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - Started without config File, please rename TEMPLATEconfig.txt to config.txt and fill the parameters.\n")
        logWriter.close()
        else:
            self.info(msg)

    def info(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

# ℹ️ See "progress_hooks" in the docstring of yt_dlp.YoutubeDL
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

# ℹ️ See docstring of yt_dlp.YoutubeDL for a description of the options
ydl_opts = {
    'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo+bestaudio',
    'merge_output_format': 'mkv',
    'writesubtitles': True,
    'subtitlesformat': 'srv3',
    'subtitle': '--write-sub --sub-lang en',
    #'subtitleslangs': 'en',
    'writethumbnail': True,
    'cookiefile': "/opt/archiving/cookies/ytcookies.txt",
    #'download_archive': "/opt/archiving/yt-dlp/linkarchive.txt",
    'retries': float('inf'),
    'throttledratelimit': 100000,
    'trim_file_name':200,
    'outtmpl':"%(channel)s-(%(id)s)-%(upload_date)s - %(title)s.%(ext)s",
    #'writedescription': True,
    #'writeinfojson': True,
    'postprocessors': [{
        'key': 'FFmpegMetadata',
        'add_chapters': True,
        'add_metadata': True,
        #'add_infojson': True
    },{
        'key': 'EmbedThumbnail',
        'already_have_thumbnail': False

    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

# Add custom headers
yt_dlp.utils.std_headers.update({'Referer': 'https://www.google.com'})

# ℹ️ See the public functions in yt_dlp.YoutubeDL for for other available functions.
# Eg: "ydl.download", "ydl.download_with_info_file"
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=7YV91e20O90'])
    #ydl.add_post_processor(MyCustomPP())
    #info = ydl.extract_info('https://www.youtube.com/watch?v=BaW_jenozKc')
    
    # ℹ️ ydl.sanitize_info makes the info json-serializable
    #print(json.dumps(ydl.sanitize_info(info)))