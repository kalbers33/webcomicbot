# webcomicbot

Steps to deploy:

Setup server:
- Create database through server
python manage.py migrate

- Create superuser through django
python manage.py createsuperuser

- Import starting data for basic webcomics supported:

python manage.py loaddata start_data.json
