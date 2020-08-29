# Vestide notifier 
 A script that scrapes vestide.nl for new rooms and notifies the user via e-mail when a new room has become available to apply for. This script does _not_ sign the user up for any rooms it merely notifies the user of a new room becoming available.
 

# Deployment
## Requirements
* Python 3.x
* PIP (generally bundled with your Python install)
* Optional: A device that is always on which can run this script periodically (e.g. Raspberry Pi with crontab or your desktop PC)

## Setup
1. Clone the repository 
2. Run `pip install -r requirements.txt` in console in this folder
3. Fill in your personal information in `.env_template` and rename it to `.env`

## Filling in the `.env` file
`SENDER_EMAIL`: The email from which you will send the email <br>
`SENDER_PASSWORD`: The password of your email account <br>
`SENDER_USERAGENT`: To enable webscraping, copy and paste the values from [this page](https://www.google.com/search?q=my+user+agent)<br>
`RECEIVER_EMAIL`: The email on which you want to receive your notification (could be the same as the sender)<br>
`RECEIVER_NAME` The name of the receiver (e.g. your name) <br>
`BASEURL` This should be the URL of the main page with all the houses offered on Vestide<br>
`HOUSEURL` This is the base URL of the house. You can obtain this by going to a random offering, copying the url and removing the parameter value (e.g. if the link is `.../?detailId=0001` then you should only remove `0001`<br>
`SMTP_SERVER`: SMTP server address from your email provider<br>
`SMTP_PORT`= SMTP port from your email provider<br>

## Setting up Gmail (a difficult example)
1. Enable 2FA on you Google account
2. Generate an app password and fill it into the `.env` file
3. When running for the first time go [here](https://accounts.google.com/b/0/DisplayUnlockCaptcha) and click continue

_Note_: Other email carriers will probably not need such an exstensive setup


# Using Vesitide notifier
Either periodically run the script manually by going running `python notifier.py` in a console or set up an automatic task with crontab.

# Q&A
*Question*: Why did you not include the URLs to Vestide?<br> 
*Answer*: The URLs might change, you might want to scrape the Dutch version of Vestide instead of the English one (or vise versa) and perhaps Vestide is not too fond of me including their URLs.

