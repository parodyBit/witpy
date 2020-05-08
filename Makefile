test:
	pytest
test-readme:
	python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.md and HISTORY.md ok") || echo "Invalid markup in README.md or HISTORY.md!"

flake8:
	pipenv run flake8 --ignore=E501,F401,E128,E402,E731,F821 witpy

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg witpy.egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"