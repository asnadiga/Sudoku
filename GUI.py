'''
Created on May 11, 2020

@author: Aniruddha Nadiga
'''
import pygame
from random import randrange
from solver import solve, poss_vals
from time import sleep 

pygame.init()
pygame.font.init()

white = (255,255,255)
black = (0,0,0)
gray = (128,128,128)


class Grid:
    #class that represents the board
    def __init__(self, width):
        #Pick one of 50 starting board randomly
        r = randrange(0,50)
        self.board = []
        f = open("sudoku.txt")
        lines = f.readlines()
        for i in range(9):
            curRow = []
            for j in range(9):
                curRow.append(int(lines[10*r+i+1][j]))
            self.board.append(curRow)
            
        #round width to nearest multiple of 9
        self.width = (width//9)*9
        
        #each square in the sudoku board is an object
        self.squares = [[Square(self.board[i][j], i, j, self.width) for j in range(9)]for i in range(9)]
        
        #currently selected square
        self.selected = (0,0)
        
    def draw(self, win):
        #draws current board on win
        win.fill(white)

        for i in range(10):
            for j in range(10):
                
                #drawing grid lines
                if i%3 == 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(win, black,(i*self.width//9,0),(i*self.width//9, self.width), thick)   
                    
                if j%3 == 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(win,black, (0, j*self.width//9), (self.width, j*self.width//9),thick)
                
                
                #Drawing current values
                if i<9 and j<9:
                    self.squares[i][j].draw(win)
    
    def select(self, i,j):
        #changing selected square
        self.squares[self.selected[0]][self.selected[1]].selected=False
        self.selected = (i,j)
        self.squares[self.selected[0]][self.selected[1]].selected=True

    
    def list_board(self):
        #returns list of lists representing current board
        boardList = []
        for i in range(9):
            curRow = []
            for j in range(9):
                curRow.append(self.squares[i][j].temp)
            boardList.append(curRow)
        return boardList
                
            
    
    def set_square(self, entry):
        #sets the selected square to entered value if it does not cause a contradiction
        i = self.selected[0]
        j = self.selected[1]
        if self.squares[i][j].value == 0:
            lb = self.list_board()
            lb[i][j] = 0
            if entry in poss_vals(lb, i, j):
                self.squares[i][j].temp = entry
    
    def is_finished(self):
        #checks if board is solved
        for i in range(9):
            for j in range(9):
                if self.squares[i][j].temp == 0:
                    return False
        return True
    
    def finish(self):
        #solves the puzzle and fills in the values
        solved = solve(self.board)
        for i in range(9):
            for j in range(9):
                self.squares[i][j].temp = solved[i][j]
class Square:
    #class representing a given square
    def __init__(self, value, row, col, width):
        self.width = width//9
        self.value = value
        self.row = row
        self.col = col
        self.temp = value
        self.selected = False
        
    def draw(self, win):
        #renders self on win. Black text for initial values and gray for user entered ones
        font = pygame.font.SysFont("comicsans", 50)
        if self.temp != 0:
            if self.value != 0:
                text = str(self.value)
                color = black
    
            else:
                text = str(self.temp)
                color = gray
            ent = font.render(text, 1, color)
            win.blit(ent, (self.col*self.width+20, self.row*self.width+15))
        #gives selected box a red outline
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (self.col*self.width,self.row*self.width, self.width ,self.width), 3)            

            



def main():
    win = pygame.display.set_mode((540,600))
    win.fill(white)
    pygame.display.set_caption("Sudoku")
    grid = Grid(540)
    grid.draw(win)
    
    #pygame.event.set_blocked(pygame.MOUSEMOTION)
    #pygame.event.set_blocked(pygame.ACTIVEEVENT)
    #pygame.event.set_blocked(pygame.VIDEOEXPOSE)
    #pygame.event.set_blocked(pygame.KEYUP)
    
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT])
    
    go = True
    newGame = True
    
    startScreen = pygame.image.load("startScreen.png")
    botBanner = pygame.image.load("botBanner.png")
    endBanner = pygame.image.load("endBanner.png")
    
    
    
    
    while go:
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        
        while newGame:
            win.blit(startScreen, (0,0))
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                go = False
            
            newGame = False        
        
        if go == False:
            break
        
        grid.draw(win)
        win.blit(botBanner, (0,540))
        pygame.display.update()  
        
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            go = False
            
        if event.type == pygame.KEYDOWN:
            keyName = pygame.key.name(event.key)
            if keyName.isdigit():
                grid.set_square(int(keyName))
                grid.draw(win)
                pygame.display.update()
                
            if keyName == 'f':
                grid.finish()
                grid.draw(win)
                pygame.display.update()
        
        #select clicked box        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[1]<=540:
                grid.select((pos[1]//(grid.width//9)),(pos[0]//(grid.width//9)))
            
        if grid.is_finished():
            
            #final update before new game or quit
            grid.draw(win)
            win.blit(endBanner, (0,540))
            pygame.display.update()
            
            #wait for a key press or quit
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                go = False
            if event.type == pygame.KEYDOWN:
                grid = Grid(540)
                newGame = True
            

            
            
if __name__=="__main__":
    main()
