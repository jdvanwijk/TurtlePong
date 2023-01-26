from settings import settings


def setup_screen(game_screen):
    """Sets up the screen (resolution, background color, screen title, colormode, tracer, listen)"""
    game_screen.setup(width=settings["SCREEN WIDTH"], height=settings["SCREEN HEIGHT"])
    game_screen.bgcolor(settings["SCREEN BG COLOR"])
    game_screen.title(settings["SCREEN TITLE"])
    game_screen.colormode(255)
    game_screen.tracer(0)
    game_screen.listen()


def bind_keys(game_screen, p1_paddle, p2_paddle):
    """Binds the keys inputs to the player paddles"""
    # Capital letters are included so that the paddle still moves when Caps Lock is turned on:
    game_screen.onkey(p1_paddle.move_up, "w")
    game_screen.onkey(p1_paddle.move_up, "W")
    game_screen.onkey(p1_paddle.move_down, "s")
    game_screen.onkey(p1_paddle.move_down, "S")
    game_screen.onkey(p2_paddle.move_up, "Up")
    game_screen.onkey(p2_paddle.move_down, "Down")
