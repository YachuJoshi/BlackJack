import random
import time

suits = ("Hearts", "Diamonds", "Spades", "Clubs")

ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)

values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        return f"Your deck: {self.deck}"

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_one(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.hand = []

    def deck_sum(self):
        sum = 0
        for card in self.hand:
            sum += card.value

        return sum


class Player(Hand):
    def __init__(self, name, balance=100):
        Hand.__init__(self)
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"{self.name} has {self.balance} & {self.hand} cards"


class Dealer(Hand):
    def __init__(self):
        Hand.__init__(self)


def deck_sum(cards):
    sum = 0
    for card in cards:
        sum += card.value

    return sum


def get_bet():
    while True:
        try:
            bet = int(input("Enter your bet: "))
            break
        except:
            print("That is not a number")

    return bet


name = input("Player, enter your name: ")
player = Player(name, 1000)
dealer = Dealer()
game_on = True

print("WELCOME TO BLACKJACK! \n")

while game_on:
    # Check for player's current balance
    if player.balance == 0:
        print("Sorry, you are out of money!")
        game_on = False
        break

    deck = Deck()
    print("Shuffling Deck..... \n")
    time.sleep(3)
    deck.shuffle()

    player_cards = []
    dealer_cards = []
    player_deck_sum = 0
    dealer_deck_sum = 0

    # Get Bet for the round
    while True:
        bet = get_bet()
        if player.balance < bet:
            print(
                "Sorry, you dont have enough fund to bet that much! Choose something lower"
            )
        else:
            break

    print("\n")
    # Distribute 2 cards for player and dealer each
    for i in range(2):
        player_cards.append(deck.deal_one())
        print(f"You got {player_cards[-1]}")
        dealer_cards.append(deck.deal_one())
        if i == 0:
            print(f"Dealer got {dealer_cards[-1]}")
        else:
            print("Dealer Card hidden")

    player_deck_sum = deck_sum(player_cards)
    dealer_deck_sum = deck_sum(dealer_cards)

    # Check for Player BLACKJACK Condition
    if player_deck_sum == 21:
        player.balance += bet
        print("BLACKJACK!")
        print("You won this round!")
        print(f"Your current balance is: {player.balance}")
        print("\n")
        game_choice = input("Would you like to continue? Yes or No: ")

        if game_choice == "Yes":
            game_on = True
        else:
            print(f"Your total balance is: {player.balance}")
            print("Thank you for playing!")
            game_on = False
            break

    # Continue if no BLACKJACK Condition
    else:
        player_choice = input("What would you like to do? Hit or Stand? ")

        # Get player's choice for hit / stand
        while player_choice == "Hit":
            new_card = deck.deal_one()
            player_cards.append(new_card)
            player_deck_sum += player_cards[-1].value
            print(f"You got {player_cards[-1]}")

            if player_deck_sum >= 21:
                break

            player_choice = input("What would you like to do? Hit or Stand? ")

        # Check for BLACKJACK Condition after Hit & wait for dealer's play
        if player_deck_sum == 21:
            print("It's a BLACKJACK! Let's see what the dealer draws next.")
            print("\n")

        # Check for BUST Condition
        if player_deck_sum > 21:
            player.balance -= bet
            print("BUST!")
            print("You lost this round!")
            print(f"Your current balance is: {player.balance}")
            print("\n")

            game_choice = None

            while game_choice != "Yes" or game_choice != "No":
                game_choice = input("Would you like to continue? Yes or No: ")
                if game_choice == "Yes":
                    game_on = True
                    break
                else:
                    print(f"Your total balance is: {player.balance}")
                    print("Thank you for playing!")
                    game_on = False
                    break
        else:
            # Flip dealer's second card
            print(f"Dealer's second card was {dealer_cards[-1]}")

            while True:
                # Check for dealer's win condition
                if dealer_deck_sum - player_deck_sum > 0 and dealer_deck_sum <= 21:
                    player.balance -= bet
                    print("You lost this round")
                    print(f"Your current balance is: {player.balance}")
                    print("\n")
                    break

                # Check for dealer's BUST condition
                if dealer_deck_sum > 21:
                    player.balance += bet
                    print("You won this round")
                    print(f"Your current balance is: {player.balance}")
                    print("\n")
                    break

                if dealer_deck_sum == 21 and player_deck_sum == 21:
                    player.balance -= bet
                    print("You lost this round")
                    print(f"Your current balance is: {player.balance}")
                    print("\n")
                    break

                # Dealer hits
                new_card = deck.deal_one()
                dealer_cards.append(new_card)
                print(f"Dealer got {dealer_cards[-1]}")
                dealer_deck_sum += dealer_cards[-1].value

            game_choice = None

            if player.balance == 0:
                print("Sorry, you are out of money!")
                game_on = False
                break

            while game_choice != "Yes" or game_choice != "No":
                game_choice = input("Would you like to continue? Yes or No: ")
                if game_choice == "Yes":
                    game_on = True
                    break
                else:
                    print("Thanks for playing!")
                    game_on = False
                    break
