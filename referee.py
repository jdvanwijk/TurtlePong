from settings import settings


class Referee:
    def check_goal_scored(self, ball, p1_score, p2_score) -> bool:
        """Competitive mode only. Checks if a goal is scored, and awards a point to the scoring player"""
        ball_exit_screen_xcor = (settings["SCREEN WIDTH"] / 2) + (settings["BALL SIZE"] / 2)

        if ball.xcor() >= ball_exit_screen_xcor:
            print("p1 scored a goal")
            goal_scored = True
            p1_score.update_score()
        elif ball.xcor() <= -ball_exit_screen_xcor:
            print("p2 scored a goal")
            goal_scored = True
            p2_score.update_score()
        else:
            goal_scored = False

        return goal_scored

    def check_game_end_coop(self, ball, coop_score) -> bool:
        """Cooperative mode only. Prints "Game Over" message, prints a message if players have exceeded top score and
        returns "is_game_over == True" if ball has left the screen """
        ball_exit_screen_xcor = (settings["SCREEN WIDTH"] / 2) + (settings["BALL SIZE"] / 2)
        if abs(ball.xcor()) >= ball_exit_screen_xcor:
            print("GAME OVER!")
            if coop_score.points > coop_score.coop_top_score:
                print(f"CONGRATULATIONS, NEW TOP SCORE: {coop_score.points}")
            is_game_over = True
        else:
            is_game_over = False

        return is_game_over

    def check_game_end_competitive(self, p1_score, p2_score) -> bool:
        """Competitive mode only. Prints a Game Over message and eturns "is_game_over == True" if a player has reached
        the end game score (defined in settings["END GAME SCORE"] """
        if p1_score.points >= settings["GAME END SCORE"] or p2_score.points >= settings["GAME END SCORE"]:
            is_game_over = True
            if p1_score.points > p2_score.points:
                print(f"GAME OVER, {p1_score.player.upper()} WINS!")
            else:
                print(f"GAME OVER, {p2_score.player.upper()} WINS!")
        else:
            is_game_over = False

        return is_game_over
