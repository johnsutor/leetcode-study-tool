.PHONY: all format format-check test type-check sync install clean

all:	
	@echo "Running make format"
	$(MAKE) format
	@echo "Running make format-check"
	$(MAKE) format-check
	@echo "Running make test"
	$(MAKE) test
	@echo "Running make type-check"
	$(MAKE) type-check

sync:
	uv sync --dev

install:
	uv sync

clean:
	rm -rf .venv

format:
	uv run ruff format ./leetcode_study_tool
	uv run ruff check ./leetcode_study_tool --fix

format-check:
	uv run ruff format ./leetcode_study_tool --check
	uv run ruff check ./leetcode_study_tool 

test:
	uv run pytest tests/ --cov --cov-fail-under=85

type-check:
	uv run mypy ./leetcode_study_tool
