from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"}
url = "https://finance.yahoo.com/quote/DELL/history?period1=1549238400&period2=1707004800&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true"
page = requests.get(url, headers=headers)
info = BeautifulSoup(page.content, "html.parser" )
list(info.children)

stock_table = info.find("table", attrs={"class": "W(100%) M(0)"})
stock_table

stock_data = []

for row in stock_table.find_all("tr")[1:]:
    columns = row.find_all("td")
    if len(columns) >= 7:
        row_data = {"Date": columns[0].text,
               "Open": columns[1].text,
               "High": columns[2].text,
               "Low": columns[3].text,
               "Close": columns[4].text,
               "Volume": columns[6].text}
        stock_data.append(row_data)
        
df = pd.DataFrame(stock_data)
df.to_csv("dell_stock.csv",index=False)