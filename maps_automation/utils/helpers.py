from math import isclose
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def coords_close(lat1, lon1, lat2, lon2, tol=0.02):
    return isclose(lat1, lat2, abs_tol=tol) and isclose(lon1, lon2, abs_tol=tol)

def is_element_present(driver, by, locator, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))
        return True
    except:
        return False
