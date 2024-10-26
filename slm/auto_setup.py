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

    # creating the script file
    with open('script.py', 'w') as f:
        f.write(f'''from selenium import webdriver
from selenium.webdriver.{browser_name.lower}.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
imprt time

load_dotenv()
driver_path = os.getenv("SELENIUM_DRIVER_PATH")
        
def main():
    service = Service(executable_path=driver_path)
    driver = webdriver.{browser_name.capital}(service=service)
    site = r'https://www.google.com/search?q=welcome+to+internet'
    driver.get(site)
    driver.implicitly_wait(10000)
    time.sleep(10)

if __name__ == "__main__":
    main()''')
        
    print("Created file: script.py")