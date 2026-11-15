class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
        self.hp=10
        self.max_hp=10
        
        self.stam=100
        self.max_stam=100
    
    def move(self, dx, dy, game_map, enemies):
        nx = self.x + dx
        ny = self.y + dy

        if not game_map.is_walkable(nx, ny):
            return
        
        if any(e.x==nx and e.y==ny for e in enemies):
            return
            
        self.x = nx
        self.y = ny
        
    def attack(self,enemies):
        for en in enemies:
            dist=abs(self.x-en.x) + abs(self.y - en.y)
            
            if dist==1:
                en.hp -= 3
                self.stam -=1
                return en
        return None