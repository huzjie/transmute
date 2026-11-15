.PHONY: install doctor test run clean

install:
	pip install -e ".[serve]"

doctor:
	python -m transmute.cli.main doctor

test:
	pytest -q

run:
	python -m transmute.cli.main run --config config.yaml

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
