init:
	pip install pipenv --upgrade
	pipenv install --dev
test:
	pytest tests/*
ci:
	pipenv run py.test -n 8 --boxed --junitxml=report.xml