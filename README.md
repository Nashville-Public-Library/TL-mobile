# booth

![tests](https://github.com/Nashville-Public-Library/booth/actions/workflows/main.yml/badge.svg)
[![GitHub issues](https://img.shields.io/github/issues/Nashville-Public-Library/booth.png)](https://github.com/Nashville-Public-Library/booth/issues)
[![last-commit](https://img.shields.io/github/last-commit/Nashville-Public-Library/booth)](https://github.com/Nashville-Public-Library/booth/commits/main)


[api.nashvilletalkinglibrary.com](https://api.nashvilletalkinglibrary.com)

 a simple web app to assist with various backend TL things...

 ----

## Server Config

### Linux 
Any flavor of Linux is fine. As of this writing, we're using Ubuntu.
7GB of storage and a 2-3GB of RAM is plenty.

### SSH
It should be noted that for reasons not understood, ITS blocks the SSH ports for  the entire internet. You can only SSH to servers on the Metro network.
Log in to AWS EC2, and from there you can launch a terminal in the browser. This is the only way to connect to the server from inside Metro.

### Allow Traffic
Go to the EC2 dashboard > Select your instance > Security Tab > Inbound Rules.

Allow SSH (22), HTTP (80), and HTTPS (443). For all, allow from 0.0.0.0/0.

Alternatively, you could do this when first launching the EC2 instance.

### Requirements
 - Python
 ````bash
 sudo apt install -y python3 python3-pip
 ````
 - Git (probably installed already. Just run `git` and if you get an error, run this:)
 ````bash
 sudo apt install -y git
 ````
 - Gunicorn
 ````bash
 pip install gunicorn
````
- Nginx
````bash
sudo apt install -y nginx
````
- Chrome

    - Instructions to install Google Chrome browser

- Chromedriver

    - Instructions to install Chromedriver

If you get errors when installing any of these, consult the internet (or ChatGPT, which is free to use).

- Timezone

Next, we need to change the timezone to Central Time. The command below will automatically adjust for Daylight Saving Time.
````bash
sudo timedatectl set-timezone America/Chicago
````

### Environment Variables
Set in the systemctl config file

### Nginx
nginx stuff...use IP at first to get working, then domain name

### Systemctl service
set this up...

### Certbot
SSL Cert...

## Testing
Run `pytest` at the top level directory to run the basic tests.

## Misc

## Volunteer Photos
Crop the photo to be a headshot and copy it to `static/img/vol/`. The file should be labelled the same way their name shows up in VIC, but remove the space between the first and last name. If the name in VIC is Steve Rogers, the photo should be `SteveRogers.jpg`. All photos must be a .JPG.

Don't forget to continually update your `requirement.txt` file as you go: 
````python
pip freeze > requirements.txt
````
