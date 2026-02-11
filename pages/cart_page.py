from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def has_item(self, item_name: str) -> bool:
        item = (By.XPATH, f"//div[@class='inventory_item_name' and normalize-space()='{item_name}']")
        return self.wait.until(EC.visibility_of_element_located(item)).is_displayed()

    def checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()
