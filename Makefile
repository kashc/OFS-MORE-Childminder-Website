-include .makerc

run:
	$(PYTHON_CMD) manage.py runserver --settings=$(PROJECT_SETTINGS)
test:
	$(PYTHON_CMD) manage.py test --settings=$(PROJECT_SETTINGS)
install:
	$(PIP_CMD) install -r requirements.txt
migrate:
	$(PYTHON_CMD) manage.py makemigrations --settings=$(PROJECT_SETTINGS)
	$(PYTHON_CMD) manage.py migrate --settings=$(PROJECT_SETTINGS)
static:
	$(PYTHON_CMD) manage.py collectstatic --settings=$(PROJECT_SETTINGS)
