from dotenv import load_dotenv, set_key
import os
import requests
import zipfile
import shutil

import os
import requests
import zipfile
import shutil
import platform

def get_latest_chromedriver_info():
    """Fetches the latest ChromeDriver version and download URL for the user's OS."""
    chrome_testing_url = "https://googlechromelabs.github.io/chrome-for-testing/"
    api_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve the latest ChromeDriver information.")
    
    data = response.json()
    stable_version_info = data["channels"]["Stable"]

    # Detect the OS to get the right driver
    os_name = platform.system().lower()
    
    if os_name == "windows":
        os_key = "win64"
    elif os_name == "darwin":
        os_key = "mac-arm64" if platform.processor() == "arm" else "mac-x64"
    elif os_name == "linux":
        os_key = "linux64"
    else:
        raise Exception(f"Unsupported OS: {os_name}")

    # Fetch the corresponding driver URL for the detected OS
    for download_info in stable_version_info["downloads"]["chromedriver"]:
        if download_info["platform"] == os_key:
            return stable_version_info["version"], download_info["url"]

    raise Exception(f"No driver found for the platform: {os_key}")

def download_driver(browser_name):
    home_dir = os.path.expanduser("~")
    driver_dir = os.path.join(home_dir, ".selenium_drivers", browser_name)
    os.makedirs(driver_dir, exist_ok=True)

    if browser_name.lower() == 'chrome':
        # Get the latest ChromeDriver version and download URL dynamically
        version, url = get_latest_chromedriver_info()
        driver_filename = 'chromedriver.exe' if platform.system().lower() == 'windows' else 'chromedriver'
    elif browser_name.lower() == 'firefox':
        # For Firefox (GeckoDriver), you can either use a specific version or the latest release
        url = 'https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.30.0-win64.zip'
        driver_filename = 'geckodriver.exe'
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    zip_path = os.path.join(driver_dir, f"{browser_name}_driver.zip")

    # Download the driver
    print(f"Downloading {browser_name} driver from {url}...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        # Save the ZIP file
        with open(zip_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"{browser_name} driver downloaded successfully at {zip_path}")
    else:
        raise Exception(f"Failed to download driver from {url}")

    # Extract the ZIP file
    print(f"Extracting {browser_name} driver...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(driver_dir)
    except zipfile.BadZipFile:
        raise Exception(f"Error: The downloaded ZIP file for {browser_name} is corrupt or invalid.")

    # Remove the ZIP file after extraction (optional)
    os.remove(zip_path)

    # Path to the extracted driver
    driver_path = os.path.join(driver_dir, driver_filename)

    return driver_path


def update_env(driver_path):
    # Update or create .env file in the current working directory
    env_file = os.path.join(os.getcwd(), ".env")
    load_dotenv(env_file)
    set_key(env_file, "SELENIUM_DRIVER_PATH", driver_path)
