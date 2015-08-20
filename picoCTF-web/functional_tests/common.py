"""
Common fields used in functional tests
"""

import os
import time

from subprocess import Popen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

BASE_URI = "http://127.0.0.1/"
TIMEOUT = 10

test_user = {
    "username": "testuser",
    "password": "testpassword",
    "first_name": "test",
    "last_name": "user",
    "email": "test@test.test",
}

xvfb_process = None

def start_xvfb():
    global xvfb_process
    # run an x virtual frame buffer so firefox can run headlessly
    xvfb_process = Popen(["Xvfb", ":40", "-ac"])
    os.environ["DISPLAY"] = ":40"

def stop_xvfb():
    global xvfb_process
    xvfb_process.kill()

def find_id_with_timeout(driver, ID, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, ID))
    )

def login_test_user(driver):
    driver.get(BASE_URI)

    # grab the fields
    username = find_id_with_timeout(driver, "username")
    password = find_id_with_timeout(driver, "password")

    # set the fields
    username.send_keys(test_user["username"])
    password.send_keys(test_user["password"])

    # submit the form
    username.submit()

    # wait for processing
    time.sleep(1)

    assert any([cookie['name'] == "flask" for cookie in driver.get_cookies()]), "Could not login user."
