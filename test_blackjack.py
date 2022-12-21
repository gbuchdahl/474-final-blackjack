from basic_strategy import BasicStrategy
from blackjack import BlackjackGame, BlackjackStrategy
from deep_q import DeepQBlackjack
from q_learning import QBet, QStrategyStdBet
from scipy.stats import describe

print("Welcome, Professor Glenn!")
print("Project: Blackjack")
print("By Gabriel Buchdahl & Trey Skidmore")
print("If you haven't installed the virtual env, try `make install-venv`")
print(
    "If you haven't yet, check out our readme at https://github.com/gbuchdahl/474-final-blackjack#readme")

print("\n\n")

print("First, we spent a lot of time coding a model for the game of Blackjack.")
print("Here's what it looks like in verbose mode, playing a few hands")

game = BlackjackGame(strategy=BasicStrategy(), verbose=True)
game.play(num_hands=2)

print("\n\n")

print("As a benchmark, we implemented basic strategy, the best possible blackjack strategy.")
print("Basic Strategy, No Bet Size Adjustment\n------")

game = BlackjackGame(strategy=BasicStrategy(), verbose=False)
results = []
initial_bankroll = 1_000_000
for _ in range(5):
    res = game.play(num_hands=100_000, initial_bankroll=initial_bankroll)
    results.append(100 * (1 + ((res[0] - initial_bankroll) / res[1])))
    print("Return: {:.4f}%".format(100 * (1 + ((res[0] - initial_bankroll) / res[1]))))

print("As you can see, it is extremely close to break-even. This is possible due to a few quirks "
      "in our Blackjack implementation (we applied an approximation for split) as well as the "
      "fact that we pay blackjack out 3 to 2.")

print(describe(results))
print("\n\n")

print("Basic Strategy, Q-Learned Bet Size Adjustment (trained for 120s)\n------")
q_bet = QBet()
q_bet.q_learn(2)
game = BlackjackGame(strategy=q_bet, verbose=False, num_decks=2)
results = []
initial_bankroll = 1_000_000
for _ in range(5):
    res = game.play(num_hands=100_000, initial_bankroll=initial_bankroll)
    results.append(100 * (1 + ((res[0] - initial_bankroll) / res[1])))
    print("Return: {:.4f}%".format(100 * (1 + ((res[0] - initial_bankroll) / res[1]))))

print(describe(results))
print("\n\n")

print("Q-Learned Strategy (10 seconds), No Bet Size Adjustment\n------")
q_learn = QStrategyStdBet()
q_learn.q_learn(2)
game = BlackjackGame(strategy=q_learn, verbose=False, num_decks=2)
results = []
initial_bankroll = 1_000_000
for _ in range(5):
    res = game.play(num_hands=100_000, initial_bankroll=initial_bankroll)
    results.append(100 * (1 + ((res[0] - initial_bankroll) / res[1])))
    print("Return: {:.4f}%".format(100 * (1 + ((res[0] - initial_bankroll) / res[1]))))

print(describe(results))
dqn = DeepQBlackjack()
results = []
dqn.load_model("trained-dqn-model.h5")

print("\n\n")
print("The model is pre-trained, and this runs very quickly on my M1 Max laptop, "
      "but for some reason, it takes forever to run on the zoo, perhaps due to worse hardware "
      "acceleration support.")
print("Deep-Q Strategy, No Bet Size Adjustment\n------")

game = BlackjackGame(dqn, num_decks=2, verbose=False)
initial_bankroll = 1_000_000
for _ in range(5):
    res = game.play(num_hands=100_000, initial_bankroll=initial_bankroll)
    results.append(100 * (1 + ((res[0] - initial_bankroll) / res[1])))
    print("Return: {:.4f}%".format(100 * (1 + ((res[0] - initial_bankroll) / res[1]))))

print(describe(results))
print("\n\n")


class Endboss(BlackjackStrategy):
    def select_action(self, hand, shoe):
        return dqn.select_action(hand, shoe)

    def select_bet_size(self, shoe):
        return q_bet.select_bet_size(shoe)


endboss = Endboss()
game = BlackjackGame(endboss, num_decks=2, verbose=False)
initial_bankroll = 1_000_000
results = []
print("Deep-Q Strategy, Q-Learned Bet Size Adjustment\n------")
for _ in range(5):
    res = game.play(num_hands=50_000, initial_bankroll=initial_bankroll)
    results.append(100 * (1 + ((res[0] - initial_bankroll) / res[1])))
    print("Return: {:.4f}%".format(100 * (1 + ((res[0] - initial_bankroll) / res[1]))))
print(describe(results))

print(
    "If you haven't yet, check out our readme for analysis at "
    "https://github.com/gbuchdahl/474-final-blackjack#readme")
