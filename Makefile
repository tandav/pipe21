.PHONY: test
test:
	pytest --cov=pipe21 --doctest-glob='reference.md'

.PHONY: coverage
coverage:
	pytest --cov=pipe21 --cov-report=html
	open htmlcov/index.html

.PHONY: bumpver
bumpver:
	# usage: make bumpver PART=minor
	bumpver update --no-fetch --$(PART)
