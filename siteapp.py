from rafflechecker import RaffleChecker
from flask import Flask, render_template, redirect, url_for, request
import random
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/rafflechecker", methods=["POST","GET"])
def rafflechecker():
    if request.method == "POST":
        mylist = request.form["tickets"]
        #print(mylist)
        #return render_template("raffleresults.html",mylist=mylist)
        return redirect(url_for("raffleresult",mylist=mylist))
    else:
        return render_template("rafflechecker.html")
    #my_numbers = ["1884","1930","2487","2816"]

    #index = 1
    #while index < 5000:
    #    index = index + 1
    #    ran = random.randint(0,9999)
    #    my_numbers.append(str(ran))

    #rc = RaffleChecker(my_numbers)
    #rc.collect_winning_numbers()
    #a = rc.check_winner()
    #return a
@app.route("/raffleresults<mylist>")
def raffleresult(mylist):
    splitlist = mylist.split(",")
    rc = RaffleChecker(splitlist)
    rc.collect_winning_numbers()
    rc.check_winner()
    todays_number = rc.today_number()
    any_win = rc.any_win()
    return render_template("raffleresults.html",mylist=splitlist,todays_number=todays_number,any_win=any_win)
if __name__ == "main__":
    app.run(debug=True)
