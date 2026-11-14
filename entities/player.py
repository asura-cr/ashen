class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def move(self, dx, dy, game_map, enemies):
        nx = self.x + dx
        ny = self.y + dy

        if not game_map.is_walkable(nx, ny):
            return
        
        if any(e.x==nx and e.y==ny for e in enemies):
            return
            
        self.x = nx
        self.y = ny