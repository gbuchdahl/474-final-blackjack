import scipy

from blackjack import BlackjackStrategy, Action, PlayableHand, BlackjackGame
from cards import Shoe, Card


class TestStrategy(BlackjackStrategy):
    def select_action(self, hand: PlayableHand, shoe: Shoe) -> Action:
        if hand.get_value()[0] < 16:
            return Action.HIT
        else:
            return Action.STAND

    def select_bet_size(self, shoe: Shoe) -> int:
        return 10


strategy = TestStrategy()
strategy.print_strategy()

results = []
for _ in range(10):
    game = BlackjackGame(strategy, num_decks=2, verbose=False)
    initial_bankroll = 1_000_000
    res = game.play(num_hands=500_000, initial_bankroll=initial_bankroll)[0]
    results.append(res / initial_bankroll)
    print("Result: %f", res / initial_bankroll)

print(scipy.stats.describe(results))
