#!/usr/bin/env python3
import re
import requests
import urllib.request
import time
import lxml.html
from bs4 import BeautifulSoup
import datetime
import random
from flask import Flask
app = Flask(__name__)

@app.route('/')

# Link to the Google Spreadsheet for the 2020-2021 Raffle.
# Note, it's one large link broken up to be more "readable"
#
# https://docs.google.com/spreadsheets/d/e/2PACX-1vTRDUpatyCE0JFXKdd-
# _LZPqQEsU63XtX0ZnyX1n0zEfdoF2aNVCMJqGPphOcj9STeWxdMuVMAA-QTX/pubhtml/
# sheet?headers=false&gid=652560800

class RaffleChecker:

    todays_number = ""
    numbers_dict = {}
    ticket_array = None
    td_data = None
    anotherwin_array = []

    def __init__(self,ticket_array):
        self.ticket_array = ticket_array

    def collect_winning_numbers(self):
        # Let's get the date so we can strip the year for `year=` of URL.
        now = datetime.datetime.now()
        # in URL, ID=29 is the ID to the PICK 4 evening numbers
        url = "https://www.palottery.state.pa.us/Games/Print-Past-Winning-Numbers.aspx?id=29&year={}&print=1".format(now.year)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        self.td_data = soup.findAll('td')

        td_number = 1
        for td in self.td_data:
            # the first <td> </td> is the date
            if td_number == 1:
                curdate = lxml.html.fromstring(str(td)).text_content().rstrip().lstrip()

            # the second <td> </td> is the number & wild ball (discard it)
            if td_number == 2:
                num_list = lxml.html.fromstring(str(td)).text_content().replace("Wild Ball:", "").rstrip().lstrip().replace(' ','').strip()
                numbers = ""
                for num in num_list:
                    if num.isnumeric():
                        numbers = numbers + num
                    if len(numbers) > 3:
                        break;
                if len(self.todays_number) == 0:
                    self.todays_number = numbers
                curnum = numbers

            # the third and final <td> </td> is garbage.
            # so, let's add number to dictionary and reset.
            if td_number == 3:
                self.numbers_dict.update({curnum:curdate})
                td_number = 1
                # probably don't need to clear these, but what the heck
                curdate = ""
                curnum = ""
                # we continue to end this iteration of the loop and this allows
                #us to skip over incrementing td_number pre-maturely
                continue

            # increment for the next pass
            td_number = td_number + 1

    def check_winner(self):
        win = False;
        for num in self.ticket_array:
            # if the incoming data doesn't contain a leading 0, the check will fail.
            if len(num) < 4:
                num = "0"+num
            if self.todays_number == num:
                win = True;
            if num in self.numbers_dict:
                date = self.numbers_dict[num]
                self.anotherwin_array.append("Looks like you won on " + date + " with " + num)

    def today_number(self):
        if len(self.todays_number) == 0:
            return "Error: todays number not set!"
        else:
            return self.todays_number

    def any_win(self):
        print(len(self.anotherwin_array))
        if len(self.anotherwin_array) == 0:
            self.anotherwin_array.append("You have not won anything yet!")
        return self.anotherwin_array

if __name__ == '__main__':
    my_numbers = ["1884","1930","2487","2816"]
    rc = RaffleChecker(my_numbers)
    rc.collect_winning_numbers()
    rc.check_winner()


# hacky test ....
#index = 1
#while index < 5000:
#    index = index + 1
#    ran = random.randint(0,9999)
#    my_numbers.append(str(ran))
