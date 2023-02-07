format:
	pipenv run black --verbose ./

lint:
	pipenv run pylint --verbose *.py

typecheck:
	pipenv run mypy ./ --ignore-missing-imports --no-implicit-optional

pre_commit: format lint typecheck

docker_build:
	docker build --no-cache -t fast-server .
docker_run:
	docker run -d --name fastcontainer -p 80:80 fast-server