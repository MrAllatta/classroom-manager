include .env
export

VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python

.PHONY: venv install execute execute-watch prepare submit clean

venv:
	python -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

prepare:
	mkdir -p handoffs results deliverables tmp

execute:
	$(PYTHON) executor.py --no-watch

execute-watch:
	$(PYTHON) executor.py --watch

execute-task:
	@if [ -z "$(TASK_ID)" ]; then \
		echo "Usage: make execute-task TASK_ID=<task-id>"; \
		exit 1; \
	fi
	@echo "Executing task: $(TASK_ID)"
	$(PYTHON) executor.py --no-watch

submit-task:
	@if [ -z "$(TASK_FILE)" ]; then \
		echo "Usage: make submit-task TASK_FILE=<path-to-json>"; \
		exit 1; \
	fi
	@if [ ! -f "$(TASK_FILE)" ]; then \
		echo "Error: Task file not found: $(TASK_FILE)"; \
		exit 1; \
	fi
	@cp $(TASK_FILE) handoffs/
	@echo "✓ Task submitted from $(TASK_FILE)"
	@$(MAKE) execute

clean:
	rm -rf $(VENV) __pycache__ tmp/*.tmp
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
		
