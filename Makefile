render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

start:
	uv run python manage.py runserver

test:
	uv run python manage.py test

fixtures:
	uv run python manage.py dumpdata auth.User --indent 2 > task_manager/fixtures/users.json
