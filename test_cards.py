from cards import Hand, Card, Shoe

hand = Hand()
ace = Card(1)
eight = Card(8)

hand.add_card(ace)
hand.add_card(ace)
hand.add_card(eight)

assert hand.get_value() == (20, True)
assert hand.is_bust() is False

hand.add_card(eight)
assert hand.get_value() == (18, False)
assert hand.is_bust() is False
print(hand)

hand.add_card(eight)
assert hand.is_bust() is True

jack = Card(11)
hand = Hand()
hand.add_card(jack)
hand.add_card(ace)
print(hand)
assert hand.is_blackjack() is True


shoe = Shoe(2)
for _ in range(52 * 2):
    shoe.deal()
assert shoe.cards == []
assert len(shoe.discards) == 52 * 2

print(shoe)

for _ in range(52):
    _hand = shoe.deal_hand()

assert shoe.cards == []
assert len(shoe.discards) == 52 * 2

print("All tests passed!")
