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
        x=0
        y=0
        
        if player.x>self.x:
            x = 1
        elif player.x<self.x:
            x = -1
            
        if player.y>self.y:
            y=1
        elif player.y < self.y:
            y=-1
            
        nx = self.x + x
        ny = self.y + y
        
        if (nx,ny)==(player.x ,player.y):
            return
        if any(e.x==nx and e.y==ny for e in enemies if e is not self):
            return
        if game_map.is_walkable(nx,ny):
            self.x=nx
            self.y=ny