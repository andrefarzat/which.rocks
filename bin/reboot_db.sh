rm arena/db.sqlite3
rm arena/migrations/00*.py
python3 manage.py makemigrations arena
python3 manage.py migrate
python3 manage.py createsuperuser
