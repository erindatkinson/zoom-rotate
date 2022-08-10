install:
	pipenv install

get:
	pipenv run ./main.py download

.PHONY: install get
