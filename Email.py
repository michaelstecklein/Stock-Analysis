import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from Util import *
 
 
def send_email_update(message):
	fromaddr = "bgrogh@gmail.com"
	toaddr = "michaelstecklein@yahoo.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Stock Analysis Update, {}".format(get_last_update_date())
	 
	body = "{}".format(message)
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "robert123abc")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
