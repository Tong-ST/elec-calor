import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, jsonify, flash, get_flashed_messages
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL 

from helper import calculate_unit, apology, update_format, is_float, appliance_array, location_array

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

# Custom filter
app.jinja_env.filters["update_format"] = update_format

# Dictionary to store calculated data
calculated_data = {}

first_time_visit = True

TIME_TYPE = [
    "hour per day",
    "minute per day"
]

# import list from helper
appliance_array = appliance_array
location_array = location_array

@app.route("/", methods=["GET", "POST"])
def home():
    """Home page"""
    # Ensure no session left from last one
    if session.get("first_time", True):
        # print("Visit the first time")
        session.clear()
        session["first_time"] = False
    
    global appliance_array
    global location_array
    global calculated_data
    session_charge = session.get("charge_rate", 1.0)
    session_location = session.get("location", 'custom')
    
    if "user_id" in session and request.method != "POST":
        # If logged in, fetch user data from database
        user_data = cal_data_from_user()
        
    
    if request.method == "POST":
        update_charge_input = request.form.get("charge_rate")
        location_rate = request.form.get("location_rate")
        
        if update_charge_input:
            if not is_float(update_charge_input) and not update_charge_input.isdigit():
                return apology("Invalid input try again", "/", 400)
            
            # Update charge rate in session
            session["charge_rate"] = float(update_charge_input)
            session["location"] = location_rate
            session_charge = session.get("charge_rate", update_charge_input)
            session_location = session.get("location", 'th')
            flash(f"Charge rate updated to {update_charge_input} per kWh")
            
            if "user_id" in session:
                user_data = cal_data_from_user()
                try:
                    db.execute("INSERT INTO users_personalize (uid, charge_rate, location) VALUES (?, ?, ?)", session["user_id"], session_charge, session_location)
                except Exception as e:
                    db.execute("UPDATE users_personalize SET charge_rate = ?, location = ? WHERE uid = ?", session_charge, session_location, session["user_id"])
            
            return render_template("index.html", calculated_data=user_data if "user_id" in session else session.get("current_list", []), update_charge=session_charge, current_location=session_location, jinja_array=appliance_array, location_array=location_array)
            
        app_type = request.form.get(f'app_type')
        app_name = request.form.get(f'app_name')
        amount = request.form.get(f'amount')
        power_usage = request.form.get(f'power_usage')
        usage_per_day = request.form.get(f'usage_per_day')
        usage_type = request.form.get(f'usage_type')
        power_factor = request.form.get(f'power_factor')

        if not app_type or not app_name or not amount or not power_usage or not usage_per_day or not usage_type or not power_factor:
           return apology("Please enter all that required", "/", 400)
        
        if not is_float(power_factor):
            return apology("Invalid input try again", "/", 400)
        
        if not amount.isdigit() or not power_usage.isdigit() or not usage_per_day.isdigit():
            return apology("Invalid input try again", "/", 400)
        
        if not isinstance(app_name, str):
            return apology("Invalid input try again", "/", 400)
        
        if usage_type.lower() not in TIME_TYPE:
            return apology("Invalid input try again", "/", 400)
        
        # if app_type.lower() not in APP_TYPE:
        type_in_list = False
        for i in range(len(appliance_array)):
            if app_type.lower() == appliance_array[i][0]:
                type_in_list = True
                break
            else:
                type_in_list = False
                
        if not type_in_list:    
            return apology("input try again", "/", 400)
        
        
        amount = int(amount)
        power_usage = int(power_usage)
        usage_per_day = int(usage_per_day)
        power_factor = float(power_factor)
        
        # calculate usage per day based
        if usage_type.lower() == "hour per day":
            if usage_per_day > 24:
                return apology("Please enter less than 24 for hours", "/", 400)
            usage_per_day = usage_per_day * 60
        
        if usage_per_day > 1440:
            return apology("Please enter less than 1440 for min a day", "/", 400)
        
        # Store calculated data in session or database
        if "user_id" in session:            
            db.execute(
                "INSERT INTO users_input (uid, app_name, app_type, amount, power_usage, usage_per_day, power_factor) VALUES (?, ?, ?, ?, ?, ?, ?)",
                session["user_id"], app_name, app_type, amount, power_usage, usage_per_day, power_factor
            )
            session_charge, session_location = update_user_charge()
            user_data = cal_data_from_user()
            return render_template("index.html", calculated_data=user_data, update_charge=session_charge, current_location=session_location, jinja_array=appliance_array, location_array=location_array)
        
        else:
            # Track current input to store when user register
            if "current_input" not in session:
                session["current_input"] = []
            current_input = {
                "app_name": app_name,
                "app_type": app_type,
                "amount": amount,
                "power_usage": power_usage,
                "usage_per_day": usage_per_day,
                "power_factor": power_factor,
                "session_input_id": len(session["current_input"])
            }
            session["current_input"].append(current_input)
                
            if "current_list" not in session:
                session["current_list"] = []
            item_unit = calculate_unit(amount, power_usage, usage_per_day, power_factor)
            cal_appliance = {
                app_name: {
                    "amount": amount,
                    "unit_per_day": item_unit,
                    "power_usage": power_usage,
                    "usage_per_day": usage_per_day,
                    "power_factor": power_factor,
                    "session_item_id": len(session["current_list"])
                }
            }
            
            if "charge_rate" not in session:
                session["charge_rate"] = session_charge
            
            if "location" not in session:
                session["location"] = session_location
            
            session["current_list"].append(cal_appliance)
            calculated_data = session.get("current_list", [])
            return render_template("index.html", calculated_data=calculated_data, update_charge=session_charge, current_location=session_location, jinja_array=appliance_array, location_array=location_array)
    else:
        if "user_id" in session:
            session_charge, session_location = update_user_charge()
        else:
            session_charge = session.get("charge_rate", 1.0)
        return render_template("index.html", calculated_data=user_data if "user_id" in session else session.get("current_list", []), update_charge=session_charge, current_location=session_location, jinja_array=appliance_array, location_array=location_array)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    # session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", "/login", 403)

        elif not password:
            return apology("must provide password", "/login", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            return apology("invalid username and/or password", "/login",403)

        session["user_id"] = rows[0]["id"]
        
        flash("login successfully!")
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/about")
def about():
    if request.method == "POST":
        pass
    else:
        return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        regis_username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hashed_password = generate_password_hash(password, method='scrypt', salt_length=16)
        
        if not regis_username:
            return apology("Missing username", "/register")

        if not password:
            return apology("Missing password", "/register")

        password_length = len(password)
        if password_length < 8 or password_length > 16:
            return apology("Enter password between 8-16 char", "/register")
        
        if not password == confirmation:
            return apology("Password doesn't match", "/register")

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", regis_username, hashed_password)
        
        except Exception as e:
            return apology("Registration failed username already exist", "/register", 500) 
        
        user_id = db.execute("SELECT id FROM users WHERE username = ?", regis_username)

        # Store calculated data in database
        for item in session.get("current_input", []):
            db.execute(
                "INSERT INTO users_input (uid, app_name, app_type, amount, power_usage, usage_per_day, power_factor) VALUES (?, ?, ?, ?, ?, ?, ?)",
                user_id[0]["id"], str(item["app_name"]), str(item["app_type"]), item["amount"], item["power_usage"], item["usage_per_day"], item["power_factor"]
            )
        try:
            db.execute("INSERT INTO users_personalize (uid, charge_rate, location) VALUES (?, ?, ?)", user_id[0]["id"], session["charge_rate"] if "charge_rate" in session else 1.0, session.get("location", 'th'))
            
        except Exception as e:
            db.execute("UPDATE users_personalize SET charge_rate = ? WHERE uid = ?", session["charge_rate"] if "charge_rate" in session else 1.0, user_id[0]["id"])

        session["user_id"] = user_id[0]["id"]

        # Set session user_id after registration
        flash("Registered successfully!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/delete", methods=["POST"])
def delete_item():
    if "user_id" in session:
        item_id = request.form.get("my_item_id")
        db.execute("DELETE FROM users_input WHERE id = ? AND uid = ?", item_id, session["user_id"])
    else:
        if "current_list" in session:
            item_id = int(request.form.get("my_item_id"))
            # session["current_list"] = [item for item in session["current_list"] if list(item.values())[0]["session_item_id"] != item_id]
            for item in session.get("current_list", []):
                for v in item.values():
                    if v["session_item_id"] == item_id:
                        session["current_list"].remove(item)
                
            for item in session.get("current_input", []):
                if item["session_input_id"] == item_id:
                    session["current_input"].remove(item)
            # print("input", session.get("current_input", []))
            # print("list:", session.get("current_list", []))
    return redirect("/")


def cal_data_from_user():
    all_user_input = db.execute("SELECT id, uid, app_name, app_type, amount, power_usage, usage_per_day, power_factor FROM users_input WHERE uid = ?", session["user_id"])
            
    user_data = []
            
    for item in all_user_input:
        item_unit = calculate_unit(item["amount"], item["power_usage"], item["usage_per_day"], item["power_factor"])
                
        cal_appliance = {}
        cal_appliance[item["app_name"]] = {"amount":item["amount"], "unit_per_day":item_unit, "item_id":item["id"], "power_usage":item["power_usage"], "power_factor":item["power_factor"], "usage_per_day":item["usage_per_day"]}
        user_data.append(cal_appliance)
    return user_data

def update_user_charge():
    user_charge = db.execute("SELECT charge_rate, location FROM users_personalize WHERE uid = ?", session["user_id"])
    session_charge = user_charge[0]["charge_rate"] if user_charge else 1.0
    session_location = user_charge[0].get("location", 'th')
    return session_charge, session_location


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")