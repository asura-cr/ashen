import os
import msvcrt
from world.map import Gamemap
from entities.player import Player
from entities.enemy import Enemy
from systems.spawning import spawn_enemies

def main():
    gm=Gamemap(50,20)
    gm.generate_rooms(10,5,10)
    gm.connect_all_rooms()
    if not gm.validate():
        print("Map Validation failed")
        return
    x,y= gm.rooms[0].center()
    pl=Player(x,y)
    en=spawn_enemies(gm,pl,5)
    print([(e.x, e.y) for e in en])
    input("press enter to continue")

    while True:
        os.system("cls")
        gm.display(pl,en)
        print("Use WASD To Move \n Q to quit")
        key = msvcrt.getch().decode("utf-8").lower()
        
        if key == "w":
            pl.move(0, -1, gm,en )
        elif key == "s":
            pl.move(0, 1, gm,en)
        elif key == "a":
            pl.move(-1, 0, gm,en)
        elif key == "d":
            pl.move(1, 0, gm,en)
        elif key == "q":
            break
        if key in ("w","a","s","d"):
            for enemy in en:
                if enemy.can_see_pl(pl):
                    enemy.move_towards_pl(pl,gm,en)
if __name__ == "__main__":
    main()