.PHONY: clean-pyc clean-coverage-report

build-dev: clean-pyc clean-coverage-report
	docker-compose build swish-acquisition-build-dev

run: build-dev clean-container
	docker-compose up -d swish-acquisition-run

ssh:
	docker-compose exec swish-acquisition-run /bin/sh

test:
	python -m pytest -sv --cov-report term-missing --cov-report html:coverage_report --cov-report xml:coverage_report/cov.xml --junitxml=coverage_report/pytest.xml --cov=swish_acquisition/ --disable-warnings -p no:cacheprovider tests/

testd: build-dev clean-test-container
	docker-compose --file docker-compose.test.yml up --exit-code-from swish-acquisition-test swish-acquisition-test

lint:
	flake8 swish_acquisition/ tests/

lintd: build-dev clean-test-container
	docker-compose --file docker-compose.test.yml up --exit-code-from swish-acquisition-lint swish-acquisition-lint

type-hint:
	python -m mypy swish_acquisition/

type-hintd: build-dev clean-test-container
	docker-compose --file docker-compose.test.yml up --exit-code-from swish-acquisition-type-hint swish-acquisition-type-hint

clean-pyc:
	# clean all pyc files
	find . -name '__pycache__' | xargs rm -rf | cat
	find . -name '*.pyc' | xargs rm -f | cat

clean-coverage-report:
	rm -rf ./coverage_report .coverage

clean-container:
	# stop and remove useless containers
	docker-compose down --remove-orphans

clean-test-container:
	# stop and remove useless containers defined for testing
	docker-compose --file docker-compose.test.yml down --remove-orphans
