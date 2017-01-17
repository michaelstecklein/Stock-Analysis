import datetime
from WatchlistPortfolioIndices import *
from Database import *
from Indicators import *




class Strategy:
	def __init__(self):
		self.run_strategy()
	def run_strategy(self):
		raise NotImplementedError("'run_strategy' method must be implemented")
	def results(self):
		raise NotImplementedError("'results' method must be implemented")


class RSIStrategy(Strategy):
	__N = 14
	__HIGH_RSI = 70
	__LOW_RSI = 30
	__WARN_HIGH_RSI = 65
	__WARN_LOW_RSI = 35
	__warn_portfolio = {}
	__warn_watchlist = {}
	__high_tickers = {}
	__low_tickers = {}
	def run_strategy(self):
		for ticker in PORTFOLIO:
			rsi = self.calculate_RSI(ticker, datetime.date.today())
			if rsi >= self.__WARN_HIGH_RSI or rsi <= self.__WARN_LOW_RSI:
				self.__warn_portfolio[ticker] = rsi
		for ticker in WATCHLIST:
			rsi = self.calculate_RSI(ticker, datetime.date.today())
			if rsi >= self.__WARN_HIGH_RSI or rsi <= self.__WARN_LOW_RSI:
				self.__warn_watchlist[ticker] = rsi
		for ticker in INDICES:
			rsi = self.calculate_RSI(ticker, datetime.date.today())
			if rsi >= self.__HIGH_RSI:
				self.__high_tickers[ticker] = rsi
			if rsi <= self.__LOW_RSI:
				self.__low_tickers[ticker] = rsi
		for ticker in get_Stocks_tickers():
			rsi = self.calculate_RSI(ticker, datetime.date.today())
			if rsi >= self.__HIGH_RSI:
				self.__high_tickers[ticker] = rsi
			if rsi <= self.__LOW_RSI:
				self.__low_tickers[ticker] = rsi
	def results(self):
		r = self.get_strategy_name() + "\n"
		r += "Portfolio:\n"
		r += str(self.__warn_portfolio) + "\n\n"
		r += "Watchlist:\n"
		r += str(self.__warn_watchlist) + "\n\n"
		r += "All stocks:\n"
		r += "High:\n"
		r += str(self.__high_tickers) + "\n\n"
		r += "Low:\n"
		r += str(self.__low_tickers) + "\n\n"
		return r
	def calculate_RSI(self, ticker, date):
		return RSI(self.__N, ticker, date)
	def get_strategy_name(self):
		return "RSI"

class RSIExpStrategy(RSIStrategy):
	__N = 22
	def calculate_RSI(self, ticker, date):
		return RSIExp(self.__N, ticker, date)
	def get_strategy_name(self):
		return "RSIExp"









__STRATEGIES = []

def add_to_list(strategy):
	__STRATEGIES.append(strategy)

def results():
	res = ""
	for strategy in __STRATEGIES:
		res += strategy.results() + "\n"
	return res
