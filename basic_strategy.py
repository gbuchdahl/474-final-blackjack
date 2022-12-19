
from blackjack import Action

def basic_strategy(hand):        
    if hand.hand.is_blackjack():
        return Action.STAND
    if len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 8:
        return Action.SPLIT
    elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 1:
        return Action.SPLIT
    elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 9:
        if hand.upcard.get_value() != 7 and hand.upcard.get_value() != 10 and hand.upcard.get_value() != 1:
            return Action.SPLIT
        return Action.STAND
    elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 7 and hand.upcard.get_value() <= 7 and hand.upcard.get_value() != 1:
        return Action.SPLIT
    elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 6 and hand.upcard.get_value() <= 6 and hand.upcard.get_value() != 1:
        return Action.SPLIT
    elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 4 and (hand.upcard.get_value() == 5 or hand.upcard.get_value() == 6):
        return Action.SPLIT
    elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 2 and hand.upcard.get_value() <= 7 and hand.upcard.get_value() != 1:
        return Action.SPLIT
    elif len(hand.hand) == 2 and hand.hand[0].value == hand.hand[1].value and hand.hand[0].value == 3 and hand.upcard.get_value() <= 7 and hand.upcard.get_value() != 1:
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