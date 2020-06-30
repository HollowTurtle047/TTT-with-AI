
from collections import Counter

BOARD = [0,1,2,3,4,5,6,7,8]

def main():
    
    board = BOARD
    player1 = []
    player2 = []
    
    while True:
        if not board:
            return 'Draw'
        
        # player 1 turn
        
        # player 2 turn

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
    
if '__name__' == '__main__':
    main()