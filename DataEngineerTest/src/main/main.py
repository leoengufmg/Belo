from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import datetime

from selenium import *
from selenium import webdriver

import logging
# creating logger
logger = logging.getLogger(__name__)
#logger.debug('This is a debug message')
#logger.info('This is an info message')
#logger.warning('This is a warning message')
#logger.error('This is an error message')
#logger.critical('This is a critical message')

# formatter of logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# handler
handler = logging.FileHandler('app.log')
handler.setFormatter(formatter)

# add handler
logger.addHandler(handler)


def get_page(url):
    '''
    Set up the request headers that we're going to use, to simulate a request by the Chrome browser.

    Args:
        - url of the page (string)

    Return:
        - object requested using requests library
    '''
    logger.info('Starting the execution get_page...')
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'DNT': '1',  # Do Not Track Request Header
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    logger.info('Finishing the execution get_page...')
    return requests.get(url, headers=headers)



def scrape_table_first_attempt(baseurl, tickerslist, tabslist):
    '''
    :param baseurl: url to make a request (string)
    :param tickerslist: list of ticker that need to scrap into yahoo finance (list of string)
    :param tabslist: list of features inside the page that need to scrap (list of string)
    :return: Data Frame with the requested output
    '''
    logger.info('Starting the execution scrape_table_first_attempt...')
    # Set the current date and time
    scrape_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Defining column name
    column_name = ["Ticker", "Field", "Value", "End Date", "Scrape Date"]
    data = []
    for ticker in tickerslist:
        flag = 0
        # define list to store column name and scraped values
        for tab in tabslist:
            # Set the URL for the current ticker
            url = base_url.format(ticker, tab, ticker)

            # Make a request to the URL
            response = get_page(url)
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")
            # scrape date
            scrape_date = datetime.datetime.now().strftime('%m-%d-%Y')

            if (tab == "financials") and (flag == 0):
                try:
                    flag = 1
                    enddate = soup.find_all("div", class_="Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)")
                    enddate = enddate[0].text.replace("/", "-")
                except:
                    #print("An exception occurred")
                    pass
            table_field = soup.find_all("div", class_="D(tbr) fi-row Bgc($hoverBgColor):h")
            # Find the table containing the financial data
            for i in table_field:
                value = list()
                # Append ticker
                value.append(ticker)
                aux = 0
                for j in i:
                    if aux == 0:
                        # append Field
                        value.append(j.text)
                    if aux == 1:
                        # append value
                        value.append(j.text)
                    aux += 1
                # Append End Date
                value.append(enddate)

                # Append Scrape Date
                value.append(scrape_date)

                # Create a DataFrame with custom column labels
                data.append(value)
    df = pd.DataFrame(data, columns=column_name)
    logger.info('Finishing the execution scrape_table_first_attempt...')
    return df


