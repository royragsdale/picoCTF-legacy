"""
Functional tests regarding user management.
"""

import pytest
import time
import api

from common import *

from api.common import safe_fail, WebException, InternalException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestFunctionalUserManagement(object):
    """
    Basic tests for user management
    """

    def setup_class(self):
        start_xvfb()
        self.driver = webdriver.Firefox()

    def teardown_class(self):
        stop_xvfb()

    def find_id(self, ID):
        return find_id_with_timeout(self.driver, ID)

    def test_site_liveness(self):
        self.driver.get(BASE_URI)
        assert "Cyberstakes" in self.driver.title, "Website does not appear to be up."

    def test_registration(self):
        """
        Tests registration functionality. Assumes that test_user does not exist.
        Deletes cookies after confirming successful registration
        """

        self.driver.get(BASE_URI)

        # make the form a registration form
        set_register = self.find_id("set-register")
        set_register.click()

        # grab the fields
        username = self.find_id("username")
        password = self.find_id("password")
        first_name = self.find_id("first-name")
        last_name = self.find_id("last-name")
        email = self.find_id("email")

        # set the fields
        username.send_keys(test_user["username"])
        password.send_keys(test_user["password"])
        first_name.send_keys(test_user["first_name"])
        last_name.send_keys(test_user["last_name"])
        email.send_keys(test_user["email"])

        # submit the form
        username.submit()

        # wait for processing
        time.sleep(1)

        assert any([cookie['name'] == "flask" for cookie in self.driver.get_cookies()]), "Could not register user."
        self.driver.delete_all_cookies()

    def test_login(self):
        """
        Tests login functionality. Assumes that test_user has been created.
        Leaves cookies set for future tests.
        """
        login_test_user(self.driver)

    def test_account_page(self):
        """
        TODO
        """
