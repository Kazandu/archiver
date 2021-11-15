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
