# TL Mobile

![tests](https://github.com/Nashville-Public-Library/TL-mobile/actions/workflows/main.yml/badge.svg)
[![GitHub issues](https://img.shields.io/github/issues/Nashville-Public-Library/TL-mobile.png)](https://github.com/Nashville-Public-Library/TL-mobile/issues)
[![last-commit](https://img.shields.io/github/last-commit/Nashville-Public-Library/TL-mobile)](https://github.com/Nashville-Public-Library/TL-mobile/commits/main)


[app.nashvilletalkinglibrary.com](https://app.nashvilletalkinglibrary.com)

 a simple mobile app for TL listeners...

## Requirements

### [Python](https://www.python.org/downloads/)

- Use version 3.10 or above
- The production server is running version 3.12
- Make sure to select "add to PATH" during installation.

## Development

- Clone this depository
    ````bash
    git clone https://github.com/Nashville-Public-Library/TL-mobile.git
    ````

- cd into the directory
    ````bash
    cd TL-mobile
    ````

- Create a virtual environment
    ````bash 
    py -m venv venv
    ````
    - Depending on your OS, instead of `py` you may need to use `python` or `python3`


- Activate virtual environment
    - On Windows:

    ````bash
    venv\Scripts\activate
    ````
    - On Mac:

    ````bash
    source venv/bin/activate
    ````

    >[IMPORTANT]
    >If done correctly, you should see `(venv)` in the terminal. Do not continue unless you see `(venv)` in the terminal.


- Install Dependencies
    ````bash
    pip install -r requirements.txt
    ````

- Launch the app
    ````bash
    py application.py
    ````
    - Depending on your OS, instead of `py` you may need to use `python` or `python3`

## Misc

If you add 3rd party libraries, don't forget to add them to the `requirements.txt` file as you go: 
````bash
pip freeze > requirements.txt
````