all: init test sphinx

init:
	easy_install tox coverage Sphinx

test:
	coverage erase
	tox
	coverage html

docs: sphinx

sphinx:
	python setup.py build_sphinx
