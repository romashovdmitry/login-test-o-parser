# Django imports
from django.core.management.base import BaseCommand

# telegram lib imports
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# config data import
from test_parser.settings import TELEGRAM_TOKEN

# custom Telegram foo import
from bot.bot_actions import return_last_parsing, start


class CustomFilter(filters.MessageFilter):
    ''' custom filter for message Список товаров '''
    def filter(self, message):
        return message.text == 'Список товаров'
    

class Command(BaseCommand):
    ''' Django command for starting Telegram bot '''
    def handle(self, *args, **kwargs):
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        app.add_handler(CommandHandler('start', start))

        app.add_handler(MessageHandler(CustomFilter(), return_last_parsing))

        app.run_polling(pool_timeout=1)