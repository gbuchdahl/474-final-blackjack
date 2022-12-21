from time import sleep

from basic_strategy import BasicStrategy
from blackjack import BlackjackGame
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
print("Here are it's results over 5 100,000 hand games")
print("Basic Strategy, No Bet Size Adjustment\n------")

game = BlackjackGame(strategy=BasicStrategy(), verbose=False)
results = []
initial_bankroll = 1_000_000
for _ in range(20):
    res = game.play(num_hands=100_000, initial_bankroll=initial_bankroll)
    results.append((res[0] - initial_bankroll) / res[1])
    print("Return:", (res[0] - initial_bankroll) / res[1])
print(describe(results))

print("As you can see, it is extremely close to break-even. This is possible due to a few quirks "
      "in our Blackjack implementation (we applied an approximation for split) as well as the "
      "fact that we pay blackjack out 3 to 2.")

print("\n\n")

print("Next, we tried using Q-learning to select bet sizes based on the \"count\" of the shoe.")
print("Here are it's results over 5 100,000 hand games")
print("Basic Strategy, Q-Learned Bet Size Adjustment\n------")
q_bet = QBet()
q_bet.q_learn(4)
game = BlackjackGame(strategy=q_bet, verbose=False, num_decks=4)
results = []
initial_bankroll = 1_000_000
for _ in range(20):
    res = game.play(num_hands=100_000, initial_bankroll=initial_bankroll)
    results.append((res[0] - initial_bankroll) / res[1])
    print("Return:", (res[0] - initial_bankroll) / res[1])
print(describe(results))

print("\n\n")

print("Then, we tried to use Q-learning to see if it could come up with a strategy competitive "
      "with the performance of basic strategy.")
print("Here are it's results over 5 100,000 hand games")
print("Q-Learned Strategy, No Bet Size Adjustment\n------")
q_bet = QStrategyStdBet()
q_bet.q_learn(4)
game = BlackjackGame(strategy=q_bet, verbose=False, num_decks=4)
results = []
initial_bankroll = 1_000_000
for _ in range(20):
    res = game.play(num_hands=100_000, initial_bankroll=initial_bankroll)
    results.append((res[0] - initial_bankroll) / res[1])
    print("Return:", (res[0] - initial_bankroll) / res[1])
print(describe(results))

print("As you can see, it struggled to beat basic strategy. It's likely that the state space was "
      "too large for Q-Learning to be effective.")

dqn = DeepQBlackjack()
results = []
dqn.load_model("trained-dqn-model.h5")

print("\n\n")
print("Finally, we used Deep-Q learning with a neural network.")
print("Here are it's results over 5 50,000 hand games")
print("The model is pre-trained, and this runs very quickly on my M1 Max laptop, "
      "but for some reason, it takes forever to run on the zoo, perhaps due to worse hardware "
      "acceleration support.")
print("Deep-Q Strategy, No Bet Size Adjustment\n------")

game = BlackjackGame(dqn, num_decks=2, verbose=False)
initial_bankroll = 1_000_000
for _ in range(20):
    res = game.play(num_hands=100_000, initial_bankroll=initial_bankroll)
    results.append((res[0] - initial_bankroll) / res[1])
    print("Return:", (res[0] - initial_bankroll) / res[1])
print(describe(results))

print("We were able to achieve results with greater than 99% return, nearly as good as basic "
      "strategy.")
print("This was our goal for the project!")
print("To view the outputted strategy, as well as learn more about the project, check out our "
      "readme!")
