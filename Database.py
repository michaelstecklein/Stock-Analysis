#!/usr/bin/python

import datetime
import MySQLdb
import sys
import os
from Log import *

DATABASE_NAME = 'StockData'
DAILYDATA_TABLE_NAME = 'DailyData'
MARKETDATES_TABLE_NAME = 'MarketDates'
STOCKS_TABLE_NAME = 'Stocks'
INDICES_TABLE_NAME = 'Indices'

__USERNAME = 'python_user'
__PASSWORD = 'password'
__DAILYDATA_TABLE_CREATE =   """	CREATE TABLE IF NOT EXISTS {0}(
					ticker VARCHAR(5) NOT NULL,
					date DATE NOT NULL,
					open FLOAT NOT NULL,
					high FLOAT NOT NULL,
					low FLOAT NOT NULL,
					close FLOAT NOT NULL,
					volume BIGINT NULL DEFAULT -1,
					adj_close FLOAT NOT NULL,
					PRIMARY KEY(ticker, date)); """.format(DAILYDATA_TABLE_NAME)
__MARKETDATES_TABLE_CREATE = """	CREATE TABLE IF NOT EXISTS {0}(
					date DATE NOT NULL,
					day_number INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT); """.format(MARKETDATES_TABLE_NAME)
__STOCKS_TABLE_CREATE =      """ 	CREATE TABLE IF NOT EXISTS {0}(
					ticker VARCHAR(5) NOT NULL PRIMARY KEY,
					company_name VARCHAR(30),
					indices SET('NASDAQ','S&P500','DJI') NULL DEFAULT NULL,
					on_watchlist ENUM('True','False') NULL DEFAULT 'False',
					in_portfolio ENUM('True','False') NULL DEFAULT 'False',
					first_data_date DATE NULL,
					last_update_date DATE NULL); """.format(STOCKS_TABLE_NAME)
__INDICES_TABLE_CREATE =      """ 	CREATE TABLE IF NOT EXISTS {0}(
					ticker VARCHAR(5) NOT NULL PRIMARY KEY,
					on_watchlist ENUM('True','False') NULL DEFAULT 'False',
					in_portfolio ENUM('True','False') NULL DEFAULT 'False',
					first_data_date DATE NULL,
					last_update_date DATE NULL); """.format(INDICES_TABLE_NAME)


def __startup():
	os.system("mysql.server start")

def __shutdown():
	os.system("mysql.server stop")

def query(command):
	#print command
	try:
		connection = MySQLdb.connect('localhost', __USERNAME, __PASSWORD, DATABASE_NAME);
	except MySQLdb.Error, e:
		log_error("Error occurred when connecting to database {0}\n{1}".format(DATABASE_NAME, e), shutdown=True)
	try:
		cursor = connection.cursor()
		cursor.execute(command)
		if "INSERT" or "UPDATE" in command:
			connection.commit()
		#return cursor
		return cursor.fetchall()
	except MySQLdb.Error, e:
		log_error("Error occurred when executing command {0}\n{1}".format(command, e), shutdown=True)
		
def __create_db():
	query("CREATE DATABASE IF NOT EXISTS {0};".format(DATABASE_NAME)) 
	query("USE {0};".format(DATABASE_NAME)) 

def __create_tables():
	query(__DAILYDATA_TABLE_CREATE)
	query(__MARKETDATES_TABLE_CREATE)
	query(__STOCKS_TABLE_CREATE)
	query(__INDICES_TABLE_CREATE)

def run_db_setup_routine():
	__startup()
	__create_db()
	__create_tables()

def insert(table, value):
	query("INSERT IGNORE INTO {0} VALUES({1});".format(table,value))

def insert_Stocks_table( ticker, company_name="", indices="", on_watchlist=False, in_portfolio=False, first_data_date=None, last_update=None):
	insert(STOCKS_TABLE_NAME, """ "{0}","{1}","{2}",{3},{4},"{5}","{6}" """.format(ticker,company_name,indices,on_watchlist,in_portfolio,first_data_date,last_update))

def update_Stocks_indices(indices, ticker):
	query("UPDATE Stocks SET indices='{0}' WHERE ticker='{1}';".format(indices,ticker))

def update_Stocks_first_data_date(ticker, first_data_date):
	query("UPDATE Stocks SET first_data_date='{0}' WHERE ticker='{1}';".format(first_data_date,ticker))

