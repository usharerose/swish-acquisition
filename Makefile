.PHONY: clean-pyc

build-dev: clean-pyc
	docker-compose build swish-acquisition-build-dev

run: build-dev clean-container
	docker-compose up -d swish-acquisition-run

ssh:
	docker-compose exec swish-acquisition-run /bin/sh

test:
	pytest -sv tests/

testd: build-dev clean-test-container
	docker-compose --file docker-compose.test.yml up --exit-code-from swish-acquisition-test swish-acquisition-test

lint:
	flake8 swish_acquisition/ tests/

lintd: build-dev clean-test-container
	docker-compose --file docker-compose.test.yml up --exit-code-from swish-acquisition-lint swish-acquisition-lint

type-hint:
	mypy swish_acquisition/

type-hintd: build-dev clean-test-container
	docker-compose --file docker-compose.test.yml up --exit-code-from swish-acquisition-type-hint swish-acquisition-type-hint

clean-pyc:
	# clean all pyc files
	find . -name '__pycache__' | xargs rm -rf | cat
	find . -name '*.pyc' | xargs rm -f | cat

clean-container:
	# stop and remove useless containers
	docker-compose down --remove-orphans

clean-test-container:
	# stop and remove useless containers defined for testing
	docker-compose --file docker-compose.test.yml down --remove-orphans
