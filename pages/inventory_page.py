from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    INVENTORY_TITLE = (By.CLASS_NAME, "title")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self) -> bool:
        return self.wait.until(EC.visibility_of_element_located(self.INVENTORY_TITLE)).is_displayed()

    @staticmethod
    def _slugify(item_name: str) -> str:
        # SauceDemo usa slug en ids: "Sauce Labs Backpack" -> "sauce-labs-backpack"
        return item_name.strip().lower().replace(" ", "-")

    def add_item_by_name(self, item_name: str):
        slug = self._slugify(item_name)
        add_btn = (By.CSS_SELECTOR, f"button[data-test='add-to-cart-{slug}']")
        self.wait.until(EC.element_to_be_clickable(add_btn)).click()

    def go_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()

