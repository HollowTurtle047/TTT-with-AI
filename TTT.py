
from collections import Counter
import numpy as np
import copy

BOARD = [0]*9
cur_turn = True
p1_record = []
p2_record = []
record_path = 'record.npy'

def main():
    
    board = BOARD
    global cur_turn
    
    while True:
        block = index_in_board(board, 0)
        if not block:
            print('Draw')
            return 0
        
        if cur_turn:
            # player 1 turn
            show(board)
            board = turn(board)
            player = index_in_board(board, 1)
            if isWin(player):
                show(board) # show the final board
                np.save(record_path, np.array(p1_record)) # save the winner decision
                print('player1 win')
                return 1
        else:
            # player 2 turn
            show(board)
            board = turn([-i for i in board])
            player = index_in_board(board, 1)
            board = [-i for i in board]
            if isWin(player):
                show(board)
                np.save(record_path, np.array(p1_record)) # save the winner decision
                print('player2 win')
                return 2
        cur_turn = not cur_turn
        
def isWin(player):
    row = [i//3 for i in player]
    col = [i%3 for i in player]
    
    if 0 in player and 4 in player and 8 in player:
        return True
    elif 2 in player and 4 in player and 6 in player:
        return True
    elif Counter(row).most_common(1)[0][1] == 3:
        return True
    elif Counter(col).most_common(1)[0][1] == 3:
        return True
    else:
        return False
    
def turn(board):
    # board 0:block 1:player -1:opponent
    pos = human_player(board)
    t = [0]*9
    t[pos] = 1
    print('test:{} and {}'.format(board,t))
    if cur_turn:
        p1_record.append([copy.deepcopy(board),t])
    else:
        p2_record.append([copy.deepcopy(board),t])
    board[pos] = 1
    return board
    
def show(board):
    num2piece = {0:' ', 1:'*', -1:'#'}
    board = [num2piece[x] if x in board else x for x in board]
    print('')
    print(' {} | {} | {} '.format(board[0],board[1],board[2]))
    print('---+---+---')
    print(' {} | {} | {} '.format(board[3],board[4],board[5]))
    print('---+---+---')
    print(' {} | {} | {} '.format(board[6],board[7],board[8]))
    
def index_in_board(board, piece):
    return [i for i,x in enumerate(board) if x==piece]

def valid_input(valid_list, mesg):
    valid_list = [str(i) for i in valid_list]
    while True:
        inputStr = input(mesg + '\r\n').upper()
        if inputStr in valid_list:
            return inputStr
        print('Invalid input')
        
def human_player(board):
    block = index_in_board(board, 0)
    pos = valid_input(block, ''.join(map(str,block)))
    return int(pos)

if __name__ == '__main__':
    main()