import pytest
import os
import time
from Pages.Login_Page import LoginPage

@pytest.mark.failtest
def test_failed_login(driver, config):
    login = LoginPage(driver)
    login.open()
    username = config["users"]["locked"]["username"]
    password = config["users"]["locked"]["password"]
    os.makedirs("Screenshot", exist_ok=True)
    driver.save_screenshot("Sceenshot/screenshot_login.png")
    login.login(username, password)
    time.sleep(10)
    os.makedirs("Screenshot", exist_ok=True)
    driver.save_screenshot("Screenshot/Tc2_login_failed.png")
    loginpage = LoginPage(driver)
    Tc2_validation = config["Validation_data"]["Tc2"]
    assert Tc2_validation in loginpage.get_error()
