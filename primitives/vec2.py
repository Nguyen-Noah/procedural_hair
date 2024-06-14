import math

class vec2:
    def __init__(self, *args):
        """
        Initionalize the vector2
        :position: two-length tuple (x, y)
        :angle: angle, in degrees counterclockwise from right
        """
        if len(args) == 1 and isinstance(args[0], vec2):
            self._x, self._y = args[0].position
        elif len(args) == 2:
            self.x, self.y = args
        else:
            raise ValueError('Invalid number of arguments. Expected either a tuple or two integers.')

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return vec2(self.x / mag, self.y / mag)
        return vec2(0, 0)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def copy(self):
        return vec2(self.x, self.y)
    
    @property
    def tuple(self):
        return (self.x, self.y)

    @property
    def position(self):
        return (self.x, self.y)

    @position.setter
    def position(self, new_position):
        self.x = new_position[0]
        self.y = new_position[1]

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value

    
    def __add__(self, other):
        copy = self.copy()
        copy.x += other.x
        copy.y += other.y
        return copy
    
    def __sub__(self, other):
        copy = self.copy()
        copy.x -= other.x
        copy.y -= other.y
        return copy
    
    def __mul__(self, other):
        copy = self.copy()
        copy.x *= other.x
        copy.y *= other.y
        return copy
    
    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return self.__str__()

temp = vec2(0, 0)
temp_to_add = vec2(10, 20)

temp += temp_to_add