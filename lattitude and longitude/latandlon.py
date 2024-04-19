import pandas as pd
import gdown
import re
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gc
import time
import pytz
import datetime
import logging
from tqdm import tqdm
import traceback
import sys

def driver_setup():# Assigning a Headless Firefox Driver
  options = webdriver.ChromeOptions()
  options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'  # Path to Chrome executable
  options.add_argument('chromedriver.exe')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=options)
  return driver

def save_data_to_disk(data, filename):
    if os.path.isfile(filename):
        existing_df = pd.read_csv(filename)
        data = pd.concat([existing_df, data], ignore_index=True)
        os.remove(filename)
        data.to_csv(filename,index=False)
    else:
        data.to_csv(filename, mode='w', header=True, index=False)


gdown.download(id = '1DuT3nnIouLKuRFbGo5lqcQwKTTb5GM8r')
df = pd.read_csv('suburbs.csv')


driver = driver_setup()
driver.implicitly_wait(5)
driver.get('https://www.google.com/maps/')

totlis = [5290, 6348]
st_rng = totlis[0]
end_rng = totlis[1]
total_rng = abs(end_rng - st_rng)

pbar = tqdm(total=total_rng, desc='Searching', unit='query')

for sub in range(st_rng, end_rng):

    pbar.update(1)

    driver.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys(df['0'][sub])
    driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').click()
    time.sleep(3)

    current_url = driver.current_url

    pattern = r'(-\d+\.\d+!4d\d+\.\d+!)'
    match = re.search(pattern, current_url)

    if match:
        desired_portion = match.group(1)
        lat_and_long=desired_portion[:-1].replace('!4d',',')

        main ={
            'Search_string': df['0'][sub],
            'lat_and_lon' : lat_and_long
        }

        tempdf = pd.DataFrame(main, index=[0])
        tempfilename = 'Lat_and_lon_1.csv'
        save_data_to_disk(tempdf, tempfilename)
        tempdf = pd.DataFrame()

    driver.find_element(By.XPATH, '//*[@id="searchbox"]/div[2]/button').click()