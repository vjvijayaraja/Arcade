import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips do you want to bet : "))
        except:
            print("Enter an integer")
        else:
            if chips.bet >= chips.total:
                print("You don't have that many chips.")
            else:
                break

def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()
    return single_card

def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input("Hit or stand? (h, s) ")
        if x.lower() == 'h':
            hit(deck, hand)
        elif x.lower() == 's':
            print("Dealer's Turn")
            playing = False
        else:
            print("Invalid input. Please enter 'h' or 's'.")
            continue
        break

def show(player, dealer):
    print("\nDealer's Hand")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand")
    for card in player.cards:
        print('', card)

def show_all(player, dealer):
    print("\nDealer's Hand")
    for card in dealer.cards:
        print('', card)
    print(f"Value of Dealer's hand: {dealer.value}")

    print("\nPlayer's Hand")
    for card in player.cards:
        print('', card)
    print(f"Value of Player's hand: {player.value}")

def player_busts(player, dealer, chips):
    print("PLAYER BUSTS!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("DEALER BUSTS! PLAYER WINS!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()

def push(player, dealer):
    print("It's a tie! PUSH.")

playing = True

while True:
    print("BLACKJACK")
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()
    take_bet(player_chips)

    show(player_hand, dealer_hand)

    while playing:
        hit_or_stand(deck, player_hand)
        show(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    print(f"\nPlayer's total chips are at: {player_chips.total}")
    new_game = input("New game? [y/n] ")
    if new_game.lower() == 'y':
        playing = True
        continue
    else:
        print("Goodbye!")
        break