A Shopping App Using Python and Django
======================================

## Introduction
This application provides Ecommerce features where it handles as below:
- There are three types of users
  - Admin (Administrator, Django provides superuser)
    - Admin handle entire website like: CURD operation over Category and Products
    - After [logging](http://localhost:8000/admin) from admin he/she can manage product enventry like:
    - ### Category
        - [Category Listing](http://localhost:8000/category/list/)
        - [Create Category](http://localhost:8000/category/create/)
        - Update
        - Delete
    - ### Product
        - [Product Listing](http://localhost:8000/product/list/)
        - [Create Product](http://localhost:8000/product/create/)
        - Update
        - Delete
  - Customer
    - Customer can create account from [here](http://localhost:8000/signup/)
    - After logging he/she can checkout and can see Orders listing
  - Anonymous
    - This is guest user only he/she can product listing, categories, product details, and cart details
    - For chechout cart items he/she have to signup.

## Dependencies
 - python >=3.10.x or above
 - pip >=23.x.x or above (latest)
 - MySql (mariadb-server database)
 - After setup maria-server, create a database and update it in `DATABASES` section setting.py 
 - mysqlclient (pip install mysqlclient)
 - [django_sass](https://pypi.org/project/django-sass/)
 - [bootstrap5](https://pypi.org/project/django-bootstrap5/)
 - [pilow](https://pypi.org/project/pillow/)

## How to install run
After resolving above dependencies, follow below steps:
```bash
cd ROOT-DIR
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```` 

http://localhost:8000