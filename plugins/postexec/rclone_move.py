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
config = configparser.ConfigParser()
pluginconfig = configparser.ConfigParser()

#logWriter = open (pwd+"/logs/"+datumHeute+"_downloader.log", "a+")
#if (os.path.isfile(pwd+"/config.ini")):
#    config.read(pwd+'/config.ini')
#    logLevel = config['DOWNLOADER']['LogLevel']
#    dldir = config['DOWNLOADER']['downloaddir']
#else:
#    print("ERROR: NO CONFIG FILE! Exiting...")
#    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - Started without config File, please rename TEMPLATEconfig.txt to config.txt and fill the parameters.\n")
#    quit()

def rclonemove(filetomove,logWriter,dldir):
    if (os.path.isfile(pwd+"/plugins/postexec/rclone_move.ini")):
        pluginconfig.read(pwd+'/plugins/postexec/rclone_move.ini')
        dstdir = pluginconfig['MAIN']['destinationdir']
    else:
        print("ERROR: NO RCLONE_CONFIG FILE! Exiting...")
        logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - Started without rclone config File, please rename TEMPLATErclone_move.ini to rclone_move.ini and fill the parameters.\n")
        quit()
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - [PostExec] - Starting Rclone upload...\n")   
    PostDLCall = subprocess.Popen(["rclone", "move", f"{filetomove}", f"{dstdir}", "-P"],stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True, universal_newlines=True)
    PostDLCall_return,PostDLCall_error = PostDLCall.communicate()
    #print(PostDLCall_return)
    if (PostDLCall_error):
        logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - [PostExec] -"+PostDLCall_error+"\n")
        print(PostDLCall_error)
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - [PostExec] - Run finished, closing...\n")