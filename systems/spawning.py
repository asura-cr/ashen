import random
from entities.enemy import Enemy,MOB_TYPES

def spawn_enemies(game_map,player,amount):
    enemies=[]
    attempts=0
    kinds=list(MOB_TYPES)
    weights =[MOB_TYPES[k]["weight"] for k in kinds]
    k=random.choices(kinds,weights)[0]
    while len(enemies)<amount and attempts < amount*10:
        attempts+=1
        
        room=random.choice(game_map.rooms)
        x= random.randint(room.x+1,room.x + room.width-2)
        y= random.randint(room.y+1,room.y+ room.height -2)
        
        if (x,y) == (player.x,player.y):
            continue
        if not game_map.is_walkable(x,y):
            continue
        if any(e.x==x and e.y==y for e in enemies):
            continue
        enemies.append(Enemy(x,y,k))
        
    return enemies