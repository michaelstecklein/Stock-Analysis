#!/usr/bin/python

from Database import *
from Scraper import *
from WatchlistPortfolioIndices import *
from Indicators import *
from Results import *
from Log import *
from Scheduler import *
from Email import *
import Strategy


# TODO:	
#	Restructure Database.py to be more organized and editable



def run():
	# Setup db
	log_segment("Setting up db")
	run_db_setup_routine()

	# Populate Stocks table
	log_segment("Updating Stocks table")
	scrape_indices()

	# Populate MarketDates table
	log_segment("Updating MarketDates table")
	update_stock_dates()

	# Update watchlist, portfolio, and indices
	log_segment("Updating Indices table")
	update_indice_prices()
	log_segment("Updating watchlist")
	update_watchlist()
	log_segment("Updating portfolio")
	update_portolio()
	
	# Populate DailyData table
	log_segment("Updating DailyData table")
	update_stock_prices()

	log_segment("Setup and update completed")

	# Update indicators
	log_segment("Updating indicators")
	update_indicators()
	
	# Get results
	rsi = RSIResults()
	indicator_results = rsi.get_results()
	log(indicator_results)

	# Send email
	log_segment("Sending email")
	send_email_update(indicator_results)










launchd_run(run) # will use launchd to time the run rather than my custom scheduler

'''
while True:
	wait_for_scheduled_run(run)
'''
