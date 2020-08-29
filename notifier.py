import os 
import requests
import sqlite3
import smtplib
import unicodedata
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import parse_qs

load_dotenv()
connection = sqlite3.connect('housinglist.db')
cursor = connection.cursor()

def make_db():
    makeTable = """CREATE TABLE IF NOT EXISTS houses(
            ID INT,
            timeadded DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
    cursor.execute(makeTable)
    connection.commit()


headers = {"User-Agent": os.getenv('SENDER_USERAGENT')}

def find_houses():
    housesPage = requests.get(os.getenv('BASEURL'), headers = headers)
    housesSoup = BeautifulSoup(housesPage.content, 'html.parser')
    houses = housesSoup.findAll("article", {"class": 'house-thumb'})

    for house in houses:
        for a in house.findAll('a', href=True):
            houseID = parse_qs(urlparse.urlparse(a['href']).query)['detailId'][0]
            cursor.execute("SELECT COUNT(*) FROM houses WHERE ID = ?", (houseID,))

            if cursor.fetchone()[0] == 0:
                scan_housepage(houseID)
                cursor.execute("INSERT INTO houses (ID) VALUES (?)", (houseID,))
                connection.commit()

def scan_housepage(ID):
    houseURL = '{}{}'.format(os.getenv('HOUSEURL'), ID)
    housePage = requests.get(houseURL, headers = headers)
    houseSoup = BeautifulSoup(housePage.content, 'html.parser')

    #This could potentially break as Vestide updates their website. 
    houseAddress =  houseSoup.find("p", {"class":'details-address'}).get_text().strip()
    houseDescription =  houseSoup.find("p", {"class":'details-intro'}).get_text().strip()
    houseAreaPrice =  houseSoup.find("p", {"class":'details-figures'})
    houseAreaPriceElts = houseAreaPrice.findAll('span')
    houseArea = houseAreaPriceElts[0].get_text().strip()
    housePrice = unicodedata.normalize(u'NFKD', houseAreaPriceElts[2].get_text().strip()).encode('ascii', 'ignore').decode('utf8')

    send_mail(houseURL, houseAddress, houseDescription, houseArea, housePrice)


def send_mail(houseURL, houseAddress, houseDescription, houseArea, housePrice):
    server = smtplib.SMTP(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))

    subject = 'A new room has been added to Vestide!'
    body = 'Hi {}!\n\nA new room has been added to Vestide! Information about the room: \n\nAddress: {}\nDescription: {}\nSurface area: {}\nRent: {}\n\nURL: {}\n\n\n\nWarning! This is an automated message, the information could be wrong. Always verify the information manually!'.format(os.getenv('RECEIVER_NAME'), houseAddress, houseDescription, houseArea, housePrice, houseURL)
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        os.getenv('SENDER_EMAIL'),
        os.getenv('RECEIVER_EMAIL'),
        msg
    )

    server.quit()

make_db()
find_houses()
connection.close()

