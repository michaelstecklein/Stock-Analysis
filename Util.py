from Database import *




def flatten_tuple(t):
	return [element for tupl in t for element in tupl]


def get_last_update_date():
	REF_STOCK = 'AAPL'
	d = query("SELECT date FROM DailyData WHERE ticker='{}' ORDER BY date DESC LIMIT 1;".format(REF_STOCK))[0][0]
	print "TYPE: ",type(d)
	return query("SELECT date FROM DailyData WHERE ticker='{}' ORDER BY date DESC LIMIT 1;".format(REF_STOCK))[0][0]
