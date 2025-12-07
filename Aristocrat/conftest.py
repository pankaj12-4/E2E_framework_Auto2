import tempfile

import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

# @pytest.fixture
# def driver():
#     chrome_options = Options()
#
#     # 1) Completely new temporary profile (no saved passwords)
#     temp_profile_dir = tempfile.mkdtemp()
#     chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")
#
#     # 2) Disable password manager + its bubbles
#     prefs = {
#         "credentials_enable_service": False,
#         "profile.password_manager_enabled": False,
#     }
#     chrome_options.add_experimental_option("prefs", prefs)
#
#     # 3) Extra flags to avoid password / leak popups
#     chrome_options.add_argument("--disable-save-password-bubble")
#     chrome_options.add_argument(
#         "--disable-features=PasswordManagerOnboarding,PasswordLeakDetection"
#     )
#
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.maximize_window()
#     yield driver
#     driver.quit()

