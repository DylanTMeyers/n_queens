
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import *
from os.path import exists
import random
import math
from PIL import Image, ImageTk
class game():

    def __init__(self, rows, solution,moves,time = 0):
        self.rows = rows
        self.square_size = math.trunc(64/(rows/14))

        self.root = tk.Tk()

        self.root.geometry('1000x1000')
        
        self.square_middle = {}
        self.create_canvas(self.root)
        ttk.Button(self.canvas, text= "Exit", command= self.root.destroy)

        self.solution = solution
        self.moves = moves
        self.on_queen = False
        self.curr_queen = -10
        

        self.queens = {}


        image=Image.open('images/Q_black.png')
        image = image.convert('RGBA')
        # Transparency
        newImage = []
        for item in image.getdata():
            if item[:3] == (255, 255, 255):
                newImage.append((255, 255, 255, 0))
            else:
                newImage.append(item)

        image.putdata(newImage)

        # Resize the image in the given (width, height)
        img=image.resize((self.square_size, self.square_size))

        # Conver the image in TkImage
        self.img=ImageTk.PhotoImage(img)

        
        self.draw_pieces()
        if self.query_solution():
                self.canvas.create_text(500, 970, text=f"It took {time} seconds", fill="blue", font=('Helvetica 20 bold'))
                self.canvas.create_text(500, (500 -( self.rows*self.square_size/2)-20), text="THIS IS A SOLUTION!", fill="blue", font=('Helvetica 20 bold'))
            

        else:
            self.canvas.create_text(500, (500 -( self.rows*self.square_size/2)-20), text="THIS IS NOT A SOLUTION!", fill="red", font=('Helvetica 20 bold'))
            btn = Button(self.root, text='Find a solution', width=10,
             height=1, bd='10', command=self.root.destroy)
            btn.place(x=450, y=950)
 

        self.root.mainloop()
        

    def create_canvas(self,root):
        self.canvas = tk.Canvas(root,width=1000,
           height=1000)
        self.canvas.bind('<Motion>', self.handlehover)

        self.canvas.pack()
        self.draw_board()
        

    def draw_board(self):
        curr_col = 'khaki'
        num_x = 0
        for x in range(0,self.rows*self.square_size,self.square_size):
            num_y = 0
            for y in range(0,self.rows*self.square_size,self.square_size):

                x2, y2 = x + self.square_size, y + self.square_size
                x_1 = x+ (500 -( self.rows*self.square_size/2))
                y_1 = y+ (500 -( self.rows*self.square_size/2))
                x_2= x2 +(500 -( self.rows*self.square_size/2))
                y_2 = y2 + (500 -( self.rows*self.square_size/2))

                self.canvas.create_rectangle(x_1, y_1, x_2, y_2, fill=curr_col)
                self.square_middle[(num_x, num_y)] = (x_2+((x_1-x_2)/2),y_2+(y_1-y_2)/2)
                num_y = num_y + 1
                curr_col = ('khaki'
                    if curr_col == 'cornflower blue'
                    else'cornflower blue')

            if self.rows%2 ==0:
                curr_col = ('khaki'
                    if curr_col == 'cornflower blue'
                    else 'cornflower blue')
            num_x = num_x + 1

    def draw_pieces(self):
        for i in range(self.rows):
            self.queens[i,self.solution[i]] = (self.square_middle[i, self.solution[i]][0],self.square_middle[i, self.solution[i]][1])
            self.canvas.create_image(
                self.square_middle[i, self.solution[i]][0],self.square_middle[i, self.solution[i]][1],
                image=self.img, tags='piece')

    def handlehover(self,event):
        num_queens = 0
        for i in self.queens:
            num_queens = num_queens + 1
            if self.on_queen == False and self.queens[i][0]-(self.square_size/2) <event.x and event.x <self.queens[i][0]+(self.square_size/2) and self.queens[i][1]-(self.square_size/2)<event.y and event.y <self.queens[i][1]+(self.square_size/2):

                moves = self.possible_attacks(i)
                self.highlight_moves(moves)
                self.curr_queen = i
                self.canvas.config(cursor="hand1")
                self.on_queen = True
                break
            elif i == self.curr_queen and self.queens[i][0]-(self.square_size/2) <event.x and event.x <self.queens[i][0]+(self.square_size/2) and self.queens[i][1]-(self.square_size/2)<event.y and event.y <self.queens[i][1]+(self.square_size/2):
                self.canvas.config(cursor="hand1")
                break
                
            if num_queens == len(self.queens) and self.on_queen == True:
                self.curr_queen = -10
                self.canvas.config(cursor="")
                self.on_queen = False
        if self.on_queen == False:
            self.canvas.delete("hint")
            
    def possible_attacks(self,piece):
        temp_list = []
        for move in self.moves:
            move1 = move[1].split(",")
            move2 = move[2].split(",")
        
            if int(move1[1]) == piece[0] and int(move1[0]) == piece[1]:
                temp_list.append((move[0],move[2], self.square_middle[(int(move2[1]), int(move2[0]))]))
        return temp_list

    def highlight_moves(self,moves):
        for move in moves:
            if move[0]:
                self.canvas.create_rectangle(
                        move[2][0] - (self.square_size/2),
                        move[2][1] - (self.square_size/2),
                        move[2][0] + (self.square_size/2),
                        move[2][1] + (self.square_size/2),
                        fill='red', tags='hint')
            else:
                self.canvas.create_rectangle(
                        move[2][0] - (self.square_size/2),
                        move[2][1] - (self.square_size/2),
                        move[2][0] + (self.square_size/2),
                        move[2][1] + (self.square_size/2),
                        fill='blue', tags='hint')
                        
    def query_solution(self):
        for move in self.moves:
            if move[0]:
                return False
        return True

        

        




