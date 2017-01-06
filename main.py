#!/usr/bin/python

import Database as db
from Scraper import *


#db.run_db_setup_routine()


scrape_SP500()
scrape_DJI()
scrape_NYSE()
