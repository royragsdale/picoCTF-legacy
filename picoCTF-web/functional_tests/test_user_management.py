"""
Functional tests with Selenium.
"""

import pytest

from api.common import safe_fail, WebException, InternalException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URI = "http://127.0.0.1/"

class TestFunctionalBasic(object):
    """
    Basic tests for administrators.
    """

    def setup_class(self):
        self.driver = webdriver.PhantomJS()

    def teardown_class(self):
        pass

    def test_site_liveness(self):
        self.driver.get(BASE_URI)
        assert "Cyberstakes" in self.driver.title, "Website does not appear to be up."

    def test_registration(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get(BASE_URI)
        #username_field = self.driver.find_element_by_id("username")
        #password_field = self.driver.find_element_by_id("password")

        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
