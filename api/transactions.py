# sqlalchemy import
from sqlalchemy import create_engine

# for env. imports
import os
from dotenv import load_dotenv
load_dotenv()

# import models
from api.models.product import Product

# Telegram import
from bot.bot_actions import send_tg_message

# imports for annotation
from selenium import webdriver
from typing import List


class SQLTransactions():
    ''' for cleaning table products '''

    password = os.getenv('DB_PASSWORD')
    name = os.getenv('DB_NAME')
    host = 'test_parser_db'
    user = os.getenv('DB_USER')

    # create connection
    db = create_engine(
        f'mysql://{user}:{password}@{host}/{name}')
    conn = db.connect()

    def delete_all_data(self) -> None:
        ''' clean table products'''
        self.db.execute(
            "DELETE FROM products;"
        )


def push_data_to_db(product_list: List[Product], driver: webdriver.Remote) -> None:
    ''' clean db and push product list to db '''
    SQLTransactions().delete_all_data()
    Product.objects.bulk_create(product_list)
    driver.quit()
    send_tg_message(len(product_list))
    return
