from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CheckoutPage:
    # Step One: Your Information
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    # Titles
    TITLE = (By.CSS_SELECTOR, ".title")

    # Step Two: Overview
    FINISH_BTN = (By.ID, "finish")

    # Complete
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    def _set_input_value(self, locator, value: str):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()

        # Limpieza fuerte
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)

        # 1) Intento humano
        el.send_keys(value)

        # 2) SIEMPRE disparar eventos para que la app "registre" el cambio
        self.driver.execute_script(
            """
            const el = arguments[0];
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            el,
        )

        # 3) Si la app igual no lo registra, setear usando el setter nativo del input
        if el.get_attribute("value") != value:
            self.driver.execute_script(
                """
                const el = arguments[0];
                const val = arguments[1];
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(el, val);
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.dispatchEvent(new Event('blur', { bubbles: true }));
                """,
                el,
                value,
            )

        # Verificación final (valor en DOM)
        assert el.get_attribute("value") == value, f"No se pudo setear el input: {locator}"
        return el

    def fill_information(self, first: str, last: str, zip_code: str):
        first_el = self._set_input_value(self.FIRST_NAME, first)
        self._set_input_value(self.LAST_NAME, last)
        zip_el = self._set_input_value(self.POSTAL_CODE, zip_code)

        # Forzar blur / change
        zip_el.send_keys(Keys.TAB)

        btn = self.wait.until(EC.presence_of_element_located(self.CONTINUE_BTN))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", btn
        )

        try:
            self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

        # Confirmar navegación a Overview
        try:
            self.wait.until(lambda d: "checkout-step-two" in d.current_url)
        except TimeoutException:
            title = self.wait.until(EC.visibility_of_element_located(self.TITLE)).text
            errors = self.driver.find_elements(*self.ERROR_MESSAGE)
            err_text = errors[0].text if errors else "No existe nodo de error"
            raise AssertionError(
                f"No avanzó a Overview. URL: {self.driver.current_url}. "
                f"Título: {title}. Error: {err_text}"
            )

    def finish(self):
        btn = self.wait.until(EC.presence_of_element_located(self.FINISH_BTN))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", btn
        )
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BTN)).click()

    def success_message(self) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(self.COMPLETE_HEADER)
        ).text

