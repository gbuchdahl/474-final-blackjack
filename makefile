readme:
	@echo "Blackjack: by Gabriel Buchdahl & Trey Skidmore"
	@echo "Please read the readme formatted nicely on Github"
	@echo "https://github.com/gbuchdahl/474-final-blackjack#readme"

install-venv:
	python3 -m venv venv
	pip install -r requirements.txt
	source venv/bin/activate

test:
	@echo "Running test script"
	@echo "Remember to make & source the virtual environment first"
	python3 test_blackjack.py