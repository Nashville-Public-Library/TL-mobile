# TL Mobile

![tests](https://github.com/Nashville-Public-Library/TL-mobile/actions/workflows/main.yml/badge.svg)
[![GitHub issues](https://img.shields.io/github/issues/Nashville-Public-Library/TL-mobile.png)](https://github.com/Nashville-Public-Library/TL-mobile/issues)
[![last-commit](https://img.shields.io/github/last-commit/Nashville-Public-Library/TL-mobile)](https://github.com/Nashville-Public-Library/TL-mobile/commits/main)


[app.nashvilletalkinglibrary.com (NOT WORKING YET)](https://app.nashvilletalkinglibrary.com)

 a simple mobile app for TL listeners...


## Testing
Run `pytest` at the top level directory to run the basic tests.

## Misc

Don't forget to continually update your `requirement.txt` file as you go: 
````bash
pip freeze > requirements.txt
````
## Development

- Clone this depository
    ````bash
    https://github.com/Nashville-Public-Library/TL-mobile.git
    ````

- cd into the folder in the terminal or open the folder in your IDE
    ````bash
    cd TL-mobile
    ````

- Create a virtual environment
    ````bash 
    py -m venv venv
    ````
    - Depending on your OS, you may need to use `python` or `python3` instead of `py`


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
    >If done correctly, you should see `(venv)` in the terminal. Don't run the rest of these commands unless you see `(venv)` in the terminal.


- Install 3rd party libraries
    ````bash
    pip install -r requirements.txt
    ````

