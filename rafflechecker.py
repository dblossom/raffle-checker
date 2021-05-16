#!/usr/bin/env python3
from rafflecollector import RaffleCollector

class RaffleChecker:

    ticket_array = None
    anotherwin_dict = {}
    winning_numbers = {}
    todays_number = ""

    def __init__(self,ticket_array):
        collector = RaffleCollector()
        self.ticket_array = ticket_array
        self.winning_numbers = collector.winning_numbers()
        self.todays_number = collector.today_number()

    def check_winner(self):
        for key, value in self.winning_numbers.items():
            for num in self.ticket_array:
                if num == value:
                    self.anotherwin_dict.update({key:value})

    def any_win(self):
        return self.anotherwin_dict

    def validate_input(self,input):
        if len(input) == 0:
            return False
        for item in input:
            if not(item.isnumeric()) or len(item) > 4:
                return False
        return True

    def today_number(self):
        return self.todays_number
