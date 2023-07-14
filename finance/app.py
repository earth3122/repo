import os

import requests
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# pk_f052930c805c4570bc8dd638d64ac3ac

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get user's portfolio
    portfolio = db.execute("SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
                           user_id=session["user_id"])

    # Lookup current prices for each stock
    total_value = 0
    for stock in portfolio:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total"] = stock["price"] * stock["total_shares"]
        total_value += stock["total"]

    # Get user's cash balance
    rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    cash = rows[0]["cash"]
    total_value += cash

    return render_template("portfolio.html", portfolio=portfolio, cash=cash, total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted and exists
        symbol = request.form.get("symbol")
        if not symbol or not lookup(symbol):
            return apology("invalid symbol")

        # Ensure shares was submitted and is a positive integer
        shares = request.form.get("shares")
        if not shares or not shares.isdigit():
            return apology("invalid number of shares")

        # Look up stock information
        stock = lookup(symbol)

        # Calculate total cost of shares
        price = stock["price"]
        total_cost = price * int(shares)

        # Ensure user can afford the purchase
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash = rows[0]["cash"]
        if cash < total_cost:
            return apology("can't afford")

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
                   total_cost=total_cost, user_id=session["user_id"])

        # Record the purchase in transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=symbol, shares=int(shares), price=price)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get the transaction history for the current user
    transactions = db.execute(
        "SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = :user_id ORDER BY transacted DESC",
        user_id=session["user_id"]
    )

    # Render the history template with the transaction history data
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol or lookup(symbol) is None:
            return apology("Invalid symbol. Please try again.", 400)

        # Get stock quote using lookup function
        quote = lookup(symbol)

        # Render quoted.html with stock quote values embedded
        if quote is not None:
            return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=usd(quote["price"]))
        else:
            return render_template("quote.html", error="Invalid symbol. Please try again.")

    # Render quote.html with empty form
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username is not already taken
        if len(rows) != 0:
            return apology("username already taken")

        # Insert new user into database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash_val)",
                   username=request.form.get("username"),
                   hash_val=generate_password_hash(request.form.get("password")))

        # Redirect user to login page
        flash("Registered successfully. Please log in.")
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate user input
        if not symbol:
            return apology("must select symbol", 400)

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive number of shares", 400)

        # Get the current user's portfolio
        portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                               user_id=session["user_id"], symbol=symbol).fetchone()

        if not portfolio or portfolio["shares"] < int(shares):
            return apology("not enough shares", 400)

        # Calculate the new cash balance and update the database
        stock = lookup(symbol)
        value = int(shares) * stock["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]).fetchone()["cash"]
        db.execute("UPDATE users SET cash = :cash + :value WHERE id = :user_id",
                   cash=cash, value=value, user_id=session["user_id"])

        # Update the portfolio
        db.execute("UPDATE portfolio SET shares = :shares - :sold_shares WHERE user_id = :user_id AND symbol = :symbol",
                   shares=portfolio["shares"], sold_shares=int(shares), user_id=session["user_id"], symbol=symbol)

        # Insert a new transaction into the history table
        db.execute("INSERT INTO history (user_id, symbol, shares, price, transacted) VALUES (:user_id, :symbol, :shares, :price, :transacted)",
                   user_id=session["user_id"], symbol=symbol, shares=-int(shares), price=stock["price"], transacted=datetime.now())

        # Commit the changes to the database
        db.commit()

        # Redirect to the home page
        return redirect("/")
    else:
        # Get a list of the symbols that the user owns
        rows = db.execute("SELECT symbol FROM portfolio WHERE user_id = :user_id AND shares > 0",
                          user_id=session["user_id"])
        symbols = [row["symbol"] for row in rows]

        # Render the sell form
        return render_template("sell.html", symbols=symbols)
