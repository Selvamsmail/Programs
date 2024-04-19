import pandas as pd
import gdown
import re
import requests
from bs4 import BeautifulSoup
import shutil
from requests_html import HTMLSession
import asyncio
from requests_html import AsyncHTMLSession
import json
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import gc
import time
import pytz
import datetime
import logging
from tqdm import tqdm
import traceback
from saver import save_data_to_disk
from spliterlist import splits

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
        
ranlis = [str(i) + '-' + str(i+30) for i in range(40000) if i % 400 == 0]

def in_ranlis(number):
    for ran in ranlis:
        start, end = map(int, ran.split('-'))
        if start <= number <= end:
            return True
    return False

linksdf = pd.read_parquet('links.parquet')

print(linksdf.shape)
linksdf.drop_duplicates(inplace=True)
linksdf.dropna(inplace=True)
linksdf.reset_index(drop=True, inplace=True)
print(linksdf.shape)

driver = driver_setup()

def save_state(strng):
    state = {
        "strng": strng,
    }
    with open("extractor3state.json", "w") as json_file:
        json.dump(state, json_file)

def load_state():
    try:
        with open("extractor3state.json", "r") as json_file:
            state = json.load(json_file)
            strng = state["strng"]
    except FileNotFoundError:
        strng = splits[2][0]
    return strng

strng = load_state()
    
while strng < len(linksdf):
    end_rng = splits[2][1]
    for inde, row in tqdm(linksdf.iloc[strng:end_rng].iterrows(), total=len(linksdf.iloc[strng:end_rng]), desc="Processing Rows"):
        driver.get(row['link'])
        time.sleep(1.5)
        try:
            if driver.find_element(By.CSS_SELECTOR,'.styles_exp-alert-message__nUbfX.styles_error__IhAVp'):
                continue
        except:
            pass
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.styles_key-skill__GIPn_ > div > a, .getJobKeySkillsSection.key-skill a')))
        except:
            print("...")
            driver.quit()
            driver = driver_setup()
            driver.get(row['link'])
            time.sleep(4)
        try:
            job_title = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            job_title = "N/A"
        try:
            company_name = driver.find_element(By.CSS_SELECTOR, '.styles_jd-header-comp-name__MvqAI > a').text
        except:
            company_name = "N/A"

        try:
            experience = driver.find_element(By.CSS_SELECTOR, '.styles_jhc__exp__k_giM, .slide-meta.getExperience > span').text
        except:
            experience = "N/A"

        try:
            salary = driver.find_element(By.CSS_SELECTOR, '.styles_jhc__salary__jdfEC, .job-meta.slide-meta-sal').text
        except:
            salary = "N/A"
        try:
            location = driver.find_element(By.CSS_SELECTOR, '.styles_jhc__loc___Du2H, .row.nomb.getCityLinks').text
        except:
            location = "N/A"

        try:
            description = driver.find_element(By.CSS_SELECTOR, '.styles_job-desc-container__txpYf > div > div , .nConfig_textblock').text
        except:
            description = "N/A"

        try:
            li_elements = driver.find_elements(By.CSS_SELECTOR, '.styles_key-skill__GIPn_ > div > a, .getJobKeySkillsSection.key-skill a')
            l = [i.text for i in li_elements]
        except:
            l = []

        try:
            posted_on = driver.find_element(By.CSS_SELECTOR, '.styles_jhc__stat__PgY67 > span, .sumFoot > span').text
        except:
            posted_on = "N/A"

        current_date = datetime.datetime.now().date()
        data = {
            'job_title':job_title,
            'company_name':company_name,
            'experience':experience,
            'salary':salary,
            'location':location,
            'description':description,
            'posted_on':posted_on,
            'current_date':current_date,
            'link':row['link'],
            'sal_range': row['sal_range']
        }
        for i in range(len(l)):
            data['skill'+str(i+1)]=l[i]
        try:
            lable_span = driver.find_elements(By.CSS_SELECTOR, '.styles_job-desc-container__txpYf > div > div.styles_other-details__oEN4O > div')    
            for lable in lable_span:
                labl = lable.find_element(By.CSS_SELECTOR, 'label').text
                ans = lable.find_element(By.CSS_SELECTOR, 'span').text
                data[labl] = ans
        except:
            lable_span = driver.find_elements(By.CSS_SELECTOR, '.getJobDescriptionOtherDetails.JD.av_textblock_section.jDisc.mt25 p')
            for lable in lable_span:
                labl = lable.find_element(By.CSS_SELECTOR, 'em').text
                ans = lable.find_element(By.CSS_SELECTOR, 'span').text
                data[labl] = ans
        if data != {}:
            tempdf = pd.DataFrame(data, index=[0])
            tempdf['current_date'] = tempdf['current_date'].astype(str)
            tempfilename = 'Naukri_raw3.parquet'  # Change the file extension to '.parquet'
            save_data_to_disk(tempdf, tempfilename)
            tempdf = pd.DataFrame()
            save_state(strng)
        strng = inde + 1