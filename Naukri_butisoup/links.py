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

def save_state(save, strng, pg):
    state = {
        "save": save,
        "strng": strng,
        "pg": pg
    }
    with open("Link_variables.json", "w") as json_file:
        json.dump(state, json_file)

def load_state():
    try:
        with open("Link_variables.json", "r") as json_file:
            state = json.load(json_file)
            save = state["save"]
            strng = state["strng"]
            pg = state["pg"]
    except FileNotFoundError:
        # Default values if file doesn't exist
        save = 0
        strng = 0 #filtrange
        pg = 0
    return save, strng, pg


driver = driver_setup()

save, strng, pg = load_state()

pageinfoserch = 1
rangesal = ['3to6', '6to10', '10to15', '15to25', '25to50', '50to75', '75to100', '100to500', '0to3']
for filt in range(strng,len((rangesal))):
    strng = filt 
    if pageinfoserch == 1:
        driver.get('https://www.naukri.com/jobs-in-india-'+str(pg)+'?jobAge=15&ctcFilter='+rangesal[filt])# continue run page 
        pageinfoserch = 0 
    else:
        driver.get('https://www.naukri.com/jobs-in-india?jobAge=15&ctcFilter='+rangesal[filt]) # run page from start
    time.sleep(3)
    total = int(driver.find_element(By.CLASS_NAME, 'styles_h1-wrapper__mHVA1').text.split('of')[-1].split('\n')[0].strip())
    ################################
    sub_save = 0
    ################################
    while True:    
        time.sleep(4)
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
        except NoSuchElementException:
            print("...closing driver")
            driver.quit()
            driver = driver_setup()
            driver.get('https://www.naukri.com/jobs-in-india-'+str(pg)+'?jobAge=15&ctcFilter='+rangesal[filt])# continue run page 
            time.sleep(3)
        
        job_articles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cust-job-tuple')))
        for job_element in job_articles:
            data = {}
            data['sal_range'] = rangesal[filt] 
            try:
                data['link'] = job_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                continue
            if data != {}:
                try:
                    print(f'\rpg: {pg} / {total//20}, Progress: {save} filtlevel_save: {sub_save}, total: {total}, filtlevel: {filt}', end='')
                except:
                    print(f'\rProgress: {save}, filtlevel_save: {sub_save}, total: {total}, filtlevel: {filt}', end='')
                save += 1
                sub_save +=1
                tempfilename = 'links.parquet'  # Change the file extension to '.parquet'
                save_data_to_disk(pd.DataFrame(data, index=[0]), tempfilename)
                tempdf = pd.DataFrame()
                save_state(save, strng, pg)
                # linksdf = pd.concat([linksdf,pd.DataFrame(data, index=[0])], ignore_index=True)
        time.sleep(1)
        next_button = driver.find_element(By.LINK_TEXT, "Next")
        is_disabled = next_button.get_attribute('disabled') is not None
        if is_disabled or sub_save > 40000:
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