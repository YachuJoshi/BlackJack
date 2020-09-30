from game import Game

name = input("Player, enter your name: ")
game = Game(name)
print(f'You have a total balance of: {game.player.balance}')

print("\nWELCOME TO BLACKJACK!")
print(
    """
Get as close to 21 as you can without going over!
Dealer hits until she reaches wins or she busts. Aces count as 1 or 11. \n
    """
)

game.start_game()