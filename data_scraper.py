#!/usr/bin/env python3
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time


nse_20_url = 'https://www.investing.com/indices/kenya-nse-20-historical-data'
nse_url = 'https://www.nse.co.ke/'
start_date = "01/01/2012"
nse_20_data = []
list_item = []

def scrape_investing_dot_com(url, start_date):
    # Path to chrome driver if it isn't in Windows PATH
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    sbox = driver.find_element_by_class_name("historicDate")
    sbox.click()
    # .clear() returns a NoneType
    sbox = driver.find_element_by_id("startDate").clear()
    # Fetch the element again
    sbox = driver.find_element_by_id("startDate")
    sbox.send_keys(start_date)
    sbox = driver.find_element_by_id("startDate")
    sbox.send_keys(Keys.ENTER)

    time.sleep(5)
    nse_20_soup = BeautifulSoup(driver.page_source, 'lxml')
    date_pick = nse_20_soup.find('div', {'class': 'dateRange inlineblock datePickerBinder arial_11 lightgrayFont'}).text
    hist_data = nse_20_soup.find('section', {'id': 'leftColumn'})
    tables = hist_data.find('table', {'id': 'curr_table'})
    # Remove the newlines 
    daily_data = [[item.text.strip().replace('\n', ',')] for item in tables.find_all('tr')]
    # Split on the comma
    for index, item in enumerate(daily_data):
        daily_data[index] = daily_data[index][0].split(',')

    # Clean the data
    for list_item in daily_data:
        # for one list item
        for index, item in enumerate(list_item):
            steppr = index + 1
            if steppr < len(list_item) and not index % 2:
                if index == 0:
                    nse_20_data.append(list_item[index].strip() + ' ' + list_item[steppr].strip())
                else:
                    nse_20_data.append(list_item[index].strip() + ',' + list_item[steppr].strip())
            elif steppr == 11:
                nse_20_data.append(list_item[index])
    driver.close()
    driver.quit()
    return nse_20_data

def scrape_nse_dot_com(url):
    page = requests.get(url, verify=False, stream=True)
    soup = BeautifulSoup(page.text, 'lxml')
    tickers = soup.find('div', {'class': 'modcontent'}).text.replace(u'\xa0', u'').split('|')
    for ticker in tickers:
    	return ticker

if __name__ == "__main__":
    scrape = scrape_investing_dot_com(nse_20_url, start_date)
