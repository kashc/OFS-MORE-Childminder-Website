-include .makerc

run:
	$(PYTHON_CMD) manage.py runserver --settings=childminder.settings.dev
test:
	$(PYTHON_CMD) manage.py test --settings=childminder.settings.dev
install:
	$(PIP_CMD) install -r requirements.txt
migrate:
	$(PYTHON_CMD) manage.py makemigrations --settings=childminder.settings.dev
	$(PYTHON_CMD) manage.py migrate --settings=childminder.settings.dev
static:
	$(PYTHON_CMD) manage.py collectstatic --settings=childminder.settings.dev
