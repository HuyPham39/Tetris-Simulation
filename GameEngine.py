# I chose to do all seven options for problem C

import turtle, random

SCALE = 40 #Controls how many pixels wide each grid square is

class Game:
    '''
    Purpose: An object of this class represents a game of Tetris.
    Instance variables:
        self.active: 
            This represents the Tetromino currently being controlled by the player.
        self.occupied: 
            A list of occupied squares in the game.
        self.game_levels: 
            This represents the settings of the game's difficulty and rewards for each level there is.
        self.game_level: 
            The current level of the game.
        self.scores: 
            The current score of the game.
        self.score_board: 
            The turtle responsible for drawing the score board on the screen.
    Methods: 
        gameloop(self):
            This is the gameloop of the game, responsible for making the active Tetromino fall and update the game attributes.
        gameover(self):
            This allows the console to know whether the game is over.
        score_update(self):
            This updates the game score.
        move_left(self):
            Allow the player to move the active Tetromino left.
        move_right(self):
            Allow the player to move the active Tetromino right.
        drop(self):
            Allow the player to drop the active Tetromino to the current floor.
        full_line_status(self, row):
            Checks whether a line is full of squares or not at the specified row.
        line_elimination(self):
            Eliminates all current line of squares in the game and move the above squares down.
        rotate(self):
            This method rotates the active Tetromino 90 degrees clockwise.
        rotate_valid(self, coordinates):
            Checks whether a rotation move is valid.
    '''

    def __init__(self):
        #Setup window size based on SCALE value.
        turtle.setup(SCALE*12+20+100, SCALE*22+20)

        #Bottom left corner of screen is (-1.5,-1.5)
        #Top right corner is (10.5, 20.5)
        turtle.setworldcoordinates(-3.9, -1.5, 10.5, 20.5)
        cv = turtle.getcanvas()
        cv.adjustScrolls()

        #Ensure turtle is running as fast as possible
        turtle.hideturtle()
        turtle.delay(0)
        turtle.speed(0)
        turtle.tracer(0, 0)

        #Draw rectangular play area, height 20, width 10
        turtle.bgcolor('black')
        turtle.pencolor('white')
        turtle.penup()
        turtle.setpos(-0.525, -0.525)
        turtle.pendown()
        for i in range(2):
            turtle.forward(10.05)
            turtle.left(90)
            turtle.forward(20.05)
            turtle.left(90)
        
        self.active = Block(random.randint(1,7))
        self.occupied = []
        for rows in range(23):
            row = []
            for collumns in range(10):
                element = False
                row.append(element)
            self.occupied.append(row)

        self.game_levels = {1:[100,300], 2:[150,200], 3:[200,150], 4:[250,100]}
        self.game_level = 1

        self.scores = 0
        self.score_board = turtle.Turtle()
        self.score_board.pu()
        self.score_board.goto(-2,18)
        self.score_board.color("White")
        self.score_board.hideturtle()
        self.score_board.write(f"Scores: {self.scores}\n Level: {self.game_level}", False, "right", ("Tetramino", 10, "bold"))

        turtle.ontimer(self.gameloop, self.game_levels[self.game_level][1])
        turtle.onkeypress(self.move_left, 'Left')
        turtle.onkeypress(self.move_right, 'Right')
        turtle.onkeypress(self.drop, 'space')
        turtle.onkeypress(self.rotate, 'Up')

        #These three lines must always be at the BOTTOM of __init__
        turtle.update()
        turtle.listen()
        turtle.mainloop()

    def gameloop(self):
        if self.active.valid(0, -1, self.occupied):
            self.active.move(0, -1)
        else:
            for square in self.active.squares:
                self.occupied[square.ycor()] [square.xcor()] = square
            self.line_elimination()
            if self.game_over():
                message = turtle.Turtle()
                message.goto(-2.5,14)
                message.color("White")
                message.hideturtle()
                message.write("GAME\nOVER!!!", False, "center", ("Tetramino", 20, "bold"))
                turtle.update()
                return
            self.active = Block(random.randint(1,7))
        turtle.update()
        turtle.ontimer(self.gameloop, self.game_levels[self.game_level][1]) 

    def game_over(self):
        bottom_square_y = 100
        for square in self.active.squares:
            y = square.ycor()
            if y < bottom_square_y:
                bottom_square_y = y          
        if bottom_square_y > 19:
            return True
        return False

    def score_update(self):
        self.score_board.clear()
        self.scores += self.game_levels[self.game_level][0]
        if self.scores >= 6000:
            self.game_level = 4
        elif self.scores >= 2000:
            self.game_level = 3
        elif self.scores >= 600:
            self.game_level = 2
        self.score_board.write(f"Scores: {self.scores}\n Level: {self.game_level}", False, "right", ("Tetramino", 10, "bold"))
        turtle.update()

    def move_left(self):
        if self.active.valid(-1, 0, self.occupied):
            self.active.move(-1, 0)
        turtle.update()
    
    def move_right(self):
        if self.active.valid(1, 0, self.occupied):
            self.active.move(1, 0)
        turtle.update()

    def drop(self):
        while self.active.valid(0, -1, self.occupied):
            self.active.move(0, -1)
        turtle.update()

    def full_line_status(self, row):
        for collumn in range(10):
            if isinstance(self.occupied[row][collumn], turtle.Turtle) == False:
                return False
        return True

    def line_elimination(self):
        rows_completed = []
        for row in range(23):
            if self.full_line_status(row):
                rows_completed.append(row)
        for row in rows_completed:
            for collumn in range(10):
                self.occupied[row][collumn].goto(-50,0)
                self.occupied[row][collumn] = False
        if len(rows_completed) == 4:
            for i in range(6):
                self.score_update()
        elif len(rows_completed) == 3:
            for i in range(4):
                self.score_update()
        else:
            for i in range(len(rows_completed)):
                self.score_update()
        if rows_completed != []:
            for collumn in range(10):
                for upper_row in range(rows_completed[-1], 23):
                    if isinstance(self.occupied[upper_row][collumn], turtle.Turtle):
                        x = self.occupied[upper_row][collumn].xcor()
                        y = self.occupied[upper_row][collumn].ycor() - len(rows_completed)
                        self.occupied[upper_row][collumn].goto(x, y)
                        self.occupied[upper_row - len(rows_completed)][collumn] = self.occupied[upper_row][collumn]
                        self.occupied[upper_row][collumn] = False
        turtle.update()

    def rotate(self):
        new_pos = [[],[],[],[]]
        i = 0
        if self.active.variation == 1:
            if self.active.squares[0].ycor() == self.active.squares[1].ycor():   
                for square in self.active.squares:
                    new_x = square.ycor() - self.active.squares[2].ycor() + self.active.squares[2].xcor()
                    new_y = self.active.squares[2].xcor() - square.xcor() + self.active.squares[2].ycor()
                    new_pos[i].append(new_x)
                    new_pos[i].append(new_y)
                    i += 1
            else:
                for square in self.active.squares:
                    new_x = self.active.squares[2].ycor() - square.ycor() + self.active.squares[2].xcor()
                    new_y = square.xcor() - self.active.squares[2].xcor() + self.active.squares[2].ycor()
                    new_pos[i].append(new_x)
                    new_pos[i].append(new_y)
                    i += 1                                
        if self.active.variation == 2:
            for square in self.active.squares:
                new_x = square.ycor() - self.active.squares[2].ycor() + self.active.squares[2].xcor()
                new_y = self.active.squares[2].xcor() - square.xcor() + self.active.squares[2].ycor()
                new_pos[i].append(new_x)
                new_pos[i].append(new_y)
                i += 1
        if self.active.variation == 3:
            for square in self.active.squares:
                new_x = square.ycor() - self.active.squares[1].ycor() + self.active.squares[1].xcor()
                new_y = self.active.squares[1].xcor() - square.xcor() + self.active.squares[1].ycor()
                new_pos[i].append(new_x)
                new_pos[i].append(new_y)
                i += 1
        if self.active.variation == 4:
            for square in self.active.squares:
                new_x = square.xcor()
                new_y = square.ycor()
                new_pos[i].append(new_x)
                new_pos[i].append(new_y)
                i += 1
        if self.active.variation == 5:
            if self.active.squares[0].ycor() < self.active.squares[3].ycor():
                for square in self.active.squares:
                    new_x = square.ycor() - self.active.squares[1].ycor() + self.active.squares[1].xcor()
                    new_y = self.active.squares[1].xcor() - square.xcor() + self.active.squares[1].ycor()
                    new_pos[i].append(new_x)
                    new_pos[i].append(new_y)
                    i += 1
            else:
                for square in self.active.squares:
                    new_x = self.active.squares[1].ycor() - square.ycor() + self.active.squares[1].xcor()
                    new_y = square.xcor() - self.active.squares[1].xcor() + self.active.squares[1].ycor()
                    new_pos[i].append(new_x)
                    new_pos[i].append(new_y)
                    i += 1
        if self.active.variation == 6:
            for square in self.active.squares:
                new_x = square.ycor() - self.active.squares[1].ycor() + self.active.squares[1].xcor()
                new_y = self.active.squares[1].xcor() - square.xcor() + self.active.squares[1].ycor()
                new_pos[i].append(new_x)
                new_pos[i].append(new_y)
                i += 1
        if self.active.variation == 7:
            if self.active.squares[0].xcor() < self.active.squares[3].xcor():
                for square in self.active.squares:
                    new_x = square.ycor() - self.active.squares[2].ycor() + self.active.squares[2].xcor()
                    new_y = self.active.squares[2].xcor() - square.xcor() + self.active.squares[2].ycor()
                    new_pos[i].append(new_x)
                    new_pos[i].append(new_y)
                    i += 1
            else:
                for square in self.active.squares:
                    new_x = self.active.squares[2].ycor() - square.ycor() + self.active.squares[2].xcor()
                    new_y = square.xcor() - self.active.squares[2].xcor() + self.active.squares[2].ycor()
                    new_pos[i].append(new_x)
                    new_pos[i].append(new_y)
                    i += 1
        if self.rotate_valid(new_pos):
            for square in range(4):
                self.active.squares[square].goto(new_pos[square][0], new_pos[square][1])
        turtle.update()

    def rotate_valid(self, coordinates):
        for square in range(4):
            x = coordinates[square] [0]
            y = coordinates[square] [1]
            if x < 0 or x > 9:
                return False
            elif y < 0:
                return False
            elif self.occupied[y] [x] != False:
                return False
        return True
         
