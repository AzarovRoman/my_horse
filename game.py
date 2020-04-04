import random

from itertools import product, permutations, chain
from string import ascii_uppercase, digits
from collections import namedtuple


coordinates = namedtuple('coord', ('x', 'y'))


class Cell:
    def __init__(self):
        self.check_horse = False
        self.check_use = False

    def fill(self):
        if self.check_horse:
            return '?'
        elif self.check_use:
            return 'X'
        else:
            return ' '


class Field:
    def __init__(self):
        self.field = []

    def filling(self):
        for i in range(8):
            line = []
            for j in range(8):
                cell = Cell()
                line.append(cell)
            self.field.append(line)
        return self.field

    def visual(self, horse):
        result_field = []
        for i in horse.field:
            line = []
            for j in i:
                line.append(j.fill())
            result_field.append(line)
            alph_counter = 0

        for k in result_field:
            alph = ascii_uppercase[alph_counter]
            print(' ----------------------------------------------------------------')
            print(
                alph + '|       |       |       |       |       |       |       |       |')
            for i in k:
                print(' |   ' + i + '  ', end='')
            print('')
            print(' |       |       |       |       |       |       |       |       |')
            alph_counter += 1

        numb = []
        for i in range(1, 9):
            numb.append('     ' + str(i) + '  ')

        for i in numb:
            print(i, end ='')
        print('')


class Horse:

    def __init__(self, field):
        self.field = field
        self.current_coordinates = None

    def convert_coordinates(self, coordinate):
        try:
            x_coord, y_coord = coordinate
            x_coord = ascii_uppercase[:8].index(x_coord.upper())
            y_coord = digits[1:9].index(y_coord)
            return x_coord, y_coord

        except ValueError:
            return None

    def move(self, coordinates_movment):
        x_coord, y_coord = coordinates_movment

        if self.current_coordinates is not None:
            x_current, y_current = self.current_coordinates
            self.field[x_current][y_current].check_use = True
            self.field[x_current][y_current].check_horse = False

        self.field[x_coord][y_coord].check_horse = True
        self.current_coordinates = coordinates(x_coord, y_coord)

        return False

    def progress_check(self, coordinates_movements):
        if not self.current_coordinates and coordinates_movements:
            return True

        try:
            x_current, y_current = self.current_coordinates
            x_coord, y_coord = coordinates_movements
            x_res, y_res = abs(x_current - x_coord), abs(y_current - y_coord)

            if not self.field[x_coord][y_coord].check_use:
                return (x_res, y_res) in ((1, 2), (2, 1))

        except TypeError:
            return False

        return False

    def search_movements(self):
        a = [1, -1]
        b = [2, -2]
        movements_list = []

        x_current, y_current = self.current_coordinates
        coords = list(chain(*[permutations(i) for i in product(a, b)]))

        for x, y in coords:
            x += x_current
            y += y_current
            new_coord = coordinates(x, y)
            if 8 > x >= 0 and 8 > y >= 0:
                if not self.field[x][y].check_use:
                    movements_list.append(new_coord)

        return movements_list


def game():
    field = Field()
    horse = Horse(field.filling())
    check_finish = False
    check_gamer = True
    check_horse = False

    while not check_horse:
        movement_coordinates = horse.convert_coordinates(input('выберите куда ставим коня: '))
        if horse.progress_check(movement_coordinates):
            horse.move(movement_coordinates)
            check_horse = True
        else:
            print('-введена неверная координата-')

    while not check_finish:
        field.visual(horse)

        if check_gamer:
            movement_coord = horse.convert_coordinates(input('введите координаты формата А1: '))

            if horse.progress_check(movement_coord):
                horse.move(movement_coord)
                check_gamer = False

            if not horse.search_movements():
                check_finish = True
                break

        else:
            #print(horse.search_movements())
            horse.move(random.choice(horse.search_movements()))
            check_gamer = True

        print('\n')

        if horse.search_movements() == ():
            check_finish = True
            break


game()
