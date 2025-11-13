import pytest
from maps_automation.core.driver_factory import create_driver

#this fixture will take care of setup & teardown process of chrome driver
@pytest.fixture(scope="session")
def driver():
    driver = create_driver(headless=False)
    yield driver
    driver.quit()
