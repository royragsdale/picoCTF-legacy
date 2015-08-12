"""
Functional tests with Selenium.
"""

import pytest

from api.common import safe_fail, WebException, InternalException
from common import clear_collections, ensure_empty_collections
from common import base_team, base_user, new_team_user
from conftest import setup_db, teardown_db

from selenium import webdriver

BASE_URI = "http://127.0.0.1/"

class TestFunctionalBasic(object):
    """
    Basic tests for administrators.
    """

    def setup_class(self):
        setup_db()
        self.driver = webdriver.PhantomJS()

    def teardown_class(self):
        teardown_db()

    def test_site_liveness(self):
        self.driver.get(BASE_URI)
        assert "Cyberstakes" in self.driver.title, "Website does not appear to be up."

