import os
from datetime import datetime
import shutil
import pytest
import tempfile
from selenium.common.exceptions import WebDriverException
from utils.driver_factory import get_driver


@pytest.fixture
def driver():
    profile_dir = tempfile.mkdtemp(prefix="selenium-profile-")
    d = get_driver(user_data_dir=profile_dir)
    yield d
    try:
        d.quit()
    finally:
        shutil.rmtree(profile_dir, ignore_errors=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Solo en fallos durante la fase "call"
    if rep.when != "call" or not rep.failed:
        return

    # Solo si el test usa el fixture "driver"
    if "driver" not in item.fixturenames:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    os.makedirs("artifacts/screenshots", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"artifacts/screenshots/{item.name}-{ts}.png"

    try:
        # Si la sesión ya murió, esto lanza excepción -> la atrapamos
        driver.save_screenshot(filename)
    except WebDriverException:
        # No convertir un fallo normal en INTERNALERROR
        pass

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Solo en fallo del "call" (no setup/teardown)
    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    screenshots_dir = os.path.join("artifacts", "screenshots")
    _ensure_dir(screenshots_dir)

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(screenshots_dir, f"{item.name}-{ts}.png")

    try:
        driver.save_screenshot(filename)
    except Exception:
        return

    # Attach a Allure (si está disponible)
    try:
        import allure
        allure.attach.file(
            filename,
            name=f"screenshot-{item.name}",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception:
        pass
