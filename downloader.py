import os
from time import sleep
import re
import subprocess
import configparser
pwd=os.getcwd()
from datetime import datetime
datumHeute = datetime.date(datetime.now()).strftime("%Y%m%d")
import time
import json
import yt_dlp
import glob
import pdb
import sys
#from plugins.postexec import rclone_move
from plugins.postexec import postexec
config = configparser.ConfigParser()

logWriter = open (pwd+"/logs/"+datumHeute+"_downloader.log", "a+")


if (os.path.isfile(pwd+"/config.ini")):
    config.read(pwd+'/config.ini')
    logLevel = config['DOWNLOADER']['LogLevel']
    dldir = config['DOWNLOADER']['downloaddir']
    cookiefile = config['DOWNLOADER']['cookiefile']
    archivefile = config['DOWNLOADER']['archivefile']
    postdownloadscript = config['DOWNLOADER']['postdownloadscript']
    #dlDir = config['WATCHER']['downloaddir']

else:
    print("ERROR: NO CONFIG FILE! Exiting...")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - Started without config File, please rename TEMPLATEconfig.txt to config.txt and fill the parameters.\n")
    quit()

if (os.path.isfile(pwd+"/dl_batch.txt")):
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - Downloader process started\n")

    class MyLogger:
        def debug(self, msg):
            # For compatability with youtube-dl, both debug and info are passed into debug
            # You can distinguish them by the prefix '[debug] '
            if msg.startswith('[debug] '):
                pass
            else:
                self.info(msg)

        def info(self, msg):
            if (logLevel == "DEBUG"):
                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]-[INFO] - ")+msg+"\n")

        def warning(self, msg):
            if (logLevel == "WARN"):
                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]-[WARN] - ")+msg+"\n")

        def error(self, msg):
            if (logLevel == "ERROR"):
                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]-[ERROR] - ")+msg+"\n")

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
        'cookiefile': cookiefile,
        'retries': float('inf'),
        'throttledratelimit': 100000,
        'trim_file_name':200,
        'outtmpl': dldir+"%(channel)s-(%(id)s)-%(upload_date)s - %(title)s.%(ext)s",
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

    if ("--ignore-archive" not in sys.argv):
        ydl_opts.update({'download_archive': archivefile,})
        

    # Add custom headers
    yt_dlp.utils.std_headers.update({'Referer': 'https://www.google.com'})

    # ℹ️ See the public functions in yt_dlp.YoutubeDL for for other available functions.
    # Eg: "ydl.download", "ydl.download_with_info_file"
    with open(pwd+"/dl_batch.txt") as dl_batch:
        for link in dl_batch:
            if (link == "" or link == "\n" or link == "\r\n"):
                pass
            else:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
                    if (glob.glob(dldir+"/*.srv3")):
                        subfilelist = glob.glob(dldir+"/*.srv3")
                        for subfile in subfilelist:
                            #YTSubConvCMD = "mono "+pwd+"/postprocessors/YTSubConverter/YTSubConverter.exe --visual "+'"'+subfile+'"'
                            #YTSubConvCall = subprocess.Popen(YTSubConvCMD, shell=True, stdout=subprocess.PIPE, close_fds=True, universal_newlines=True)
                            YTSubConvCall = subprocess.Popen(["mono", f"{pwd}/postprocessors/YTSubConverter/YTSubConverter.exe", "--visual", subfile],stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True, universal_newlines=True)
                            YTSubConvCallCall_return,YTSubConvCallCall_error = YTSubConvCall.communicate()
                            if(logLevel=="DEBUG"):
                                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [DEBUG] - [downloader/YTSubConverter] -"+YTSubConvCallCall_return+"\n")
                                print(YTSubConvCallCall_return)
                            if(YTSubConvCallCall_error):
                                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - [downloader/YTSubConverter] -"+YTSubConvCallCall_error+"\n")
                                print(YTSubConvCallCall_error)
                            convertedsubfile = glob.glob(dldir+"/*.ass")
                            VideoFile = glob.glob(dldir+"/*.mkv")
                            VideoFileEdited = VideoFile[0]+".edited.mkv"
                            FFmpegMergeSubCall = subprocess.Popen(["ffmpeg", "-y","-hide_banner","-loglevel","error", "-i", VideoFile[0], "-i", convertedsubfile[0], "-c", "copy", VideoFileEdited],stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True, universal_newlines=True)
                            #FFmpegMergeSubCall = subprocess.Popen(["ffmpeg -y -i "+'"'+VideoFile[0]+'"'+" -i "+'"'+convertedsubfile[0]+'"'+" -c copy "+'"'+VideoFile[0]+"edited.mkv"+'"'], shell=True, stdout=subprocess.PIPE, close_fds=True, universal_newlines=True)
                            FFmpegMergeSubCall_return,FFmpegMergeSubCall_error = FFmpegMergeSubCall.communicate()
                            if(logLevel=="DEBUG"):
                                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [DEBUG] - [downloader/FFmpegMerge] -"+FFmpegMergeSubCall_return+"\n")
                                print(FFmpegMergeSubCall_return)
                            if(FFmpegMergeSubCall_error):
                                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - [downloader/FFmpegMerge] -"+FFmpegMergeSubCall_error+"\n")
                                print(FFmpegMergeSubCall_error)
                            os.remove(subfile)
                            os.remove(str(convertedsubfile[0]))
                            os.replace(VideoFileEdited, str(VideoFile[0]))
                            FinalFile = str(VideoFile[0])
                            if (postdownloadscript == "none"):
                                continue
                            else:
                                
                                #rclone_move.rclonemove(FinalFile,logWriter,dldir)
                                postexec.executePostexec(FinalFile,logWriter,dldir)
                                
                                #STATT HIER DIRECT DEN RCLONE UPLOAD MACHEN EINFACH HIER EINE ANDERE .py STARTEN LASSEN, VARs ÜBERGEBEN UND DANN IN DER CONFIG MITGEBEN WELCHE .py GESTARTET WERDEN SOLL, Z.B EINFACH EINEN ORDNER PLUGINS MACHEN UND DA EIN 
                                #FERTIGES RCLONE PLUGIN LIEFERN
                                #PostDLCall = subprocess.Popen(["rclone", "move", "/opt/archiving/export/TEST", "HoloDrive:TEST"],stdout=subprocess.PIPE, close_fds=True, universal_newlines=True)
                                #PostDLCall_return = PostDLCall.communicate()[0]
                    
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - Run finished, closing...\n")
    logWriter.close()
else:
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - No dl_batch.txt present, closing...\n")
    logWriter.close()
    quit()
