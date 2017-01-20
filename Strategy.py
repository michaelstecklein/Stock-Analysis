import datetime
from WatchlistPortfolioIndices import *
from Database import *
from Indicators import *




class Strategy:
	pass
	def calculate_RSI(self, ticker, date):
		return RSI(self.__N, ticker, date)
	def get_strategy_name(self):
		return "RSI"


