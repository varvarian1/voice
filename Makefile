VENV = venv
PYTHON = python3
PIP = $(PYTHON) -m pip

SDIR = ./src

all: $(VENV)
	python3 $(SDIR)/main.py

requirements: $(VENV)
	$(PIP) install -r requirements.txt

freeze:
	$(PIP) freeze > requirements.txt

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

rebuild:
	rm -rf $(VENV)
	$(MAKE) venv

.PHONY: all requirements freeze rebuild
