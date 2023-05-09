from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pyperclip
import sys
def crawler(url, ex):
    options = Options()
    options.add_argument("incognito")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
 
    driver.get(url)
    src = driver.page_source

    driver.implicitly_wait(20)
    f = open('GFG.html', 'w', encoding="utf-8")
    f.write(src)
    f.close()


    #sign in with Facebook
    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="login-button"]').click()
    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="facebook-login"]').click()


    #sign in 

    #username
    driver.find_element(By.ID, 'email').send_keys('username') #put username of facebook account 

    driver.find_element(By.ID, 'pass').send_keys('password') #put password of facebook account 
    driver.find_element(By.ID, 'loginbutton').click()

    

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        

        # Wait to load page
        time.sleep(0.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    lst1 = driver.find_elements(By.XPATH, '//a[@data-testid="internal-track-link"]')
    lst2 = driver.find_elements(By.XPATH, '//img[@class="mMx2LUixlnN_Fu45JpFB rkw8BWQi3miXqtlJhKg0 Yn2Ei5QZn19gria6LjZj"]')
    songList = []
    imgList = []
    for song in lst1:
        songList += [song.get_attribute("href")]
    for img in lst2:
        imgList += [img.get_attribute("src")]

    # open all liked tracks
    driver.get(url)

    driver.find_element(By.XPATH, '//button[@class="T0anrkk_QA4IAQL29get"]').click()
    driver.find_element(By.XPATH, '//button[@class="wC9sIed7pfp47wZbmU6m QgtQw2NJz7giDZxap2BB"]').click()
    driver.find_element(By.XPATH, '//ul[@class="SboKmDrCTZng7t4EgNoM"]/li[1]/button[1]').click()
    
    if ex == 'mp3':
        return songList + [pyperclip.paste()]
    elif ex == 'jpg':
        return imgList + [pyperclip.paste()]
    
    


if __name__ == '__main__':
    print(crawler(sys.argv[2], sys.argv[1]))
