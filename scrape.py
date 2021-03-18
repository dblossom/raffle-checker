#!/usr/bin/env python3
import re
import requests
import urllib.request
import time
import lxml.html
from bs4 import BeautifulSoup

#url = 'https://www.palottery.state.pa.us/Games/Print-Past-Winning-Numbers.aspx?id=29&year=2020&print=1'
url = 'https://www.palottery.state.pa.us/Games/Print-Past-Winning-Numbers.aspx?id=29&year=2021&print=1'
response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")
data = soup.findAll('td')

n = 1
long_string = ""
my_numbers = ["1884","1930","2487","2816"]
numbers_dict = {}
todays_number = ""

for d in data:
    if n == 1:
        curdate = lxml.html.fromstring(str(d)).text_content().rstrip().lstrip()
        long_string = long_string + curdate
    if n == 2:
        test = lxml.html.fromstring(str(d)).text_content().replace("Wild Ball:", "").rstrip().lstrip().replace(' ','').strip()
        numbers = ""
        for i in test:
            if i.isnumeric():
                numbers = numbers + i
            if len(numbers) > 3:
                break;
        if len(todays_number) == 0:
            todays_number = numbers
        long_string = long_string + " - " + numbers + "\n"
        curnum = numbers
    n = n + 1
    if n > 3:
        numbers_dict.update({curnum:curdate})
        n = 1
        # probably don't need to clear these, but what the heck
        curdate = ""
        curnum = ""


win = False;
anotherwin = ""
for num in my_numbers:
    if todays_number == num:
        win = True;
        #break;
    if num in numbers_dict:
        date = numbers_dict[num]
        anotherwin = "Looks like you also won on " + date + " with " + num + "\n" + anotherwin
email_string = ""
email_string = "Today's number is: " + todays_number + "\n"
email_string = email_string + "As a reminder your numbers are: " + str(my_numbers).strip('[]') +"\n"
if win:
    email_string = email_string + "Which matches todays number, Congrats!" + "\n"

if anotherwin == "":
    anotherwin = "You have not won anything yet!"
email_string = email_string + anotherwin

print(email_string)
