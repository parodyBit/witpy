init:
	pip install pipenv --upgrade
	pipenv install --dev
test:
	pytest tests/*
ci:
	pipenv run py.test -n 8 --boxed --junitxml=report.xml
publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info