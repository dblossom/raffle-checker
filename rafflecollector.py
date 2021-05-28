# Link to the Google Spreadsheet for the 2020-2021 Raffle.
# Note, it's one large link broken up to be more "readable"
#
# https://docs.google.com/spreadsheets/d/e/2PACX-1vTRDUpatyCE0JFXKdd-
# _LZPqQEsU63XtX0ZnyX1n0zEfdoF2aNVCMJqGPphOcj9STeWxdMuVMAA-QTX/pubhtml/
# sheet?headers=false&gid=652560800
import re
import requests
import urllib.request
import time
import lxml.html
from bs4 import BeautifulSoup
import datetime

class RaffleCollector:

    start_date = datetime.datetime(2020,7,1)
    numbers_dict = {}
    todays_number = ""

    def __init__(self):
        self.collect_winning_numbers()
        self.today_number()

    def collect_winning_numbers(self):
        # Let's get the date so we can strip the year for `year=` of URL.
        now = datetime.datetime.now()
        # in URL, ID=29 is the ID to the PICK 4 evening numbers
        url = "https://www.palottery.state.pa.us/Games/Print-Past-Winning-Numbers.aspx?id=29&year={}&print=1".format(now.year)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        td_data = soup.findAll('td')

        # The raffle runs across a year, and our data is based on an entire year
        if (now.year > self.start_date.year):
            url = "https://www.palottery.state.pa.us/Games/Print-Past-Winning-Numbers.aspx?id=29&year={}&print=1".format(self.start_date.year)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            td_data = td_data + soup.findAll('td')

        td_number = 1
        for td in td_data:
            # the first <td> </td> is the date
            if td_number == 1:
                curdate = lxml.html.fromstring(str(td)).text_content().rstrip().lstrip()
                curdate = datetime.datetime.strptime(curdate,"%m/%d/%Y")

            # the second <td> </td> is the number & wild ball (discard it)
            if td_number == 2:
                num_list = lxml.html.fromstring(str(td)).text_content().replace("Wild Ball:", "").rstrip().lstrip().replace(' ','').strip()
                numbers = ""
                for num in num_list:
                    if num.isnumeric():
                        numbers = numbers + num
                    if len(numbers) > 3:
                        break;
                # the first one in result is today's number
                if len(self.todays_number) == 0:
                    self.todays_number = numbers
                curnum = numbers

            # the third and final <td> </td> is garbage.
            # so, let's add number to dictionary and reset.
            if td_number == 3:
                # raffle runs across two years 7/1/2020 - 6/30/2012,
                #so want to strip first half of year, those results don't apply.
                if curdate < self.start_date:
                    continue
                # check fails w/o leading zero due to being a string not int
                # TODO: possible bug -- need to append 0's until len = 4
                if len(curnum) < 4:
                    curnum = "0"+curnum
                self.numbers_dict.update({curdate:curnum})
                td_number = 1
                # probably don't need to clear these, but what the heck
                curdate = ""
                curnum = ""
                # we continue to end this iteration of the loop and this allows
                #us to skip over incrementing td_number pre-maturely
                continue

            # increment for the next pass
            td_number = td_number + 1

    def today_number(self):
        if len(self.todays_number) == 0:
            return "Error: todays number not set!"
        else:
            return self.todays_number

    def winning_numbers(self):
        return self.numbers_dict
