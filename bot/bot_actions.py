# Python import
import requests

# telegram imports
from telegram import Update
from telegram.ext import Updater, CallbackContext, ContextTypes
import telegram

# import models
from api.models.product import Product

# config data import
from test_parser.settings import TELEGRAM_ADMIN_ID, TELEGRAM_TOKEN

# for annotation imports
from typing import List

# async imports
from asgiref.sync import sync_to_async


async def return_last_parsing(update: Update, context: CallbackContext):
    ''' return for bot list of last parsing result '''
    products = await sync_to_async(list)(Product.objects.all())
    result = ''
    i = 0
    while i < len(products):
        result += f'{i+1}. {products[i].name}: {products[i].product_url}\n'
        if (i+1) % 10 == 0:
            await update.message.reply_text(result)
            result = ''
        i += 1
    if result:
        await update.message.reply_text(result)


async def start(update: Updater, context: ContextTypes.DEFAULT_TYPE):
    ''' just for start command '''
    await update.message.reply_text('HELLO!')


def send_tg_message(saved_product_counter) -> None:
    ''' synchronic send message to Telegram admin '''
    chat_id = TELEGRAM_ADMIN_ID
    api_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': 'Задача на парсинг товаров с сайта Ozon завершена.\n'
            f'Сохранено {saved_product_counter}'
    }
    requests.post(url=api_url, params=params)
