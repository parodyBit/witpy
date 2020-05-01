init:
	pip install pipenv --upgrade
	pipenv install --dev
test-readme:
	@pipenv run python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.md and HISTORY.md ok") || echo "Invalid markup in README.md or HISTORY.md!"
test:
	tox
ci:
	pipenv run py.test
publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info