from pages.login_page import LoginPage
from utils.driver_factory import get_driver
import pytest

@pytest.mark.smoke
def test_valid_login_smoke():
    driver = get_driver()
    try:
        page = LoginPage(driver)
        page.load()
        page.login("standard_user", "secret_sauce")
        assert page.is_inventory_visible(), "No se mostró Inventario tras login válido"
    finally:
        driver.quit()

def test_valid_login_smoke(driver):
    page = LoginPage(driver)
    page.load()
    page.login("standard_user", "secret_sauce")
    assert page.is_inventory_visible()


def test_invalid_login_shows_error(driver):
    page = LoginPage(driver)
    page.load()
    page.login("standard_user", "wrong_password")
    assert "Username and password do not match" in page.get_error_message()

def test_valid_login_smoke(driver):
    page = LoginPage(driver)
    page.load()
    page.login("standard_user", "secret_sauce")
    assert page.is_inventory_visible(), "No se mostró Inventario tras login válido"


def test_invalid_login_shows_error(driver):
    page = LoginPage(driver)
    page.load()
    page.login("standard_user", "wrong_password")

    msg = page.get_error_message()
    assert "Username and password do not match" in msg, f"Mensaje inesperado: {msg}"

