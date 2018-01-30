#!/usr/bin/python3
# Set the path to your python3 above

# Modified by Kiefer von Gaza and Jonah Quist
# Modifications:
#   Add in score function.

# Set up relative path for util; sys.path[0] is directory of current program
import os, sys
utilpath = sys.path[0] + "/../cmput_496/util"
sys.path.append(utilpath)

from gtp_connection_go1 import GtpConnectionGo1
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard

class Go1():
    def __init__(self):
        """
        Player that selects moves randomly from the set of legal moves.
        With the fill-eye filter.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "Go1"
        self.version = 0.1
    def get_move(self,board, color):
        return GoBoardUtil.generate_random_move(board,color,True)

    def score(self, board, connection):
        empties = board.get_empty_positions(1)
        scratch_board = board.copy().board
        # the scratch board entries have 4 states
        # 9 -> black territory
        # 8 -> white territory
        # 7 -> neutral territory
        # 0 -> undetermined territory
        # evaluate territory
        for e in empties:
            n_colors = []
            for n in [e-1, e+1, e-board.NS, e+board.NS]:
                n_colors.append(scratch_board[n])
            if 1 in n_colors:
                scratch_board[e] = 9
            if 2 in n_colors:
                if scratch_board[e] == 9:
                    scratch_board[e] = 7
                else:
                    scratch_board[e] = 8
        # spread through empty territory
        while 0 in scratch_board:
            for i in range(len(scratch_board)):
                if scratch_board[i] == 0:
                    for n in [i-1, i+1, i-board.NS, i+board.NS]:
                        if scratch_board[n] == 9:
                            scratch_board[i] = 9
                        if scratch_board[n] == 8:
                            if scratch_board[i] == 9:
                                scratch_board[i] = 7
                            else:
                                scratch_board[i] = 8
                        if scratch_board[n] == 7:
                            scratch_board[i] = 7
        score = -connection.komi
        with open('log.txt', 'a') as f:
            f.write(str(scratch_board))
        # count territory
        for i in scratch_board:
            if (i == 9) or (i == 1): 
                score += 1
            elif (i == 8) or (i == 2):
                score -= 1
        # construct return message
        if score < 0:
            return 'W+' + str(abs(score))
        elif score > 0:
            return 'B+' + str(score)
        else:
            return '0'


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnectionGo1(Go1(), board)
    con.start_connection()



if __name__=='__main__':
    run()
