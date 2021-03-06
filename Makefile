.PHONY: help docs
.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Removing cached python compiled files
	find . -name \*pyc  | xargs  rm -fv
	find . -name \*pyo | xargs  rm -fv
	find . -name \*~  | xargs  rm -fv
	find . -name __pycache__  | xargs  rm -rfv

run_local: ## Starts local django server
	make clean
	bash scripts/run_local.sh

populate_db: ## Populate Application DB with dummy data
	make clean
	python quick_test_seeding.py

test: ## Run tests
	make clean
	pytest .

lint: ## Run code linters
	make clean
	black --check bookstoreapi
	isort --check bookstoreapi
	flake8 bookstoreapi

fmt format: ## Run code formatters
	make clean
	black bookstoreapi
	isort bookstoreapi