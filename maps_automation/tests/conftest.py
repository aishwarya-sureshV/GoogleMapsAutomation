import pytest
from maps_automation.core.driver_factory import create_driver

@pytest.fixture(scope="session")
def driver():
    driver = create_driver(headless=False)
    yield driver
    driver.quit()
