import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class HomePage(BasePage):
    search_input = (By.NAME, "search")
    search_results = (By.CSS_SELECTOR, ".product-card")
    page_title = "Halyk Market - Выгодные покупки в рассрочку"

    def search_product(self, product_name):
        search_input = self.driver.find_element(By.CLASS_NAME, "search-input")
        search_input.clear()
        search_input.send_keys(product_name + Keys.RETURN)

    def get_search_results_title(self):
        return self.driver.find_element(By.XPATH, "//h1[@class='category-page-title']").text

    def click_first_search_result(self):
        first_search_result = self.find_element(*self.search_results)
        first_search_result.click()
        time.sleep(5)

    def get_page_title(self):
        return self.driver.title
