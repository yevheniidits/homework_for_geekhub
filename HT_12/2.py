"""
Видозмініть програму так, щоб метод __init__ мався в класі «геометричні фігури»
та приймав кольор фігури при створенні екземпляру, а методи __init__ підкласів
доповнювали його та додавали початкові розміри.
"""


class Figure(object):
    """ Main class for all geometric figures """

    def __init__(self, colour):
        """ set default colour of figure when initialize class """
        self.colour = colour

    def change_colour(self, new_colour):
        """ change default colour (new_colour: str)"""
        self.colour = new_colour
        print(f'New colour is {self.colour}')


class Oval(Figure):
    """ Subclass for oval figure. Inherits from class Figure """

    def __init__(self, colour, height, width):
        """ set colour (str) and sizes (height:float, width: float) """
        Figure.__init__(self, colour)
        self.height = height
        self.width = width

    def info(self):
        """ print colour and size """
        print(f'Colour is {self.colour}, size is {self.height} {self.width}')


class Square(Figure):
    """ Subclass for square figure. Inherits from class Figure """

    def __init__(self, colour, side_size):
        """ set colour (str) and side sizes (float) """
        Figure.__init__(self, colour)
        self.side_size = side_size

    def info(self):
        """ print colour and size """
        print(f'Colour is {self.colour}, size is {self.side_size}')


# test
square_fig = Square('white', 5)
square_fig.info()
square_fig.change_colour('black')
square_fig.info()
oval_fig = Oval('orange', 4, 7)
oval_fig.info()
