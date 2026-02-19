import pytest
import allure

from pages.login_page import LoginPage


@allure.epic("E-Commerce Platform")
@allure.feature("Authentication")
@allure.story("Valid login")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Login with valid credentials")
def test_valid_login_smoke(driver):
    page = LoginPage(driver)
    page.load()
    page.login("standard_user", "secret_sauce")
    assert page.is_inventory_visible(), "No se mostró Inventario tras login válido"


@allure.epic("E-Commerce Platform")
@allure.feature("Authentication")
@allure.story("Invalid login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login with invalid credentials shows error")
def test_invalid_login_shows_error(driver):
    page = LoginPage(driver)
    page.load()
    page.login("standard_user", "wrong_password")

    msg = page.get_error_message()
    assert "Username and password do not match" in msg
