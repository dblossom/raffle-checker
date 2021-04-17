from rafflechecker import RaffleChecker
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, template_folder='.')

# default route, might change this at deployment
@app.route('/')
def index():
    return render_template("index.html")

# route to page that takes an array of tickets from a form
@app.route("/rafflechecker", methods=["POST","GET"])
def rafflechecker():
    if request.method == "POST":
        mylist = request.form["tickets"]
        # did something get passed?
        if len(mylist) > 0:
            return redirect(url_for("raffleresult",mylist=mylist))
        else:
            return render_template("rafflechecker.html")
    else:
        return render_template("rafflechecker.html")

# route to results page
@app.route("/raffleresults<mylist>")
def raffleresult(mylist):
    # we split the input string into a list but the comma deliminator
    splitlist = [num.strip() for num in mylist.split(",")]
    # create a rafflechecker object
    rc = RaffleChecker(splitlist)
    # let's validate the input ... this should be done by the RaffleChecker
    # constructor and toss some kind of error that we can check for here ...
    valid = rc.validate_input(splitlist)
    if not(valid):
        # input route
        return redirect(url_for("input_error",mylist=mylist))
    # again, more things that should be isolated to rafflechecker
    rc.collect_winning_numbers()
    rc.check_winner()
    todays_number = rc.today_number()
    other_win = rc.any_win()
    # so, the results from any_win() hang around. I've tried sessions
    # but making a copy of the dictionary and clearing any_win seems
    # to be the easiest, esp for this simple applicatoin
    any_win = other_win.copy()
    other_win.clear()
    return render_template("raffleresults.html",mylist=splitlist,todays_number=todays_number,any_win=any_win)

# the route to take if the input is an error 
@app.route("/input_error<mylist>")
def input_error(mylist):
    return render_template("inputerror.html",mylist=mylist)

if __name__ == "main__":
    app.run()
