# Ozon parser

DRF API Service for parsing products on Ozon. 

## Quick Start

1. Clone the repository

```
git init
git clone https://github.com/romashovdmitry/login-test-o-parser.git
```
2. There is a file example.env. Open this file, pass your comfortable values to variables and change name to .env, in particular to pass you Telegram Token and Telegram chat_id. 

3. Run docker-compose 

```
docker-compose up
```

4. Create a superuser to access the Django admin panel

```
docker ps
```

Copy container id of image "test_parser-django_test_parser" and put instead of CID

```
docker exec -t -i CID bash
python3 manage.py createsuperuser
```

Create username and password. 

5. Open [admin panel](http://127.0.0.1:8000/admin/), authorize as admin. 

Open [Swagger page](http://127.0.0.1:8000/docs/). 

Parse Ozon, enjoy products and get notifications by Telegram!

## Stack

- [ ] Docker, docker compose for containerization
- [ ] Framework: Django
- [ ] API: Django Rest Framework (DRF)
- [ ] Database: MySQL
- [ ] Swagger for describing implemented methods in OpenAPI format
- [ ] Celery: asynchronous message processing
- [ ] Python Telegram Bot: for processing updates from bot
- [ ] Selenuim: for loading pages and navigation throw them
- [ ] Beautifulsoup: for processing DOM

## API Endpoints

- /v1/products/
    - GET: get list of all campaigns
    - POST: create new campaign
- /v1/products/{id}
    - GET: retrieve information about a single product by id
