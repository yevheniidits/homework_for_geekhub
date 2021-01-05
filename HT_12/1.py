"""
Напишіть програму, де клас «геометричні фігури» (figure) містить властивість
color з початковим значенням white і метод для зміни кольору фігури, а його
підкласи «овал» (oval) і «квадрат» (square) містять методи __init__ для
завдання початкових розмірів об'єктів при їх створенні.
"""


class Figure(object):
    """ Main class for all geometric figures """

    # default colour for all figures
    colour = 'white'

    def change_colour(self, new_colour):
        """ change default colour (new_colour: str) """
        self.colour = new_colour
        print(f'New colour of figure is {new_colour}')


class Oval(Figure):
    """ Subclass for oval figure. Inherits from class Figure """

    def __init__(self, height, width):
        """ set sizes of figure (height: float, width: float) """
        self.height = height
        self.width = width


class Square(Figure):
    """ Subclass for square figure. Inherits from class Figure """

    def __init__(self, side_size):
        """ set side sizes of figure (side_size: float) """
        self.side_size = side_size


# test
square_fig = Square(5)
print(square_fig.colour)
square_fig.change_colour('black')
print(square_fig.colour)
