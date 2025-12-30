import os
import time
import pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def sluggify(text):
    slug = text.strip().lower().replace(' ', '-').replace("'", '')
    return slug

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=/home/ubuntu/.config/google-chrome/SeleniumProfile")
chrome_options.add_argument("--profile-directory=Default")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com")
driver.maximize_window()

### reload page
driver.get("http://localhost:7860/")
time.sleep(10)

### prompt image
e = driver.find_element(By.XPATH, '//input[@type="file"]')
img_filepath = f'/home/ubuntu/vault/audiobook/psychology/0039-dont-get-attached-easily/tmp/images/img-0000.jpg'
e.send_keys(f'{img_filepath}') 
time.sleep(1)

### prompt text
pyautogui.moveTo(500, 1100)
pyautogui.click()
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('delete')
time.sleep(1)
###
prompt = 'a young man standing on a quiet city street, looking ahead thoughtfully, hands in pockets, not interacting with anyone around him, embodying a sense of emotional distance'
e = driver.find_element(By.XPATH, "//span[contains(text(), 'Prompts')]/following-sibling::div//textarea")
driver.execute_script("arguments[0].focus();", e)
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
actions.send_keys(prompt)
actions.perform()

### gen video
e = driver.find_element(By.XPATH, '//button[text()="Generate"]')
e.click()

### save video
for _ in range(60):
    try:
        video = driver.find_element(By.XPATH, "//video[@data-testid='detailed-video']")
    except:
        time.sleep(5)
        continue
    video_url = video.get_attribute("src")

    import requests

    video_url = video.get_attribute("src")
    output_file = "output.mp4"

    # Download the video
    response = requests.get(video_url, stream=True)
    response.raise_for_status()  # make sure the request worked

    with open(output_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"Video saved as {output_file}")

