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
	python -m ruff format ./leetcode_study_tool
	python -m ruff check ./leetcode_study_tool --fix

format-check:
	python -m ruff format ./leetcode_study_tool --check
	python -m ruff check ./leetcode_study_tool 

test:
	pytest tests/ --cov --cov-fail-under=85

type-check:
	python -m mypy ./leetcode_study_tool
