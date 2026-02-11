import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



def get_driver(headless: bool | None = None, user_data_dir: str | None = None):
    if headless is None:
        headless = os.getenv("HEADLESS", "1") == "1"  # default: headless ON

    options = Options()

    # Evitar prompts/password manager/leak detection
    options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--password-store=basic")
    options.add_argument("--use-mock-keychain")
    options.add_argument("--disable-notifications")

    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            # en algunos builds ayuda:
            "profile.password_manager_leak_detection": False,
        },
    )

    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)
    return driver
