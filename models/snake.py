import typing
from .pointset import PointSet
from .point import Point
from .move import Move


class Snake:

    def __init__(self, id:str, name:str , health: int, body: typing.List[typing.Dict[str, int]], head: typing.Dict[str, int], foods: typing.List[Point]):
        # assign object variables 
        self.id = id 
        self.name = name
        self.health = health
        self.head = Point(head["x"], head["y"])
        self.tail = Point(body[-1]["x"], body[-1]["y"])

        # construct pointset of body
        body_point_list: typing.List[Point] = []
        for body_point in body:
            body_point_list.append(
                Point(body_point["x"], body_point["y"])
            )
        self.body = PointSet(*body_point_list)

        # from the list of food passed in to the snake order by distance of head to food
        food_with_distances = []
        for food in foods[1:]:
            distance_of_head_to_food = self.head.distance(food)
            food_with_distances.append({
                "food": food,
                "distance_from_head": distance_of_head_to_food
            })
        food_with_distances.sort(key = lambda food: food["distance_from_head"])

        self.ordered_foods = food_with_distances
        
    # returns immediate possible moves that can be done without dying
    def get_possible_moves(self, hazard_point_set):
        possible_moves = [ 
            Move(self.head, "up"),
            Move(self.head, "down"),
            Move(self.head, "left"),
            Move(self.head, "right")
        ]
        filtered_moves = []
        for move in possible_moves:
            if self._is_valid_move(move, hazard_point_set):
                filtered_moves.append(move)

        return filtered_moves
                
    def _is_valid_move(self, move, hazard_point_set):
        if hazard_point_set.contains(move.target_point):
            return False
        if move.target_point.is_outofbounds(10, 10):
            return False
        if self.body.contains(move.target_point):
            return False


        # cover edge case of when head is surrounded by body on three sides 
        if move.move_verb == "up" and self.body.contains(self.head.translate_point(0, -1)) and self.body.contains(self.head.translate_point(1, 0)) and self.body.contains(self.head.translate_point(-1, 0)):
            return True
        elif move.move_verb == "down" and self.body.contains(self.head.translate_point(0, 1)) and self.body.contains(self.head.translate_point(1, 0)) and self.body.contains(self.head.translate_point(-1, 0)):
            return True
        elif move.move_verb == "right" and self.body.contains(self.head.translate_point(0, -1)) and self.body.contains(self.head.translate_point(0, 1)) and self.body.contains(self.head.translate_point(-1, 0)):
            return True
        elif move.move_verb == "left" and self.body.contains(self.head.translate_point(0, -1)) and self.body.contains(self.head.translate_point(0, 1)) and self.body.contains(self.head.translate_point(1, 0)):
            return True

        # cover edge case of when head is in a corner
        if move.move_verb == "up" and self.head.translate_point(0, -1).is_outofbounds(10, 10) and (self.head.translate_point(1, 0).is_outofbounds(10, 10) or self.head.translate_point(-1, 0).is_outofbounds(10, 10)):
            return True
        elif move.move_verb == "down" and self.head.translate_point(0, 1).is_outofbounds(10, 10) and (self.head.translate_point(1, 0).is_outofbounds(10, 10) or self.head.translate_point(-1, 0).is_outofbounds(10, 10)):
            return True
        elif move.move_verb == "right" and self.head.translate_point(-1, 0).is_outofbounds(10, 10) and (self.head.translate_point(0, 1).is_outofbounds(10, 10) or self.head.translate_point(0, -1).is_outofbounds(10, 10)):
            return True
        elif move.move_verb == "left" and self.head.translate_point(1, 0).is_outofbounds(10, 10) and (self.head.translate_point(0, 1).is_outofbounds(10, 10) or self.head.translate_point(0, -1).is_outofbounds(10, 10)):
            return True
            
        # check if move will lead us to a dead end
        # TODO: change this to check if the move will result in the snake forming a circle as a result of the move
        x_intercepts_for_move = self.body.get_x_intercepts_for_point(move.target_point)

        y_intercepts_for_move = self.body.get_y_intercepts_for_point(move.target_point)


        if len(x_intercepts_for_move) % 2 != 0 and len(y_intercepts_for_move) != 0:
            return False
        
        return True
            
    # returns the next move this snake will make
    def determine_move(self, target_food_point: Point, list_of_possible_moves):
        closest_move = list_of_possible_moves[0]
        for move in list_of_possible_moves:
            if move.target_point.distance(target_food_point) < closest_move.target_point.distance(target_food_point):
                closest_move = move

        return closest_move

    
