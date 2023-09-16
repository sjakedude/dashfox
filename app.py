from cgitb import text
from flask import Flask
from flask import request
from flask import Response
from datetime import datetime
import json
import os
import subprocess
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
        output=str(check_output("Z:\Private\conecommons\scripts\\theconeportal\\update.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/git/deploy/conecommons", endpoint="git_deploy_conecommons", methods=["GET"])
def git_deploy_conecommons():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\conecommons\\update.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/git/deploy/dashfox", endpoint="git_deploy_dashfox", methods=["GET"])
def git_deploy_dashfox():
    try:
        command = "Z:\Private\conecommons\scripts\dashfox\\update.bat"
        subprocess.Popen(["cmd", "/c", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return generate_response(200, "RESTARTING API")
    except CalledProcessError:
        return generate_response(200, "ERROR")


# ================
# Minecraft Routes
# ================

@app.route("/minecraft/status", endpoint="minecraft_status", methods=["GET"])
def minecraft_status():
    try:
        output=str(check_output("powershell Z:\Private\conecommons\scripts\minecraft\get_running_servers.ps1", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")


@app.route("/minecraft/start_ftb", endpoint="minecraft_start_ftb", methods=["GET"])
def plutonium_gungame():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\minecraft\start_minecraft_ftb_server.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")

@app.route("/minecraft/stop_ftb", endpoint="minecraft_stop_ftb", methods=["GET"])
def plutonium_domination():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\minecraft\stop_minecraft_ftb_server.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")

@app.route("/minecraft/start_latest", endpoint="minecraft_start_latest", methods=["GET"])
def plutonium_gungame():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\minecraft\start_minecraft_latest_server.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")

@app.route("/minecraft/stop_latest", endpoint="minecraft_stop_latest", methods=["GET"])
def plutonium_domination():
    try:
        output=str(check_output("Z:\Private\conecommons\scripts\minecraft\stop_minecraft_latest_server.bat", shell=True))
        return generate_response(200, output)
    except CalledProcessError:
        return generate_response(200, "ERROR")

if __name__ == "__main__":
    app.run(host="192.168.0.219", port=5000, debug=True)
