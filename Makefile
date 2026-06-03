
install:

run:

debug:

clean:

lint:
	source venv/bin/activate\
	&& flake8 .\
	&& mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports\
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	source venv/bin/activate\
	&& flake8 .\
	&& mypy --strict .
