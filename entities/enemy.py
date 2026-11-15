MOB_TYPES={
    "goblin":{"name":"Goblin","hp":10,"damage":1,"icon":"●","weight":10,"sight":6},
    "orc":{"name": "Orc","hp":25 ,"damage":5,"icon":"ø","weight":2,"sight":4},
    "zombie":{"name": "Zombie","hp": 15,"damage":4,"icon":"Z","weight":7,"sight":5},
    "ogres":{"name": "Ogre","hp": 30,"damage":8,"icon":"Θ","weight":1,"sight":3}
}

class Enemy:
    def __init__(self,x,y,mob):
        self.x=x
        self.y=y
        
        data=MOB_TYPES[mob]
        self.name=data["name"]
        self.max_hp=data["hp"]
        self.hp=data["hp"]
        self.damage=data["damage"]
        self.icon= data["icon"]
        self.sight = data["sight"]
        
    
    def can_see_pl(self,player,radius=None):
        if radius is None:
            radius=self.sight
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
        
    def attack(self,player):
        distance=abs(self.x-player.x) + abs(self.y-player.y)
        
        if distance==1:
            damage=self.damage
            player.hp -= damage
            return damage
        
        return 0