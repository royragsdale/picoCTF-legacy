"""
Functional tests regarding solving problems.
"""

import pytest
import time
import api

from common import *

from api.common import safe_fail, WebException, InternalException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestFunctionalProblemWorflow(object):
    """
    Basic tests for user management.
    Assumes the test_user has been created on the server.
    """

    def setup_class(self):
        start_xvfb()
        self.driver = webdriver.Firefox()

    def teardown_class(self):
        stop_xvfb()

    def find_id(self, ID):
        return find_id_with_timeout(self.driver, ID)

    def test_problems_accesible(self):
        """
        Tests that at least one problem is accessible from the problems page.
        """

        self.driver.get(BASE_URI+"problems")
