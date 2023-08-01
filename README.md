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
To get list of products from bot just send text "Список товаров".

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

# * about parsing. 

There is a method [define_class](https://github.com/romashovdmitry/login-test-o-parser/blob/f7bbae15c69d8020695856b861280f58522ff517/api/parser.py#L39-L50) in class SiteParse. This method has been designed to handle scenarios where the class for the tag has been modified or changed. In such cases, if the application is unable to locate the product by class, it will fallback to searching by XPath.

The ideal approach is to implement this fallback check for all elements in the application. It aims to follow a priority-based strategy as follows:

1. Check by Style: Initially, try locating elements using the style attribute.
2. XPath Fallback: If the element is not found by style, attempt to find it using XPath.
3. Selector Fallback: If the element cannot be found by XPath, try locating it using the CSS selector.
