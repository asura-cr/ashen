class Enemy:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.hp=10
        self.max_hp=10
        self.name = "Goblin"
    
    def can_see_pl(self,player,radius=6):
        x = self.x - player.x
        y = self.y - player.y
        z= x**2 + y**2
        return z<=radius**2
    
    def move_towards_pl(self,player,game_map,enemies):
        path = game_map.find_path(
            (self.x,self.y),
            (player.x,player.y),walkable_only=True
        )
        
        if not path or len(path) <2:
            return
        
        nx,ny=path[1]
        
        if (nx,ny)==(player.x,player.y):
            return

        if any(e.x==nx and e.y==ny for e in enemies if e is not self):
            return
        
        self.x=nx
        self.y=ny