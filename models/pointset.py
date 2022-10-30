import typing
from .point import Point


class PointSet:
    def __init__(self, *args: typing.List[Point]):
        self.points_list = args
    
    def get_list(self):
        return self.points_list

    def add_points(self, *points: typing.List[Point]):
        self.points_list = self.points_list + points

    def merge(self, other):
        self.points_list = self.points_list + other.points_list
    
    def __repr__(self):
        return "[{}]".format(self.points_list)

    def get_x_intercepts_for_point(self, point):
        x_intercepts = []
        last_point = None
        for point_in_list in self.points_list:
            if point_in_list.y == point.y and point_in_list.x < point.x:
                if last_point is None:
                    last_point = point_in_list
                elif point_in_list.x - last_point.x == 1:
                    x_intercepts.pop()
                    last_point = point_in_list
                
                x_intercepts.append(point_in_list)
            
                    
        return x_intercepts

    def get_y_intercepts_for_point(self, point):
        y_intercepts = []
        last_point = None
        for point_in_list in self.points_list:
            if point_in_list.x == point.x and point_in_list.y < point.y:
                if last_point is None:
                    last_point = point_in_list
                elif last_point.y - point_in_list.y == 1:
                    y_intercepts.pop()
                    last_point = point_in_list
                
                y_intercepts.append(point_in_list)
            
                    
        return y_intercepts

    def determine_max_and_min_x_for_y(self, y):
        max_point = None
        min_point = None
        for point_in_list in self.points_list:
            if point_in_list.y == y:
                if max_point is None or max_point.x < point_in_list.x:
                    max_point = point_in_list
                    
                if min_point is None or min_point.x > point_in_list.x:
                    min_point = point_in_list
                    
        return max_point, min_point

    def determine_max_and_min_y_for_x(self, x):
        max_point = None
        min_point = None
        for point_in_list in self.points_list:
            if point_in_list.x == x:
                if max_point is None or max_point.y < point_in_list.y:
                    max_point = point_in_list

                if min_point is None or min_point.y > point_in_list.y:
                    min_point = point_in_list
                    
        return max_point, min_point

            

    def contains(self, point):
        for point_in_list in self.points_list:
            if point == point_in_list:
                return True 
        return False
    