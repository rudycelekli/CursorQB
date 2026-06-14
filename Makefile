.PHONY: check test

check:
	bash scripts/validate.sh

test:
	python3 -m unittest discover -s tests -v
