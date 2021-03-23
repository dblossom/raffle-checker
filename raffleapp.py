#from rafflechecker import RaffleChecker
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
        return redirect(url_for("raffleresult",mylst=mylist))
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
@app.route("/raffleresults<mylst>")
def raffleresult(mylst):
    return f"<p>{mylst}</p>"
    #return render_template("raffleresults.html",mylst)
if __name__ == "main__":
    app.run(debug=True)
