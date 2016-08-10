
from collections import deque
from random import randint
from point import GPoint

class GStruct:
    pass

DIRECTIONS          = GStruct()
DIRECTIONS.DOWN     = GPoint(x=0, y=1)
DIRECTIONS.UP       = GPoint(x=0, y=-1)
DIRECTIONS.LEFT     = GPoint(x=-1, y=0)
DIRECTIONS.RIGHT    = GPoint(x=1, y=0)

class GSnake(object):
    """docstring for GSnake"""
    def __init__(self, bodey=deque(), max_x=8, max_y=6):
        super(GSnake, self).__init__()
        self._current_direction = DIRECTIONS.DOWN
        self._previous_direction = DIRECTIONS.DOWN
        self._bodey = bodey
        self._apple = GPoint(x=randint(0, max_x), y=randint(0, max_y))
        self._max_x = max_x
        self._max_y = max_y
        self._bite_self = False

        self._GenerateApple()


    @property
    def head(self):
        return self._bodey[0]

    @property
    def apple(self):
        return self._apple

    @property
    def is_alive(self):
        a = 0 <= self.head.x < self._max_x
        b = 0 <= self.head.y < self._max_y
        c = not self._bite_self
        print(a, b, c)
        return a and b and c    
    

    def MakeStep(self):
        head = self._bodey[0]
        new_head = head + self._current_direction
        if new_head in self._bodey:
            self._bite_self = True
        self._bodey.appendleft(new_head)
        if new_head == self.apple:
            self._GenerateApple()
        else:
            self._bodey.pop()
        self._previous_direction = self._current_direction


    def ChangeDirection(self, new_direction=DIRECTIONS.UP):
        dd = self._previous_direction + new_direction
        if dd.x == 0 and dd.y == 0:
            pass
        else:
            self._current_direction = new_direction


    def GetAsDict(self):
        res = {"bodey": []}
        for point in self._bodey:
            res["bodey"].append({"x": point.x, "y": point.y})
        return res


    def _GenerateApple(self):
        apple = GPoint(x=randint(0, self._max_x - 1), y=randint(0, self._max_y - 1))
        while apple in self._bodey:
            apple = GPoint(x=randint(0, self._max_x - 1), y=randint(0, self._max_y - 1))
        self._apple = apple
