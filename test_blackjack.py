from blackjack import BlackjackStrategy, Action, PlayableHand, BlackjackGame
from cards import Shoe, Card


class TestStrategy(BlackjackStrategy):
    def get_action_from_total(self, total: int, is_soft: bool, upcard: Card, shoe: Shoe) -> Action:
        if total < 16:
            return Action.HIT
        else:
            return Action.STAND

    def select_bet_size(self, shoe: Shoe) -> int:
        return 10


strategy = TestStrategy()
strategy.print_strategy()

results = []
for _ in range(10):
    game = BlackjackGame(strategy, num_decks=2, verbose=False, num_hands=500000,
                         initial_bankroll=100000)
    res = game.play()
    results.append(res / 100000)

print(results)
