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


@app.route("/status_pihole", endpoint="status_pihole", methods=["GET"])
def status_pihole():
    try:
        dir=str(check_output("docker ps", shell=True))
        if "pihole" in dir:
            return generate_response(200, "ONLINE")
        else:
            return generate_response(200, "OFFLINE")
    except CalledProcessError:
        return generate_response(200, "OFFLINE")


@app.route("/status_httpd", endpoint="status_httpd", methods=["GET"])
def status_httpd():
    try:
        process_list=str(check_output("tasklist", shell=True))
        if "httpd.exe" in process_list:
            return generate_response(200, "ONLINE")
        else:
            return generate_response(200, "OFFLINE")
    except CalledProcessError:
        return generate_response(200, "OFFLINE")


@app.route("/status_docker", endpoint="status_docker", methods=["GET"])
def status_docker():
    try:
        process_list=str(check_output("tasklist", shell=True))
        if "docker.exe" in process_list:
            return generate_response(200, "ONLINE")
        else:
            return generate_response(200, "OFFLINE")
    except CalledProcessError:
        return generate_response(200, "OFFLINE")

@app.route("/status_mouse", endpoint="status_mouse", methods=["GET"])
def status_mouse():
    try:
        process_list=str(check_output("tasklist", shell=True))
        if "Mobile Mouse.exe" in process_list:
            return generate_response(200, "ONLINE")
        else:
            return generate_response(200, "OFFLINE")
    except CalledProcessError:
        return generate_response(200, "OFFLINE")

@app.route("/status_gungame", endpoint="status_gungame", methods=["GET"])
def status_gungame():
    try:
        process_list=str(check_output("tasklist", shell=True))
        if "Plutonium.exe" in process_list:
            return generate_response(200, "ONLINE")
        else:
            return generate_response(200, "OFFLINE")
    except CalledProcessError:
        return generate_response(200, "OFFLINE")

if __name__ == "__main__":
    app.run(host="192.168.0.219", port=5000, debug=True)
