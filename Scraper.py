import requests
import csv
import datetime
from bs4 import BeautifulSoup
from Database import *



SP500 = "S&P500"
DJI = "DJI"
NASDAQ = "NASDAQ"






class DailyPrices:
	date = datetime.date.today()
	openn = 0.0
	high = 0.0
	low = 0.0
	close = 0.0
	volume = 0
	adj_close = 0.0
	def __init__(self,d,o,h,l,c,v,a):
		self.date = d
		self.openn = o
		self.high = h
		self.low = l
		self.close = c
		self.volume = v
		self.adj_close = a







def __get_price_history_for_dates(ticker, start, end):
	page = requests.get('http://chart.finance.yahoo.com/table.csv?s={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=d&ignore=.csv'.format(ticker,start.day,start.month-1,start.year,end.day,end.month-1,end.year)) # csv of price history from Jan 1, 1970 to today
	prices = csv.reader(page.text.splitlines())
	daily_price_list = []
	for p in prices:
		days_price = DailyPrices(p[0],p[1],p[2],p[3],p[4],p[5],p[6])
		daily_price_list.append(days_price)
	return daily_price_list


def __get_price_history(ticker):
	start_date = datetime.date(1970,1,1)
	today = datetime.date.today()
	return __get_price_history_for_dates(ticker, start_date, today)


__reference_stocks = ('IBM','KO')
def scrape_stock_dates():
	daily_price_lists = []
	for ticker in __reference_stocks:
		daily_price_lists.append(__get_price_history(ticker))
	for i in range(0, len(daily_price_lists[0])):
		date = daily_price_lists[0][i].date
		print "Date: ", date
		for l in daily_price_lists:
			if date != l[i].date:
				print "ERROR: dates do not match in 'scrape_stock_dates': {0}  {1}".format(date,l[i].date)
				sys.exit(1)
		insert_MarketDates_table(date)


def scrape_price_history(ticker):
	# scrape price history
	prices = __get_price_history(ticker)
	#print prices
	# populate db
	# set first_data_date for stock



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
	
