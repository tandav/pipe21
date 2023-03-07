.PHONY: test
test:
	python -m pytest -v --cov=pipe21 tests

.PHONY: coverage
coverage:
	python -m pytest --asyncio-mode=strict --cov=pipe21 --cov-report=html tests
	open htmlcov/index.html

.PHONY: bumpver
bumpver:
	# usage: make bumpver PART=minor
	bumpver update --no-fetch --$(PART)
