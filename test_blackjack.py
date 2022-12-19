import scipy

from blackjack import BlackjackStrategy, Action, PlayableHand, BlackjackGame
from cards import Shoe, Card
from q_learning import QStrategyStdBet, QBet
from basic_strategy import basic_strategy

class TestStrategy(BlackjackStrategy):
    def select_action(self, hand: PlayableHand, shoe: Shoe) -> Action:
        return basic_strategy(hand)

    def select_bet_size(self, shoe: Shoe) -> int:
        return 10
        # if shoe.get_count() > 5:
        #     return 50
        # elif shoe.get_count() > 10:
        #     return 500
        # elif shoe.get_count() < -5:
        #     return 0
        # return 10



strategy = QBet()
strategy.q_learn()
# strategy.print_strategy()
#strategy = TestStrategy()
print(strategy.Q_dict)
results = []
for _ in range(10):
    game = BlackjackGame(strategy, num_decks=4, verbose=False)
    initial_bankroll = 1_000_000
    res = game.play(num_hands=100000, initial_bankroll=initial_bankroll)
    results.append((res[0] - initial_bankroll)/ res[1])
    print("Result: ", (res[0] - initial_bankroll)/ res[1])

print(scipy.stats.describe(results))
