from tkinter import *
import numpy as np

SIZE_OF_BOARD = 600
SYMBOL_SIZE = (SIZE_OF_BOARD//3-SIZE_OF_BOARD//8)//2
SYMBOL_THICKNESS = 50
RED = '#EE4035'
BLUE = '#0492CF'
GREEN = '#7BC043'


class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('tic-tac-toe')
        self.canvas = Canvas(self.window, width=SIZE_OF_BOARD, height=SIZE_OF_BOARD)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.initboard()
        self.Xturn = True
        self.XWins = 0
        self.OWins = 0
        self.ties = 0

    def mainloop(self):
        self.window.mainloop()

    def initboard(self):
        self.boardStatus = np.zeros((3, 3))
        for i in [1/3, 2/3]:
            self.canvas.create_line(i*SIZE_OF_BOARD, 0, i*SIZE_OF_BOARD, SIZE_OF_BOARD, width=3)
            self.canvas.create_line(0, i*SIZE_OF_BOARD, SIZE_OF_BOARD, i*SIZE_OF_BOARD, width=3)
        self.gameover = False

    def click(self, event):
        pos = [event.x, event.y]
        gridPos = self.convertPos(pos)
        if not self.gameover:
            if self.boardStatus[gridPos[0]][gridPos[1]] == 0:
                if self.Xturn:
                    self.drawX(gridPos)
                    self.boardStatus[gridPos[0]][gridPos[1]] = -1
                else:
                    self.drawO(gridPos)
                    self.boardStatus[gridPos[0]][gridPos[1]] = 1
                self.Xturn = not self.Xturn
        else:
            self.canvas.delete('all')
            self.initboard()
        msg = self.isGameOver()
        if self.gameover:
            self.displayGameover(msg)

    def convertPos(self, pos):
        pos = np.array(pos, dtype=int)
        return np.array(pos//(SIZE_OF_BOARD/3), dtype=int)

    def convertGrid(self, gridpos):
        return (SIZE_OF_BOARD//3)*gridpos+SIZE_OF_BOARD//6

    def drawX(self, gridPos):
        pos = self.convertGrid(gridPos)
        self.canvas.create_line(pos[0]-SYMBOL_SIZE, pos[1]-SYMBOL_SIZE,
                                pos[0]+SYMBOL_SIZE, pos[1]+SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, fill=RED)
        self.canvas.create_line(pos[0]+SYMBOL_SIZE, pos[1]-SYMBOL_SIZE,
                                pos[0]-SYMBOL_SIZE, pos[1]+SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, fill=RED)

    def drawO(self, gridPos):
        pos = self.convertGrid(gridPos)
        self.canvas.create_oval(pos[0]-SYMBOL_SIZE, pos[1]-SYMBOL_SIZE,
                                pos[0]+SYMBOL_SIZE, pos[1]+SYMBOL_SIZE,
                                width=SYMBOL_THICKNESS, outline=BLUE)

    def isWinner(self, player):
        for i in range(3):
            if self.boardStatus[i][0] == self.boardStatus[i][1] == self.boardStatus[i][2] == player:
                return True
            if self.boardStatus[0][i] == self.boardStatus[1][i] == self.boardStatus[2][i] == player:
                return True
        if self.boardStatus[0][0] == self.boardStatus[1][1] == self.boardStatus[2][2] == player:
            return True
        if self.boardStatus[0][2] == self.boardStatus[1][1] == self.boardStatus[2][0] == player:
            return True
        return False

    def isTie(self):
        r, c = np.where(self.boardStatus == 0)
        if len(r) == 0:
            return True
        else:
            return False

    def isGameOver(self):
        if self.isWinner(-1):
            self.gameover = True
            return 'X wins!'
        if self.isWinner(1):
            self.gameover = True
            return 'O wins!'
        if self.isTie():
            self.gameover = True
            return "it's a tie!"
        return ''

    def displayGameover(self, msg):
        if msg == 'X wins!':
            self.XWins += 1
            color = RED
        elif msg == 'O wins!':
            self.OWins += 1
            color = BLUE
        else:
            self.ties += 1
            color = GREEN
        self.canvas.delete('all')
        self.canvas.create_text(SIZE_OF_BOARD//2, SIZE_OF_BOARD//4, font='cmr 60 bold', fill=color, text=msg)
        scoreText = '   scores \n'
        scoreText += 'player X: ' + str(self.XWins) + '\n'
        scoreText += 'player O: ' + str(self.OWins) + '\n'
        scoreText += '    ties: ' + str(self.ties) + '\n'
        self.canvas.create_text(SIZE_OF_BOARD//2, 5*SIZE_OF_BOARD//8, font='cmr 40 bold', fill=GREEN, text=scoreText)
        self.canvas.create_text(SIZE_OF_BOARD//2, 15*SIZE_OF_BOARD//16, font='cmr 20 bold',
                                fill='gray', text='click to play again')


game = TicTacToe()
game.mainloop()
