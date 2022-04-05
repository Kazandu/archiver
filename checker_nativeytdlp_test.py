import os
from time import sleep
import re
import subprocess
import configparser
pwd=os.getcwd()
from datetime import *
import time
import json
import yt_dlp
import glob
import pdb
import sys
#from plugins.postexec import rclone_move
from plugins.postexec import postexec
from dateutil.parser import isoparse

    # ℹ️ See docstring of yt_dlp.YoutubeDL for a description of the options
ydl_opts = {
#    'listformats': 'true',
    'forceprint':'title',
    'skip_download':'true'
    }
    # Add custom headers
#yt_dlp.utils.std_headers.update({'Referer': 'https://www.google.com'})
print("\n########################\nCONVERTED EXAMPLE BELOW\n########################\n")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#    ydl.download(["https://www.youtube.com/watch?v=mFLu8TKDsrk"])
    meta = ydl.extract_info(
            'https://www.youtube.com/watch?v=mFLu8TKDsrk', download=False) 
    formats = meta.get('formats', [meta])
    video_date = meta.get('upload_date', None)
    video_uploader = meta.get('uploader', None)
    video_title = meta.get('title', None)
    for f in formats:
        if f['protocol'] == 'https':
            print(f['format_id'],f['protocol'], f['vcodec'])
    print("Uploaddatum preconvert: "+video_date)
    newuploaddate = isoparse(video_date)
    print("Isoparsed upload date: "+newuploaddate.strftime("%Y%m%d"))
    datumHeute = datetime.now()
    print("Datum heute: "+ datumHeute.strftime("%Y%m%d"))
    print((datumHeute - newuploaddate).days)
    print(video_uploader)
    print(video_title)
    if ("https vp9" or "https av01" in formats):
        print("yaaay vp9")
    else:
        print("eeeh kein vp9")

print("\n########################\nUNCONVERTED EXAMPLE BELOW\n########################\n")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#    ydl.download(["https://www.youtube.com/watch?v=mFLu8TKDsrk"])
    meta = ydl.extract_info(
        'https://www.youtube.com/watch?v=X47y6JbuDW8', download=False) 
    formats = meta.get('formats', [meta])
    for f in formats:
        if f['protocol'] == 'https':
            print(f['format_id'],f['protocol'], f['vcodec'])
    if ("https vp9" in formats or "https av01" in formats):
        print("yaaay vp9")
    else:
        print("eeeh kein vp9")

        
print("\n########################\nCOPYRIGHT EXAMPLE BELOW\n########################\n")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download(["https://www.youtube.com/watch?v=mFLu8TKDsrk"])
        meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=h9fesFwxJu8', download=False) 
        #formats = meta.get('formats', [meta])
        video_date = meta.get('upload_date', None)
        #video_uploader = meta.get('uploader', None)
        video_title = meta.get('id', None)
        for f in formats:
            if f['protocol'] == 'https':
                print(f['format_id'],f['protocol'], f['vcodec'])
except Exception as e:
    #continue
    if "copyright" in str(e):
        print("copyright")
    elif "members-only" in str(e):
        print("member only")
    elif "Private" in str(e):
        print("private")
    else:
        print("unknown case")
    pass



print("\n########################\nMEMBERONLY EXAMPLE BELOW\n########################\n")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download(["https://www.youtube.com/watch?v=mFLu8TKDsrk"])
        meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=uVeRObMKMJY', download=False) 
        formats = meta.get('formats', [meta])
        for f in formats:
            if f['protocol'] == 'https':
                print(f['format_id'],f['protocol'], f['vcodec'])
except Exception as e:
    #continue
    if "copyright" in str(e):
        print("copyright")
    elif "members-only" in str(e):
        print("member only")
    elif "Private" in str(e):
        print("private")
    else:
        print("unknown case")
    pass



print("\n########################\nPRIVATED EXAMPLE BELOW\n########################\n")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download(["https://www.youtube.com/watch?v=mFLu8TKDsrk"])
        meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=ImjFF-suFz8', download=False) 
        formats = meta.get('formats', [meta])
        for f in formats:
            if f['protocol'] == 'https':
                print(f['format_id'],f['protocol'], f['vcodec'])
except Exception as e:
    #continue
    if "copyright" in str(e):
        print("copyright")
    elif "members-only" in str(e):
        print("member only")
    elif "Private" in str(e):
        print("private")
    else:
        print("unknown case")
    pass  

print("\n########################\nINVALID VIDEO EXAMPLE BELOW\n########################\n")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download(["https://www.youtube.com/watch?v=mFLu8TKDsrk"])
        meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=ImasasaF-suFz8', download=False) 
        formats = meta.get('formats', [meta])
        for f in formats:
            if f['protocol'] == 'https':
                print(f['format_id'],f['protocol'], f['vcodec'])
except Exception as e:
    #continue
    if "copyright" in str(e):
        print("copyright")
    elif "members-only" in str(e):
        print("member only")
    elif "Private" in str(e):
        print("private")
    else:
        print("unknown case")
    pass  

print("\n########################\nTERMINATED CHANNEL EXAMPLE BELOW\n########################\n")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download(["https://www.youtube.com/watch?v=mFLu8TKDsrk"])
        meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=nWhHktrGT5E', download=False) 
        formats = meta.get('formats', [meta])
        for f in formats:
            if f['protocol'] == 'https':
                print(f['format_id'],f['protocol'], f['vcodec'])
except Exception as e:
    #continue
    if "copyright" in str(e):
        print("copyright")
    elif "members-only" in str(e):
        print("member only")
    elif "Private" in str(e):
        print("private")
    elif "Video unavailable" in str(e):
        print("Video removed or Channel terminated")
    else:
        print("unknown case")
    pass  

print("\n########################\nREMOVED VIDEO EXAMPLE BELOW\n########################\n")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download(["https://www.youtube.com/watch?v=mFLu8TKDsrk"])
        meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=VDCQ5Uz6Lhs', download=False) 
        formats = meta.get('formats', [meta])
        for f in formats:
            if f['protocol'] == 'https':
                print(f['format_id'],f['protocol'], f['vcodec'])
except Exception as e:
    #continue
    if "copyright" in str(e):
        print("copyright")
    elif "members-only" in str(e):
        print("member only")
    elif "Private" in str(e):
        print("private")
    else:
        print("unknown case")
    pass 