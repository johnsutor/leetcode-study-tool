all:	
	@echo "Running make format"
	$(MAKE) format
	@echo "Running make format-check"
	$(MAKE) format-check
	@echo "Running make test"
	$(MAKE) test
	@echo "Running make type-check"
	$(MAKE) type-check

format:
	ruff format .
	isort --profile black .

format-check:
	ruff check .
	isort --check-only --profile black .

test:
	pytest tests/ --cov --cov-fail-under=85

type-check:
	mypy src