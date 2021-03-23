from rafflechecker import RaffleChecker
from flask import Flask
import random
app = Flask(__name__)

@app.route('/')
def index():
    my_numbers = ["1884","1930","2487","2816"]

    index = 1
    while index < 5000:
        index = index + 1
        ran = random.randint(0,9999)
        my_numbers.append(str(ran))

    rc = RaffleChecker(my_numbers)
    rc.collect_winning_numbers()
    a = rc.check_winner()
    return a
#    return 'Hello, World!'
