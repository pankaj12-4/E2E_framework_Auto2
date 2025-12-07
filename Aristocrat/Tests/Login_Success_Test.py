import pytest
import os
from Pages.Login_Page import LoginPage
from Pages.Inventory_Page import InventoryPage

@pytest.mark.success
def test_success_login(driver, config):
    login = LoginPage(driver)
    login.open()
    os.makedirs("Screenshot", exist_ok=True)
    driver.save_screenshot("Screenshot/ss_before_login.png")
    # Get username and password from YAML
    username = config["users"]["standard"]["username"]
    password = config["users"]["standard"]['password']
    login.login(username, password)
    os.makedirs("Screenshot", exist_ok=True)
    driver.save_screenshot("screenshot_login.png")
    inventory = InventoryPage(driver)
    Tc1_validation = config["Validation_data"]["Tc1"]
    assert inventory.is_logo_displayed(), Tc1_validation
