# -*- coding: utf-8 -*-
import sys
import codecs
from copy import copy

class Goban(object):

    class Untouchable(Exception): pass

    empty = 0
    black = 1
    white = 2
    invalid = 3
    around_moves = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def __init__(self, size):
        self.size = size
        self.data = [ [ self.empty for i in range(size) ]
            for j in range(size) ]

    def render(self, output=sys.stdout, html=False):
        for i, line in enumerate(self.data):
            for j, point in enumerate(line):
                if point == self.empty:
                    s = self._empty_str(i, j)
                    if html:
                        s = '<a href="#" onclick="touch(%s, %s)">%s</a>' % (j, i, s)
                elif point == self.black:
                    s = u'●'
                else:
                    s = u'○'
                if html and j == self.size-1:
                    s = s + '<br />'
                output.write(s)
            output.write('\n')

    @classmethod
    def get_opponent_color(cls, color):
        return cls.black if color is cls.white else cls.white

    def touch(self, x, y, color):
        if self.get_state(x, y) is not self.empty:
            raise self.Untouchable()
        prev_data = copy(self.data)
        self.data[y][x] = color
        gottens = set()
        checked = set()
        opponent = self.get_opponent_color(color)
        for move_x, move_y in self.around_moves:
            next_x = x + move_x
            next_y = y + move_y
            if self.get_state(next_x, next_y) is not opponent: continue
            if not self.check_alive(next_x, next_y, opponent, checked):
                self._get_stones(next_x, next_y, gottens)
        for gotten_x, gotten_y in gottens:
            self.data[gotten_y][gotten_x] = self.empty
        if not self.check_alive(x, y, color):
            self.data = prev_data
            raise self.Untouchable()
        return len(gottens)

    def _get_stones(self, x, y, gottens):
        color = self.get_state(x, y)
        gottens.add((x, y))
        targets = []
        target = (x, y)
        while target is not None:
            x, y = target
            for move_x, move_y in self.around_moves:
                next_x = x + move_x
                next_y = y + move_y
                if self.get_state(next_x, next_y) is not color: continue
                if (next_x, next_y) not in gottens:
                    targets.append((next_x, next_y))
                    gottens.add((next_x, next_y))
            target = targets.pop() if targets else None

    def get_state(self, x, y):
        if x < 0 or self.size <= x or y < 0 or self.size <= y:
            return self.invalid
        return self.data[y][x]

    def check_alive(self, x, y, color, checked=None):
        if checked is None: checked = set()
        if (x, y) in checked: return True
        checked.add((x, y))
        targets = []
        target = (x, y)
        while target is not None:
            x, y = target
            for move_x, move_y in self.around_moves:
                next_x = x + move_x
                next_y = y + move_y
                state = self.get_state(next_x, next_y)
                if state is self.empty:
                    return True
                elif state is color:
                    if (next_x, next_y) not in checked:
                        targets.append((next_x, next_y))
                        checked.add((next_x, next_y))
            target = targets.pop() if targets else None
        return False

    def is_kou(self, prev_goban):
        if prev_goban is None: return False
        for y in range(self.size):
            for x in range(self.size):
                if prev_goban.data[y][x] != self.data[y][x]:
                    return False
        return True

    def _empty_str(self, x, y):
        if x == 0:
            if y == 0:
                return u'┏'
            elif y == self.size - 1:
                return u'┓'
            else:
                return u'┯'
        elif x == self.size - 1:
            if y == 0:
                return u'┗'
            elif y == self.size - 1:
                return u'┛'
            else:
                return u'┷'
        else:
            if y == 0:
                return u'┠'
            elif y == self.size - 1:
                return u'┨'
            elif self.is_star(x, y):
                return u'╋'
            else:
                return u'┼'

    def is_star(self, x, y):
        if self.size == 19:
            positions = (3, 9, 15)
        elif self.size == 13:
            positions = (3, 9)
        else:
            positions = ()
        return ((x in positions and y in positions) or
            self.size % 2 and x == y == self.size / 2)

def test():
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    goban_size = 19
    goban = Goban(goban_size)
    goban.touch(3, 3, Goban.black)
    goban.touch(15, 15, Goban.white)
    gotten = goban.touch(3, 4, Goban.black)
    gotten = goban.touch(2, 3, Goban.black)
    gotten = goban.touch(2, 2, Goban.white)
    gotten = goban.touch(3, 2, Goban.white)
    gotten = goban.touch(1, 3, Goban.white)
    gotten = goban.touch(2, 4, Goban.white)
    gotten = goban.touch(4, 3, Goban.white)
    gotten = goban.touch(4, 4, Goban.white)
    goban.render()
    gotten = goban.touch(3, 5, Goban.white)
    goban.render(sys.stdout)
    print 'white got', gotten, 'stones.'

def main():
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    goban_size = 19
    goban = Goban(goban_size)
    turn = Goban.black
    while True:
        goban.render(sys.stdout)
        try:
            input = raw_input()
        except EOFError:
            break
        x, y = [ int(d) for d in input.split(',') ]
        try:
            goban.touch(x, y, turn)
        except Goban.Untouchable, e:
            print u'着手できません'
        else:
            turn = Goban.get_opponent_color(turn)

if __name__ == '__main__':
    main()
