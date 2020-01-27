.PHONY: dev-deps test-deps development ci-deps extras-deps style-check pretty tag-type tag-patch tag-feature package
SHELL := /bin/bash

dev-deps:
	pip install ".[dev]"

test-deps:
	pip install ".[test]"

development: dev-deps test-deps

ci-deps: dev-deps test-deps
	pip install ".[ci]"

extras-deps: dev-deps test-deps ci-deps

pretty:
	black  src/bitex
	isort --recursive src/bitex

style-check:
	flake8  src/bitex
	black --check --diff src/bitex
	isort --recursive --diff --check-only src/bitex

tag-type:
	@bash .circleci/tag_type.sh

tag-feature:
	@echo Tagging new Feature
	bumpversion minor --verbose

tag-patch:
	@echo Tagging new Patch
	bumpversion patch --verbose

package:
	@echo Creating distribution
	pip install --upgrade setuptools wheel
	python setup.py sdist bdist_wheel
	@echo Checking packaging
	pip install --upgrade twine
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ --non-interactive --skip-existing dist/*
	tox -e packaging
