import sys
import os
import datetime


__LOG_FILE = "program.log"




__HAS_RUN = False
def __log(msg):
	if not __HAS_RUN and os.path.isfile(__LOG_FILE):
		os.remove(__LOG_FILE)
		global __HAS_RUN
		__HAS_RUN = True
	print msg
	with open(__LOG_FILE,'a') as f:
		f.write("{}\n".format(msg))

def log(msg):
	__log(msg)

def log_error(err_msg, shutdown=False):
	__log("ERROR ------------------------------------------------------")
	__log(err_msg)
	__log("------------------------------------------------------------")
	if shutdown:
		sys.exit(1)

def log_segment(segment_title):
	'''
	__log("")
	__log(":::::::::::::::::::::::::::::::::::::::::::  {}".format(segment_title))
	'''
	timestamp = "{}  ".format(datetime.datetime.now())
	segment_title = "  " + segment_title
	l = len(timestamp)
	total_len = 60
	formatted_msg =  timestamp + (':' * (total_len - l)) + segment_title
	__log(formatted_msg)

def log_start(start_msg):
	__log("")
	__log("")
	__log("============================================================")
	__log(start_msg)
	__log("============================================================")

def log_stop(stop_msg):
	__log("")
	__log("============================================================")
	__log(stop_msg)
	__log("============================================================")
	__log("")
