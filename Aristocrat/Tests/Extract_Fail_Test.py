import time
import pytest
import os
from Pages.Login_Page import LoginPage
from Pages.Inventory_Page import InventoryPage


@pytest.mark.extract
def test_extract_data(driver, config):
    login = LoginPage(driver)
    login.open()
    #username and password from YAML
    username = config["users"]["standard"]["username"]
    password = config["users"]["standard"]['password']
    login.login(username, password)
    os.makedirs("Screenshot", exist_ok=True)
    driver.save_screenshot("Screenshot/tc3_after_login.png")
    inventory = InventoryPage(driver)
    products = inventory.get_products()
    os.makedirs("Screenshot", exist_ok=True)
    driver.save_screenshot("Screenshot/tc3_get_products.png")
    with open("products.txt", "w") as f:
        for item in products:
            f.write(item + "\n")
    os.makedirs("Screenshot", exist_ok=True)
    driver.save_screenshot("Screenshot/tc3_product_file.png")
    time.sleep(3)
    driver.find_element("id", "react-burger-menu-btn").click()
    time.sleep(3)
    driver.find_element("id", "logout_sidebar_link").click()
    Tc3_validation = config["Validation_data"]["Tc3"]
    assert Tc3_validation in driver.current_url


