from entities.items import ITEMS


ATTACKS = {
    "slash":       {"name": "Slash",       "key": "z", "dmg": 3,  "stam": 5,  "range": 1},
    "powerslash":  {"name": "Power Slash", "key": "x", "dmg": 10, "stam": 25, "range": 1},
    "lunge":       {"name": "Lunge",       "key": "c", "dmg": 5,  "stam": 10, "range": 2},
    "spear_throw": {"name": "Spear Throw", "key": "v", "dmg": 7,  "stam": 15, "range": 3},
    "bow":         {"name": "Bow",         "key": "b", "dmg": 1,  "stam": 3,  "range": 5},
}

class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
        self.hp=10
        self.max_hp=10
        
        self.stam=100
        self.max_stam=100
        
        self.inv={
            "small_hp":1,
            "small_stam":1,
            "full_stam":0
            }
        
        
    
    def move(self, dx, dy, game_map, enemies):
        nx = self.x + dx
        ny = self.y + dy

        if not game_map.is_walkable(nx, ny):
            return
        
        if any(e.x==nx and e.y==ny for e in enemies):
            return
            
        self.x = nx
        self.y = ny
        
    def attack(self,enemies,atkmove):
        data=ATTACKS[atkmove]
        
        if self.stam <= data["stam"]:
            return None,"no_stam"
        
        in_range=[e for e in enemies if abs(self.x -e.x) + abs(self.y-e.y) <= data["range"]]
        if not in_range:
            return None,"no_mob_nearby"
        
        target=min(in_range,key=lambda e: abs(self.x - e.x) + abs(self.y - e.y))
        target.hp -= data["dmg"]
        self.stam -= data["stam"]
        return target,"hit"
    
    def use_item(self,item):
        d=ITEMS[item]
        
        if self.inventory[item]<=0:
            return "none_left"
        
        if d["effect"]=="hp":
            if self.hp>=self.max_hp:
                return "full"
            self.hp = min(self.max_hp,self.hp+d["amount"])
        elif d["effect"]=="stam":
            if self.stam>=self.max_stam:
                return "full"
            self.stam=min(self.max_stam,self.stam+d["amount"])
        