import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "({},{})".format(self.x, self.y)
        
    def distance(self, other):
        # distance formula d = _/(x2 - x1)**2 + (y2 - y1)**2
        return math.sqrt(abs(other.x - self.x)**2 + abs(other.y - self.y)**2)

    def translate_point(self, delta_x, delta_y):
        return Point(self.x + delta_x, self.y + delta_y)
    
    def is_outofbounds(self, grid_x, grid_y):
        return self.x > grid_x or self.y > grid_y or self.x < 0 or self.y < 0


        