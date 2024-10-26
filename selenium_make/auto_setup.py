import sys
import subprocess

def install_dependencies():
    subprocess.run([sys.executable, "-m", "pip", "install", "selenium"])
    subprocess.run([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    subprocess.run([sys.executable, "-m", "pip", "install", "webdriver-manager"])

def create_script(browser_name):
    # installing dependencies
    install_dependencies()

    with open('requirements.txt', 'w') as req_file:
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=req_file)

    if browser_name.lower() == 'chrome':
        driver='ChromeDriverManager'
    else:
        driver='GeckoDriverManager'

    # creating the script file
    with open('script.py', 'w') as f:
        f.write(f'''from selenium import webdriver
from selenium.webdriver.{browser_name.lower()}.service import Service
from webdriver_manager.{browser_name.lower()} import {driver}
from bs4 import BeautifulSoup
import time

def main():
    service = Service(executable_path={driver}().install())
    driver = webdriver.{browser_name.capitalize()}(service=service)
    site = r'https://www.google.com/search?q=welcome+to+internet'
    driver.get(site)
    driver.implicitly_wait(10000)
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()''')
        
    print("Created file: script.py")