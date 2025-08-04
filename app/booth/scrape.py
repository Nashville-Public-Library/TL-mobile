'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from app.booth.hours import hour1, hour2
from app.ev import EV
from app.booth.utils import date_is_weekend


def scrape_VIC(date):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    os_name = os.name
    if os_name == 'nt':
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    else:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

    date = date.strftime('%m%d%Y')
    driver.get(f'https://www.volgistics.com/vicnet/15495/schedule?view=day&date={date}')

    driver.implicitly_wait(10)

    email = driver.find_element(by=By.NAME, value="email")
    password = driver.find_element(by=By.NAME, value="password")

    email.send_keys(EV().VIC_user)
    password.send_keys(EV().VIC_pass)

    submit = driver.find_element(by=By.CLASS_NAME, value="mat-mdc-raised-button")
    submit.click()

    # now we're logged in

    driver.implicitly_wait(15)

    shifts = driver.find_elements(By.CLASS_NAME, 'column-details-desktop')
    ret_val: list = []
    for shift in shifts:
        ret_val.append(shift.text)

    driver.quit()
    return ret_val

def remove_extra_text(booth: str, shift: str, hour: str) -> str:
    text_to_remove = ('• Other - Talking Library\Staff Service', '• Other - Talking Library\Collection Service', 
                'AM Newspaper Reading', 'The Tennessean', 'Nashville Ledger', 'Nashville Scene', '"', '1 more needed', 'Account Staff', booth, hour)
    for text in text_to_remove:
        shift = shift.replace(text, '')
    booth_return = shift.strip()
    if booth_return == '':
        booth_return = 'Empty'
    return booth_return

def get_scrape_and_filter(date) -> dict:
    '''
    get all the elements via selenium and loop through them to match booth numbers and hours. start out assuming all booths are closed,
    and update the dictionary only when there is a match.p
    '''
    booth1 = "Booth 1"
    booth2 = "Booth 2"
    booth3 = "Booth 3"
    newspaper = "AM Newspaper Reading"
    
    schedule = {
        "newspaper": [],
        "9": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "10": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "11": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "12": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "13": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "14": {"booth1": "closed", "booth2": "closed", "booth3": "closed"},
        "15": {"booth1": "closed", "booth2": "closed", "booth3": "closed"}
    }

    # no need to run this function on weekends
    if date_is_weekend(date=date):
        return schedule

    nine = "9:00am - 10:00am"
    ten = "10:00am - 11:00am"
    eleven = "11:00am - 12:00pm"
    twelve = "12:00pm - 1:00pm"
    one = "1:00pm - 2:00pm"
    two = "2:00pm - 3:00pm"
    three = "3:00pm - 4:30pm"
    
    shifts = scrape_VIC(date)
    for shift in shifts:

        if newspaper in shift:
            schedule["newspaper"].append(remove_extra_text(booth=newspaper, shift=shift, hour="9:00am - 11:00am"))

        if (booth1 in shift) and (nine in shift):
            schedule['9']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=nine)

        if (booth2 in shift) and (nine in shift):
            schedule['9']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=nine)

        if (booth3 in shift) and (nine in shift):
            schedule['9']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=nine)

        
        if (booth1 in shift) and (ten in shift):
            schedule['10']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=ten)

        if (booth2 in shift) and (ten in shift):
            schedule['10']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=ten)

        if (booth3 in shift) and (ten in shift):
            schedule['10']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=ten)

        
        if (booth1 in shift) and (eleven in shift):
            schedule['11']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=eleven)

        if (booth2 in shift) and (eleven in shift):
            schedule['11']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=eleven)

        if (booth3 in shift) and (eleven in shift):
            schedule['11']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=eleven)

        
        if (booth1 in shift) and (twelve in shift):
            schedule['12']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=twelve)

        if (booth2 in shift) and (twelve in shift):
            schedule['12']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=twelve)

        if (booth3 in shift) and (twelve in shift):
            schedule['12']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=twelve)

        
        if (booth1 in shift) and (one in shift):
            schedule['13']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=one)

        if (booth2 in shift) and (one in shift):
            schedule['13']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=one)

        if (booth3 in shift) and (one in shift):
            schedule['13']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=one)


        if (booth1 in shift) and (two in shift):
            schedule['14']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=two)

        if (booth2 in shift) and (two in shift):
            schedule['14']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=two)

        if (booth3 in shift) and (two in shift):
            schedule['14']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=two)
        

        if (booth1 in shift) and (three in shift):
            schedule['15']['booth1'] = remove_extra_text(booth=booth1, shift=shift, hour=three)

        if (booth2 in shift) and (three in shift):
            schedule['15']["booth2"] = remove_extra_text(booth=booth2, shift=shift, hour=three)

        if (booth3 in shift) and (three in shift):
            schedule['15']["booth3"] = remove_extra_text(booth=booth3, shift=shift, hour=three)
   
    return schedule