class Square(turtle.Turtle):
    '''
    Purpose:
        An object of this class represents a square, which is a turtle, in the game.
    Instance variables:
        None
    Methods: 
        None
    '''
    def __init__(self, x, y, color):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.shapesize(SCALE / 20)
        self.speed(0)
        self.fillcolor(color)
        self.pencolor('gray')
        self.penup()
        self.goto(x,y)

class Block:
    '''
    Purpose:
        An object of this class represents a possible Tetromino.
    Instance variables:
        self.squares:
            This is a list of the corresponding squares of the Tetromino.
    Methods:
        move(self):
            Move the Tetromino to the desired location.
        valid(self):
            Checks whether a proposed move is valid or not.
    '''
    def __init__(self, variation):
        self.variation = variation
        if variation == 0:
            self.squares = []
        else:
            self.squares = []
            if variation == 1:
                block1 = Square(3, 21, 'Cyan')
                block2 = Square(4, 21, 'Cyan')
                block3 = Square(5, 21, 'Cyan')
                block4 = Square(6, 21, 'Cyan')
            elif variation == 2:
                block1 = Square(4, 22, 'Blue')
                block2 = Square(4, 21, 'Blue')
                block3 = Square(5, 21, 'Blue')
                block4 = Square(6, 21, 'Blue')
            elif variation == 3:
                block1 = Square(4, 21, 'Orange')
                block2 = Square(5, 21, 'Orange')
                block3 = Square(6, 21, 'Orange')
                block4 = Square(6, 22, 'Orange')
            elif variation == 4:
                block1 = Square(4, 21, 'Yellow')
                block2 = Square(4, 22, 'Yellow')
                block3 = Square(5, 21, 'Yellow')
                block4 = Square(5, 22, 'Yellow')
            elif variation == 5:
                block1 = Square(4, 21, 'Green')
                block2 = Square(5, 21, 'Green')
                block3 = Square(5, 22, 'Green')
                block4 = Square(6, 22, 'Green')
            elif variation == 6:
                block1 = Square(4, 21, 'Purple')
                block2 = Square(5, 21, 'Purple')
                block3 = Square(5, 22, 'Purple')
                block4 = Square(6, 21, 'Purple')
            elif variation == 7:
                block1 = Square(4, 22, 'Red')
                block2 = Square(5, 22, 'Red')
                block3 = Square(5, 21, 'Red')
                block4 = Square(6, 21, 'Red')
            self.squares.append(block1)
            self.squares.append(block2)
            self.squares.append(block3)
            self.squares.append(block4)

    def move(self, dx, dy):
        for square in self.squares:
            x = square.xcor() + dx
            y = square.ycor() + dy
            square.goto(x, y)
    
    def valid(self, dx, dy, occupied):
        for square in self.squares:
            x = square.xcor() + dx
            y = square.ycor() + dy
            if x < 0 or x > 9:
                return False
            elif y < 0:
                return False
            elif occupied[y] [x] != False:
                return False
        return True

if __name__ == '__main__':
        Game()