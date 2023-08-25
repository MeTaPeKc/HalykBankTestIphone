from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FavoritesPage(BasePage):
    def go_to_favorites(self):
        favorites_button = self.find_element(By.XPATH, "//*[@id='__layout']/div/header/div[2]/div/div[3]/a[1]/div")
        favorites_button.click()
