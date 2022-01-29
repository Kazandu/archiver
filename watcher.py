import os
from time import sleep
import re
import subprocess
import configparser
config = configparser.ConfigParser()
pwd=os.getcwd()
from datetime import datetime
datumHeute = datetime.date(datetime.now()).strftime("%Y%m%d")
import time
import pycurl
from io import BytesIO

def YTComTabPycurlScraper(scrapeUrl):
    output = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, scrapeUrl)
    c.setopt(pycurl.WRITEFUNCTION, output.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.COOKIEJAR, YTcookie)
    c.setopt(pycurl.COOKIEFILE, YTcookie)
    c.perform()
    scrapedHTML = output.getvalue()
    regexstageone = re.findall('(videoId":")(.{11})', str(scrapedHTML))
    for i in regexstageone:
        stageonetostring = str(i)
        regexstagetwo = re.search("(.*)(.{11})(\')", stageonetostring)
        IdList= list(dict.fromkeys(regexstagetwo[2]))
        #old
        #linkWriteAdd = open ("videoIDoutput.txt", "a+")
        #linkWriteAdd.write(regexstagetwo[2]+"\n")
        #linkWriteAdd.close()
    lines_seen = set()
    outfile = open("videoIDoutputdeduped.txt", "w")
    for line in open("videoIDoutput.txt", "r"):
            if line not in lines_seen: # not a duplicate
                    outfile.write(line)
                    lines_seen.add(line)
    outfile.close()
    with open("videoIDoutputdeduped.txt", 'r') as fin:
        print(fin.read())




if (os.path.isfile(pwd+"/config.ini")):
    config.read(pwd+'/config.ini')
    #dlDir = config['WATCHER']['downloaddir']
    YTcookie = config['GENERAL']['YTcookie']

else:
    print("ERROR: NO CONFIG FILE! Exiting...")
    logWriter = open (pwd+"/logs/"+datumHeute+"_watcher.log", "a+")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - Started without config File, please rename TEMPLATEconfig.txt to config.txt and fill the parameters.\n")
    logWriter.close()
    quit()

if (os.path.isfile(pwd+"/watcher_channels.txt")):
    logWriter = open (pwd+"/logs/"+datumHeute+"_watcher.log", "a+")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - Process started\n")
    logWriter.close()
    with open(pwd+"/watcher_channels.txt") as check_batch:
        for line in check_batch:


            code here
    logWriter = open (pwd+"/logs/"+datumHeute+"_watcher.log", "a+")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [INFO] - Run finished, closing...\n")
    logWriter.close()
else:
    logWriter = open (pwd+"/logs/"+datumHeute+"_watcher.log", "a+")
    logWriter.write(datetime.time(datetime.now()).strftime("[%H:%M:%S]")+" [ERROR] - No watcher_channels.txt present, closing...\n")
    logWriter.close()
    quit()
