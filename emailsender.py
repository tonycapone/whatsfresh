# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# Create a text/plain message

def sendEmail(subject, body, to):
	msg = MIMEText(body)


	# me == the sender's email address
	me = "tony@anthonyrhowell.net"

	
	
	
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = to

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')
	s.sendmail(me, [to], msg.as_string())
	s.quit()
