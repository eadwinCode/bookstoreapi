.PHONY: help docs
.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Removing cached python compiled files
	find . -name \*pyc  | xargs  rm -fv
	find . -name \*pyo | xargs  rm -fv
	find . -name \*~  | xargs  rm -fv
	find . -name __pycache__  | xargs  rm -rfv

run_local:clean ## Starts local django server
	bash scripts/run_local.sh

run_prod:clean ## Starts local django server
	bash scripts/run_prod.sh

populate_db:clean ## Populate Application DB with dummy data
	python quick_test_seeding.py

test:clean ## Run tests
	pytest .

lint:clean ## Run code linters
	black --check bookstoreapi
	isort --check bookstoreapi
	flake8 bookstoreapi

fmt format:clean ## Run code formatters
	black bookstoreapi
	isort bookstoreapi