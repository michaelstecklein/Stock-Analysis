import requests
import csv
from bs4 import BeautifulSoup
from Database import *



SP500 = "S&P500"
DJI = "DJI"
NASDAQ = "NASDAQ"






class DailyPrices:
	pass





def scrape_price(ticker, day):
	pass




def scrape_SP500():
	page = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = BeautifulSoup(page.text,"lxml")
	table = soup.find_all('table')[0]
	sp500_tickers = []

	# parse and insert into db
	for row in table.find_all('tr')[1:]:
		cols = row.find_all('td')
		ticker = cols[0].a.text
		company_name = cols[1].a.text
		sp500_tickers.append(ticker)
		insert_Stocks_table(ticker,company_name)

	# update S&P500 entries in the db
	for row in query("SELECT ticker, indices FROM {0}".format(STOCKS_TABLE_NAME)):
		ticker = row[0]
		indices = row[1]
		isInSP500 = sp500_tickers.count(ticker) > 0
		if SP500 not in indices and isInSP500:
			if indices == '':
				update_Stocks_indices(SP500,ticker)
			else:
				update_Stocks_indices("{0},{1}".format(indices,SP500),ticker)
		if SP500 in indices and not isInSP500:
			withComma = "{},".format(SP500)
			if withComma in indices:
				update_Stocks_indices(indices.replace(withComma,''),ticker)
			else:
				update_Stocks_indices(indices.replace(SP500,''),ticker)
	



def scrape_DJI():
	page = requests.get('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')
	soup = BeautifulSoup(page.text,"lxml")
	table = soup.find_all('table')[1]
	dji_tickers = []

	# parse and insert into db
	for row in table.find_all('tr')[1:]:
		cols = row.find_all('td')
		ticker = cols[2].a.text
		company_name = cols[0].a.text
		dji_tickers.append(ticker)
		insert_Stocks_table(ticker,company_name)

	# update DJI entries in the db
	for row in query("SELECT ticker, indices FROM {0}".format(STOCKS_TABLE_NAME)):
		ticker = row[0]
		indices = row[1]
		isInDJI = dji_tickers.count(ticker) > 0
		if DJI not in indices and isInDJI:
			if indices == '':
				update_Stocks_indices(DJI,ticker)
			else:
				update_Stocks_indices("{0},{1}".format(indices,DJI),ticker)
		if DJI in indices and not isInDJI:
			withComma = "{},".format(DJI)
			if withComma in indices:
				update_Stocks_indices(indices.replace(withComma,''),ticker)
			else:
				update_Stocks_indices(indices.replace(DJI,''),ticker)




def scrape_NASDAQ():
	pass





def scrape_NYSE():
	page = requests.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download')
	reader = csv.reader(page.text.splitlines())
	for entry in reader:
		ticker = entry[0]
		company_name = entry[1]
		insert_Stocks_table(ticker,company_name)
	
