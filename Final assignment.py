import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True),
                             y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True),
                             y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
                      height=900,
                      title=stock,
                      xaxis_rangeslider_visible=True)
    fig.show()


# Working with Tesla data
tesla = yf.Ticker('TSLA')
tesla_history = tesla.history(period='max')
tesla_data = pd.DataFrame(tesla_history)
tesla_data.reset_index(inplace=True)
print(tesla_data.tail())

# Working with Tesla revenue
url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork23455606-2022-01-01'
request = requests.get(url).text
soup = BeautifulSoup(request, 'html5lib')
quarterly_revenue_table = soup.find_all('div', class_='col-xs-6')[1]
quarterly_revenue_data = quarterly_revenue_table.find('tbody').find_all('tr')
quarterly_revenue_df = pd.DataFrame(columns=['Date', 'Revenue'])
for data in quarterly_revenue_data:
    info = data.find_all('td')
    date = info[0].text
    revenue = info[1].text
    line = {'Date': [date], 'Revenue': [revenue]}
    line_df = pd.DataFrame(line)
    quarterly_revenue_df = pd.concat([quarterly_revenue_df, line_df], axis=0, ignore_index=True)
tesla_revenue = quarterly_revenue_df
tesla_revenue = tesla_revenue.replace('\$', '', regex=True)
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue = tesla_revenue.replace(',', '', regex=True)
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].astype(float)
print(tesla_revenue.head())

# Working with GME data
gme = yf.Ticker('GME')
gme_history = gme.history(period='max')
gme_data = pd.DataFrame(gme_history)
gme_data.reset_index(inplace=True)
print(gme_data.head())

# Working with GME revenue
url2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
request2 = requests.get(url2).text
soup2 = BeautifulSoup(request2, 'html5lib')
read_html_gme = pd.read_html(str(soup))
gme_revenue = read_html_gme[1]
gme_revenue.columns = ['Date', 'Revenue']
gme_revenue = gme_revenue.replace('\$', '', regex=True)
gme_revenue = gme_revenue.replace(',', '', regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue['Revenue'] = gme_revenue['Revenue'].astype(float)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
print(gme_revenue.tail())

# Building graphs

make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data, gme_revenue, 'GME')
