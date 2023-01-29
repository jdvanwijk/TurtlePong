from turtle import Turtle
from settings import settings


class Paddle(Turtle):
    def __init__(self, player):
        super().__init__()
        self.shape("square")
        self.color(settings["PADDLE COLOR"])
        paddle_width = settings["PADDLE WIDTH"] / 20
        paddle_length = settings["PADDLE LENGTH"] / 20
        self.shapesize(paddle_width, paddle_length)
        self.setheading(90)
        self.penup()
        self.owner = player
        self.freeze = False
        self.paddle_reset()

    def move_up(self):
        """Moves the paddle up, unless the top of the screen has been reached."""
        wall_collision_y_cor = (settings["SCREEN HEIGHT"] / 2) - (settings["PADDLE LENGTH"] / 2)

        if not self.freeze:
            if self.ycor() < wall_collision_y_cor:
                # If there's enough space to move the paddle by its full amount, it will do so. Otherwise, the paddle
                # only moves up by the amount of pixels that it needs to hit the wall:
                if self.ycor() + settings["PADDLE SPEED"] < wall_collision_y_cor:
                    self.forward(settings["PADDLE SPEED"])
                else:
                    self.forward(wall_collision_y_cor - self.ycor())

    def move_down(self):
        """Moves the paddle down, unless the bottom of the screen has been reached."""
        wall_collision_y_cor = -((settings["SCREEN HEIGHT"] / 2) - (settings["PADDLE LENGTH"] / 2))

        if not self.freeze:
            if self.ycor() > wall_collision_y_cor:
                # If there's enough space to move the paddle by its full amount, it will do so. Otherwise, the paddle
                # only moves down by the amount of pixels that it needs to hit the wall:
                if self.ycor() - settings["PADDLE SPEED"] > wall_collision_y_cor:
                    self.back(settings["PADDLE SPEED"])
                else:
                    self.back(abs(wall_collision_y_cor - self.ycor()))

    def paddle_reset(self):
        """Resets the position of the player paddles at the beginning of the new round."""
        paddle_x_position = (settings["SCREEN WIDTH"] / 2) - settings["PADDLE DISTANCE FROM GOAL"]
        if self.owner == "p1":
            self.setposition(-paddle_x_position, 0)
        else:
            self.setposition(paddle_x_position, 0)
