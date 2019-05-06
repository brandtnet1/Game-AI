import random

if random.random() >= .5: # 50% of the time humans start first, other computer starts first
    human_moves_first = True
    computer_symbol = 'O'
    human_symbol = 'X'
    turn_index = 0
else:
    human_moves_first = False
    computer_symbol = 'X'
    human_symbol = 'O'
    turn_index = 1

def wins(board):
    """Return true is there is a winner, also returns current players symbol if true"""
    # Check rows for winner
    for row in range(6):
        for col in range(4):
            if (board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]) and (board[row][col] != 0):
                return True, board[row][col]
    
    # Check columns for winner
    for row in range(3):
        for col in range(7):
            if (board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]) and (board[row][col] != 0):
                return True, board[row][col]
    
    # Check diagonals for winner
    for row in range(3):
        for col in range(4):
            if (board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]) and (board[row][col] != 0):
                return True, board[row][col]

    for row in range(5, 2, -1):
        for col in range(3):
            if (board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]) and (board[row][col] != 0):
                return True, board[row][col]
    # No win
    return False, ' '
    
def score(board):
    """Score a given board from the computer's perspective.
    
       Computer wins score 1 (best outcome for the computer)
       Human wins score -1 (worst outcome for the computer)
       Ties and incomplete games are 0
    """
    if wins(board)[1] == computer_symbol:
        return 1
    elif wins(board)[1] == human_symbol:
        return -1
    else:
        return 0
 
        
def minimax(board, depth, alpha, beta, is_max_player):
    """Execute the minimax algorithm by exploring the subtree, identifying the
       move at each level that yields the best outcome for its player
       
       Returns: 
           the best score that the player can obtain in this subtree
           the move yielding that best score
    """
    # Base conditions: return a score
    current_score = score(board)
    if current_score != 0 or depth == 0:
        return current_score, None
        
    possible_moves = []
    
    for move in range(7): # In possible_moves, index is column # and value at that index is the lowest free row
        possible_moves.append(possible_move(board,move))
        
    if is_max_player:
        best_value = -100
        best_move = None
        
        for move in range(len(possible_moves)):
            i = possible_moves[move]

            if i == None or i == -1: # If theres no open row in the current column
                continue

            board[i][move] = computer_symbol
            value, response = minimax(board, depth - 1, alpha, beta, False)
            board[i][move] = 0
            
            alpha = max(alpha, value)
            
            if value > best_value:
                best_value = value
                best_move = move
                    
            if beta <= alpha:
                break
                  
    if not is_max_player:
        best_value = 100
        best_move = None
        
        for move in range(len(possible_moves)):
            i = possible_moves[move]
            
            if i == None or i == -1: # If theres no open row in the current column
                continue
            
            board[i][move] = human_symbol
            value, response = minimax(board, depth - 1, alpha, beta, True)
            board[i][move] = 0
            
            beta = min(beta, value)

            if value < best_value:
                best_value = value
                best_move = move

            if beta <= alpha:
                break

    return best_value, best_move
    
def display(board):
    print ''
    
    for row in range(6):
        for col in range(7):
            print board[row][col],
        print '\n',

    print ''
    
def possible_move(board, move):
    for i in range (5, - 1, - 1):
        if i == 0:
            if board[i][move] != 0: # No open row
                return None
        if board[i][move] == 0: # Open row, return its index
            return i
    
def get_move(board, playerSymbol):
    looping = True;
    
    while looping:
        looping = False
        
        print 'Enter a column, 1-7: ',
        move = int(raw_input())
        
        if move < 1 or move > 7:
            print 'Choose a different position.'
            looping = True
            
    make_move(board, move - 1, playerSymbol)

def make_move(board, move, symbol):
    for i in range (5, - 1, - 1):
        if board[i][move] == 0: # Look for an open row
            board[i][move] = symbol
            break
        elif i == 0 and board[i][move] != 0: # None open ask for a new selection
            get_move(board, symbol)
    
def play():
    board = [[0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0]]
             
    turn = 0

    print 'Human is ', human_symbol
    print 'Computer is ', computer_symbol, '\n'
    
    while turn < 42:
        # Human turn
        if turn % 2 == turn_index:
            if turn == 0:
                print '1 2 3 4 5 6 7',
                display(board)
            get_move(board, human_symbol)
        # Computer turn
        else:
            print 'Computers Turn'
            best_value, best_move = minimax(board, 10, -100, 100, True)
            make_move(board, best_move, computer_symbol)
            
        display(board)

        # Check for wins
        if wins(board)[0]:
            if wins(board)[1] == human_symbol:
                print 'Man triumphs over machine!'
                turn = 42
            elif wins(board)[1] == computer_symbol:
                print 'A dark day for humanity...'
                turn = 42
        
        turn += 1
     
    if turn == 42:  
        print 'The only winning move is not to play.'
        
play()