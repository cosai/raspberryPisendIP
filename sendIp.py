from urllib.request import Request, urlopen
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import requests
import time

# author: cosai
# This file should run on startup of raspberry pi
# This program will work not more than 5 minutes
# Once this program starts running it is reading a temporary sms page.
# You can send an SMS to the phone number with a secret keyword from your mobile phone
# If that page has a key word (for here it is RASPSENDIP)
# raspberry pi sends its ipconfig command output and its name (if you haven't changed it will be pi) to specified email address
# if it manages to find the keyword and sends the email the program stops.

isdone=False
numberofsecondsrunning=0
secretkeyword="RASPSENDIP"
sender_email = "sender@gmail.com"
receiver_email = "receiver@gmail.com"
password = "password"

#gets the name of the raspberry pi (user)
def whoiam()->str:
    result=subprocess.run(['whoami'],stdout=subprocess.PIPE)
    resstr=result.stdout.decode('utf-8')
    return resstr

def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        something = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        #print("No internet connection available.")
        return False
    return False


def learnip()->str:
    result=subprocess.run(['ifconfig'],stdout=subprocess.PIPE)
    resstr=result.stdout.decode('utf-8')
    return resstr

#this is sending html email
def sendemail(emailmes,subjectmessage):

    message = MIMEMultipart("alternative")
    message["Subject"] = subjectmessage
    message["From"] = sender_email
    message["To"] = receiver_email

    
    text=emailmes
    html=emailmes.replace("\n","<br>")
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


while not isdone and numberofsecondsrunning < 300:
    if connected_to_internet():
        linkp="https://freephonenum.com/us/receive-sms/5417083275"
        req = Request(linkp, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        webpagestr = webpage.decode('utf-8')
        pos=webpagestr.find(secretkeyword)
        #this if part can be omitted and the code can be changed so that raspberry pi sends ip when it connects internet.
        if pos >=0:
            iptext=learnip()
            raspberrypiname=whoiam()
            messsubject="IP address of "+raspberrypiname
            sendemail(iptext,messsubject)
            isdone=True
    numberofsecondsrunning=numberofsecondsrunning+10
    time.sleep(10)
