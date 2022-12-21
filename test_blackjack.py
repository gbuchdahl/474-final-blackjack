import scipy

from blackjack import BlackjackStrategy, Action, PlayableHand, BlackjackGame
from cards import Shoe, Card
from q_learning import QStrategyStdBet, QBet
from basic_strategy import basic_strategy


class TestStrategy(BlackjackStrategy):
    def select_action(self, hand: PlayableHand, shoe: Shoe) -> Action:
        return basic_strategy(hand)

    def select_bet_size(self, shoe: Shoe) -> int:
        # if shoe.get_count() > 5:
        #     return 50
        # elif shoe.get_count() > 10:
        #     return 500
        # elif shoe.get_count() < -5:
        #     return 0
        return 10


# strategy = QBet()
# strategy.q_learn()
# strategy.print_strategy()
strategy = TestStrategy()

# strategy = TestStrategy()
# strategy.print_strategy()

results = []
for _ in range(10):
    game = BlackjackGame(strategy, num_decks=2, verbose=False, is_stacked=True)
    initial_bankroll = 1_000_000
    res = game.play(num_hands=500_000, initial_bankroll=initial_bankroll)
    results.append((res[0] - initial_bankroll) / res[1])
    print("Result: ", (res[0] - initial_bankroll) / res[1])
game.plot()
print(scipy.stats.describe(results))
