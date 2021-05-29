#!/usr/bin/env python3
from database import Database
from rafflecollector import RaffleCollector
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time


class Emailer:

    db = Database()
    email_id = os.environ['RAFFLE_EMAIL']
    email_pass = os.environ['RAFFLE_EMAIL_PASSWORD']
    port = 465  # For SSL
    context = ssl.create_default_context()
    message = MIMEMultipart("alternative")

    def __init__(self):
        self.send_alive_email()
        self.check_db_tickets()

    def check_db_tickets(self):
        ticket_list = self.db.get_all_tickets()
        rc = RaffleCollector()
        raffle_winners = rc.winning_numbers()
        for key, value in raffle_winners.items():
            for tup in ticket_list:
                if tup[0] == int(value):
                    self.build_message(self.db.get_email_pid(tup[1]),
                                       tup[0])
                    self.send_email()


    def build_message(self,to_email,ticket):
        self.message["From"] = self.email_id
        self.message["To"] = to_email
        self.message["Subject"] = "Congratulations, You're a winner!"
        text = """\
        Congratulations! Ticket# """ + str(ticket) + """ is a winner!
        """
        winner_message = MIMEText(text,"plain")
        self.message.attach(winner_message)


    def send_email(self):
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login(self.email_id, self.email_pass)
            server.sendmail(self.email_id, self.message["To"], self.message.as_string())

    def send_alive_email(self):
        self.message["From"] = self.email_id
        self.message["To"] = self.db.get_email_pid(1)
        self.message["Subject"] = "Daily heartbeat email!"
        text = """\
        This is your daily heartbeat email!
        """
        heartbeat = MIMEText(text,"plain")
        self.message.attach(heartbeat)
        self.sendmail()

if __name__ == "__main__":
    e = Emailer()
    schedule.every().day.at("22:00").do(e.__init__)
    while True:
        schedule.run_pending()
        time.sleep(1)