def scrap_ticker(ticker, field, headers, driver):
    xpath = {
        "OperatingIncome" : {
            "base_url" : "https://finance.yahoo.com/quote/"+ticker+"/financials?p="+ticker,
            "xpath_name": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[5]/div[1]/div[1]/div[1]',
            "xpath_value": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[5]/div[1]/div[2]/span'
        },
        "NetIncomeContinuousOperations" : {
            "base_url" : "https://finance.yahoo.com/quote/"+ticker+"/cash-flow?p="+ticker,
            "xpath_name": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/span',
            "xpath_value": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/span'
        },
        "RetainedEarnings" : {
            "base_url" : "https://finance.yahoo.com/quote/"+ticker+"/balance-sheet?p="+ticker,
            "xpath_name": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/span',
            "xpath_value": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[1]/div[2]/span'
        },
        "ChangesCash" : {
            "base_url" : "https://finance.yahoo.com/quote/"+ticker+"/cash-flow?p="+ticker,
            "xpath_name": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div[1]/div[1]/div[1]/span',
            "xpath_value": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div[1]/div[2]/span'
        },
        "NetBorrowings" : {
            "base_url" : "https://finance.yahoo.com/quote/"+ticker+"/balance-sheet?p="+ticker,
            "xpath_name": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[11]/div[1]/div[1]/div[1]/span',
            "xpath_value": '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[11]/div[1]/div[2]/span'
        }
    }
    value = list()
    # append ticker
    print(ticker)
    value.append(ticker)
    # Set the URL for the current ticker
    try:
        url = xpath[field]["base_url"]
        print(url)
        driver.get(url)
        driver.implicitly_wait(15)
        # append Field
        driver.find_element("xpath", '//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button/div/span').click()
        tmp_value = driver.find_element("xpath", xpath[field]['xpath_name']).text
    except:
        print("Find error to scrap name!")
        tmp_value = "-"
    value.append(tmp_value)
    print(tmp_value)
    # append Value
    try:
        driver.implicitly_wait(5)
        tmp_value = driver.find_element("xpath", xpath[field]['xpath_value']).text
    except:
        tmp_value = "-"
    value.append(tmp_value)
    print(tmp_value)
    # append End Date
    try:
        driver.implicitly_wait(5)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        table_EndDate = soup.find_all("div", class_="Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)")
        table_EndDate = table_EndDate[0].text
        #print(table_EndDate)
    except:
        print("An exception occurred")
        table_EndDate = "-"
    value.append(table_EndDate)
    # append scrape_date
    scrape_date = datetime.datetime.now().strftime('%m-%d-%Y')
    value.append(scrape_date)
    print(scrape_date)
    return value


def scrape_table_second_attempt():
    driver = webdriver.Chrome()
    driver.get("https://finance.yahoo.com/quote/JNJ/financials?p=JNJ")
    driver.find_element("xpath", '//*[@id="myLightboxContainer"]/section/button[1]').click()
    # Set the tickers and fields to be scrapped
    tickers = ["JNJ", "BRK.B", "JPM", "MMM", "ABBV", "DIS", "T", "PG", "LOW", "CI"]
    fields = ["OperatingIncome", "NetIncomeContinuousOperations", "RetainedEarnings", "ChangesCash", "NetBorrowings"]

    tabs = ["financials", "balance-sheet", "cash-flow"]

    # Set the period to be last 4 quarters
    period = "last4quarters"

    # Set the base URL for the Yahoo Finance webpage
    base_url = "https://finance.yahoo.com/quote/{}/{}?p={}"

    # Column name
    column_name = ["Ticker", "Field", "Value", "End Date", "Scrape Date"]

    # Create an empty list to store the data
    data = []

    # Set the current date and time
    scrape_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Set header to use request.get(url)
    headers = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', \
                'Accept-Language': 'en-US, en;q=0.5'})

    for ticker in tickers:
        # define list to store column name and scraped values
        for field in fields:
            value = list()
            try:
                value = scrap_ticker(ticker, field, headers, driver)
                data.append(value)
                print()
            except:
                print("Find error...")
                print()
    return pd.DataFrame(data, columns=column_name)
    driver.close()
if __name__ == "__main__":

    logger.info('Starting Main program!')
    tickers = ["JNJ", "BRK.B", "JPM", "MMM", "ABBV", "DIS", "T", "PG", "LOW", "CI"]
    fields = ["Operating Income", "Net Income From Continuing Operations", "Retained Earnings", "Change In Cash",
              "Net Borrowings"]
    tabs = ["financials", "balance-sheet", "cash-flow"]

    base_url = "https://finance.yahoo.com/quote/{}/{}?p={}"

    df_result_first = (scrape_table_first_attempt(base_url, tickers, tabs))
    date = datetime.date.today().strftime('%Y-%m-%d')
    writer = pd.ExcelWriter('Yahoo-Finance-Scrape-First-' + date + '.xlsx')
    df_result_first.to_excel(writer)
    writer.save()
    del writer
    #
    df_result_second = scrape_table_second_attempt()
    #writer = pd.ExcelWriter('Yahoo-Finance-Scrape-Second-' + date + '.xlsx')
    df_result_second.to_csv('Yahoo-Finance-Scrape-Second-' + date + '.csv',index=False)
    logger.info('Finishing  Main program!')
