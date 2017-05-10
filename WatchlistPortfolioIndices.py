

WATCHLIST = 	[
		'FB',
		'USO',
		'UCO',
		'AAPL',
		'GOOG',
		'TSLA',
		'F',
		'TXN',
		'LMT',
		'BAC',
		'AYI',
		'CRM',
		];

PORTFOLIO = 	[
		'USO',
		'UCO',
		'F',
		'EDV'
		];

INDICES = 	[
		'^GSPC', # S&P500
		'^IXIC', # NASDAQ composite
		'^DJI',  # DOW 30
		'USO', # oil ETF
		'UCO', # short-term oil ETF
		'EDV', # long-term treasurty ETF
		'BND', # total bond ETF
		'VTI', # total market ETF
		'VOO', # S&P500 ETF
		'VO',  # medium cap ETF
		'VB',  # small cap ETF
		'VXUS',# total international ETF
		'^VIX',# volatility (S&P500)
		'XIV', # inverse ^VIX
		'USL', # US oil long
		'VHT', # healthcare ETF
		'XLE'  # energy ETF
		];





from Database import *
from Scraper import *

def update_watchlist():
	tickers = get_Stocks_tickers()
	for ticker in tickers:
		update_Stocks_watchlist(ticker, ticker in WATCHLIST)
	tickers = get_Indices_tickers()
	for ticker in tickers:
		update_Indices_watchlist(ticker, ticker in WATCHLIST)

def update_portolio():
	tickers = get_Stocks_tickers()
	for ticker in tickers:
		update_Stocks_portfolio(ticker, ticker in PORTFOLIO)
	tickers = get_Indices_tickers()
	for ticker in tickers:
		update_Indices_portfolio(ticker, ticker in PORTFOLIO)

def update_indice_prices():
	for index in INDICES:
		insert_Indices_table(index)
		last_update = get_Indices_last_update(index)
		if last_update is None:
			scrape_price_history(index)
		else:
			scrape_price_history(index,start_date=last_update)
		update_Indices_last_update(index)
