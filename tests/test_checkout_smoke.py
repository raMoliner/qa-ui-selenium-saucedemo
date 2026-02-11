from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
import pytest

@pytest.mark.smoke
def test_checkout_smoke_e2e(driver):
    item = "Sauce Labs Backpack"

    login = LoginPage(driver)
    login.load()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.is_loaded(), "Inventory no cargó tras login"
    inventory.add_item_by_name(item)
    inventory.go_to_cart()

    cart = CartPage(driver)
    assert cart.has_item(item), "El item no está en el carrito"
    cart.checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_information("Rai", "Moliner", "00000")
    checkout.finish()

    assert "Thank you for your order!" in checkout.success_message()
