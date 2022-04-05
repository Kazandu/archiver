import os
from time import sleep
import re
import subprocess
import configparser
config = configparser.ConfigParser()
pwd=os.getcwd()
from datetime import *
datumHeute = datetime.date(datetime.now()).strftime("%Y%m%d")
import time
import yt_dlp
from tqdm import tqdm
from dateutil.parser import isoparse
print("####################################################################################################\n############################### KAZ ARCHIVER - CHECKER #############################################\n####################################################################################################")

if (os.path.isfile(pwd+"/config.ini")):
    config.read(pwd+'/config.ini')
    dlDir = config['CHECKER']['downloaddir']
    cookiefile = config['DOWNLOADER']['cookiefile']

else:
    print("ERROR: NO CONFIG FILE! Exiting...")
    logWriter = open (pwd+"/logs/"+datumHeute+"_checker.log", "a+")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - Started without config File, please rename TEMPLATEconfig.txt to config.txt and fill the parameters.\n")
    logWriter.close()
    quit()
 #Linecounter for progressbar
with open(pwd+"/check_batch.txt", 'r') as checkbatchcount:
    lines = checkbatchcount.readlines()
    num_lines = len([l for l in lines])
    pbar = tqdm(total=num_lines, ncols=100, colour='#00ff00', unit='link',desc='Progress', bar_format="{desc}:{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]")
    checkbatchcount.close()


if (os.path.isfile(pwd+"/check_batch.txt")):
    ydl_opts = {
#    'listformats': 'true',
    'cookiefile': cookiefile
    }
    logWriter = open (pwd+"/logs/"+datumHeute+"_checker.log", "a+")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - Process started\n")
    logWriter.close()
    with open(pwd+"/check_batch.txt") as check_batch:
        for line in check_batch:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    videoresult = ydl.extract_info(line, download=False) 
                    formats = videoresult.get('formats', [videoresult])
                    video_date = videoresult.get('upload_date', None)
                    #video_uploader = videoresult.get('uploader', None)
                    video_id = videoresult.get('id', None)
                    datetoday = datetime.now()
            except Exception as e:
                if "copyright" in str(e):
                    #print("copyright")
                    ErrorType= "Copyright"
                elif "members-only" in str(e):
                    #print("member only")
                    ErrorType= "Member-only locked"
                elif "Private" in str(e):
                    #print("private")
                    ErrorType= "Privated"
                elif "Video unavailable" in str(e):
                    #print("Video removed or Channel terminated")
                    ErrorType= "Removed"
                else:
                    #print("unknown case")
                    ErrorType= "UNKNOWN ERROR"
                ErrorBatchWriter = open (pwd+"/error_batch.csv", "a+")
                ErrorBatchWriter.write(ErrorType+";"+line.replace('\n','')+";"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")
                #line enthält einen umbruch, musste anders machen
                ErrorBatchWriter.close()
                continue
            

            #print(ytdlpCall_return)
            if ("https vp9" in formats or "https av01" in formats):
                linkWriteAdd = open (dlDir+"/dl_batch.txt", "a+")
                linkWriteAdd.write(line)
                linkWriteAdd.close()
                time.sleep(2) 
                pbar.update(n=1)

                logWriter = open (pwd+"/logs/"+datumHeute+"_checker.log", "a+")
                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - Video ID ["+line.replace('\n','')+"] converted, adding to downloader and removing queue...\n")
                logWriter.close()
            else:
                linkWriteRequeue = open (pwd+"/next_queue.txt", "a+")
                linkWriteRequeue.write(line)
                linkWriteRequeue.close()
                time.sleep(2)
                pbar.update(n=1)

                logWriter = open (pwd+"/logs/"+datumHeute+"_checker.log", "a+")
                logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - Video ID ["+line.replace('\n','')+"] not converted yet, keeping in queue...\n")
                logWriter.close()
    os.replace(pwd+"/next_queue.txt", pwd+"/check_batch.txt")
    logWriter = open (pwd+"/logs/"+datumHeute+"_checker.log", "a+")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - Run finished, closing...\n")
    logWriter.close()
else:
    logWriter = open (pwd+"/logs/"+datumHeute+"_checker.log", "a+")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - No check_batch.txt present, closing...\n")
    logWriter.close()
    quit()
