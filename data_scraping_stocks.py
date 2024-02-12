from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

#Scrape_Dell_stock_data_from_yahoo_finance
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"}
url1 = "https://finance.yahoo.com/quote/DELL/history?period1=1549238400&period2=1707004800&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true"
page1 = requests.get(url1, headers=headers)
info1 = BeautifulSoup(page1.content, "html.parser" )
list(info1.children)

dell_stock_table = info1.find("table", attrs={"class": "W(100%) M(0)"})
dell_stock_table

dell_stock_data = []

for row in dell_stock_table.find_all("tr")[1:]:
    columns = row.find_all("td")
    if len(columns) >= 7:
        row_data = {"Date": columns[0].text,
               "Open": columns[1].text,
               "High": columns[2].text,
               "Low": columns[3].text,
               "Close": columns[4].text,
               "Volume": columns[6].text}
        dell_stock_data.append(row_data)
        
dell_df = pd.DataFrame(dell_stock_data)
dell_df.to_csv("dell_stock.csv",index=False)

#Scrape_S&P500index_data_from_yahoo_finance
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"}
url2 = "https://finance.yahoo.com/quote/%5ESPX/history?period1=1549238400&period2=1706918400&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true"
page2 = requests.get(url2, headers=headers)
info2 = BeautifulSoup(page2.content, "html.parser" )
list(info2.children)

snp500_stock_table = info2.find("table", attrs={"class": "W(100%) M(0)"})
snp500_stock_table

import pandas as pd

snp500_stock_data = []

for row in snp500_stock_table.find_all("tr")[1:]:
    columns = row.find_all("td")
    if len(columns) >= 7:
        row_data = {"Date": columns[0].text,
               "Open": columns[1].text,
               "High": columns[2].text,
               "Low": columns[3].text,
               "Close": columns[4].text,
               "Volume": columns[6].text}
        snp500_stock_data.append(row_data)
        
snp500_df = pd.DataFrame(snp500_stock_data)
snp500_df.to_csv("S&P500_index.csv",index=False)

#Combine_stock_data
dell_df = pd.read_csv("dell_stock.csv",  parse_dates=["Date"])
snp500_df = pd.read_csv("S&P500_index.csv", parse_dates=["Date"])
combine_df = pd.merge(dell_df, snp500_df, on="Date", suffixes=("DELL","S&P500"))
combine_df.to_csv("combined_stock_data.csv", index=False)
