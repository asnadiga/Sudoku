'''
Created on May 11, 2020

@author: Aniruddha Nadiga
'''
from os import system, name 
from time import sleep 



board = grid = [
[4, 0, 0, 0, 0, 5, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 9, 8],
[3, 0, 0, 0, 8, 2, 4, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 8, 0],
[9, 0, 3, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 3, 0, 6, 7, 0],
[0, 5, 0, 0, 0, 9, 0, 0, 0],
[0, 0, 0, 2, 0, 0, 9, 0, 7],
[6, 4, 0, 3, 0, 0, 0, 0, 0]
]



def print_board(board):
    for row in range(len(board)):
        if row%3 == 0:
            print("-"*60)
        for col in range(len(board[row])):
            if col%3==0:
                print('|', end = '  ')
            else:
                print('   ', end='')
            if(board[row][col]==0):
                print('*', end='  ')
            else:
                print(board[row][col], end='  ')
        print('|') 
         
def poss_vals(curBoard, i,j):
    possible = [1,2,3,4,5,6,7,8,9]
    return poss_col(curBoard, poss_row(curBoard, poss_box(curBoard, possible, i, j), i), j)

def poss_row(curBoard, possible, i):
    return [x for x in possible if x not in curBoard[i]]

def poss_col(curBoard, possible, j):
    temp = []
    for row in range(9):
        temp.append(curBoard[row][j])
    return [x for x in possible if x not in temp]

def poss_box(curBoard, possible, i ,j):
    temp = []
    for row in range(3):
        for col in range(3):
            temp.append(curBoard[(i//3)*3+row][(j//3)*3+col])
    return [x for x in possible if x not in temp]

def find_empty(curBoard):
    for i in range(9):
        for j in range(9):
            if curBoard[i][j] == 0:
                return (i,j)
    return None

def solve(curBoard):
    cur = find_empty(curBoard)
    
    if not cur:
        return curBoard
    else: 
        row, col = cur
        
    for guess in poss_vals(curBoard, row, col):
        curBoard[row][col] = guess
        if solve(curBoard):
            return curBoard
        else:
            curBoard[row][col] = 0
    return False

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    else: 
        _ = system('clear') 


def main():
    print_board(board)
    solved = solve(board)
    print("----------------------------")
    print_board(solved)
if __name__== "__main__":
    main()