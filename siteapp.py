from rafflechecker import RaffleChecker
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/rafflechecker", methods=["POST","GET"])
def rafflechecker():
    if request.method == "POST":
        mylist = request.form["tickets"]
        # hack workaround for now - basically if the user hits Submit
        # and "tickets" is empty it breaks
        if len(mylist) > 0:
            return redirect(url_for("raffleresult",mylist=mylist))
        else:
            return render_template("rafflechecker.html")
    else:
        return render_template("rafflechecker.html")

@app.route("/raffleresults<mylist>")
def raffleresult(mylist):
    print(mylist)
    splitlist = [num.strip() for num in mylist.split(",")]
    rc = RaffleChecker(splitlist)
    valid = rc.validate_input(splitlist)
    if not(valid):
        return redirect(url_for("input_error",mylist=mylist))
    rc.collect_winning_numbers()
    rc.check_winner()
    todays_number = rc.today_number()
    any_win = rc.any_win()
    #rc.reset()
    return render_template("raffleresults.html",mylist=splitlist,todays_number=todays_number,any_win=any_win)

@app.route("/inputerror<mylist>")
def input_error(mylist):
    return render_template("inputerror.html",mylist=mylist)

if __name__ == "main__":
    app.run()
