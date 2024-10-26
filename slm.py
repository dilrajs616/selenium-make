import argparse
from utils import download_driver, update_env

def main():
    parser = argparse.ArgumentParser(description="Selenium Wrapper (slm)")
    subparsers = parser.add_subparsers(dest="command")

    # slm init <browser_name>
    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('browser_name', help="Name of the browser (chrome, firefox, etc.)")

    args = parser.parse_args()

    if args.command == "init":
        browser_name = args.browser_name
        driver_path = download_driver(browser_name)
        update_env(driver_path)
        print(f"Driver for {browser_name} installed at {driver_path} and path updated in .env")

if __name__ == "__main__":
    main()
