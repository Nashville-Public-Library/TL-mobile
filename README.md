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
````python
pip freeze > requirements.txt
````
## Development

First, setup a virtual environment:
````python 
python -m venv venv
````

Then activate it:
````python
venv\scripts\activate
````

Next, install the "Flask" library:

````python
pip install Flask
````

And finally, install the "requests" module:

````python
pip install requests
````

You may have to update to the latest version of Python as well. To do so, run:

````python
python.exe -m pip install --upgrade pip
````

