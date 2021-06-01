""" Python Top Down Shooter - ZombieDungeon
    *
    *

    param:
        Author: Stefan Nemanja Banov & Phillip Tran
        Date: 06.06.2021
        Version: 1.0.0
        License: free

"""


class Score:

    def __init__(self):
        self.score = 0

    # ------- Score Manipulation ------- #

    def add_score(self, score):
        """
        add_score

            add a certain amount of

            param:
                score(int): the amount that should be added to the score

            return:
                none

            test:
                * score increases
        """
        self.score += score