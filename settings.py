settings = {
    "SCREEN WIDTH": 640,
    "SCREEN HEIGHT": 480,
    "FRAME RATE": 120,
    "SCREEN BG COLOR": "black",
    "SCREEN TITLE": "P0NG",

    "BALL SIZE": 15,
    "BALL COLOR": (255, 255, 255),
    "BALL SPEED": 2,                        # Amount of pixels the ball moves at every screen refresh

    "BALL SPEED UP": True,                  # Can be turned off if user does not want ball to speed up during the game
    "BALL MAX SPEED UP": 2,                 # The total amount of pixels that the ball is allowed to accelerate
    "BALL COLOR GRADIENT": [(255, 255, 255), (255, 234, 226), (255, 213, 198), (255, 191, 170),
                            (255, 169, 143), (255, 147, 116), (255, 123, 90), (255, 97, 64), (255, 65, 36),
                            (255, 0, 0)],   # IMPORTANT: first value needs to be the same as "BALL COLOR"

    "PADDLE WIDTH": 12,
    "PADDLE LENGTH": 60,
    "PADDLE SPEED": 20,
    "PADDLE DISTANCE FROM GOAL": 70,
    "PADDLE COLOR": "white",

    "SCOREBOARD X-POSITION": 50,
    "SCOREBOARD Y-POSITION": 180,
    "SCOREBOARD FONT": ("Courier", 30, "bold"),
    "SCOREBOARD ALIGNMENT": "center",

    "COUNTDOWN FONT": ("Courier", 60, "bold"),
    "COUNTDOWN ALIGNMENT": "center",
    "COUNTDOWN TIME": 3,

    "GAME END SCORE": 5,
}
