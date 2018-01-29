#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
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


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnectionGo1(Go1(), board)
    con.start_connection()

def score():
	empties = self.board.get_empty_positions()
	scratch_board = self.board.copy()
	# the scratch board entries have 4 states
	# 9 -> black territory
	# 8 -> white territory
	# 7 -> neutral territory
	# 0 -> undetermined territory
	# evaluate territory
	for e in empties:
		n_colors = []
		# does this part work? i have no fuckin idea
		for n in self.board._neighbours(e):
			n_colors.append(scratch_board[n])
		if 1 in n_colors:
			scratch_board[e] == 9
		if 2 in n_colors:
			if scratch_board[e] == 9:
				scratch_board[e] = 7
			else:
				scratch_board[e] = 8
	score_b = 0
	# count territory
	for i in scratch_board:
		if scratch_board[i] == 9 
			score += 1
		elif scratch_board[i] == 8:
			score -= 1
	# construct return message
	if score < 0:
		return 'W+' + str(score)
	elif score > 0:
		return 'B+' + str(score)
	else:
		return '0'

if __name__=='__main__':
    run()
