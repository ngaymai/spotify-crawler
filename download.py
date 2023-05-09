import time
# import codecs
import requests
import os
import string
import sys
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

CWD = os.getcwd()
LOCATION = os.path.join(CWD,'MUSIC')
if os.path.isdir(LOCATION)==False:
    os.mkdir(LOCATION)


def get_ID(session, id):
    LINK = f'https://api.spotifydown.com/getId/{id}'
    headers = {
        'authority': 'api.spotifydown.com',
        'method': 'GET',
        'path': f'/getId/{id}',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    response = session.get(url = LINK, headers=headers)
    if response.status_code == 200 : 
        data = response.json()
        return data
    return None

def generate_Analyze_id(session, yt_id):

    DL      = 'https://corsproxy.io/?https://www.y2mate.com/mates/analyzeV2/ajax'
    data    = {
        'k_query': f'https://www.youtube.com/watch?v={yt_id}',
        'k_page': 'home',
        'hl': 'en',
        'q_auto': 0,
    }
    headers = {
            'authority': 'corsproxy.io',
            'method': 'POST',
            'path': '/?https://www.y2mate.com/mates/analyzeV2/ajax',
            'origin': 'https://spotifydown.com',
            'referer': 'https://spotifydown.com/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-fetch-mode': 'cors',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
    RES = session.post(url=DL, data=data, headers=headers)
    if RES.status_code ==200:
        return RES.json()
    return None

def generate_Conversion_id(session,  analyze_yt_id, analyze_id):

    DL      = 'https://corsproxy.io/?https://www.y2mate.com/mates/convertV2/index'
    data    = {
        'vid'   : analyze_yt_id,
        'k'     : analyze_id,
    }
    headers = {
            'authority': 'corsproxy.io',
            'method': 'POST',
            'path': '/?https://www.y2mate.com/mates/analyzeV2/ajax',
            'origin': 'https://spotifydown.com',
            'referer': 'https://spotifydown.com/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-fetch-mode': 'cors',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
  
    RES = session.post(url=DL, data=data, headers=headers)
    if RES.status_code ==200:
        return RES.json()
    return None
def returnSPOT_ID(link):
    return link.split('/')[-1].split('?si')[0]

## NEW
def get_PlaylistMetadata(session, Playlist_ID):
    URL = f'https://api.spotifydown.com/metadata/playlist/{Playlist_ID}'
    headers = {
        'authority': 'api.spotifydown.com',
        'method': 'GET',
        'path': f'/metadata/playlist/{Playlist_ID}',
        'scheme': 'https',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    meta_data = session.get(headers=headers, url=URL)
    if meta_data.status_code == 200 : 
        return meta_data.json()['title'] + ' - ' + meta_data.json()['artists']
    return None
    
def get_PlaylistMetadataTrack(session, Playlist_ID):
    URL = f'https://api.spotifydown.com/metadata/track/{Playlist_ID}'
    headers = {
        'authority': 'api.spotifydown.com',
        'method': 'GET',
        'path': f'/metadata/track/{Playlist_ID}',
        'scheme': 'https',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    meta_data = session.get(headers=headers, url=URL)
    if meta_data.status_code == 200 : 
        return meta_data.json()['title'] + ' - ' + meta_data.json()['artists']
    return None
    
    
    
def errorcatch(session, SONG_ID):
    print('[*] Trying to download...')
    headers = {
        'authority': 'api.spotifydown.com',
        'method': 'GET',
        'path': f'/download/{SONG_ID}',
        'scheme': 'https',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    x = session.get(headers=headers, url='https://api.spotifydown.com/download/'+ SONG_ID)
    if x.status_code == 200 : 
        return x.json()['link']
    return None


def downloader(url):
    # Create Session 
    session = requests.Session()


    SPOTIFY_PLAYLIST_LINK = url
    OFFSET_VARIABLE = 0 #<-- Change to start from x number of songs

    ID = returnSPOT_ID(SPOTIFY_PLAYLIST_LINK)

    PlaylistName = get_PlaylistMetadata(session, ID)

    print('[*] SPOTIFY PLAYLIST NAME    : ', PlaylistName)

    headers = {
            'authority': 'api.spotifydown.com',
            'method': 'GET',
            'path': f'/trackList/playlist/{ID}',
            'scheme': 'https',
            'accept': '*/*',
            'dnt': '1',
            'origin': 'https://spotifydown.com',
            'referer': 'https://spotifydown.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

    Playlist_Link = f'https://api.spotifydown.com/trackList/playlist/{ID}'

    offset_data = {}
    offset = OFFSET_VARIABLE
    page = 0
    offset_data['offset'] = offset

    response = session.get(url = Playlist_Link,headers=headers,params=offset_data )

    while offset != None :
        if response.status_code == 200 : 
            Tdata = response.json()['trackList']
            page = response.json()['nextOffset']
            for count,song in enumerate(Tdata):
                yt_id = get_ID(session=session, id=song['id'])
                if yt_id is not None:
                    filename = song['title'].translate(str.maketrans('', '', string.punctuation)) + ' - ' + song['artists'].translate(str.maketrans('', '', string.punctuation)) + '.mp3'
                    print('*'*25, str(count+1) + '/' + str(len(Tdata)), '*'*25)
                    print('[*] Name of Song         : ', song['title'])
                    print('[*] Spotify ID of Song   : ',song['id'])
                    print('[*] Youtube ID of Song   : ',yt_id['id'])
                    try:
                        data  = generate_Analyze_id(session = session, yt_id = yt_id['id'])
                        try:
                            DL_ID = data['links']['mp3']['mp3128']['k']
                            DL_DATA = generate_Conversion_id(session= session,  analyze_yt_id = data['vid'], analyze_id = DL_ID )
                            DL_LINK = DL_DATA['dlink']
                        except  Exception as NoLinkError:
                            CatchMe = errorcatch(session=session, SONG_ID=song['id'])
                            if CatchMe is not None:
                                DL_LINK = CatchMe
                        if DL_LINK is not None:
                            ## DOWNLOAD
                            link= session.get(DL_LINK)
                            
                            # Create Folder for Playlist 
                            FolderPath = ''.join(e for e in PlaylistName if e.isalnum() or e in [' ', '_'])
                            playlist_folder_path = os.path.join(LOCATION, FolderPath)
                            if not os.path.exists(playlist_folder_path):
                                os.makedirs(playlist_folder_path)
                                
                            ## Save    
                            with open(os.path.join(playlist_folder_path,filename), 'wb') as f:
                                f.write(link.content)
                        else:
                            print('[*] No Download Link Found.')
                    except Exception as error_status:
                        print('[*] Error Status Code : ',error_status)
                        
                else:
                    print('[*] No data found for : ', song)
        if page!=None:
            offset_data['offset'] = page
            response = session.get(url = Playlist_Link, params=offset_data, headers=headers)
        else:
            break 

def downloadOne(url):
    session = requests.Session()
    ID = returnSPOT_ID(url)
    URL = f'https://api.spotifydown.com/download/{ID}'

    headers = {
            'authority': 'api.spotifydown.com',
            'method': 'GET',
            'path': f'/download/{ID}',
            'scheme': 'https',
            'accept': '*/*',
            'dnt': '1',
            'origin': 'https://spotifydown.com',
            'referer': 'https://spotifydown.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }


    response = requests.get(URL, headers=headers)
    data = response.json()
    PlaylistName = data['metadata']['album']

    filename = data['metadata']['title'].translate(str.maketrans('', '', string.punctuation)) + ' - ' + data['metadata']['artists'].translate(str.maketrans('', '', string.punctuation)) + '.mp3'
    link = session.get(data['link'])
# Create Folder for Playlist 
    FolderPath = ''.join(e for e in PlaylistName if e.isalnum() or e in [' ', '_'])
    playlist_folder_path = os.path.join(LOCATION, FolderPath)
    if not os.path.exists(playlist_folder_path):
        os.makedirs(playlist_folder_path)
                                
            ## Save    
    with open(os.path.join(playlist_folder_path,filename), 'wb') as f:
        f.write(link.content)  
    return filename

if __name__ == '__main__':
    if sys.argv[1] == 'all':
        downloader(sys.argv[2])
    elif sys.argv[1] == 'one':
        options = Options()
        options.add_argument("incognito")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(sys.argv[2])
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//button[@class="T0anrkk_QA4IAQL29get"]').click()
        driver.find_element(By.XPATH, '//button[@class="wC9sIed7pfp47wZbmU6m QgtQw2NJz7giDZxap2BB"][@aria-expanded="false"]').click()
        driver.find_element(By.XPATH, '//ul[@class="SboKmDrCTZng7t4EgNoM"]/li[1]/button[1]').click()
        song = downloadOne(pyperclip.paste())
       
        print('[*] SPOTIFY SONG NAME    : ' + song)
    
      


    