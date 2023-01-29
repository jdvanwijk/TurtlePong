from turtle import Screen
from screen_setup import setup_screen, bind_keys
from paddle import Paddle
from scoreboard import CompetitiveScore, CooperativeScore
from ball import Ball
from referee import Referee
from countdown import Countdown
from settings import settings
from time import sleep

# Setup game objects:
screen = Screen()
setup_screen(screen)
ball = Ball()
referee = Referee()
p1_paddle = Paddle("p1")
p2_paddle = Paddle("p2")
bind_keys(screen, p1_paddle, p2_paddle)

if settings["COOPERATIVE"]:
    coop_score = CooperativeScore()
else:
    p1_score = CompetitiveScore("p1")
    p2_score = CompetitiveScore("p2")

countdown = Countdown()

screen.update()


def start_round():
    """- Reset ball to its starting position and properties \n- Reset paddle positions \n- Display countdown
    \n- Serve ball"""
    p1_paddle.freeze = True
    p2_paddle.freeze = True
    sleep(2)

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
    \n- Add point to score in coop mode if paddle collision \n- Refresh screen"""
    ball.move()

    if ball.wall_collision():
        ball.apply_direction_change_after_wall_collision()

    paddle_collision = ball.paddle_collision(p1_paddle, p2_paddle)
    if paddle_collision[0]:
        ball.apply_changes_after_paddle_collision(paddle_collision[1])
        if settings["COOPERATIVE"]:
            coop_score.update_score()

    screen.update()
    sleep(1 / settings["FRAME RATE"])


# Game starts here:
if settings["COOPERATIVE"]:
    print(f"Current Top Score: {coop_score.coop_top_score}")
    start_round()

    game_end = False
    while not game_end:
        generate_next_frame()
        game_end = referee.check_game_end_coop(ball, coop_score)

    coop_score.update_coop_top_score()

if not settings["COOPERATIVE"]:
    game_end = False
    while not game_end:
        start_round()

        goal_scored = False
        while not goal_scored:
            generate_next_frame()
            goal_scored = referee.check_goal_scored(ball, p1_score, p2_score)
            game_end = referee.check_game_end_competitive(p1_score, p2_score)

screen.exitonclick()

# TODO: continuous paddle moving without blocking other keys possible?
# TODO: very occasionally, the ball can get stuck in one of the walls. Find a fix for this glitch
# TODO: add max angle as a setting
# TODO: make a settings GUI for the user
# TODO: calculation of x-speed and y-speed can probably be simplified - calculate heading integer
#       (instead of constantly calculating speed floats) and apply to ball heading. (How to change heading
#       without changing appearance of the sprite?)
# TODO: program some "surprise modes" - for example, there's a 5% chance that there's more than one ball in a round,
#       or the ball is extra big, etc.
# TODO: there could be special powers that appear on the screen occasionally and that you can pick up by hitting them
#       with the ball. For example, if you hit the ball, the ball will curve unexpectedly when moving toward
#       your opponent, or the opponent will only see the ball on the second half of the screen (so it's difficult
#       to anticipate), or the ball is momentarily extra fast, etc.
