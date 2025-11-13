import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from maps_automation.core.js_waiter import JSWaiter

class GoogleMapsPage:
    SEARCH_BOX = (By.ID, "searchboxinput")
    ZOOM_IN_BTN = (By.CSS_SELECTOR, "button[aria-label='Zoom in']")
    ZOOM_OUT_BTN = (By.CSS_SELECTOR, "button[aria-label='Zoom out']")
    INFO_PANEL = (By.CSS_SELECTOR, "div[role='region']")
    CANVAS = (By.CSS_SELECTOR, "canvas")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open_maps(self, url="https://www.google.com/maps"):
        self.driver.get(url)
        JSWaiter.wait_for_ready_state(self.driver)

    def search_location(self, location_name):
        search_box = self.wait.until(EC.presence_of_element_located(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(location_name)
        search_box.send_keys(Keys.ENTER)
        JSWaiter.wait_for_url_change(self.driver, self.driver.current_url)
        JSWaiter.wait_for_ready_state(self.driver)

    def parse_lat_lon_from_url(self):
        """Waits until Google Maps URL contains lat/lon/zoom pattern and returns them gracefully."""
        pattern = re.compile(r"@(-?\d+\.\d+),(-?\d+\.\d+),(\d+)z")

        try:
            WebDriverWait(self.driver, 10).until(lambda d: pattern.search(d.current_url))
            url = self.driver.current_url
            match = pattern.search(url)

            if match:
                lat, lon, zoom = map(float, match.groups())
                print(f"Map loaded: lat={lat}, lon={lon}, zoom={zoom}")
                return lat, lon, zoom
            else:
                print("Map URL pattern not found after waiting.")
                return None, None, None

        except Exception as e:
            print(f"Timed out waiting for map URL to update: {e}")
            return None, None, None

    def zoom_in(self):
        self.wait.until(EC.element_to_be_clickable(self.ZOOM_IN_BTN)).click()

    def zoom_out(self):
        self.wait.until(EC.element_to_be_clickable(self.ZOOM_OUT_BTN)).click()

    def is_info_panel_visible(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.INFO_PANEL))
            return True
        except:
            return False

    def do_dummy_click(self):
        search_box = self.wait.until(EC.presence_of_element_located(self.SEARCH_BOX))
        search_box.click()
        time.sleep(2)

    def pan_map(self, dx=300, dy=0):

        js_pan = f"""
        const mapDiv = document.querySelector('canvas');
        const down = new MouseEvent('mousedown', {{bubbles: true, clientX: 400, clientY: 400}});
        const move = new MouseEvent('mousemove', {{bubbles: true, clientX: {400 + dx}, clientY: {400 + dy}}});
        const up = new MouseEvent('mouseup', {{bubbles: true}});
        mapDiv.dispatchEvent(down);
        mapDiv.dispatchEvent(move);
        mapDiv.dispatchEvent(up);
        """
        self.driver.execute_script(js_pan)
        time.sleep(3)
