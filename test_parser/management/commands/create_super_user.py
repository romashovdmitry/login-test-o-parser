# Django import
from django.core.management.base import BaseCommand

# import models
from django.contrib.auth.models import User

# .env libs import
import os
from dotenv import load_dotenv
load_dotenv()

class Command(BaseCommand):
    """autocreate superuser"""
    def handle(self, *args, **options):

        username = os.getenv('SUPER_USERNAME')
        password = os.getenv('SUPER_PASSWORD')
        email = os.getenv('SUPER_EMAIL')

        if not User.objects.filter(username=username).exists():

            User.objects.create_superuser(
                username=username, 
                email=email, 
                password=password
            )