from rafflechecker import RaffleChecker
from database import Database
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, template_folder='templates')

# default route, might change this at deployment
#@app.route('/')
#def index():
#    return render_template("rafflechecker.html")

# route to page that takes an array of tickets from a form
@app.route("/", methods=["POST","GET"])
def rafflechecker():
    if request.method == "POST":
        mylist = request.form.get("tickets")
        # did something get passed?
        if len(mylist) > 0:
            ticketlist = create_list(mylist)
            rc = validate_list(ticketlist)
            if rc == -1:
                return render_template("inputerror.html",mylist=mylist)
            rc.check_winner()
            todays_number = rc.today_number()
            other_win = rc.any_win()
            # so, the results from any_win() hang around. I've tried sessions
            # but making a copy of the dictionary and clearing any_win seems
            # to be the easiest, esp for this simple applicatoin
            any_win = other_win.copy()
            other_win.clear()
            # do we want to save the tickets?
            if request.form.get("saveticket"):
                save_tickets(ticketlist,
                             request.form.get("name"),
                             request.form.get("email"))
            return render_template("raffleresults.html",
                                    mylist=ticketlist,
                                    todays_number=todays_number,
                                    any_win=any_win)
        else:
            return render_template("rafflechecker.html")
    else:
        return render_template("rafflechecker.html")

def save_tickets(splitlist,name,email):
    db = Database()
    # check if email exists, if so, check ticket table for matching
    # add any unique tickets
    # else: add as new user & new tickets (should check for tickets too)
    if db.lookup_person(email) == -1:
        db.add_person(name,email)

    for ticket in splitlist:
        db.add_ticket(ticket,email)

def create_list(mylist):
    # we split the input string into a list but the comma deliminator
    splitlist = [num.strip() for num in mylist.split(",")]
    # let's remove any duplicate nonsense - yes a oneliner but easier to read
    return list(dict.fromkeys(splitlist))

def validate_list(ticketlist):
    # create a rafflechecker object
    rc = RaffleChecker(ticketlist)
    # let's validate the input ... this should be done by the RaffleChecker
    # constructor and toss some kind of error that we can check for here ...
    valid = rc.validate_input(ticketlist)
    if not(valid):
        return -1;
    # return the valid RaffleChecker object
    return rc

if __name__ == "__main__":
    app.run()
