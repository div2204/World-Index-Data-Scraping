from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd

# Base URL and headers for requests
BASE_URL = 'https://finance.yahoo.com/quote/%5E{}'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

# Function to get data for a specific index
def get_data(index):
    url = BASE_URL.format(index)
    try:
        page = requests.get(url, headers=HEADERS)
        page.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data for {index}: {e}")
        return ['N/A', 'N/A']

    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        price = soup.find(class_='livePrice svelte-mgkamr').text.strip()
    except AttributeError:
        price = 'N/A'
    try:
        change = soup.find(class_='priceChange svelte-mgkamr').text.strip()
    except AttributeError:
        change = 'N/A'
    return [price, change]

# Initialize DataFrame
df2 = pd.DataFrame(columns=['Date', 'Index', 'Price (USD)', 'Change'])

# List of indices to gather data for
indices = ['GSPC', 'DJI', 'IXIC', 'NYA', 'XAX', 'BUK100P', 'RUT', 'VIX', 'FTSE', 'STOXX50E', 'XDB', 'XDE', 'XDN', 'XDA']

# Function to gather data for all indices
def gather_data():
    for index in indices:
        today = datetime.date.today()
        data = get_data(index)
        data.insert(0, index)
        data.insert(0, today)
        df2.loc[len(df2)] = data

# Gather data and save to CSV
gather_data()
df2.to_csv(r"C:\\Users\\hp\\Desktop\\Web Scraping\\index_data.csv", index=False)
print("Data gathered and saved.")
