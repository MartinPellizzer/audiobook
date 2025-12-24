
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=/home/ubuntu/.config/google-chrome/SeleniumProfile")
# optional: specify a profile within that folder
chrome_options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com")

