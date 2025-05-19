from src.square import Square

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
    def __init__(self, x, y, variation):
        self.variation = variation
        self.center = (x,y)
        if variation == 0:
            self.squares = []
        else:
            self.squares = []
            # I block
            if variation == 1:
                block1 = Square(x-1, y, 'Cyan')
                block2 = Square(x, y, 'Cyan')
                block3 = Square(x+1, y, 'Cyan')
                block4 = Square(x+2, y, 'Cyan')
                self.center = (x+0.5, y-0.5) 
            # J block
            elif variation == 2:
                block1 = Square(x-1, y+1, 'Blue')
                block2 = Square(x-1, y, 'Blue')
                block3 = Square(x, y, 'Blue')
                block4 = Square(x+1, y, 'Blue')
            # L block
            elif variation == 3:
                block1 = Square(x-1, y, 'Orange')
                block2 = Square(x, y, 'Orange')
                block3 = Square(x+1, y, 'Orange')
                block4 = Square(x+1, y+1, 'Orange')
            # O block
            elif variation == 4:
                block1 = Square(x, y, 'Yellow')
                block2 = Square(x, y+1, 'Yellow')
                block3 = Square(x+1, y, 'Yellow')
                block4 = Square(x+1, y+1, 'Yellow')
                self.center = (x+0.5, y+0.5)
            # S block
            elif variation == 5:
                block1 = Square(x-1, y, 'Green')
                block2 = Square(x, y, 'Green')
                block3 = Square(x, y+1, 'Green')
                block4 = Square(x+1, y+1, 'Green')
            # T block
            elif variation == 6:
                block1 = Square(x-1, y, 'Purple')
                block2 = Square(x, y, 'Purple')
                block3 = Square(x, y+1, 'Purple')
                block4 = Square(x+1, y, 'Purple')
            # Z block
            elif variation == 7:
                block1 = Square(x-1, y+1, 'Red')
                block2 = Square(x, y+1, 'Red')
                block3 = Square(x, y, 'Red')
                block4 = Square(x+1, y, 'Red')

            self.squares.append(block1)
            self.squares.append(block2)
            self.squares.append(block3)
            self.squares.append(block4)