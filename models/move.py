
class Move:

    def __init__(self, initial_point, move_verb):
        self.initial_point = initial_point
        self.move_verb = move_verb
        
        if move_verb == "up":
            self.target_point = self.initial_point.translate_point(0, 1)
        elif move_verb == "down":
            self.target_point = self.initial_point.translate_point(0, -1)
        elif move_verb == "left":
            self.target_point = self.initial_point.translate_point(-1, 0)
        elif move_verb == "right":
            self.target_point = self.initial_point.translate_point(1, 0)

    def __str__(self):
        return self.move_verb

    def __repr__(self):
        return self.move_verb
            
        
            