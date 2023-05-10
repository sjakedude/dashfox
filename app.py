from cgitb import text
from flask import Flask
from flask import request
from flask import Response
from datetime import datetime
import json
import os
from subprocess import check_output
from subprocess import CalledProcessError

app = Flask(__name__)

def generate_response(status, text):
    response = Response(text, status=status)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/")
def connect():
    return "DashFox Backend API is ONLINE"

# ================
# Plutonium Routes
# ================

@app.route("/plutonium/status", endpoint="plutonium_status", methods=["GET"])
def plutonium_status():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\plutonium\status.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/plutonium/gungame", endpoint="plutonium_gungame", methods=["GET"])
def plutonium_gungame():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\plutonium\select_gungame.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")

@app.route("/plutonium/domination", endpoint="plutonium_domination", methods=["GET"])
def plutonium_domination():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\plutonium\select_domination.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")

# ==========
# Git Routes
# ==========

@app.route("/git/deploy/theconeportal", endpoint="git_deploy_theconeportal", methods=["GET"])
def git_deploy_theconeportal():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\theconeportal\update.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/git/deploy/conecommons", endpoint="git_deploy_conecommons", methods=["GET"])
def git_deploy_conecommons():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\conecommons\update.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/git/deploy/dashfox", endpoint="git_deploy_dashfox", methods=["GET"])
def git_deploy_dashfox():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\dashfox\update.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")

if __name__ == "__main__":
    app.run(host="192.168.0.219", port=5000, debug=True)
