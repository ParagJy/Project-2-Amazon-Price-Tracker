import requests
from bs4 import BeautifulSoup as BS
import smtplib
import csv
import datetime
import os
import time

url = "https://www.amazon.in/Samsung-Galaxy-Ultra-Cream-Storage/dp/B0BRSLH4B5/ref=sr_1_1?crid=3R9G8LBG99ZT9&keywords=samsung+galaxy+s23+ultra&qid=1689140392&sprefix=samsung+galaxy+s23+ultra%2Caps%2C2383&sr=8-1"

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

def check_price():
    page = requests.get(url, headers=headers)
    soup = BS(page.content, "html.parser")
    product_title = soup.find(id = "productTitle")
    #print(product_title)

    price = soup.find(id = "priceblock_ourprice")
    price_float =  float(price.replace(",",""))

    file_exists = True

    if not os.path.exists("./price.csv"):
        file_exists = False

    with open("price.csv","a") as file:
        writer = csv.writer(file,lineterminator ="\n")
        fields = ["Timestamp","price"]

        if not file_exists:
            writer.writerow(fields)

        timestamp = f"{datetime.datetime.date(datetime.datetime.now())},{datetime.datetime.time(datetime.datetime.now())}"
        writer.writerow([timestamp, price_float])
        print("wrote csv data")

    return price_float

def notify():
    server = smtplib.SMTP("smtp.gmail.com")
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("""EMAIL""","""PASSWORD""")  # EMAIL = USER EMAIL ID   &   PASSWORD = USER EMAIL ID PASSWORD

    subject= "Hey! The prices are affordable"
    body = "SALE IS ON, BEST TIME TO BUY THE PRODUCT. BUY IT RIGHT NOW!!" + url
    msg = f"Subject:{subject}\n\n\n\n{body}"

    server.sendmail("""email_1""","""email_2""",msg)   # email_1=senders email     &     email_2=receiver email
    server.quit()

while True:
    price = check_price()
    if(price < 120000):
        notify()
        break
    time.sleep(36000)