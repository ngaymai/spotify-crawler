from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pyperclip
import sys
import requests
import os
import string


CWD = os.getcwd()
LOCATION = os.path.join(CWD,'PICTURE')
if os.path.isdir(LOCATION)==False:
    os.mkdir(LOCATION)



def returnID(link):
    return link.split('/')[-1].split('?image')[0] + '.jpg'
def downloader(url):
    
    response = requests.get(url)
    name = returnID(url)
                            ## Save    
    with open(os.path.join(LOCATION,name), 'wb') as f:        
        f.write(response.content)
       


if __name__ == '__main__':
    downloader(sys.argv[1])
    
      