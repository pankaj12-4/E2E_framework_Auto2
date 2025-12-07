from selenium.webdriver.common.by import By

class InventoryPage:
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    ITEMS = (By.CLASS_NAME, "inventory_item")

    def __init__(self, driver):
        self.driver = driver

    def is_logo_displayed(self):
        return self.driver.find_element(*self.APP_LOGO).is_displayed()

    def get_products(self):
        items = self.driver.find_elements(*self.ITEMS)
        return [i.text for i in items]
