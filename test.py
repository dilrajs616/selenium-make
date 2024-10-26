from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Automatically download and manage ChromeDriver
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
site = r'https://www.google.com/search?q=welcome+to+internet'
driver.get(site)
driver.implicitly_wait(10000)
time.sleep(10)