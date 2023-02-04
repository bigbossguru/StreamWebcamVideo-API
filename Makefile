format:
	pipenv run black --verbose ./

lint:
	pipenv run pylint --verbose *.py

typecheck:
	pipenv run mypy ./ --ignore-missing-imports --no-implicit-optional

pre_commit: format lint typecheck