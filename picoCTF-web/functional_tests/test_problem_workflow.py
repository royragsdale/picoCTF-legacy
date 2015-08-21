"""
Functional tests regarding solving problems.
"""

import pytest
import time
import api

from common import *

from api.common import safe_fail, WebException, InternalException
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class TestFunctionalProblemWorflow(object):
    """
    Basic tests for user management.
    Assumes the test_user has been created on the server.
    """

    def setup_class(self):
        start_xvfb()
        self.driver = webdriver.Firefox()
        self.test_user = register_test_user(self.driver)

    def teardown_class(self):
        deactivate_test_user(self.driver, self.test_user)
        stop_xvfb()

    def find_id(self, ID):
        return find_id_with_timeout(self.driver, ID)

    def find_class(self, CLASS):
        return find_class_with_timeout(self.driver, CLASS)

    def find_xpath(self, XPATH):
        return find_xpath_with_timeout(self.driver, XPATH)

    def test_problems_accesible(self):
        """
        Tests that at least one problem is accessible from the problems page.
        """

        self.driver.get(BASE_URI+"problems")

        try:
            some_problem_description = self.find_class("problem-description")
        except TimeoutException as e:
            assert False, "No problems are visible to a new user."

    def test_solve_getting_started(self):
        """
        Tests if the "Getting Started!" problem from Cyberstakes can be solved.
        This test will ensure that hints are properly displayed and that challenges can be solved.
        If it does not exist, this test will fail.
        """

        self.driver.get(BASE_URI+"problems")

        try:
            problem_title = self.find_xpath('//h4[contains(text(), "Getting Started")]')
        except TimeoutException as e:
            assert False, "Getting Started is not a loaded problem."

        # gets the parent of the title, and grabs the pid from it
        pid = problem_title.find_element(By.XPATH, "..").get_attribute("data-target")[1:]

        # open the hints tab
        hints_link = self.find_xpath('//a[@class="hint-tab-button"][@data-pid="{}"]'.format(pid))
        hints_link.click()

        # ensure that the hints tab is open
        parent_li = hints_link.find_element(By.XPATH, "..")
        assert parent_li.get_attribute("class") == "active", "Hints tab is not active after clicking"

        # get the flag from the second hint
        hint_pane = self.find_id("{}hint".format(pid))
        second_hint = hint_pane.find_element(By.XPATH, ".//li[2]")
        flag = second_hint.get_attribute("innerHTML")

        # reopen the solve tab
        solve_link = self.find_xpath('//a[@class="solve-tab-button"][@data-pid="{}"]'.format(pid))
        solve_link.click()

        # ensure that the solve tab is open
        parent_li = solve_link.find_element(By.XPATH, "..")
        assert parent_li.get_attribute("class") == "active", "Solve tab is not active after clicking"

        # submit an invalid flag
        flag_input = self.find_xpath('//input[@data-pid="{}"]'.format(pid))
        flag_input.send_keys("this_is_not_the_flag")
        flag_input.submit()

        # wait for processing and re-rendering
        time.sleep(3)

        # confirm that the tab is still Unsolved
        problem_title = self.find_xpath('//h4[contains(text(), "Getting Started")]')
        right_text = problem_title.find_element(By.XPATH, ".//div").get_attribute("innerHTML")
        assert "Unsolved" in right_text, "Problem is not displayed as Unsolved"

        # submit the real flag
        flag_input = self.find_xpath('//input[@data-pid="{}"]'.format(pid))
        flag_input.send_keys(flag)
        flag_input.submit()

        # wait for processing and re-rendering
        time.sleep(3)

        # confirm that the tab is now labeled as Solved
        problem_title = self.find_xpath('//h4[contains(text(), "Getting Started")]')
        right_text = problem_title.find_element(By.XPATH, ".//div").get_attribute("innerHTML")
        assert "Solved" in right_text, "Problem is not displayed as Solved"

    def test_shell_page(self):
        """
        Tests if the first shell server can be logged into and used from the shellinabox page
        """

        self.driver.get(BASE_URI+"shell")

        # wait for shellinabox
        time.sleep(1.5)

        # first connection, just enter username to create account
        actions = ActionChains(self.driver)
        actions.send_keys(self.test_user["username"])
        actions.send_keys(Keys.ENTER)
        actions.perform()

        # login time
        time.sleep(0.5)

        # reconnect
        self.driver.get(BASE_URI+"shell")

        # wait for shellinabox
        time.sleep(1.5)

        # Our account has been created, time to log in
        actions = ActionChains(self.driver)
        actions.send_keys(self.test_user["username"])
        actions.send_keys(Keys.ENTER)
        actions.perform()

        # process time
        time.sleep(0.5)

        actions = ActionChains(self.driver)
        actions.send_keys(self.test_user["password"])
        actions.send_keys(Keys.ENTER)
        actions.perform()

        # login time
        time.sleep(0.5)

        # Our account has been created, time to log in
        actions = ActionChains(self.driver)
        actions.send_keys("whoami")
        actions.send_keys(Keys.ENTER)
        actions.perform()

        # time for command to run
        time.sleep(1.5)

        # verify that the output looks correct

        # enter the shellinabox iframe
        self.driver.switch_to.frame(self.find_xpath("//iframe[1]"))
        scrollable = self.find_id("scrollable")

        # capture all terminal output
        terminal_output = "\n".join([line.get_attribute("innerHTML") for line in scrollable.find_elements(By.XPATH, './/span')])

        assert "{}@shell:~$ whoami".format(self.test_user["username"]) in terminal_output, "Could not use webshell"
