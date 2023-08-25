from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    def get_product_title(self):
        product_title_element = self.find_element(By.XPATH, "//*[@id='product-page']/div/div/div[1]/div[2]/section/h1")
        return product_title_element.text
