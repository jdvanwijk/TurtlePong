from turtle import Screen
from screen_setup import setup_screen, bind_keys
from paddle import Paddle
from scoreboard import CompetitiveScore, CooperativeScore
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

if settings["COOPERATIVE"]:
    coop_score = CooperativeScore()
else:
    p1_score = CompetitiveScore("p1")
    p2_score = CompetitiveScore("p2")

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


def check_for_goal():
    """Check if a goal was scored and if so, add a point to that player's (competitive mode only)"""
    goal_report = ball.check_goal()
    if goal_report[0]:
        goal = True
        if goal_report[1] == "p1":
            p1_score.update_score()
        elif goal_report[1] == "p2":
            p2_score.update_score()
        screen.update()
        if not game_end:
            sleep(2.5)
    else:
        goal = False

    return goal


def check_for_game_end():
    """Check if the end game score determined in settings['END GAME SCORE'] has been reached by one of the players"""
    if settings["COOPERATIVE"]:
        ball_exit_screen_xcor = (settings["SCREEN WIDTH"] / 2) + (settings["BALL SIZE"] / 2)
        if abs(ball.xcor()) >= ball_exit_screen_xcor:
            is_game_over = True
        else:
            is_game_over = False

    if not settings["COOPERATIVE"]:
        if p1_score.points >= settings["GAME END SCORE"] or p2_score.points >= settings["GAME END SCORE"]:
            is_game_over = True
            if p1_score.points > p2_score.points:
                print(f"GAME OVER, {p1_score.player.upper()} WINS!")
            else:
                print(f"GAME OVER, {p2_score.player.upper()} WINS!")
        else:
            is_game_over = False

    return is_game_over


# Game starts here:
if settings["COOPERATIVE"]:
    print(f"Current Top Score: {coop_score.coop_top_score}")
    start_round()

    game_end = False
    while not game_end:
        generate_next_frame()
        game_end = check_for_game_end()

    coop_score.update_coop_top_score()

if not settings["COOPERATIVE"]:
    game_end = False
    while not game_end:
        start_round()

        goal_scored = False
        while not goal_scored:
            generate_next_frame()
            goal_scored = check_for_goal()
            game_end = check_for_game_end()

screen.exitonclick()

# TODO: continuous paddle moving without blocking other keys possible?
# TODO: calculation of x-speed and y-speed can probably be simplified - calculate heading integer
#       (instead of constantly calculating speed floats) and apply to ball heading. (How to change heading
#       without changing appearance of the sprite?)
# TODO: program some "surprise modes" - for example, there's a 5% chance that there's more than one ball in a round,
#       or the ball is extra big, etc.
# TODO: there could be special powers that appear on the screen occasionally and that you can pick up by hitting them
#       with the ball. For example, if you hit the ball, the ball will curve unexpectedly when moving toward
#       your opponent, or the opponent will only see the ball on the second half of the screen (so it's difficult
#       to anticipate), or the ball is momentarily extra fast, etc.