def update_Stocks_last_update(ticker):
	date = query("SELECT date FROM DailyData WHERE ticker='{0}' ORDER BY date DESC LIMIT 1;".format(ticker))[0][0]
	query("UPDATE Stocks SET last_update_date='{0}' WHERE ticker='{1}';".format(date,ticker))

def update_Stocks_watchlist(ticker,truefalse):
	query("UPDATE {0} SET on_watchlist='{1}' WHERE ticker='{2}';".format(STOCKS_TABLE_NAME,truefalse,ticker))

def update_Stocks_portfolio(ticker,truefalse):
	query("UPDATE {0} SET in_portfolio='{1}' WHERE ticker='{2}';".format(STOCKS_TABLE_NAME,truefalse,ticker))

def get_Stocks_for_indice(ticker):
	if ticker is None:
		result = query("SELECT ticker FROM {0};".format(STOCKS_TABLE_NAME))
	else:
		result = query("SELECT ticker FROM {0} WHERE FIND_IN_SET('{1}',indices) > 0;".format(STOCKS_TABLE_NAME,ticker))
	return [element for tupl in result for element in tupl]

def get_Stocks_last_update(ticker):
	return query("SELECT last_update_date FROM {0} WHERE ticker='{1}';".format(STOCKS_TABLE_NAME,ticker))[0][0]

def get_Stocks_tickers():
	result = query("SELECT ticker FROM {0};".format(STOCKS_TABLE_NAME))
	return [element for tupl in result for element in tupl]

def insert_MarketDates_table(date):
	insert(MARKETDATES_TABLE_NAME, "'{0}',{1}".format(date,"NULL"))

def clear_MarketDates_table():
	query("DELETE FROM {0};".format(MARKETDATES_TABLE_NAME))
	query("ALTER TABLE {0} AUTO_INCREMENT = 1;".format(MARKETDATES_TABLE_NAME))

def reset_MarketDates_table(): # resets auto_increment
	result = query("SELECT day_number FROM {0} ORDER BY day_number DESC LIMIT 1;".format(MARKETDATES_TABLE_NAME))
	query("ALTER TABLE {0} AUTO_INCREMENT = {1};".format(MARKETDATES_TABLE_NAME,result[0][0]))

def get_last_update_MarketDates():
	result = query("SELECT date FROM {0} ORDER BY day_number DESC LIMIT 1;".format(MARKETDATES_TABLE_NAME))
	if len(result) == 0:
		return None
	else:
		return result[0][0]


def insert_DailyData_table(ticker,date,openn,high,low,close,volume,adj_close):
	insert(DAILYDATA_TABLE_NAME,"'{0}','{1}',{2},{3},{4},{5},{6},{7}".format(ticker,date,openn,high,low,close,volume,adj_close))



def get_Indices_last_update(ticker):
	return query("SELECT last_update_date FROM {0} WHERE ticker='{1}';".format(INDICES_TABLE_NAME,ticker))[0][0]

def update_Indices_last_update(ticker):
	date = query("SELECT date FROM DailyData WHERE ticker='{0}' ORDER BY date DESC LIMIT 1;".format(ticker))[0][0]
	query("UPDATE Indices SET last_update_date='{0}' WHERE ticker='{1}';".format(date,ticker))

def update_Indices_first_data_date(ticker, first_data_date):
	query("UPDATE Indices SET first_data_date='{0}' WHERE ticker='{1}';".format(first_data_date,ticker))

def insert_Indices_table(ticker, on_watchlist=False, in_portfolio=False, first_data_date=None, last_update=None):
	insert(INDICES_TABLE_NAME, """ "{0}",{1},{2},"{3}","{4}" """.format(ticker,on_watchlist,in_portfolio,first_data_date,last_update))

def update_Indices_watchlist(ticker, truefalse):
	query("UPDATE {0} SET on_watchlist='{1}' WHERE ticker='{2}';".format(INDICES_TABLE_NAME,truefalse,ticker))

def update_Indices_portfolio(ticker, truefalse):
	query("UPDATE {0} SET in_portfolio='{1}' WHERE ticker='{2}';".format(INDICES_TABLE_NAME,truefalse,ticker))

def get_Indices_tickers():
	result = query("SELECT ticker FROM {0};".format(INDICES_TABLE_NAME))
	return [element for tupl in result for element in tupl]
