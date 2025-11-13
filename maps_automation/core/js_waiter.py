from selenium.webdriver.support.ui import WebDriverWait

class JSWaiter:
    @staticmethod
    def wait_for_ready_state(driver, timeout=20):
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @staticmethod
    def wait_for_url_change(driver, old_url, timeout=20):
        WebDriverWait(driver, timeout).until(lambda d: d.current_url != old_url)