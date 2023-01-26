from turtle import Turtle
from settings import settings
from time import sleep


class Scoreboard(Turtle):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.score = 0
        self.hideturtle()
        self.penup()
        self.speed("fastest")
        self.color("white")
        self.set_screen_position()
        self.write(arg=self.score, align=settings["SCOREBOARD ALIGNMENT"], font=settings["SCOREBOARD FONT"])

    def set_screen_position(self):
        """Sets the position of the scoreboard"""
        if self.player == "p1":
            self.setposition(-settings["SCOREBOARD X-POSITION"], settings["SCOREBOARD Y-POSITION"])
        else:
            self.setposition(settings["SCOREBOARD X-POSITION"], settings["SCOREBOARD Y-POSITION"])

    def update_score(self, screen):
        """Adds a point to the player's score and updates the screen and holds it for a few seconds before next round
        begins """
        self.score += 1
        self.clear()
        self.write(arg=self.score, align=settings["SCOREBOARD ALIGNMENT"], font=settings["SCOREBOARD FONT"])

        screen.update()
        sleep(2)

    def game_end(self) -> bool:
        """Checks if the game is over. Prints a message if this is true and returns bool"""
        if self.score == settings["GAME END SCORE"]:
            print(f"GAME OVER, {self.player.upper()} WINS!")
            game_end = True
        else:
            game_end = False

        return game_end
