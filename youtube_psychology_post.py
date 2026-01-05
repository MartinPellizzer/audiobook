import os
import time
import random
import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def sluggify(text):
    slug = text.strip().lower().replace(' ', '-').replace("'", '')
    return slug

with open('/home/ubuntu/vault/creds/buffer-username.txt') as f: username = f.read().strip()
with open('/home/ubuntu/vault/creds/buffer-password.txt') as f: password = f.read().strip()

geckodriver_path = 'geckodriver'
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

driver = webdriver.Firefox(service=driver_service)
driver.get('https://www.google.com')
driver.maximize_window()

driver.get("https://login.buffer.com/login")
time.sleep(10)

COOKIE_FILEPATH = 'cookies.plk'
if os.path.exists(COOKIE_FILEPATH):
    print(COOKIE_FILEPATH)
    with open(COOKIE_FILEPATH, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            print(cookie)
            if 'sameSite' in cookie:
                del cookie['sameSite']
            try: 
                driver.add_cookie(cookie)
                print(f"**********************************************************")
                print(f"Adding cookie: {cookie.get('name')}")
                print(f"**********************************************************")
            except Exception as e:
                print(f"Skipping cookie: {cookie.get('name')} - {e}")
    # driver.refresh()
    driver.get("https://publish.buffer.com/all-channels")
    # driver.get("https://www.pinterest.com")
    time.sleep(10)
else:
    e = driver.find_element(By.XPATH, '//input[@type="email"]')
    e.send_keys(username) 
    time.sleep(10)
    e = driver.find_element(By.XPATH, '//input[@id="password"]')
    e.send_keys(password) 
    time.sleep(10)
    e = driver.find_element(By.XPATH, '//div[text()="Log in"]')
    e.click()
    time.sleep(60)
    cookies = driver.get_cookies()
    with open(COOKIE_FILEPATH, 'wb') as f:
        pickle.dump(cookies, f)


for i in range(3):
    driver.get("https://publish.buffer.com/channels/69416b2f29ea336fd686e806")
    time.sleep(10)
    post_add = False
    e = driver.find_element(By.XPATH, '//button[@id="queue-tab"]')
    queue_tab = e.text
    for line in queue_tab.split('\n'):
        try: 
            queue_num = int(line)
            if queue_num < 3: post_add = True
        except: pass
    if not post_add: break
    hub_folderpath = f'/home/ubuntu/vault/audiobook/psychology'
    with open(f'{hub_folderpath}/video-i.txt') as f: short_i = int(f.read())
    ###
    e = driver.find_element(By.XPATH, '//button[text()="New"]')
    e.click()
    time.sleep(10)
    e = driver.find_element(By.XPATH, '//label[text()="Post"]')
    e.click()
    time.sleep(10)
    ###
    with open(f'{hub_folderpath}/ideas.txt') as f: content = f.read()
    ideas = content.strip().split('\n')
    idea_i = short_i
    idea = ideas[idea_i]
    i_str = ''
    if idea_i >= 1000: i_str = f'{idea_i}'
    elif idea_i >= 100: i_str = f'0{idea_i}'
    elif idea_i >= 10: i_str = f'00{idea_i}'
    else: i_str = f'000{idea_i}'
    idea_slug = sluggify(idea)
    video_folderpath = f'{hub_folderpath}/{i_str}-{idea_slug}'
    ###
    title_filepath = f'{hub_folderpath}/{i_str}-{idea_slug}/tmp/video-final/title.txt'
    description_filepath = f'{hub_folderpath}/{i_str}-{idea_slug}/tmp/video-final/description.txt'
    tags_filepath = f'{hub_folderpath}/{i_str}-{idea_slug}/tmp/video-final/tags.txt'
    try:
        with open(title_filepath) as f: 
            title = f.read()
            title_slug = sluggify(title)
    except:
        title = idea
        title_slug = idea_slug
    with open(description_filepath) as f: description = f.read()
    # with open(tags_filepath) as f: tags = f.read()
    print(title)
    print(description)
    # print(tags)
    ###
    video_animated_filepath = f'{hub_folderpath}/{i_str}-{idea_slug}/tmp/video-animated/{title_slug}.mp4'
    video_static_filepath = f'{hub_folderpath}/{i_str}-{idea_slug}/tmp/video-final/{title_slug}.mp4'
    if os.path.exists(video_animated_filepath):
        video_filepath = video_animated_filepath
    else:
        video_filepath = video_static_filepath
    print(video_filepath)
    ###
    e = driver.find_element(By.XPATH, '//input[@name="file-upload-input"]')
    e.send_keys(video_filepath)
    # e.send_keys(f'/home/ubuntu/proj/audiobook/psychology/0004-staying-calm-during-arguments/tmp/video-final/psychology-of-people-who-stay-calm-during-arguments.mp4')
    time.sleep(20)
    e = driver.find_element(By.XPATH, '//div[@role="textbox"]')
    for c in description:
        try: e.send_keys(c)
        except: break
    time.sleep(5)
    e = driver.find_element(By.XPATH, '//input[@aria-label="Video title"]')
    e.send_keys(title)
    time.sleep(5)
    e = driver.find_element(By.XPATH, '//button[text()="Schedule Post"]')
    e.click()
    time.sleep(5)
    ###
    short_i += 1
    with open(f'{hub_folderpath}/video-i.txt', 'w') as f: f.write(str(short_i))


