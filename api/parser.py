# parsing lib import
from bs4 import BeautifulSoup

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By

# import for cloudflare
import undetected_chromedriver.v2 as uc

# celery import
from celery import shared_task

# Python imports
import time
from typing import List

# import models
from api.models.product import Product

# config data import
from test_parser.settings import SITE_URL

# sqlalchemy imports
from api.transactions import push_data_to_db


class SiteParse:
    ''' class for parsing site '''    

    def __init__(self, product_count):

        self.DIFFERENCE = 36
        self.COUNTER = 0
        self.PRODUCT_LIST = []
        self.defaul_product_card_class = 'ij8 j8i'
        self.product_count = product_count

    def define_class(
            self,
            soup: BeautifulSoup,
            driver: webdriver.Remote
                    ) -> str:
        ''' for cases where classes will be changed '''
        if len(soup.find_all('div', class_=self.defaul_product_card_class)) > 0:
            return self.defaul_product_card_class
        elif len(driver.find_elements(By.XPATH, '//*[@id="paginatorContent"]/div/div/div[1]')) > 0:
            product_card = driver.find_element(By.XPATH, '//*[@id="paginatorContent"]/div/div/div[1]')
            product_card_class = product_card.get_attribute('class')
        return product_card_class

    def wait_elements(self, driver: webdriver.Remote) -> List[BeautifulSoup]:
        ''' to wait necessary elements and return them'''
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_card_class = self.define_class(soup=soup, driver=driver)
        # on last page not 36 elements
        if len(driver.find_elements("link text", "Дальше")) > 0:
            elements = soup.find_all('div', class_=product_card_class)
            while len(elements) < self.DIFFERENCE:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                elements = soup.find_all('div', class_=product_card_class)
                time.sleep(1)
        else:
            time.sleep(10)
            elements = soup.find_all('div', class_=product_card_class)
        return elements

    def get_page(self, url='https://www.ozon.ru/seller/1/products/') -> object:
        ''' got throw cloduflare'''
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        options = webdriver.FirefoxOptions()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless")
        driver = webdriver.Remote("http://firefox:4444/wd/hub", options=options)
        driver.get(url)
        while 'Just a moment' in driver.title:
            print('7')
            time.sleep(5)
            driver.get(url)
        script = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(script)
        return self.wait_elements(driver), driver

    def scrab_products(self, elements, driver):
        ''' to scrab products, add then to product_list '''
        for elem in elements:

            image = elem.find("img").get('src')
            name = elem.find("span", class_='tsBody500Medium').text
            product_url = SITE_URL + elem.find('a', class_='tile-hover-target i6l il7').get('href')
            product_url = product_url.split('?')[0]
            price = float(elem.find("span", class_='c3-a1 tsHeadline500Medium c3-b9').text[:-2].replace(" ", "").replace("\u2009", "").replace(",", "."))
            # optional for card values
            try:
                without_discount_price = int(elem.find('span', class_="c3-a1 tsBodyControl400Small c3-b0").text[:-2].replace(" ", "").replace("\u2009", ""))
            except: # bare except to not stop programm
                without_discount_price = None
            try:
                discount = int(elem.find("span", class_='tsBodyControl400Small c3-a2 c3-a7 c3-b1').text[1:-1].replace(" ", "").replace("\u2009", ""))
            except: # bare except to not stop programm
                discount = None
            try:
                rating = elem.find("span", class_='d4u').text.replace(" ", "").replace("\u2009", "")
            except: # bare except to not stop programm
                rating = None
            try:
                in_stock = int(elem.find("span", class_='e6-a4').text.replace('Осталось', '').replace('шт', '').replace(" ", "").replace("\u2009", ""))
            except: # bare except to not stop programm
                in_stock = None
            self.PRODUCT_LIST.append(
                Product(
                    name=name,
                    current_price=price,
                    without_discount_price=without_discount_price,
                    discount=discount,
                    rating=rating,
                    in_stock=in_stock,
                    image=image,
                    product_url=product_url
                )
            )
            self.COUNTER += 1
            if self.COUNTER >= self.product_count:
                push_data_to_db(driver=driver, product_list=self.PRODUCT_LIST)
                break
        return

    def scrab_page(self) -> None:
        '''scrab products '''
        if self.product_count < 36:
            self.DIFFERENCE = self.product_count
        while self.COUNTER < self.product_count:
            if (self.product_count - self.COUNTER) < 36:
                self.DIFFERENCE = self.product_count - self.COUNTER
            if self.COUNTER == 0:
                elements, driver = self.get_page()
                self.scrab_products(
                        elements=elements,
                        driver=driver
                    )
            elif len(driver.find_elements("link text", "Дальше")) > 0:
                button = driver.find_element("link text", "Дальше")
                driver.execute_script("arguments[0].click();", button)
                current_url = driver.current_url
                driver.quit()
                elements, driver = self.get_page(current_url)
                self.scrab_products(
                    elements=elements,
                    driver=driver
                    )
            else:
                push_data_to_db(driver=driver, product_list=self.PRODUCT_LIST)
                break

@shared_task
def delay_helper(product_count):
    ''' just for comfortable Celery delay task  '''
    instance = SiteParse(product_count=product_count)
    instance.scrab_page()