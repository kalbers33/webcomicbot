# webcomicbot

Steps to deploy:

Setup server:
- Create database through server
python manage.py migrate

- Create superuser through django
python manage.py createsuperuser

- Make migrations and apply them from project
python manage.py makemigrations
python manage.py migrate

