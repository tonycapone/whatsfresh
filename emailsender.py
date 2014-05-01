# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need

import email
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# Create a text/plain message

def sendEmail(subject, bodFile, to):
    
    
    
    msg = email.mime.Multipart.MIMEMultipart()
    
    
    # me == the sender's email address
    me = "tony@anthonyrhowell.net"

	
	
	
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = to
    
    fp = open(bodFile, 'r')
    att = MIMEText(fp.read(),_subtype="html")
    fp.close()
    att.add_header('Content-Disposition','attachment',filename=bodFile)
    msg.attach(att)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [to], msg.as_string())
    s.quit()
