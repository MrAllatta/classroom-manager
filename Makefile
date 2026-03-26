include .env
export

VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python

.PHONY: VENV

venv:
		python -m venv $(VENV)

install: venv
		$(PIP) install -r requirements.txt

execute:
		$(PYTHON) executor.py --no-watch

prepare:
		mkdir -p handoffs results deliverables tmp

watch:
		$(PYTHON) executor.py
		
