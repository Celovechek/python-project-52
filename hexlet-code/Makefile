install:
	uv sync

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

start:
	pyclrthon manage.py runserver 0.0.0.0:8000

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh
