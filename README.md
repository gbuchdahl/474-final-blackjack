# Blackjack

By: Gabriel Buchdahl & Trey Skidmore

### To Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python test_blackjack.py
```

### What's included

- Modules to represent cards, hand, shoe in `cards.py`
- Implmentation of the game in `blackjack.py`

### Strategies

Implement your strategy by extending the `BlackjackStrategy` class.

- All you need to implement is the `select_action` and `select_bet_size` methods, and we have
  created functions to run the game for you.
- We have included functionality to pretty-print your strategy as well.

### Tests

See `test_blackjack.py` and `test_cards.py` for tests.