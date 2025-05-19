import turtle
from .constants import SCALE

class Square(turtle.Turtle):
    '''
    Purpose:
        This class represents a square, a part of a tetromino. 
        A square has all the attributes and methods inherited from a turtle.
    Instance variables:
        None
    Methods: 
        None
    '''

    def __init__(self, x, y, color):
        # Initiate the turtle for this square
        turtle.Turtle.__init__(self)
        # Configure the square as desired
        self.shape('square')
        self.shapesize(SCALE / 20.25)
        self.speed(0)
        self.fillcolor(color)
        self.penup()
        self.goto(x,y)