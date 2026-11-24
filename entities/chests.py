import random
from entities.items import ITEMS

CHESTS={
    "common":{
        "weight":70,
        "color":"white",
        "min_loot":1,
        "max_loot":2
    },
    "rare": {
        "weight" : 25,
        "color":"bold blue",
        "min_loot":2,
        "max_loot":3
    },
    "legendary": {
        "weight":5,
        "color": "bold magenta",
        "min_loot":3,
        "max_loot":5
    }
}

class Chest:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.opened=False
        
        ra=list(CHESTS)
        weight=[CHESTS[r]["weight"]for r in ra]
        self.rarity= random.choices(
            ra,weights=weight,k=1
        )[0]
        
    def open(self,player):
        if self.opened==True:
            return []
        ra=CHESTS[self.rarity]
        kinds=list(ITEMS)
        weights=[ITEMS[k]["weight"] for k in kinds]
        count=random.randint(ra["min_loot"],ra["max_loot"])
        loot=random.choices(kinds,weights=weights,k=count)
        
        for item in loot:
            player.inv[item]=player.inv.get(item,0)+1
            return [ITEMS[k]["name"] for k in loot]