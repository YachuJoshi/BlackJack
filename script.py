import random
import time
from Deck import Deck
from Constants import ace_cards
from Player import Player, Dealer


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
print(f'You have a total balance of: {player.balance}')
dealer = Dealer("Dealer")
game_on = True

print("\nWELCOME TO BLACKJACK!")
print(
    """
Get as close to 21 as you can without going over!
Dealer hits until she reaches wins or she busts. Aces count as 1 or 11. \n
    """
)

while game_on:
    # Check for player's current balance
    if player.balance == 0:
        print("Sorry, you are out of money!")
        print("Thanks for playing!")
        game_on = False
        break

    deck = Deck()
    print("Shuffling Deck..... \n")
    time.sleep(2.4)
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
        player_card = deck.deal_one()
        player_cards.append(player_card)
        print(f"You got {player_cards[-1]}")

        # Calculate player's deck sum
        if player_card.__str__() in ace_cards:
            player_ace_choice = int(input("Would you like this Ace as 1 or 11? "))
            player_deck_sum += player_ace_choice
        else:
            player_deck_sum += player_card.value

        dealer_card = deck.deal_one()
        dealer_cards.append(dealer_card)

        if i == 0:
            print(f"Dealer got {dealer_cards[-1]}")
        else:
            print("Dealer Card hidden")
            print("\n")

        # Calculate dealer's deck sum
        if dealer_card.__str__() in ace_cards:
            dealer_ace_choice = 11 if random.randint(0, 2) > 1 else 1
            dealer_deck_sum += dealer_ace_choice
        else:
            dealer_deck_sum += dealer_card.value

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

            print(f"You got {player_cards[-1]}")

            # player_deck_sum += new_card.value
            if new_card.__str__() in ace_cards:
                player_ace_choice = int(input("Would you like this Ace as 1 or 11? "))
                player_deck_sum += player_ace_choice
            else:
                player_deck_sum += new_card.value

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
            print("\n")
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
                print("Thanks for playing!")
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
