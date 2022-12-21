readme:
	@echo "Blackjack: by Gabriel Buchdahl & Trey Skidmore"
	@echo "Please read the readme formatted nicely on Github"
	@echo "https://github.com/gbuchdahl/474-final-blackjack#readme"
	@echo "make install-venv installs the virtual environment"
	@echo "make test runs a test script"

install-venv:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

test:
	@echo "Running test script"
	@echo "Remember to make & source the virtual environment first: `make install-venv`"
	python3 test_blackjack.py