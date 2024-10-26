import argparse
from auto_setup import create_script

def main():
    parser = argparse.ArgumentParser(description="Selenium Wrapper (slm)")
    subparsers = parser.add_subparsers(dest="command")

    # slm init <browser_name>
    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('browser_name', help="Name of the browser (chrome, firefox, etc.)")

    args = parser.parse_args()

    if args.command == "init":
        browser_name = args.browser_name
        create_script(browser_name)
        print("     run the following command in terminal")
        print("     python script.py")
    

if __name__ == "__main__":
    main()
