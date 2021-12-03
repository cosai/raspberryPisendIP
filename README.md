# raspberryPisendIP

## If you send a text message to the number 5417083275 as RASPSENDIP, raspberry pi will send you an email with its IP information. The email subject will state the name of the raspberry pi user.

- This file should run on startup of raspberry pi
- This program will work not more than 5 minutes.
- IP information will be the output of *ifconfig* command
- Once this program starts running it is reading a temporary sms page.
- You can send an SMS to the phone number with a secret keyword **(RASPSENDIP)** from your mobile phone
- If it manages to find the secret keyword and sends the email,then the program stops.
- If it cannot connect to internet or can not read the SMS with secret keyword, program stops after 5 minutes. In that way, it won't drain CPU resource.

There is no specific command used in this file for raspberry pi. This file will work in Linux also.
Feel free to modify/fork as you like.
