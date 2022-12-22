
from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import datetime
def get_page(url):
    '''
    Set up the request headers that we're going to use, to simulate a request by the Chrome browser.

    Args:
        - url of the page (string)

    Return:
        - object requested using requests library
    '''
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
    return requests.get(url, headers=headers)

def test_scrape_table_first_attempt():
    baseurl = "https://finance.yahoo.com/quote/{}/{}?p={}"
    tickerslist = ["JNJ", "BRK.B"]
    tabslist = ["financials", "balance-sheet", "cash-flow"]
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
            url = baseurl.format(ticker, tab, ticker)

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

    assert type(df) == type(pd.DataFrame())

