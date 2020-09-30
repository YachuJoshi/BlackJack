import random
import time
from deck import Deck
from base import ace_cards
from player import Player, Dealer


class Game:
    def __init__(self, player_name):
        self.player = Player(player_name, 1000)
        self.dealer = Dealer("Dealer")
        self.game_on = True
        self.player_cards = []
        self.dealer_cards = []

    def init(self):
        self.deck = Deck()
        self.player_deck_sum = 0
        self.dealer_deck_sum = 0
        print("Shuffling Deck..... \n")
        time.sleep(2.4)
        self.deck.shuffle()

    def get_bet(self):
        while True:
            try:
                bet = int(input("Enter your bet: "))
                break
            except:
                print("That is not a number")

        return bet

    def handle_bet_intake(self):
        while True:
            bet = self.get_bet()
            if self.player.balance < bet:
                print(
                    "Sorry, you dont have enough fund to bet that much! Choose something lower"
                )
                print(f"You currently have: {self.player.balance}")
            else:
                break
        return bet

    def adjust_sum(self, new_card):
        # For ace cards:
        if new_card.__str__() in ace_cards:
            player_ace_choice = int(input("Would you like this Ace as 1 or 11? "))
            self.player_deck_sum += player_ace_choice
        # Else just add it to total sum
        else:
            self.player_deck_sum += new_card.value

    def deal_player_card(self):
        player_card = self.deck.deal_one()
        self.player_cards.append(player_card)
        print(f"You got {self.player_cards[-1]}")

        # Calculate player's deck sum
        self.adjust_sum(player_card)

    def distribute_cards(self, deck):
        for i in range(2):
            self.deal_player_card()

            dealer_card = deck.deal_one()
            self.dealer_cards.append(dealer_card)

            if i == 0:
                print(f"Dealer got {self.dealer_cards[-1]}")
            else:
                print("Dealer Card hidden")
                print("\n")

            # Calculate dealer's deck sum
            if dealer_card.__str__() in ace_cards:
                dealer_ace_choice = 11 if random.randint(0, 2) > 1 else 1
                self.dealer_deck_sum += dealer_ace_choice
            else:
                self.dealer_deck_sum += dealer_card.value

    def print_player_win(self):
        print("You won this round!")
        print(f"Your current balance is: {self.player.balance}")
        print("\n")

    def print_player_loss(self):
        print("You lost this round!")
        print(f"Your current balance is: {self.player.balance}")
        print("\n")

    def continue_playing(self):
        while True:
            game_choice = input("Would you like to continue? Yes or No: ")

            if game_choice[0].lower() == "y":
                self.game_on = True
                break
            elif game_choice[0].lower() == "n":
                self.game_on = False
                break
            else:
                print("I dont quite understand that")

    def start_game(self):
        while self.game_on and self.player.balance:
            self.init()

            # Get Bet for the round
            bet = self.handle_bet_intake()
            print("\n")

            # Distribute 2 cards for player and dealer each
            self.distribute_cards(self.deck)

            # Check for Player BLACKJACK Condition
            if self.player_deck_sum == 21:
                self.player.balance += bet
                print("BLACKJACK!")
                self.print_player_win()

            # Continue if no BLACKJACK Condition
            else:
                player_choice = input("What would you like to do? Hit or Stand? ")

                # Get player's choice for hit / stand
                while player_choice[0].lower() == "h":
                    self.deal_player_card()

                    if self.player_deck_sum >= 21:
                        break

                    player_choice = input("What would you like to do? Hit or Stand? ")

                # Check for BLACKJACK Condition after Hit & wait for dealer's play
                if self.player_deck_sum == 21:
                    print("It's a BLACKJACK! Let's see what the dealer draws next.")
                    print("\n")

                # Check for BUST Condition
                if self.player_deck_sum > 21:
                    self.player.balance -= bet
                    print("BUST!")
                    self.print_player_loss()

                else:
                    # Flip dealer's second card
                    print("\n")
                    print(f"Dealer's second card was {self.dealer_cards[-1]}")

                    while True:
                        # Check for dealer's win condition
                        if (
                            self.dealer_deck_sum - self.player_deck_sum > 0
                            and self.dealer_deck_sum <= 21
                        ):
                            self.player.balance -= bet
                            self.print_player_loss()
                            break

                        # Check for dealer's BUST condition
                        if self.dealer_deck_sum > 21:
                            self.player.balance += bet
                            self.print_player_win()
                            break

                        if self.dealer_deck_sum == 21 and self.player_deck_sum == 21:
                            self.player.balance -= bet
                            self.print_player_loss()
                            break

                        # Dealer hits
                        new_card = self.deck.deal_one()
                        self.dealer_cards.append(new_card)
                        print(f"Dealer got {self.dealer_cards[-1]}")
                        self.dealer_deck_sum += self.dealer_cards[-1].value

            if self.player.balance:
                self.continue_playing()
            else:
                self.game_on = False
                print("Sorry, you're out of money!")
        else:
            print("Game Over! Thank you for playing!")