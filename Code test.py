import random
import sys

def drawBoard(board):
    
    HLINE = ' +---+---+---+---+---+---+---+---+ '
    VLINE = ' |   |   |   |   |   |   |   |   | '
    
    print(' 1  2  3  4  5  6  7  8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end='')
        for x in range(8):
            print('| %s' % (board[x][y]), end='')
        print('|')
        print(VLINE)
        print(HLINE)