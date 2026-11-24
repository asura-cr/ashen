import random
from entities.enemy import Enemy,MOB_TYPES
from entities.chests import Chest

def spawn_enemies(game_map,player,amount):
    enemies=[]
    attempts=0
    kinds=list(MOB_TYPES)
    weights =[MOB_TYPES[k]["weight"] for k in kinds]
    while len(enemies)<amount and attempts < amount*10:
        attempts+=1
        k=random.choices(kinds,weights)[0]
        
        room=random.choice(game_map.rooms)
        x= random.randint(room.x+1,room.x + room.width-2)
        y= random.randint(room.y+1,room.y+ room.height -2)
        
        if (x,y) == (player.x,player.y):
            continue
        if not game_map.is_walkable(x,y):
            continue
        if (x,y) == game_map.exit:
            continue
        if any(e.x==x and e.y==y for e in enemies):
            continue
        enemies.append(Enemy(x,y,k))
        
    return enemies

def spawn_chests(gm,occupied):
    count=random.randint(1,4)
    rooms=random.sample(gm.rooms[1:],min(count,len(gm.rooms)-1))
    chests=[]
    for r in rooms:
        cx,cy=r.center()
        spots=[(cx+dx,cy+dy)for dx in range(-2,3) for dy in range(-2,3)]
        random.shuffle(spots)
        for x,y in spots:
            if gm.is_walkable(x,y) and (x,y) not in occupied and (x,y) != gm.exit:
                chests.append(Chest(x,y))
                break
    return chests