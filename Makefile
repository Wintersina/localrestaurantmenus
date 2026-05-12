VENV     = .venv
PYTHON   = $(VENV)/bin/python
PIP      = $(VENV)/bin/pip
SETTINGS = localrestaurantmenus_project.settings.development
MANAGE   = DJANGO_SETTINGS_MODULE=$(SETTINGS) $(PYTHON) manage.py

-include .env
export

.PHONY: run install migrate test shell collectstatic

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

migrate: install
	$(MANAGE) migrate

run: migrate
	$(MANAGE) runserver

test: install
	$(VENV)/bin/pytest

shell: install
	$(MANAGE) shell

collectstatic: install
	$(MANAGE) collectstatic --noinput
