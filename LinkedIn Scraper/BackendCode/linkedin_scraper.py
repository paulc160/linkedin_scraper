from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from supabase import create_client
import json
import pandas as pd
import numpy as np
import datetime
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
from datetime import timedelta

def driver_code():
    Capabilities = DesiredCapabilities.CHROME
    Capabilities["pageLoadStrategy"] = "normal"
    options = ChromeOptions()

    useragentarray = [
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.76 Mobile Safari/537.36"
    ]

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument(f"--user-data-dir=./profile{driver_num}")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("disable-infobars")
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        '/Users/paulconnolly/Desktop/ChromeDriver/chromedriver',
        options=options,
        desired_capabilities=Capabilities,
    )
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride", {"userAgent": useragentarray[0]}
    )

    options.add_argument("--disable-popup-blocking")
    #     driver.execute_script(
    #         """setTimeout(() => window.location.href="https://www.bet365.com.au", 100)"""
    #     )
    driver.get("https://www.linkedin.com/jobs/search?&location=Ireland&f_TPR=r86400&geoId=104738515&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0")
    driver.set_window_size(390, 844)
    time.sleep(1)
    return driver



def continue_in_browser(driver):
    button = driver.find_elements(By.CSS_SELECTOR, ".promo-bottom-sheet__dismiss ")
    if(len(button) > 0):
        button[0].click()
        
def accept_cookies(driver):
    cookies = driver.find_elements(By.XPATH, "/html/body/div[1]/div/section/div/div[2]/button[1]")
    if(len(cookies) > 0):
        cookies[0].click()

#infinite-scroller__show-more-button infinite-scroller__show-more-button--visible
def check_for_see_more_jobs_button(driver):
    try:
        see_more_jobs_button = driver.find_elements(By.CSS_SELECTOR,".infinite-scroller__show-more-button--visible ")
        if(len(see_more_jobs_button) > 0):
            see_more_jobs_button[0].click()
    except:
        print("No Button Found Continuing with Loader")
        
def scroll(driver, timeout):
    scroll_pause_time = timeout
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        #Check if See More Jobs Button is Visible
        check_for_see_more_jobs_button(driver)
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(scroll_pause_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        check_for_see_more_jobs_button(driver)
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height
        
def find_show_more_button(driver):
    button = driver.find_elements(By.CSS_SELECTOR, ".show-more-less-html__button ")
    if(len(button) > 0):
        button[0].click()
        
def check_description(descriptions, keyword_dict):
    for paragraph in descriptions:
        words = paragraph.split()
        
        for word in words:
            if word.lower() in keyword_dict:
                keyword_dict[word.lower()] += 1
    
    for keyword, count in keyword_dict.items():
        print(f"{keyword}: {count}")

def iterate_through_links(driver,links,companies,descriptions,job_titles,job_links):
    for i in links:
        driver.get(i)
        job_links.append(i)
        time.sleep(1)
        try:
            continue_in_browser(driver)
        except:
            print("No Continue In Browser Button Click Needed")
        time.sleep(1)
        try:
            find_show_more_button(driver)
        except:
            print("Issue with Find Show More Button")
        company_temp = driver.find_elements(By.CSS_SELECTOR, ".topcard__org-name-link ")
        description = driver.find_elements(By.CSS_SELECTOR, ".description__text ")
        title_temp = driver.find_elements(By.CSS_SELECTOR, ".top-card-layout__title ")
        for j in range(len(company_temp)):
            print(company_temp[j].text)
            try:
                companies.append(company_temp[j].text)
            except:
                companies.append("N/A")
        for k in description:
            try:
                descriptions.append(k.text)
            except:
                descriptions.append("N/A")
        for l in title_temp:
            try:
                job_titles.append(l.text)
            except:
                job_titles.append("N/A")

keyword_dict = {
    "java": 0,
    "python": 0,
    "javascript": 0,
    "sql": 0,
    "c": 0,
    "c++": 0,
    "c#": 0,
    "react": 0,
    "angular": 0,
    "azure": 0,
    "aws": 0,
    "php": 0,
    "html": 0,
    "css": 0,
    "database": 0,
    "ruby": 0,
    "typescript": 0
}
start_time = time.time()
today = date.today()
current_date = datetime.now()
current_month = current_date.month
current_year = current_date.year
API_URL = 'https://krjcvwiletbudfvdiyxt.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtyamN2d2lsZXRidWRmdmRpeXh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk3NzYyNjQsImV4cCI6MjAxNTM1MjI2NH0.pP6RLZWKt-dR-U-uBaRMwtmb9Fsh0MrPtDzpZBeIns8'
supabase = create_client(API_URL,API_KEY)
supabase
links = []
job_links = []
companies_links = []
descriptions_links = []
job_titles = []
driver_1 = driver_code()
time.sleep(2)
continue_in_browser(driver_1)
time.sleep(2)
try:
    accept_cookies(driver_1)
except:
    print("No Cookies Found Continue")
scroll(driver_1, 7)
companies = driver_1.find_elements(By.CSS_SELECTOR, ".base-search-card__subtitle ")
job_titles_links = driver_1.find_elements(By.CSS_SELECTOR, ".base-card__full-link ")
print("Number of Companies ", len(companies))
print("Number of Job Titles and Links", len(job_titles_links))
descriptions_check = []
for i in range(len(job_titles_links)):
    links.append(job_titles_links[i].get_attribute('href'))
print("Finished Loading Jobs, Number of Links Scraped: ", len(job_titles_links))
with tqdm(total=len(links)) as pbar:
    for i in links:  
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        company = soup.find_all('a', class_='topcard__org-name-link')
        description = soup.find_all('div', class_='show-more-less-html__markup')
        job_title = soup.find_all('h1', class_='top-card-layout__title')
        for j in range(len(company)):
            id_temp = job_title[j].text + company[j].text + str(current_month) + str(current_year)
            id_no_whitespace = id_temp.replace(" ", "")
            cleaned_id = ''.join(e for e in id_no_whitespace if e.isalnum()).lower()
            try:
                data,count = supabase.table('LinkedIN_Job').insert({"Link":i,
                                                                    "Job_ID": cleaned_id,
                                                               "Job_Title":job_title[j].text,
                                                               "Company":company[j].text,
                                                               "Description":description[j].text,
                                                               "Date":str(today)}).execute()
                print("Job Successfully Posted to DB")
                descriptions_check.append(description[j].text)

            except Exception as e:
                print(e)
        pbar.update(1)
check_description(descriptions_check, keyword_dict)
twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
for keyword, count in keyword_dict.items():
    try:
        current_timestamp = datetime.utcnow()
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        data = supabase.table('Daily_Keywords').select('Count','Date').eq('Keyword',keyword).gte('Date', twenty_four_hours_ago).execute()
        if(len(data.data) > 0):
            current_count = data.data[0]['Count'] + count
            update_data = supabase.table('Daily_Keywords').update({"Count":current_count}).eq('Keyword',keyword).eq('Date',data.data[0]['Date']).execute()
            print("Keyword: " + keyword + " Updated to Count: " + str(current_count))
        else:
            insert_data,count = supabase.table('Daily_Keywords').insert({"Date":str(current_timestamp),"Keyword":keyword,
                                                              "Count":count}).execute()
            print("New Keyword " + keyword + " Inserted with Count " + count)
    except Exception as e:
        print(e)
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to complete the function: {time_taken} seconds")
driver_1.quit()