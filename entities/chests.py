import random
from entities.player import ITEMS

class Chest:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.opened=False
        
    def open(self,player):
        self.opened=True
        kinds=list(ITEMS)
        weights=[ITEMS[k]["weight"] for k in kinds]
        f=random.choices(kinds,weights,k=random.randint(1,2))
        for i in f:
            player.inv[i]=player.inv.get(i,0)+1
        return [ITEMS[k]["name"] for k in f]