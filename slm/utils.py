import os
import requests
import zipfile
import shutil
import platform
from dotenv import load_dotenv, set_key

def get_driver_info(browser_name):
    """Fetches the latest driver download URL based on the browser and OS."""
    if browser_name.lower() == 'chrome':
        api_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
        response = requests.get(api_url)
        if response.status_code != 200:
            raise Exception("Failed to retrieve ChromeDriver info.")
        
        data = response.json()["channels"]["Stable"]
        version = data["version"]
        os_key = detect_os_key(browser_name)
        for download in data["downloads"]["chromedriver"]:
            if download["platform"] == os_key:
                return version, download["url"]

    elif browser_name.lower() == 'firefox':
        api_url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
        response = requests.get(api_url)
        if response.status_code != 200:
            raise Exception("Failed to retrieve GeckoDriver info.")
        
        release_data = response.json()
        os_key = detect_os_key(browser_name)
        for asset in release_data["assets"]:
            if os_key in asset["name"]:
                return release_data["tag_name"], asset["browser_download_url"]

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

def detect_os_key(browser_name):
    """Returns the correct OS key for ChromeDriver or GeckoDriver based on the platform."""
    os_name = platform.system().lower()

    if os_name == "windows":
        return "win64"
    elif os_name == "darwin":
        return "mac-arm64" if platform.processor() == "arm" else "macos"
    elif os_name == "linux":
        return "linux64"
    else:
        raise Exception(f"Unsupported OS: {os_name}")

def download_driver(browser_name):
    """Downloads the browser driver and returns its path."""
    home_dir = os.path.expanduser("~")
    driver_dir = os.path.join(home_dir, ".selenium_drivers", browser_name)
    os.makedirs(driver_dir, exist_ok=True)

    version, url = get_driver_info(browser_name)
    driver_filename = 'chromedriver' if browser_name == 'chrome' else 'geckodriver'
    driver_filename += '.exe' if platform.system().lower() == 'windows' else ''

    zip_path = os.path.join(driver_dir, f"{browser_name}_driver.zip")
    download_file(url, zip_path)
    driver_path = extract_driver(zip_path, driver_dir, driver_filename)

    return driver_path

def download_file(url, path):
    """Downloads a file from the given URL."""
    print(f"Downloading driver from {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"Driver downloaded successfully at {path}")
    else:
        raise Exception(f"Failed to download from {url}")

def extract_driver(zip_path, driver_dir, driver_filename):
    """Extracts the driver file from the ZIP archive."""
    print(f"Extracting driver to {driver_dir}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(driver_dir)
    except zipfile.BadZipFile:
        raise Exception(f"The ZIP file is corrupt or invalid.")
    
    os.remove(zip_path)  # Clean up the ZIP file
    return os.path.join(driver_dir, driver_filename)

def update_env(driver_path):
    """Updates the .env file with the driver path."""
    env_file = os.path.join(os.getcwd(), ".env")
    load_dotenv(env_file)
    set_key(env_file, "SELENIUM_DRIVER_PATH", driver_path)
