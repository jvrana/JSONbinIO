PIP=pip3

init:
	$(PIP) install pipenv --upgrade
	pipenv install --dev --skip-lock

lock:
	pipenv lock -r > requirements.txt
	pipenv lock -r > requirements-dev.txt
	pipenv lock --dev -r >> requirements-dev.txt
