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


def parse_rows(table_rows):
    parsed_rows = []

    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")

        none_count = 0

        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1

        if none_count < 4:
            parsed_rows.append(parsed_row)

    return pd.DataFrame(parsed_rows)


def clean_data(df):
    df = df.set_index(0)  # Set the index to the first column: 'Period Ending'.
    df = df.transpose()  # Transpose the DataFrame, so that our header contains the account names

    # Rename the "Breakdown" column to "Date"
    cols = list(df.columns)
    cols[0] = 'Date'
    df = df.set_axis(cols, axis='columns', inplace=False)

    numeric_columns = list(df.columns)[1::]  # Take all columns, except the first (which is the 'Date' column)

    for column_index in range(1, len(df.columns)):  # Take all columns, except the first (which is the 'Date' column)
        df.iloc[:, column_index] = df.iloc[:, column_index].str.replace(',', '')  # Remove the thousands separator
        df.iloc[:, column_index] = df.iloc[:, column_index].astype(np.float64)  # Convert the column to float64

    return df


def scrape_table_second_attempt(url):
    # Fetch the page that we're going to parse
    page = get_page(url);

    # Parse the page with LXML, so that we can start doing some XPATH queries
    # to extract the data that we want
    tree = html.fromstring(page.content)

    # Fetch all div elements which have class 'D(tbr)'
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

    # Ensure that some table rows are found; if none are found, then it's possible
    # that Yahoo Finance has changed their page layout, or have detected
    # that you're scraping the page.

    assert len(table_rows) > 0
    df = parse_rows(table_rows)
    df = clean_data(df)
    return df


def scrape_table_first_attempt(baseurl, tickerslist, tabslist):
    '''
    :param baseurl: url to make a request (string)
    :param tickerslist: list of ticker that need to scrap into yahoo finance (list of string)
    :param tabslist: list of features inside the page that need to scrap (list of string)
    :return: Data Frame with the requested output
    '''
    # Set the current date and time
    scrape_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = []
    for ticker in tickerslist:
        flag = 0
        # define list to store column name and scraped values
        column_name = []
        value = []
        for tab in tabslist:
            # Set the URL for the current ticker
            url = baseurl.format(ticker, tab, ticker)
            print(url)

            # Make a request to the URL
            response = get_page(url)

            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # scrape date
            scrape_date = datetime.datetime.now().strftime('%m-%d-%Y')
            # print(scrape_date)

            # End date
            '''
            if (tab == "financials") and (flag == 0):
                try:
                    flag = 1
                    table_EndDate = soup.find_all("div", class_="Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)")
                    table_EndDate = table_EndDate[0].text
                    #print(table_EndDate)
                except:
                    print("An exception occurred")
            '''
            enddate = scrape_date
            table_field = soup.find_all("div", class_="D(tbr) fi-row Bgc($hoverBgColor):h")
            # Find the table containing the financial data
            for i in table_field:
                aux = 0
                for j in i:
                    if aux == 0:
                        column_name.append(j.text)
                    if aux == 1:
                        value.append(j.text)
                    aux += 1
        column_name.append("Ticker")
        value.append(ticker)
        #
        column_name.append("End Date")
        value.append(enddate)
        # value.append(table_EndDate.replace("/", "-"))
        #
        column_name.append("Scrape Date")
        value.append(scrape_date)
        #
        # Create a DataFrame with custom column labels
        temp_list = [value]
        df = pd.DataFrame(temp_list, columns=column_name)
        data.append(df)
    return pd.concat([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]])


if __name__ == "__main__":
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('ticker', help='')
    # args = argparser.parse_args()
    # ticker = args.ticker
    # Set the tickers and fields to be scrapped
    tickers = ["JNJ", "BRK.B", "JPM", "MMM", "ABBV", "DIS", "T", "PG", "LOW", "CI"]
    fields = ["Operating Income", "Net Income From Continuing Operations", "Retained Earnings", "Change In Cash",
              "Net Borrowings"]
    tabs = ["financials", "balance-sheet", "cash-flow"]

    base_url = "https://finance.yahoo.com/quote/{}/{}?p={}"

    print(scrape_table_first_attempt(base_url, tickers, tabs))