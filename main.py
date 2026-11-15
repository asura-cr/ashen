import msvcrt
import time

from world.map import Gamemap
from entities.player import Player
from systems.spawning import spawn_enemies
from systems.interface import create_layout
from systems.interface import update_layout
from systems.combat import Combatlog
from systems.interface import show_game_over

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich import print
from rich.align import Align

def run_game():
    start_time=time.time()
    gm=Gamemap(100,40)
    gm.generate_rooms(20,5,15)
    gm.connect_all_rooms()
    if not gm.validate():
        print("Map Validation failed")
        return False
    x,y= gm.rooms[0].center()
    
    pl=Player(x,y)
    en=spawn_enemies(gm,pl,5)
    
    combat_log=Combatlog()
    console=Console()
    
    kills=0
        
    layout= create_layout(pl,gm,en,combat_log) 
    with Live(
        layout,
        console=console,
        screen=True,
        refresh_per_second=10
    ) as live:
            
        while True:
            
            update_layout(layout,pl,gm,en,combat_log)
            try: 
                key = msvcrt.getch().decode("utf-8").lower()
            except UnicodeDecodeError:
                continue
        
            if key == "w":
                pl.move(0, -1, gm,en )
            elif key == "s":
                pl.move(0, 1, gm,en)
            elif key == "a":
                pl.move(-1, 0, gm,en)
            elif key == "d":
                pl.move(1, 0, gm,en)
            elif key == "q":
                return False
            elif key == " ":
                t=pl.attack(en)
                en = [enemy for enemy in en if enemy.hp>0]
                if t:
                    combat_log.add(f"You hit {t.name} for 3 dmg, {t.hp}/{t.max_hp} left ","green")
                    live.refresh()
                    if t.hp <=0:
                        combat_log.add(f"You killed {t.name}","bold yellow")
                        kills +=1
            if key in ("w","a","s","d"," "):
                for enemy in en:
                    if enemy.can_see_pl(pl):
                        enemy.move_towards_pl(pl,gm,en)
                        
                    dmg=enemy.attack(pl)
                    
                    if dmg:
                        combat_log.add(f"{enemy.name} hit u for {dmg} dmg , HP Left : {pl.hp}/{pl.max_hp}","red")
                        live.refresh()
                    
                    if pl.hp <= 0:
                        combat_log.add(f"{enemy.name} killed u","bold red")
                        update_layout(layout,pl,gm,en,combat_log)
                        live.refresh()
                        break
                en = [enemy for enemy in en if enemy.hp>0]
                
                if pl.hp <= 0:
                    time_survived= int(time.time()-start_time)
                    show_game_over(layout,kills,time_survived)
                    live.refresh()
                
                    while True:
                        choice=msvcrt.getch().decode("utf-8").lower()
                    
                        if choice== "q":
                            return False
                        if choice== "r":
                            return True
    if pl.hp <= 0:
        pa=Align.center(
            Panel.fit(
                    "[red] \n YOU DIED [/red] \n [dim] your journey ends here.... [/dim]",border_style="red"))
        console.print(pa,justify="center")
        
def main():
    while True:
        restart= run_game()
        if not restart:
            break
            
            
if __name__ == "__main__":
    main()