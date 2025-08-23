PY=python
PIP=pip

.PHONY: setup test run fmt

setup:
	$(PY) -m venv .venv && . .venv/bin/activate && $(PIP) install -r requirements.txt

test:
	python -m pytest tests/test_smoke.py

run:
	$(PY) main.py "What is 12.5% of 243?"

fmt:
	@echo "Add your formatter here (e.g., black/isort)"
