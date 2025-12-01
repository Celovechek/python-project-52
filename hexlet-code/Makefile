install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

start:
	uv run python manage.py runserver 0.0.0.0:8000

render-start:
	cd hexlet-code && gunicorn task_manager.wsgi

build:
	./build.sh
