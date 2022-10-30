# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import typing

from models.snake import Snake
from models.point import Point 
from models.pointset import PointSet


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Moro-Code",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    # extract board and snake objects from request body
    board_object = game_state["board"]
    snake_object = game_state["you"]


    # extract food coordinates from board object 
    # and construct point object for each one
    food_points: typing.List[Point] = []
    for point in board_object["food"]:
        food_points.append(
            Point(point["x"], point["y"])
        )
    
    
    # construct dict of other snakes on the board and initial hazard pointset with snake bodies
    other_snakes: typing.Dict[str, Snake] = {}
    our_snake = Snake(
        snake_object["id"], 
        snake_object["name"],
        snake_object["health"],
        snake_object["body"],
        snake_object["head"],
        food_points
    )
    hazard_points_set = PointSet(*[])
    for snake in board_object["snakes"]:
        if(snake["id"] != our_snake.id):
            snake_obj = Snake(
                snake["id"],
                snake["name"],
                snake["health"],
                snake["body"],
                snake["head"],
                food_points
            )
            other_snakes["id"] = snake_obj
            hazard_points_set.merge(snake_obj.body)
            
    # add hazard points to pointset
    for hazard in board_object["hazards"]:
        hazard_points_set.add_points(Point(
            hazard["x"],
            hazard["y"]
        ))
    
    # get the possible moves for our snake which would not result in dying
    possible_moves_for_our_snake = our_snake.get_possible_moves(hazard_points_set)

    if len(our_snake.ordered_foods) == 0:
        return {
            "move": possible_moves_for_our_snake[0].move_verb
        }

    # determine which point our snake should target
    food_to_target = our_snake.ordered_foods[0]
    current_index = 0
    should_change_point = True

    # loop over the ordered list of food based on distance from our snakes head
    while should_change_point and current_index < len(our_snake.ordered_foods):
        should_change_point = False

        # look at if our closest food point is the closest food point of other snakes 
        # if our distance to that food point is further than the other snake we target 
        # the next closest food point and we do the same check
        # otherwise we target the closest food point
        for snake in other_snakes:
            if food_to_target["food"] == snake.ordered_foods[0]["food"] and food_to_target["distance_from_head"] >= snake.ordered_foods[0]["distance_from_head"]:
                  should_change_point = True
        
        if should_change_point and current_index != len(our_snake.ordered_foods) - 1:
            current_index+=1
            food_to_target = our_snake.ordered_foods[current_index]
            
    move_determined = our_snake.determine_move(food_to_target["food"], possible_moves_for_our_snake)
    
    print("\nTURN")
    print(our_snake.ordered_foods)
    print("---------------------")
    print("our snakes head: {}".format(our_snake.head))
    print("our snakes tail: {}".format(our_snake.tail))
    print("our snakes body: {}".format(our_snake.body))
    print("---------------------")
    print("food targeted {}".format(food_to_target["food"]))
    print("---------------------")
    print("possible moves: {}".format(possible_moves_for_our_snake))
    print("---------------------")
    print("move determined: {}".format(move_determined.move_verb))
    print("move target point: {}".format(move_determined.target_point))
    print("END TURN\n")
    return {
        "move": move_determined.move_verb
    }
            

# Start server when `python main.py` is run
if __name__ == "__main__":

    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
        "move": move, 
        "end": end
    })
