rm mysite/db.sqlite3
rm mysite/migrations/00*.py
python3 manage.py makemigrations mysite
python3 manage.py migrate
python3 manage.py createsuperuser
