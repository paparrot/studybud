start:
	python3 manage.py runserver

migrate:
	python3 manage.py migrate

migration:
	python3 manage.py makemigrations

show migrations:
	python3 manage.py showmigrations

create admin:
	python3 manage.py createsuperuser