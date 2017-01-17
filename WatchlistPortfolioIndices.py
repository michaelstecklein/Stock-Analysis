

WATCHLIST = 	[
		'FB', 'USO', 'UCO', 'AAPL', 'F', 'TXN', 'LMT', 'BAC', 'AYI', 'PNRA', 'CRM', '^VIX', 'XIV', 'SCI', 'USL', 'VHT', 'XLE', 'IBKR'
		];

PORTFOLIO = 	[
		'FB', 'USO', 'UCO'
		];

INDICES = 	[
		'USO', 'UCO', '^VIX', 'XIV', 'USL', 'VHT', 'XLE'
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
