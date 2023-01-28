from turtle import Turtle
from settings import settings


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.points = 0
        self.hideturtle()
        self.penup()
        self.speed("fastest")
        self.color("white")

    def update_score(self):
        """Adds a point to the score and writes it on the screen (does not update screen)"""
        self.points += 1
        self.clear()
        self.write(arg=self.points, align=settings["SCOREBOARD ALIGNMENT"], font=settings["SCOREBOARD FONT"])


class CompetitiveScore(Score):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.set_screen_position()
        self.write(arg=self.points, align=settings["SCOREBOARD ALIGNMENT"], font=settings["SCOREBOARD FONT"])

    def set_screen_position(self):
        """Sets the position of the scoreboard"""
        if self.player == "p1":
            self.setposition(settings["SCOREBOARD P1 POSITION"])
        elif self.player == "p2":
            self.setposition(settings["SCOREBOARD P2 POSITION"])


class CooperativeScore(Score):
    def __init__(self):
        super().__init__()
        self.setposition(settings["SCOREBOARD COOP POSITION"])
        self.write(arg=self.points, align=settings["SCOREBOARD ALIGNMENT"], font=settings["SCOREBOARD FONT"])
        with open("coop_top_score.txt") as top_score:
            self.coop_top_score = int(top_score.read())

    def update_coop_top_score(self):
        if self.points > self.coop_top_score:
            with open("coop_top_score.txt", "w") as top_score:
                top_score.write(str(self.points))
