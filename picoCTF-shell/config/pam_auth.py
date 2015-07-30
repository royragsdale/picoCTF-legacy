import os
import pwd
import grp
import requests
import json
import subprocess
import time

from imp import load_source
from os.path import join

DEFAULT_USER    = "nobody"
HACKSPORTS_ROOT = "/opt/hacksports/"
COMPETITORS_GROUP = "competitors"

config = load_source("config", join(HACKSPORTS_ROOT, "config.py"))
SERVER = config.WEB_SERVER
TIMEOUT=5

pamh = None

def run_login(user, password):
    r = requests.post(SERVER+"/api/user/login", data={"username": user, "password": password}, timeout=TIMEOUT)
    return str(json.loads(r.text)['message'])

def display(string):
    message = pamh.Message(pamh.PAM_TEXT_INFO, string)
    pamh.conversation(message)

def prompt(string):
    message = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, string)
    return pamh.conversation(message)

def server_user_exists(user):
    result = run_login(user, "`&/")
    return result == "Incorrect password"

def pam_sm_authenticate(pam_handle, flags, argv):
    global pamh
    pamh = pam_handle

    try:
        user = pamh.get_user(None)
    except pamh.exception, e:
        return e.pam_result

    try:
        entry = pwd.getpwnam(user)
        group = grp.getgrnam(COMPETITORS_GROUP)
        # local account exists and server account exists
        if server_user_exists(user) and user in group.gr_mem:
            response = prompt("Enter your password: ")
            result = run_login(user, response.resp)

            if "Successfully logged in" in result:
                return pamh.PAM_SUCCESS
        else:
            return pamh.PAM_USER_UNKNOWN

    # local user account does not exist
    except KeyError as e:
        try:
            if server_user_exists(user):
                subprocess.check_output(["/usr/sbin/useradd", "-m", "-G", COMPETITORS_GROUP, "-s", "/bin/bash", user])
                display("Welcome {}!".format(user))
                display("Your shell server account has been created.")
                prompt("Please press enter and reconnect.")

                # this causes the connection to close
                return pamh.PAM_SUCCESS
            else:
                display("Please make an account on the web site first.")
                return pamh.PAM_USER_UNKNOWN

        except Exception as e:
            pass

    return pamh.PAM_AUTH_ERR
