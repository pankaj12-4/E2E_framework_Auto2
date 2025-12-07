import pytest
import yaml
from selenium import webdriver

@pytest.fixture(scope="session")
def config():
    with open("Config/Global_Data_and_validation.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture
def driver():
    driver = webdriver.Edge()
    # driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
