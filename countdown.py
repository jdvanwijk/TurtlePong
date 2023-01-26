from turtle import Turtle
from settings import settings
from time import sleep


class Countdown(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()

    def display_countdown(self, game_screen):
        """Shows a countdown timer to signal the beginning of the round"""
        countdown_time = settings["COUNTDOWN TIME"]

        sleep(2)

        for _ in range(countdown_time):
            self.write(arg=countdown_time, align=settings["COUNTDOWN ALIGNMENT"], font=settings["COUNTDOWN FONT"])
            game_screen.update()
            sleep(1)
            countdown_time -= 1
            self.clear()
