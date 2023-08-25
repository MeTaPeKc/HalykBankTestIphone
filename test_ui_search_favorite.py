import re

from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from time import sleep

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.favorites_page import FavoritesPage
import unittest


class TestUISearchAndFavorite(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.halykmarket.kz/")
        self.wait_time = 60  # Устанавливаем время ожидания

        self.home_page = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.favorites_page = FavoritesPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_search_and_favorite(self):

        # Проверка заголовка страницы
        expected_title = "Halyk Market - Выгодные покупки в рассрочку"
        actual_title = self.home_page.get_page_title()
        assert expected_title == actual_title
        sleep(1)

        # Проверить, что есть результаты поиска.
        self.home_page.search_product("iPhone 14 Pro 128 Deep Purple")
        sleep(1)
        search_title_text = self.home_page.get_search_results_title()
        assert search_title_text == "По запросу «iPhone 14 Pro 128 Deep Purple» найдено"
        sleep(1)

        self.home_page.click_first_search_result()
        sleep(1)

        class CustomError(Exception):
            """Класс для пользовательской ошибки."""

            def __init__(self, message):
                self.message = message
                super().__init__(self.message)

        try:
            expected_product_title = "Смартфон Apple iPhone 14 Pro 128Gb Deep Purple"
            actual_product_title = self.product_page.get_product_title()
            if actual_product_title != expected_product_title:
                raise CustomError(f"Ожидалось: {expected_product_title}, Фактически: {actual_product_title}")
        except CustomError as e:
            self.fail(f"Ошибка: {e}")

        try:
            # Найти кнопку "Избранное" на странице продукта и кликнуть по ней
            favorite_button = self.driver.find_element(By.XPATH,
                                                       "//*[@id='product-page']/div/div/div[1]/div[2]/div/button[2]")
            favorite_button.click()
        except NoSuchElementException:
            self.fail("Кнопка 'Избранное' не найдена на странице продукта")

        try:
            favorite_button = self.driver.find_element(By.XPATH,
                                                       "//*[@id='product-page']/div/div/div[1]/div[2]/div/button[2]")
            if favorite_button.get_attribute("disabled") == "true":
                print("Кнопка 'Избранное' недоступна для нажатия")
            else:
                favorite_button.click()
        except NoSuchElementException:
            self.fail("Кнопка 'Избранное' не найдена на странице продукта")

        try:
            favorite_button = self.driver.find_element(By.XPATH,
                                                       "//*[@id='product-page']/div/div/div[1]/div[2]/div/button[2]")
            if favorite_button.get_attribute("disabled") == "true":
                print("Кнопка 'Избранное' недоступна для нажатия")
            else:
                favorite_button.click()
                print("Продукт успешно добавлен в избранное")
        except NoSuchElementException:
            self.fail("Кнопка 'Избранное' не найдена на странице продукта")

        try:
            wait = WebDriverWait(self.driver, 10)  # Ожидание до 10 секунд
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='__layout']/div/header/div[2]/div/div[3]/a[1]/div")))
            print("Продукт успешно добавлен в избранное (визуально)")
        except TimeoutException:
            self.fail("Продукт не был успешно добавлен в избранное (визуально)")

        # Получение названия товара на странице карточки товара
        product_title_card = self.product_page.find_element(By.XPATH,
                                                            "//*[@id='product-page']/div/div/div[1]/div[2]/section/h1").text

        # Получение цены товара на странице карточки товара
        js_path_card = "#product-page > div > div > div.product-wrap > div.product-desc > section > " \
                       "div.desc-price-wrap > div:nth-child(1) > div.desc-price-value"
        product_price_card = self.driver.execute_script(
            f"return document.querySelector('{js_path_card}').textContent.trim();")
        print("Цена на карточке товара:", product_price_card)

        # Перейти в раздел избранных
        self.favorites_page.go_to_favorites()

        # Ожидание, чтобы убедиться, что страница избранных загрузилась
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='__layout']/div/main/div/div/div[2]/div/div/div/div[2]/div[1]")))

        # Получение названия товара на странице избранных
        product_title_favorites = self.driver.find_element(By.XPATH,
                                                           "//*[@id='__layout']/div/main/div/div/div["
                                                           "2]/div/div/div/div[2]/div[1]").text

        # Получение цены товара на странице избранных
        js_path_favorites = "#__layout > div > main > div > div > div.favorite-body > div > div > div > " \
                            "div.product-card-content > div.product-card-pay > span.product-card-value-value"
        product_price_favorites = self.driver.execute_script(
            f"return document.querySelector('{js_path_favorites}').textContent.trim();")
        print("Цена в избранном:", product_price_favorites)

        # Сравнение названий товаров
        if product_title_card == product_title_favorites:
            print("Название продукта в избранном совпадает с названием продукта на карточке.")
        else:
            self.fail("Название продукта в избранном не совпадает с названием продукта на карточке.")

        product_price_card_clean = re.sub(r'\D', '', product_price_card)
        product_price_favorites_clean = re.sub(r'\D', '', product_price_favorites)

        # Сравнение строк с ценами
        if product_price_card_clean == product_price_favorites_clean:
            print("Цена продукта в избранном совпадает с ценой продукта на карточке.")
        else:
            self.fail("УПС! цены то не совпадают")
