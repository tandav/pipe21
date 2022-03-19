python := python3.10

LINTING_DIRS := pipe21 tests


.PHONY: lint
lint:
	#$(python) -m no_init $(LINTING_DIRS)
	$(python) -m force_absolute_imports --in-place $(LINTING_DIRS)
	$(python) -m isort --force-single-line-imports $(LINTING_DIRS)
	#$(python) -m autoflake --recursive --in-place $(LINTING_DIRS)
	#$(python) -m autopep8 --in-place --recursive --aggressive --ignore=E221,E401,E402,E501,W503,E701,E704,E721,E741,I100,I201,W504 --exclude=musictool/util/wavfile.py $(LINTING_DIRS)
	$(python) -m unify --recursive --in-place $(LINTING_DIRS)
	#$(python) -m flake8 --ignore=E221,E501,W503,E701,E704,E741,I100,I201,W504 --exclude=musictool/util/wavfile.py $(LINTING_DIRS)

.PHONY: check-mypy
check-mypy:
	$(python) -m mypy --config-file pyproject.toml $(LINTING_DIRS)

.PHONY: test
test:
	$(python) -m pytest -vv --asyncio-mode=strict tests

.PHONY: coverage
coverage:
	$(python) -m pytest --asyncio-mode=strict --cov=pipe21 --cov-report=html tests
	open htmlcov/index.html
