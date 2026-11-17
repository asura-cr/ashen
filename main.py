import msvcrt
import time

from world.map import Gamemap
from entities.player import Player,ATTACKS
from systems.spawning import spawn_enemies
from systems.interface import create_layout
from systems.interface import update_layout
from systems.combat import Combatlog
from systems.interface import show_game_over
from entities.items import ITEMS

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
            
            turn_done=False
        
            if key == "w":
                pl.move(0, -1, gm,en )
                turn_done=True
            elif key == "s":
                pl.move(0, 1, gm,en)
                turn_done=True
            elif key == "a":
                pl.move(-1, 0, gm,en)
                turn_done=True
            elif key == "d":
                pl.move(1, 0, gm,en)
                turn_done=True
            elif key == "q":
                return False
            for kind,atk in ATTACKS.items():
                if key==atk["key"]:
                    t,r=pl.attack(en,kind)
                    if r=="no_stam":
                        combat_log.add(f"You dont have enough stamina to use {atk["name"]} , {pl.stam} / {atk["stam"]} ","yellow")
                    elif r=="no_mob_nearby":
                        combat_log.add("There is no monster nearby","yellow")
                    elif r=="hit":
                        turn_done= True
                        combat_log.add(f"You use {atk["name"]} on {t.name} , remaining health : ({t.hp}/ {t.max_hp})","green")
                        if t.hp<=0:
                            combat_log.add(f"You killed {t.name}","bold yellow")
                            kills +=1
                        en = [e for e in en if e.hp>0]
                        
            for name,qty in pl.inv.items():
                if key==ITEMS[name]["key"]:
                    r = pl.use_item(name)
                    if r=="none_left":
                        combat_log.add(f"You dont have any {ITEMS[name]['name']}","yellow")
                    elif r =="full_hp":
                        combat_log.add(f"You have full hp","green")
                    elif r=="full_stam":
                        combat_log.add(f"Your stamina is already full","green")
                    else:
                        combat_log.add(r,"bold green")
                        
            if turn_done:
                for enemy in en:
                    dmg = 0
                    if abs(enemy.x - pl.x) + abs(enemy.y - pl.y) == 1:
                        dmg=enemy.attack(pl)
                    if enemy.can_see_pl(pl):
                        enemy.move_towards_pl(pl,gm,en)

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
                        try:
                            choice=msvcrt.getch().decode("utf-8").lower()
                        except UnicodeDecodeError:
                            continue
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