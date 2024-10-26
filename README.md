# selenium-make

`selenium-make` automates the installation of essential dependencies for web scraping and browser automation using Selenium and BeautifulSoup. It creates a simple Selenium-based web automation script tailored for the specified browser (Chrome or Firefox).

## Installation

To install `selenium-make`, you can use pip. Run the following command in your terminal:

```bash
pip install selenium-make
```

## Usage

After installing the package, you can initialize the selenium project by running the following command:

```bash
slm init <browser name>
```

### Supported Browsers

- **Chrome**: Use `slm init chrome` to download the ChromeDriver that is compatible with your browser version.
- **Firefox**: Use `slm init firefox` to download the GeckoDriver that is compatible with your browser version.

### Example

To initialize selenium script for using chrome, you would run:

```bash
slm init chrome
```

To initialize selenium script for using firefox, the command would be:

```bash
slm init firefox
```


## Requirements

- Python 3.6 or higher

## Contribution

If you would like to contribute to this project, please fork the repository and submit a pull request. Any enhancements, bug fixes, or suggestions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.