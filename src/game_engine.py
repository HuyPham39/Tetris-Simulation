import turtle, random
from .block import Block
from .square import Square
from .constants import SCALE

class Game:
    '''
    Purpose: An object of this class represents a game of Tetris.
    Instance variables:
        self.active: 
            This represents the Tetromino currently being controlled by the player.
        self.map: 
            A list of map squares in the game.
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
        # Setup window size based on SCALE value.
        turtle.setup(SCALE*15, SCALE*22.5)

        # Bottom left corner of screen is (-4.5,-2)
        # Top right corner is (10.5, 20.5)
        turtle.setworldcoordinates(-4.5, -2, 10.5, 20.5)
        cv = turtle.getcanvas()
        cv.adjustScrolls()

        # Ensure the default turtle is running as fast as possible
        turtle.hideturtle()
        turtle.speed(0)
        turtle.tracer(0, 0)
  
        # Draw rectangular play area, height 20, width 10
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
        
        # Game attributes: active moving block, a 2d matrix 
        # representing the game map, and a conditional variable 
        # for line elimination
        self.active = Block(4, 21, random.randint(1,7))
        self.map = [[False] * 10 for i in range(23)]
        self.is_eliminating = False

        # Attributes for the game level mechanics
        self.game_levels = {1:[100,300], 
                            2:[150,200], 
                            3:[200,150], 
                            4:[250,100]}
        self.game_level = 1

        # Draw the score board
        self.scores = 0
        self.score_board = turtle.Turtle()
        self.score_board.pu()
        self.score_board.goto(-2,18)
        self.score_board.color("White")
        self.score_board.hideturtle()
        self.score_board.write(f"Scores: {self.scores}\n" + 
                               f"Level: {self.game_level}",
                               False, 
                               "right", 
                               ("Tetramino", 10, "bold"))

        # As the game level progresses, the timer will run at a faster pace
        turtle.ontimer(self.gameloop, self.game_levels[self.game_level][1])

        # Mapping key presses to functions
        turtle.onkeypress(self.move_left, 'Left')
        turtle.onkeypress(self.move_right, 'Right')
        turtle.onkeypress(self.drop, 'space')
        turtle.onkeypress(self.rotate, 'Up')

        # Finish the setup for the mainloop
        turtle.update()
        turtle.listen()
        turtle.mainloop()

    def gameloop(self):
        # Don't process game loop if line elimination is running
        if self.is_eliminating:
            turtle.ontimer(self.gameloop, self.game_levels[self.game_level][1])
            return
        # Move the active block down by 1 every time gameloop is called
        if self.valid(self.active, 0, -1):
            self.move(self.active, 0, -1)
        else:
            # Updates the 2d matrix game map
            for square in self.active.squares:
                self.map[square.ycor()] [square.xcor()] = square
            # Calls for any line elimination
            self.is_eliminating = True
            self.line_elimination()
            self.is_eliminating = False
            # Check if the game is over
            minY = min([square.ycor() for square in self.active.squares])          
            if minY > 19:
                self.game_over()
                turtle.update()
                return
            self.active = Block(4, 21, random.randint(1,7))
        # Continuously call itself, creating the gameloop
        turtle.update()
        turtle.ontimer(self.gameloop, self.game_levels[self.game_level][1])

    # Check if the move is valid
    def valid(self, block, dx, dy):
        for square in block.squares:
            x = square.xcor() + dx
            y = square.ycor() + dy
            if x < 0 or x > 9:
                return False
            elif y < 0:
                return False
            elif self.map[y] [x] != False:
                return False
        return True
    
    # Move the active block
    def move(self, block, dx, dy):
        for square in block.squares:
            x = square.xcor() + dx
            y = square.ycor() + dy
            square.goto(x, y)
        block.center = (block.center[0] + dx,
                        block.center[1] + dy)

    # Write the game over message
    def game_over(self):
        message = turtle.Turtle()
        message.goto(-2.5,14)
        message.color("White")
        message.hideturtle()
        message.write("GAME\nOVER!!!", 
                      False, 
                      "center", 
                      ("Tetramino", 20, "bold"))

    # Eliminate full lines from the map
    def line_elimination(self):
        eliminated_rows = []

        # Iterate through the map rows
        for row in range(20):
            # Check if the row is full
            full = True
            for col in range(10):
                if self.map[row] [col] == False:
                    full = False
                    break
            # Eliminate full line
            if full:
                eliminated_rows.append(row)
                # Free the squares
                for col in range(10):
                    self.map[row][col].clear()
                    self.map[row][col].hideturtle()
                    self.map[row][col] = False
                turtle.update()

        # Condense the rows back
        for row in eliminated_rows[::-1]:
            # Shift the upper rows down by 1
            for upper_row in range(row+1, 20):
                for col in range(10):
                    if self.map[upper_row][col] != False:
                        self.map[upper_row][col].goto(col, upper_row-1)
                        self.map[upper_row-1][col] = self.map[upper_row][col]
                        self.map[upper_row][col] = False
                turtle.update()
        
        # Update the reward system
        self.score_update(len(eliminated_rows))
        turtle.update()

    def score_update(self, n):
        self.score_board.clear()
        for i in range(n):
            self.scores += self.game_levels[self.game_level][0]
        if self.scores >= 6000:
            self.game_level = 4
        elif self.scores >= 2000:
            self.game_level = 3
        elif self.scores >= 600:
            self.game_level = 2
        self.score_board.write(f"Scores: {self.scores}\n" + 
                               f"Level: {self.game_level}",
                               False, 
                               "right", 
                               ("Tetramino", 10, "bold"))

    def move_left(self):
        if self.valid(self.active, -1, 0):
            self.move(self.active, -1, 0)
        turtle.update()
    
    def move_right(self):
        if self.valid(self.active, 1, 0):
            self.move(self.active, 1, 0)
        turtle.update()

    def drop(self):
        while self.valid(self.active, 0, -1):
            self.move(self.active, 0, -1)
        turtle.update()
    
    def rotate(self):
        relative_positions = []
        new_positions = []
        rotation_matrix = ((0, 1), (-1, 0))
        for square in self.active.squares:
            x = square.xcor() - self.active.center[0]
            y = square.ycor() - self.active.center[1]
            relative_positions.append((x, y))
        for position in relative_positions:
            x = rotation_matrix[0][0] * position[0] + rotation_matrix[0][1] * position[1]
            y = rotation_matrix[1][0] * position[0] + rotation_matrix[1][1] * position[1]
            x = int(x + self.active.center[0])
            y = int(y + self.active.center[1])
            new_positions.append((x, y))
        
        if self.rotate_valid(new_positions):
            for square in range(4):
                self.active.squares[square].goto(new_positions[square][0], new_positions[square][1])
        turtle.update()

    def rotate_valid(self, coordinates):
        for square in range(4):
            x = coordinates[square] [0]
            y = coordinates[square] [1]
            if x < 0 or x > 9:
                return False
            elif y < 0:
                return False
            elif self.map[y] [x] != False:
                return False
        return True