#!/usr/bin/python3

#Name: Matthew Pessolano and Nicholas Campola
#Date: March 21st 2019
#Description: The client code for our Connect 4 solution. The client will be in charge of sending an acknowledgement when receiving the rules from the server, sending its choice of col, and receiving the board until a winner is decided. This will allow the user to play the game against an AI.
#I pledge that we have not received any unauthorized help on this assignment.
import numpy as np
import random
import socket
import time

#Description: checkwin checks the [x,y] coordinates of the board for matching values in specific directions that would equal a win in connect 4
#Parameter: Board array to access the x and y coordinates for checking possible 3-in-a-rows.
#Output: returns a boolean
def checkwin(board, x, y, player):
        WIDTH = 6
        HEIGHT = 7
        win = False
        if(not(x+3 >= HEIGHT-1)):
                #print("Horizontal check")
                if(board[x+1][y] == player): #Horizontal -
                        #print("Horizontal check 1")
                        if(board[x+2][y] == player):
                                #print("Horizontal check 2")
                                if(board[x+3][y] == player):
                                        #print("Horizontal check win")
                                        win = True
                                        
        if(not((y+3) >= WIDTH-1)):
                #print("Vertical check begin")
                if(board[x][y+1] == player):  #Vertical |
                        #print("Vertical check 1")
                        if(board[x][y+2] == player):
                                #print("Vertical check 2")
                                if(board[x][y+3] == player):
                                        #print("Vertical check 3")
                                        win = True
                                        
        if(not(x+3 >= HEIGHT-1) and not((y+3) >= WIDTH-1)):
                #print("Diagonal check /")
                if(board[x+1][y+1] == player):  #Diagonal /
                        if(board[x+2][y+2] == player):
                                if(board[x+3][y+3] == player):
                                        win = True
                                        
        if(not(x-3 < 0) and not((y+3) >= HEIGHT-1)):    
                #print("Diagonal check \ ")
                if(board[x-1][y+1] == player):  #Diagonal \
                        if(board[x-2][y+2] == player):
                                if(board[x-3][y+3] == player):
                                        win = True

        if(win == True):
                return player
        else:
                return 0
                
#Description: aiCheck intends to run the majority of the AI's decision making. In this, it will look for the player's pieces and try to find any potential wins on the next turn.
#Parameter: Board array to access the x and y coordinates for checking possible 3-in-a-rows.
#Output: the x axis value to block the player, or -1 otherwise is no block is present.
def aiCheck(board):
        WIDTH = 6
        HEIGHT = 7
        for i in range(HEIGHT):
                for j in range(WIDTH):
                        if(board[i][j] == 1):
                                if(not(i+3 >= HEIGHT-1)):
                                        #print("Horizontal check")
                                        if(board[i+1][j] == 1): #Horizontal -
                                                #print("Horizontal check 1")
                                                if(board[i+2][j] == 1):
                                                        #print("Horizontal check 2")
                                                        return i+3                                  
                                if(not((j+3) >= WIDTH-1)):
                                        #print("Vertical check begin")
                                        if(board[i][j+1] == 1):  #Vertical |
                                                #print("Vertical check 1")
                                                if(board[i][j+2] == 1):
                                                        #print("Vertical check 2")
                                                        return i
        return random.randint(0,5)
                                        

#host and port information to connect to
HOST = "10.142.0.2"
PORT = 4040

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allow us to reuse an address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# set the socket host and port number up
sock.bind((HOST, PORT))

# listen for any clients connecting
sock.listen()
while(True):
        # wait for a client to connect to us
        # accept a connection which has come through
        conn, addr = sock.accept()
        
        
        #Rules for connect 4
        string = "Rules are simple: Choose a column to place your chip, first to get four in a row in any direction wins"
        data = string.encode()
        conn.sendall(data)
        
        #Waiting for ACK to continue
        data = conn.recv(1024)
        waiting = data.decode()
        
        #Height and width cap
        WIDTH = 6
        HEIGHT = 7
        
        
        #Creating game board
        board = np.zeros(WIDTH * HEIGHT)
        board.shape = (WIDTH, HEIGHT)
        gameOver = 0
        winner = 0
        
        
        while(gameOver != 1):
                #Printing Board
                printedBoard = ""
                for i in range(HEIGHT-1, -1, -1):
                        printedBoard = printedBoard + "\n"
                        for j in range(WIDTH):
                            printedBoard = printedBoard + str(int(board[j][i])) + " "
                data = printedBoard.encode()
                conn.sendall(data)
                valid = False
                while(valid == False):
                #Getting column from client     
                        data = conn.recv(1024)
                        checkerCol = int(data.decode())
                 
                        checkerRow = HEIGHT
                
                        for i in range(HEIGHT):
                                if(board[checkerCol][i] == 0):
                                        checkerRow = checkerRow - 1
                        if(checkerRow != HEIGHT and board[checkerCol][checkerRow] == 0):
                                board[checkerCol][checkerRow] = 1
                                #Valid column
                                data = "0".encode()
                                conn.sendall(data)
                                valid = True
                        else:
                                #Invalid column
                                data = "1".encode()
                                conn.sendall(data)
                
                
                checkerRow = HEIGHT
                checked = False
                
                while(checkerRow == HEIGHT):
                        if(checked != False):
                                checkerCol = aiCheck(board)
                        else:
                                checkerCol = random.randint(0,5)
                        checkerRow = HEIGHT
                        
                        for i in range(HEIGHT):
                                if(board[checkerCol][i] == 0):
                                        checkerRow = checkerRow - 1
                        #print(checkerRow)
                        #print(" ")
                        if(checkerRow != 7):
                                if(board[checkerCol][checkerRow] == 0):
                                        board[checkerCol][checkerRow] = 2
                
                for i in range(HEIGHT):
                        for j in range(WIDTH):
                                if(board[j][i] != 0):
                                        if(winner == 0):
                                                winner = checkwin(board, j, i, board[j][i])
        
                if(winner != 0):
                        print("Player " + str(winner) + " is the winner!")
                        if(winner == 1):
                                data = "2".encode()
                                time.sleep(1)
                                conn.sendall(data)
                        else:
                                data = "3".encode()
                                time.sleep(1)
                                conn.sendall(data)
                        gameOver = 1
                else:
                        #Continue to play
                        check = "1".encode()
                        conn.sendall(check)
                        time.sleep(1)        
        conn.close()
sock.close()  
