import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def driver_setup():# Assigning a Headless Firefox Driver
  options = webdriver.ChromeOptions()
  options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'  # Path to Chrome executable
  options.add_argument('chromedriver.exe')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=options)
  return driver


driver = driver_setup()
driver.implicitly_wait(30)

driver.get("https://www.linkedin.com/authwall?trk=qf&original_referer=&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2F")
wait = WebDriverWait(driver, 10)

Sign_in_button = driver.find_element(By.XPATH, "/html/body/div/main/div/form/p/button").click()
wait = WebDriverWait(driver, 10)

email_phone = driver.find_element(By.XPATH, '//*[@id="session_key"]')
password = driver.find_element(By.XPATH, '//*[@id="session_password"]')
email_phone.send_keys("r.panneerselvam@firebird.net.in")
password.send_keys("Mk90473@yahoo.com")

submit_button = driver.find_element(By.XPATH, "/html/body/div/main/div/div/form[1]/div[2]/button")
submit_button.click()

wait = WebDriverWait(driver, 10)

url = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22102713980%22%5D&keywords=founder&origin=FACETED_SEARCH&sid=OIJ'
driver.get(url)

links = []

wait = WebDriverWait(driver, 10)

li_elements = driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")

# Iterate over the li elements and extract the link
for li in li_elements:
    link_element = li.find_element(By.TAG_NAME, "a")
    link = link_element.get_attribute("href")
    links.append(link)
    print(link) 
# for lin in links:
driver.get(links[0])
#------------------------------------------------------------------------------------------------------

name = h1_element = driver.find_element(By.CLASS_NAME, "text-heading-xlarge").text
location = span_element = driver.find_element(By.CLASS_NAME, "text-body-small inline t-black--light break-words").text
h2_elements = driver.find_element(By.CLASS_NAME, "pvs-header__title").text
print(name,location)  
input('')





