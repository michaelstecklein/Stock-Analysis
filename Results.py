import datetime
from WatchlistPortfolioIndices import *
from Database import *
from Indicators import *



class Results:
	def get_results(self):
		raise NotImplementedError("'get_results' method must be implemented")


class RSIResults(Results):
	__USE_SPACES_INSTEAD_TABS = True
	__HIGH_RSI = 70
	__LOW_RSI = 30
	__WARN_HIGH_RSI = 65
	__WARN_LOW_RSI = 35

	RESULT = ""
	
	def __header(self, title):
		SZ = 44
		l = len(title)
		self.RESULT += "{} ".format(title)
		self.RESULT += "-" * (SZ - l)
		self.RESULT += "\n"

	def __warn(self, ticker, rsi, msg):
		t = "{}".format(ticker)
		r = "{}".format(rsi)
		m = "{}".format(msg)
		if self.__USE_SPACES_INSTEAD_TABS:
			FIRST_SPACING = 7
			SECOND_SPACING = 20
			self.RESULT += "{}".format(t)
			self.RESULT += " " * (FIRST_SPACING - len(t))
			self.RESULT += "{}".format(r)
			self.RESULT += " " * (SECOND_SPACING - len(r))
			self.RESULT += "{}".format(m)
		else:
			self.RESULT += "{}\t{}\t{}".format(t,r,m)
		self.RESULT += "\n"
	
	def __check_rsi(self, ticker, rsi):
		if rsi >= self.__HIGH_RSI:
			self.__warn(ticker, rsi, "HIGH")
		elif rsi <= self.__LOW_RSI:
			self.__warn(ticker, rsi, "LOW")
		elif rsi <= self.__WARN_LOW_RSI:
			self.__warn(ticker, rsi, "l")
		elif rsi >= self.__WARN_HIGH_RSI:
			self.__warn(ticker, rsi, "h")

	def __run_ticker_list(self, ticker_list, title):
		self.__header(title)
		for ticker in ticker_list:
			rsi = RSI(ticker, datetime.date.today())
			self.__check_rsi(ticker, rsi)

	# Override
	def get_results(self):
		self.RESULT = ""
		self.__run_ticker_list(PORTFOLIO, "Portfolio")
		self.__run_ticker_list(WATCHLIST, "Watchlist")
		self.__run_ticker_list(INDICES, "Indices")
		self.__run_ticker_list(get_Stocks_tickers(), "All Stocks")
		return self.RESULT
