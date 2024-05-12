import sys
sys.path.append('/mnt/c/Users/jroge/OneDrive/Desktop/python_game/') 

from board.board import GameBoard
from character.character import Character

test_board = GameBoard()
ike = Character(show='\u2600')
ix, iy = 0, 0

boyd = Character(show='\u2609')
bx, by = 8, 8

rolf = Character(show='\u2610')
rx, ry = 0, 8

mist = Character(show='\u2629')
mx, my = 8, 0


test_board.board[iy][ix].occupant = ike
ike.x, ike.y = ix, iy

test_board.board[by][bx].occupant = boyd
boyd.x, boyd.y = rx, ry

test_board.board[ry][rx].occupant = rolf
rolf.x, rolf.y = rx, ry

test_board.board[my][mx].occupant = mist
mist.x, mist.y = rx, ry