import hashlib
import threading
from flask import Flask, request, session, render_template, redirect, url_for
from commands import *
from data import *

app = Flask(__name__)
app.secret_key = "eg648er4g56f4g86er46gdf4g31re64ge98r4g65123s11r48w4gw56e465"

def hash_data(inp):
    if not inp:
        return ""
    encoded_inp = inp.encode("utf-8")
    return hashlib.sha256(encoded_inp).hexdigest()

# Worker function to execute commands in a background thread
def execute_commands_async(commands_list):
    for command in commands_list:
        do_command(command)

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def homepage():
    if session.get("logged_in"):
        if request.method == "POST":
            # Handles both 'Commands' and 'commands' input field names from the HTML form
            inp_command = request.form.get("Commands") or request.form.get("commands") or ""
            
            if inp_command:
                commands_list = [cmd.strip().lower() for cmd in inp_command.split("and")]
                
                # Run the command processing on a non-blocking thread
                cmd_thread = threading.Thread(
                    target=execute_commands_async, 
                    args=(commands_list,), 
                    daemon=True
                )
                cmd_thread.start()

            # PRG Pattern: Instantly redirects back so the UI stays super responsive
            return redirect(url_for("homepage"))

        return render_template("home.html")
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        raw_username = request.form.get("username", "")
        raw_password = request.form.get("password", "")

        if hash_data(raw_username) == username and hash_data(raw_password) == password:
            session["logged_in"] = True
            session["username"] = raw_username
            return redirect(url_for("homepage"))
        else:
            return redirect(url_for("invalid"))

    return render_template("login.html")

@app.route("/invalid")
def invalid():
    return render_template("invalid.html")

if __name__ == "__main__":
    app.run(debug=True, port=5887, host="0.0.0.0", use_reloader=False)
