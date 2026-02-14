import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.epic("E2E Web")
@allure.feature("Checkout")
@allure.story("Compra completa exitosa")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_checkout_smoke_e2e(driver):
    item = "Sauce Labs Backpack"

    login = LoginPage(driver)
    login.load()
    with allure.step("Login con usuario estándar"):
        login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.is_loaded(), "Inventory no cargó tras login"
    with allure.step("Agregar producto al carrito"):
        inventory.add_item_by_name(item)
    inventory.go_to_cart()

    cart = CartPage(driver)
    assert cart.has_item(item), "El item no está en el carrito"
    with allure.step("Finalizar compra"):
        cart.checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_information("Rai", "Moliner", "00000")
    checkout.finish()

    assert "Thank you for your order!" in checkout.success_message()
