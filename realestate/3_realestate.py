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
from selenium.common.exceptions import NoSuchElementException
import gc
import time
import pytz
import datetime
import logging
from tqdm import tqdm
import traceback
import sys

df = pd.read_csv('suburbs.csv')

df['suburb'] = df['0'].apply(lambda x : '+'.join(x.split('-')[:-2]))
len(df['suburb'])

def driver_setup():# Assigning a Headless Firefox Driver
  options = webdriver.FirefoxOptions()
  options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'  # Path to Chrome executable
  options.add_argument('E:/Programs/geckodriver.exe')
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Firefox(options=options)
  return driver

def save_data_to_disk(data, filename):
    if os.path.isfile(filename):
        existing_df = pd.read_csv(filename)
        data = pd.concat([existing_df, data], ignore_index=True)
        os.remove(filename)
        data.to_csv(filename,index=False)
    else:
        data.to_csv(filename, mode='w', header=True, index=False)
        
driver = driver_setup()

fileind = 3

with open('real_comp_'+str(fileind)+'.txt', 'r') as file:
    st_rng = int(file.read())

totlis = [10586, 15879]
# st_rng = totlis[0] #-------------------
end_rng = totlis[1]
total_rng = abs(end_rng - st_rng)

pbar = tqdm(total=total_rng, desc='Searching', unit='query')

for sub in range(st_rng , end_rng):
  pbar.update(1)

  driver.get('https://www.realestateinvestar.com.au/Property/'+str(df['suburb'][sub]))
  text_dict = {}
  try:

    text = driver.find_element(By.CLASS_NAME, "pull-left").text

    details = {
        'string_from_domain' : df['0'][sub],
        'string_from_realestateinvestor' : text
    }

    text_dict.update(details)
    details = {}
  #------------------------------------------------------------------------------------------------------

    div_elements = driver.find_elements(By.CSS_SELECTOR, ".row.text-center > .col-md-3")

    for div in div_elements:
        p_elements = div.find_elements(By.TAG_NAME, "p")
        if len(p_elements) == 2:
            key = p_elements[1].text
            value = p_elements[0].text
            text_dict[key] = value
    text_dict.popitem()

    #------------------------------------------------------------------------------------------------------
    try:

      button_element = driver.find_element(By.XPATH, "//li/a[@aria-controls='median']")
      button_element.click()
    except:
      driver.get('https://www.realestateinvestar.com.au/Property/'+str(df['suburb'][sub]))
      button_element = driver.find_element(By.XPATH, "//li/a[@aria-controls='median']")
      button_element.click()

    median_table = driver.find_element(By.ID, "median")
    table_data = pd.read_html(median_table.get_attribute("outerHTML"))[0]

    table_dict = {}
    for row in range(1, len(table_data)):
        row_name = table_data.iloc[row][0]
        for column in range(1, len(table_data.columns)):
            column_name = table_data.iloc[0][column]
            value = table_data.iloc[row][column]
            table_dict[f"{row_name}_{column_name}"] = value

    text_dict.update(table_dict)
    table_dict = {}
    #------------------------------------------------------------------------------------------------------
    try:
      button_element = driver.find_element(By.XPATH, "//li/a[@aria-controls='rental']")
      button_element.click()
    except:
      driver.get('https://www.realestateinvestar.com.au/Property/'+str(df['suburb'][sub]))
      button_element = driver.find_element(By.XPATH, "//li/a[@aria-controls='rental']")
      button_element.click()

    median_table = driver.find_element(By.ID, "rental")
    table_data = pd.read_html(median_table.get_attribute("outerHTML"))[0]

    for row in range(1, len(table_data)):
        row_name = table_data.iloc[row][0]
        for column in range(1, len(table_data.columns)):
            column_name = table_data.iloc[0][column]
            value = table_data.iloc[row][column]
            table_dict[f"{row_name}_{column_name}"] = value

    text_dict.update(table_dict)
    table_dict = {}
    #------------------------------------------------------------------------------------------------------
    button_element = driver.find_element(By.XPATH, "//li/a[@aria-controls='sales']")
    button_element.click()

    median_table = driver.find_element(By.ID, "sales")
    table_data = pd.read_html(median_table.get_attribute("outerHTML"))[0]

    for row in range(1, len(table_data)):
        row_name = table_data.iloc[row][0]
        for column in range(1, len(table_data.columns)):
            column_name = table_data.iloc[0][column]
            value = table_data.iloc[row][column]
            table_dict[f"{row_name}_{column_name}"] = value

    text_dict.update(table_dict)
    table_dict = {}

    #------------------------------------------------------------------------------------------------------

    with open('real_comp_'+str(fileind)+'.txt', 'w') as file:
        file.write(str(sub))
    
    
    if text_dict != {}:

      tempdf = pd.DataFrame(text_dict, index=[0])
      tempfilename = 'realestateinvestar'+str(fileind)+'.csv'

      save_data_to_disk(tempdf, tempfilename)
      tempdf = pd.DataFrame()
      
  except NoSuchElementException:
    # Handle the 404 error
    None