import os
import msvcrt
from world.map import Gamemap
from entities.player import Player
from entities.enemy import Enemy

def main():
    gm=Gamemap(50,20)
    gm.generate_rooms(10,5,10)
    gm.connect_all_rooms()
    if not gm.validate():
        print("Map Validation failed")
        return
    x,y= gm.rooms[0].center()
    pl=Player(x,y)

    while True:
        os.system("cls")
        gm.display(pl)
        print("Use WASD To Move \n Q to quit")
        key = msvcrt.getch().decode("utf-8").lower()
        
        if key == "w":
            pl.move(0, -1, gm )
        elif key == "s":
            pl.move(0, 1, gm)
        elif key == "a":
            pl.move(-1, 0, gm)
        elif key == "d":
            pl.move(1, 0, gm)
        elif key == "q":
            break
if __name__ == "__main__":
    main()