from turtle import Turtle
from random import choice, uniform
from math import sqrt
from settings import settings


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color(settings["BALL COLOR"])
        self.penup()

        ball_side = settings["BALL SIZE"] / 20
        self.shapesize(ball_side, ball_side)

        self.speed = settings["BALL SPEED"]
        self.x_speed = 0
        self.y_speed = 0
        self.direction = ""    # Can be "left_up", "left_down", "right_up" or "right_down"

    def ball_reset(self):
        """Resets the ball's starting position, color and speed at the beginning of the round"""
        self.setposition(0, 0)
        self.color(settings["BALL COLOR"])
        self.speed = settings["BALL SPEED"]

    def set_y_speed(self):
        """Calculates and sets the ball's y-speed"""
        # Uses Pythagoras' Formula to determine y-speed:
        self.y_speed = sqrt((self.speed ** 2) - (self.x_speed ** 2))

    def serve(self):
        """Sets the starting direction and starting angle of the ball"""
        serving_player = choice(["p1", "p2"])
        if serving_player == "p1":
            self.direction = choice(["right_up", "right_down"])
        else:
            self.direction = choice(["left_up", "left_down"])

        self.x_speed = uniform((0.5 * self.speed), self.speed)
        self.set_y_speed()

    def move(self):
        """Moves the ball"""
        if self.direction == "right_up":
            self.setposition((self.xcor() + self.x_speed), (self.ycor() + self.y_speed))
        elif self.direction == "right_down":
            self.setposition((self.xcor() + self.x_speed), (self.ycor() - self.y_speed))
        elif self.direction == "left_up":
            self.setposition((self.xcor() - self.x_speed), (self.ycor() + self.y_speed))
        elif self.direction == "left_down":
            self.setposition((self.xcor() - self.x_speed), (self.ycor() - self.y_speed))

    def check_wall_collision(self):
        """Checks for wall collision and changes ball direction if a collision is detected"""
        def wall_collision() -> bool:
            """Checks collision between ball and wall, returns bool"""
            wall_collision_ycor = (settings["SCREEN HEIGHT"] / 2) - (settings["BALL SIZE"] / 2) - self.speed
            if abs(self.ycor()) >= wall_collision_ycor:
                collision = True
            else:
                collision = False

            return collision

        def apply_direction_change():
            """If collision is detected, changes direction of the ball"""
            # Mirror the direction vertically on wall collision:
            if self.direction == "right_up":
                self.direction = "right_down"
            elif self.direction == "right_down":
                self.direction = "right_up"
            elif self.direction == "left_up":
                self.direction = "left_down"
            elif self.direction == "left_down":
                self.direction = "left_up"

        if wall_collision():
            apply_direction_change()

    def check_paddle_collision(self, p1_paddle, p2_paddle):
        """Checks for paddle collision and changes ball direction and angle if collision is detected. Will change
        ball color and ball speed if settings['BALL SPEED UP'] == True"""
        max_x_distance_paddle_collision = (settings["PADDLE WIDTH"] / 2) + (settings["BALL SIZE"] / 2) + self.speed
        max_y_distance_paddle_collision = (settings["PADDLE LENGTH"] / 2) + (settings["BALL SIZE"] / 2) + self.speed

        def calculate_distance() -> list:
            """Calculates distance between paddle and ball, returns list with x-distance and y-distance"""
            if self.direction == "right_up" or self.direction == "right_down":
                current_x_distance_paddle_ball = p2_paddle.xcor() - self.xcor()
                current_y_distance_paddle_ball = self.ycor() - p2_paddle.ycor()
            else:
                current_x_distance_paddle_ball = self.xcor() - p1_paddle.xcor()
                current_y_distance_paddle_ball = self.ycor() - p1_paddle.ycor()

            return [current_x_distance_paddle_ball, current_y_distance_paddle_ball]

        def paddle_collision(paddle_ball_distance: list) -> bool:
            """Checks the list that was returned by calculate_distance() and determines if there was a paddle
            collision, returns bool"""
            x_distance = paddle_ball_distance[0]
            y_distance = paddle_ball_distance[1]

            if (0 <= abs(x_distance) <= max_x_distance_paddle_collision) and (
                    0 <= abs(y_distance) <= max_y_distance_paddle_collision):
                collision = True
            else:
                collision = False

            return collision

        def apply_changes(paddle_ball_distance: list):
            """If there has been a collision, apply changes to direction and angle of the ball, optionally apply
            changes to color and total speed of the ball """
            if settings["BALL SPEED UP"]:
                # Changes the hue of the ball and speed up the ball every time the ball hits a paddle:
                if self.fillcolor() != settings["BALL COLOR GRADIENT"][-1]:
                    self.speed += (settings["BALL MAX SPEED UP"] / len(settings["BALL COLOR GRADIENT"]))
                    current_gradient_index = settings["BALL COLOR GRADIENT"].index(self.fillcolor())
                    next_color = settings["BALL COLOR GRADIENT"][current_gradient_index + 1]
                    self.color(next_color)

            # Set the angle of the ball, depending on where it hits the paddle. Toward the middle, the ball will move
            # more horizontally, while toward the edges of the paddle, the ball will move more diagonally (maximum
            # angle is 45 degrees):
            y_distance = paddle_ball_distance[1]
            self.x_speed = self.speed * (1 - (abs(y_distance) / settings["PADDLE LENGTH"]))
            if self.x_speed < (self.speed / 2):     # Prevents vertical stalling of the ball (enforces max angle)
                self.x_speed = (self.speed / 2)

            self.set_y_speed()

            # Set the direction of the ball, depending on if the ball hit the top or the lower half of the paddle:
            if y_distance >= 0:     # If ball hits top half of the paddle
                if self.direction == "right_up" or self.direction == "right_down":
                    self.direction = "left_up"
                else:
                    self.direction = "right_up"
            elif y_distance < 0:    # If ball hits lower half of the paddle
                if self.direction == "right_up" or self.direction == "right_down":
                    self.direction = "left_down"
                else:
                    self.direction = "right_down"

        distance_paddle_ball = calculate_distance()
        if paddle_collision(distance_paddle_ball):
            apply_changes(distance_paddle_ball)

    def check_goal(self) -> list:
        """Checks if a goal has been scored. Prints a message and returns [goal_report].\n
        goal_report[0]: was a goal scored? -> True/False\n
        goal_report[1]: who scored the goal? -> 'p1', 'p2' or 'none'"""
        ball_exit_screen_xcor = (settings["SCREEN WIDTH"] / 2) + (settings["BALL SIZE"] / 2)

        if self.xcor() >= ball_exit_screen_xcor:
            print("p1 scored a goal")
            goal_scored = True
            scoring_player = "p1"
        elif self.xcor() <= -ball_exit_screen_xcor:
            print("p2 scored a goal")
            goal_scored = True
            scoring_player = "p2"
        else:
            goal_scored = False
            scoring_player = "none"

        goal_report = [goal_scored, scoring_player]
        return goal_report
