import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import json
from saver import *

def driver_setup():# Assigning a Headless Firefox Driver
  options = webdriver.FirefoxOptions()
  options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'  # Path to Chrome executable
  options.add_argument('E:/Programs/geckodriver.exe')
  options.add_argument('--headless')
  options.add_argument("--start-with-cache")
  options.add_argument("0")
  options.add_argument("--disk-cache-size=0")
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Firefox(options=options)
  return driver

def save_state(save, pg):
    state = {
        "save": save,
        "pg": pg
    }
    with open("Link_variables.json", "w") as json_file:
        json.dump(state, json_file)

def load_state():
    try:
        with open("Link_variables.json", "r") as json_file:
            state = json.load(json_file)
            save = state["save"]
            pg = state["pg"]
    except FileNotFoundError:
        # Default values if file doesn't exist
        save = 0
        pg = 0
    return save,pg

driver = driver_setup()

save,pg = load_state()

driver.get(f'https://www.naukri.com/jobs-in-india-{pg}?functionAreaIdGid=2&functionAreaIdGid=3&functionAreaIdGid=4&functionAreaIdGid=5&functionAreaIdGid=8&functionAreaIdGid=10&functionAreaIdGid=12&functionAreaIdGid=13&functionAreaIdGid=15&functionAreaIdGid=19&functionAreaIdGid=30&functionAreaIdGid=31&functionAreaIdGid=35&cityTypeGid=6&cityTypeGid=17&cityTypeGid=51&cityTypeGid=73&cityTypeGid=97&cityTypeGid=134&cityTypeGid=138&cityTypeGid=139&cityTypeGid=183&cityTypeGid=220&cityTypeGid=232&cityTypeGid=9508&cityTypeGid=9509&jobAge=15')
time.sleep(3)
total = int(driver.find_element(By.CLASS_NAME, 'styles_h1-wrapper__mHVA1').text.split('of')[-1].split('\n')[0].strip())

while True:    
    time.sleep(4)
    try:
        next_button = driver.find_element(By.LINK_TEXT, "Next")
    except NoSuchElementException:
        print("...closing driver")
        driver.quit()
        driver = driver_setup()
        driver.get(f'https://www.naukri.com/jobs-in-india-{pg}?functionAreaIdGid=2&functionAreaIdGid=3&functionAreaIdGid=4&functionAreaIdGid=5&functionAreaIdGid=8&functionAreaIdGid=10&functionAreaIdGid=12&functionAreaIdGid=13&functionAreaIdGid=15&functionAreaIdGid=19&functionAreaIdGid=30&functionAreaIdGid=31&functionAreaIdGid=35&cityTypeGid=6&cityTypeGid=17&cityTypeGid=51&cityTypeGid=73&cityTypeGid=97&cityTypeGid=134&cityTypeGid=138&cityTypeGid=139&cityTypeGid=183&cityTypeGid=220&cityTypeGid=232&cityTypeGid=9508&cityTypeGid=9509&jobAge=15')# continue run page 
        time.sleep(3)
    
    job_articles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.srp-jobtuple-wrapper')))
    for job_element in job_articles:
        if 'Not disclosed' not in job_element.find_element(By.CSS_SELECTOR, '.sal-wrap.ver-line').text:
            data = {}
            
            try:
                data['link'] = job_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                continue
            if data != {}:
                try:
                    print(f'\rpg: {pg} / {total//20}, Progress: {save}, total: {total},', end='')
                except:
                    print(f'\rProgress: {save}, total: {total},', end='')
                save += 1
                tempfilename = 'links.parquet'  # Change the file extension to '.parquet'
                save_data_to_disk(pd.DataFrame(data, index=[0]), tempfilename)
                tempdf = pd.DataFrame()
                save_state(save, pg)
                # linksdf = pd.concat([linksdf,pd.DataFrame(data, index=[0])], ignore_index=True)
    time.sleep(1)
    next_button = driver.find_element(By.LINK_TEXT, "Next")
    is_disabled = next_button.get_attribute('disabled') is not None
    if is_disabled:
        break
    else:
        try:
            next_button.click()
        except:
            driver.refresh()
            time.sleep(2)
            print('*-driver refreshed')
            continue                    
    pg = driver.current_url.split('india-')
    if len(pg) > 1:
        pg = (pg[1].split('?')[0])
    else:
        pg = 1
    print(end='')