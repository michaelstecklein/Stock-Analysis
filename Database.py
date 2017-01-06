#!/usr/bin/python

import datetime
import MySQLdb
import sys
import os

DATABASE_NAME = 'StockData'
DAILYDATA_TABLE_NAME = 'DailyData'
MARKETDATES_TABLE_NAME = 'MarketDates'
STOCKS_TABLE_NAME = 'Stocks'

__USERNAME = 'python_user'
__PASSWORD = 'password'
__DAILYDATA_TABLE_CREATE =   """	CREATE TABLE IF NOT EXISTS {0}(
					stock_ticker VARCHAR(5) NOT NULL,
					date DATE NOT NULL,
					open FLOAT NOT NULL,
					high FLOAT NOT NULL,
					low FLOAT NOT NULL,
					close FLOAT NOT NULL,
					adj_close FLOAT NOT NULL,
					volume BIGINT NULL DEFAULT -1,
					PRIMARY KEY(stock_ticker, date)); """.format(DAILYDATA_TABLE_NAME)
__MARKETDATES_TABLE_CREATE = """	CREATE TABLE IF NOT EXISTS {0}(
					date DATE NOT NULL,
					day_number INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT); """.format(MARKETDATES_TABLE_NAME)
__STOCKS_TABLE_CREATE =      """ 	CREATE TABLE IF NOT EXISTS {0}(
					ticker VARCHAR(5) NOT NULL PRIMARY KEY,
					company_name VARCHAR(30),
					first_data_date DATE NULL,
					indices SET('NASDAQ','S&P500','DJI') NULL DEFAULT NULL,
					on_watchlist ENUM('True','False') NULL DEFAULT 'False',
					in_portfolio ENUM('True','False') NULL DEFAULT 'False'); """.format(STOCKS_TABLE_NAME)


def __startup():
	os.system("mysql.server start")

def __shutdown():
	os.system("mysql.server stop")

def query(command):
	try:
		connection = MySQLdb.connect('localhost', __USERNAME, __PASSWORD, DATABASE_NAME);
	except MySQLdb.Error, e:
		print "ERROR connecting to database %s" % DATABASE_NAME
		print e
		sys.exit(1)
	try:
		cursor = connection.cursor()
		cursor.execute(command)
		if "INSERT" or "UPDATE" in command:
			connection.commit()
		#return cursor
		return cursor.fetchall()
	except MySQLdb.Error, e:
		print "ERROR executing command %s" % command
		print e
		sys.exit(1)
		
def __create_db():
	query("CREATE DATABASE IF NOT EXISTS {0};".format(DATABASE_NAME)) 
	query("USE {0};".format(DATABASE_NAME)) 

def __create_tables():
	query(__DAILYDATA_TABLE_CREATE)
	query(__MARKETDATES_TABLE_CREATE)
	query(__STOCKS_TABLE_CREATE)

def run_db_setup_routine():
	__startup()
	__create_db()
	__create_tables()

def insert(table, value):
	query("INSERT IGNORE INTO {0} VALUES({1});".format(table,value))

def insert_Stocks_table( ticker, company_name="", first_data_date=None, indices="", on_watchlist=False, in_portfolio=False):
	insert(STOCKS_TABLE_NAME, """ "{0}","{1}","{2}","{3}",{4},{5} """.format(ticker,company_name,first_data_date,indices,on_watchlist,in_portfolio))

def update_Stocks_indices(indices, ticker):
	query("UPDATE Stocks SET indices='{0}' WHERE ticker='{1}';".format(indices,ticker))

