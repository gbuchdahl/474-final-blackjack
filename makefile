readme:
	@echo "Blackjack: by Gabriel Buchdahl & Trey Skidmore"
	@echo "Please read the readme formatted nicely on Github"
	@echo "https://github.com/gbuchdahl/474-final-blackjack#readme"
	@echo "See makefile for how to install virtual environment"
	@echo "make test runs a test script"

venv:
	python3 -m venv venv

install:
	@echo "Make sure you run source venv/bin/activate"
	pip install -r requirements.txt

test:
	@echo "Running test script"
	@echo "Remember to make & source the virtual environment first"
	@echo "Please read the readme formatted nicely on Github"
	@echo "https://github.com/gbuchdahl/474-final-blackjack#readme"
	python3 test_blackjack.py