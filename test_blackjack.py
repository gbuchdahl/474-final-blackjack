import scipy

from blackjack import BlackjackStrategy, Action, PlayableHand, BlackjackGame
from cards import Shoe, Card
from q_learning import QStrategyStdBet


class TestStrategy(BlackjackStrategy):
    def select_action(self, hand: PlayableHand, shoe: Shoe) -> Action:
        if hand.hand.is_blackjack():
            return Action.STAND
        if len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 8:
            return Action.SPLIT
        elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 1:
            return Action.SPLIT
        elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 1:
            if hand.upcard.get_value() != 7 and hand.upcard.get_value() != 10 and hand.upcard.get_value() != 1:
                return Action.SPLIT
        elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 7 and hand.upcard.get_value() <= 7:
            return Action.SPLIT
        elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 6 and hand.upcard.get_value() <= 6:
            return Action.SPLIT
        elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 4 and (hand.upcard.get_value() == 5 or hand.upcard.get_value() == 6):
            return Action.SPLIT
        elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 2 and hand.upcard.get_value() <= 7:
            return Action.SPLIT
        elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 3 and hand.upcard.get_value() <= 7:
            return Action.SPLIT

        elif hand.get_value()[1] and hand.get_value()[0] == 20:
            return Action.STAND
        elif hand.get_value()[1] and hand.get_value()[0] == 19:
            if len(hand.hand) == 2 and hand.upcard.get_value() == 6:
                return Action.DOUBLE
            return Action.STAND
        elif hand.get_value()[1] and hand.get_value()[0] == 18:
            if hand.upcard.get_value() == 1 or hand.upcard.get_value() == 10 or hand.upcard.get_value() == 9:
                return Action.HIT
            elif len(hand.hand) == 2 and hand.upcard.get_value() <= 6:
                return Action.DOUBLE
            else:
                return Action.STAND
        elif hand.get_value()[1] and (hand.upcard.get_value() <= 2 or hand.upcard.get_value() >= 7):
            return Action.HIT
        elif hand.get_value()[1] and hand.upcard.get_value() == 3 and hand.get_value()[0] <= 16:
            return Action.HIT
        elif hand.get_value()[1] and hand.upcard.get_value() == 4 and hand.get_value()[0] <= 14:
            return Action.HIT
        elif len(hand.hand) == 2 and hand.get_value()[1]:
            return Action.DOUBLE
            
       


        elif hand.get_value()[0] == 11:
            return Action.DOUBLE
        elif hand.get_value()[0] == 10 and hand.upcard.get_value() != 10 and hand.upcard.get_value() != 1:
            return Action.DOUBLE
        elif hand.get_value()[0] == 9 and hand.upcard.get_value() >= 3 and hand.upcard.get_value() <= 6:
            return Action.DOUBLE
        




        elif hand.get_value()[0] <= 16 and (hand.upcard.get_value() >= 7 or hand.upcard.get_value() == 1):
            return Action.HIT
        elif hand.get_value()[0] == 12 and (hand.upcard.get_value() == 2 or hand.upcard.get_value() == 3):
            return Action.HIT
        elif hand.get_value()[0] >= 12 and hand.upcard.get_value() >= 2 and hand.upcard.get_value() <= 6:
            return Action.STAND
        
        elif hand.get_value()[0] <= 11:
            return Action.HIT
        else:
            return Action.STAND

    def select_bet_size(self, shoe: Shoe) -> int:
        return 10



# strategy = QStrategyStdBet()
# Q_dict = strategy.q_learn()
# strategy.print_strategy()

strategy = TestStrategy()
strategy.print_strategy()

results = []
for _ in range(10):
    game = BlackjackGame(strategy, num_decks=2, verbose=False)
    initial_bankroll = 1_000_000
    res = game.play(num_hands=500_000, initial_bankroll=initial_bankroll)
    results.append((res[0] - initial_bankroll)/ res[1])
    print("Result: ", (res[0] - initial_bankroll)/ res[1])

print(scipy.stats.describe(results))
