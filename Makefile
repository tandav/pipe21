test:
	python3 -m pytest -v tests

clean:
	rm -rf build dist pipe21.egg-info

build: clean
	python3 setup.py sdist bdist_wheel
	twine check dist/*

publish: build
	twine upload dist/*

publish_test: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
