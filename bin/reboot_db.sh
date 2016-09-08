rm arena/db.sqlite3
rm arena/migrations/0001*.py
python manage.py makemigrations arena
python manage.py migrate
python manage.py createsuperuser
