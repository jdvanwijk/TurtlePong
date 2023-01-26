from turtle import Screen
from screen_setup import setup_screen, bind_keys
from paddle import Paddle
from scoreboard import Scoreboard
from ball import Ball
from countdown import Countdown
from settings import settings
from time import sleep

# Setup game objects:
screen = Screen()
setup_screen(screen)
ball = Ball()
p1_paddle = Paddle("p1")
p2_paddle = Paddle("p2")
bind_keys(screen, p1_paddle, p2_paddle)
p1_score = Scoreboard("p1")
p2_score = Scoreboard("p2")
countdown = Countdown()


def start_round():
    """- Reset ball to its starting position and properties \n- Reset paddle positions \n- Display countdown
    \n- Serve ball"""
    p1_paddle.freeze = True
    p2_paddle.freeze = True

    ball.ball_reset()
    p1_paddle.reset_starting_position()
    p2_paddle.reset_starting_position()
    screen.update()

    countdown.display_countdown(screen)
    ball.serve()

    p1_paddle.freeze = False
    p2_paddle.freeze = False


def generate_next_frame():
    """- Move the ball \n- Check for wall and paddle collision (and change ball direction and angle accordingly)
    \n- Refresh screen"""
    ball.move()
    ball.check_wall_collision()
    ball.check_paddle_collision(p1_paddle, p2_paddle)

    screen.update()
    sleep(1 / settings["FRAME RATE"])


def check_for_goal():
    """Check if a goal was scored and if so, add a point to that player's score"""
    goal_report = ball.check_goal()
    if goal_report[0]:
        if goal_report[1] == "p1":
            p1_score.update_score(screen)
        elif goal_report[1] == "p2":
            p2_score.update_score(screen)
        goal = True
    else:
        goal = False

    return goal


def check_for_end_game():
    """Check if the end game score determined in settings['END GAME SCORE'] has been reached by one of the players"""
    if p1_score.game_end() or p2_score.game_end():
        is_game_over = True
    else:
        is_game_over = False

    return is_game_over


# Game starts here:
game_end = False
while not game_end:
    start_round()

    goal_scored = False
    while not goal_scored:
        generate_next_frame()
        goal_scored = check_for_goal()
        game_end = check_for_end_game()

screen.exitonclick()

# TODO: continuous paddle moving without blocking other keys possible?
