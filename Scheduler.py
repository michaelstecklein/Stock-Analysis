import datetime
import time
from Log import *



__SCHEDULED_RUN_TIME_HR = 15
__SCHEDULED_RUN_TIME_MIN = 45


__LAST_RUN = datetime.datetime(1962, 1, 1, __SCHEDULED_RUN_TIME_HR, __SCHEDULED_RUN_TIME_MIN)



def __should_run():
	now = datetime.datetime.now()
	if __LAST_RUN.year == now.year and __LAST_RUN.month == now.month and __LAST_RUN.day == now.day:
		return False # already ran today
	if __SCHEDULED_RUN_TIME_HR < now.hour or (__SCHEDULED_RUN_TIME_HR == now.hour and __SCHEDULED_RUN_TIME_MIN <= now.minute):
		return True # is after time and hasn't run today, should run
	return False # hasn't run today but is not time yet

__MIN_TO_SLEEP = 5
def wait_for_scheduled_run(run_method):
	while not __should_run():
		print "Sleeping"
		time.sleep(60*__MIN_TO_SLEEP)
	log_start("Started scheduled run at {}".format(datetime.datetime.now()))
	run_method()
	global __LAST_RUN
	__LAST_RUN = datetime.datetime.now()
	log_stop("Finished scheduled run at {}".format(datetime.datetime.now()))
