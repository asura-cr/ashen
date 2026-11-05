class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def move(self, dx, dy, game_map):
        nx = self.x + dx
        ny = self.y + dy

        if game_map.is_walkable(nx, ny):
            self.x = nx
            self.y = ny