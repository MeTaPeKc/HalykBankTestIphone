from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *locator):
        return WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(locator))
