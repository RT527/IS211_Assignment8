# Rafi Talukder Assignment_8
import random  # This is for random number 1-6 generation for die
import argparse
import time
"""---------------------------------------------------------------------------------"""
random.seed(0)  # This sets a fixed seed for reproducible results
"""---------------------------------------------------------------------------------"""
class Die:  # This represents a single die with 6 sides 1-6
    def __init__(self):
        self.value = 1

    def roll(self):
        self.value = random.randint(1, 6)  # This rolls dice and gives us a value between 1 and 6
        return self.value
"""---------------------------------------------------------------------------------"""
class Player:
    def __init__(self, name):  # This represents a player in game
        self.name = name
        self.total_score = 0

    def add_pts(self, pts):  # This adds points to the score
        self.total_score += pts

    def wants2roll(self, turn_total):  # This will be defined by subclasses
        raise NotImplementedError

    def __str__(self):
        return f"{self.name}: {self.total_score} points"
"""---------------------------------------------------------------------------------"""
class human(Player):  # This represents a human player
    def wants2roll(self, turn_total):
        while True:
            choice = input("Enter 'r' to roll or 'h' to hold: ").lower()
            if choice in ['r', 'h']:
                return choice == 'r'
            print("Invalid input. Please enter 'r' or 'h'.")
"""---------------------------------------------------------------------------------"""
class robot(Player):  # This represents a computer player
    def wants2roll(self, turn_total):
        threshold = min(25, 100 - self.total_score) # This is logic that makes the computer hold after 25 pts
        return turn_total < threshold               # or maybe less if it needs <25 pts
"""---------------------------------------------------------------------------------"""
class PlayerFactory:  # This class creates player objects using the Factory Pattern
    @staticmethod
    def create_player(player_type, name):
        if player_type.lower() == "human":
            return human(name)
        elif player_type.lower() == "computer":
            return robot(name)
        else:
            raise ValueError("Invalid player type. Use 'human' or 'computer'.")
"""---------------------------------------------------------------------------------"""
class PigGame:  # This class controls the overall game flow
    WINNING_SCORE = 100

    def __init__(self, player1_type="human", player2_type="computer"):
        self.die = Die()
        self.players = [
            PlayerFactory.create_player(player1_type, "Player 1"),
            PlayerFactory.create_player(player2_type, "Player 2")
        ]
        self.turn_index = 0

    def switch_player(self):  # This is logic to switch to next player
        self.turn_index = 1 - self.turn_index

    def get_current_player(self):  # Ths returns whose turn it is
        return self.players[self.turn_index]

    def play_turn(self):  # This handles one full turn for a player
        player = self.get_current_player()
        turn_total = 0
        print(f"\n--- {player.name}'s turn ---")
        while True:
            if player.wants2roll(turn_total):
                roll = self.die.roll()
                print(f"{player.name} rolled a {roll}.")
                if roll == 1:
                    print("OOPS! You rolled a 1. No points this turn. Sorry!")
                    turn_total = 0
                    break
                else:
                    turn_total += roll
                    print(f"Turn total = {turn_total}, Current total score = {player.total_score}")
            else:
                player.add_pts(turn_total)
                print(f"{player.name} holds. Turn total {turn_total} added to score.")
                break
        print(f"{player.name}'s total score: {player.total_score}\n")
        self.switch_player()

    def is_game_over(self):  # Checks to see if player has reached winning score + celebrate
        for player in self.players:
            if player.total_score >= self.WINNING_SCORE:
                print(f"🎉 WOOHOO! {player.name} WINS with {player.total_score} points! 🎉")
                return True
        return False

    def play(self):  # This loops the game until we have a winner
        print("HELLO! Welcome to the Pig 🐷 Game 🎮!")
        print("First player to reach 100 points wins!\n")

        while not self.is_game_over():
            self.play_turn()
        print("\nGame over! Thanks for playing.")
"""---------------------------------------------------------------------------------"""
if __name__ == "__main__":
    game = PigGame()
    game.play()
"""---------------------------------------------------------------------------------"""