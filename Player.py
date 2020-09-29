class Player:
    def __init__(self, name, balance=100):
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"{self.name} has {self.balance}"


class Dealer:
    def __init__(self, name):
        self.name = name
