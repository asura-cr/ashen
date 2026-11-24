import msvcrt
import time
import random

from world.map import Gamemap
from entities.player import Player,ATTACKS
from systems.spawning import spawn_enemies,spawn_chests
from systems.interface import create_layout,update_layout
from systems.combat import Combatlog
from systems.interface import show_game_over,show_game_won
from systems.leaderboard import save_run,show_lb
from entities.items import ITEMS


from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich import print
from rich.align import Align


def run_game(player_name):
    start_time=time.monotonic()
    time_survived= int(time.monotonic()-start_time)
    gm=Gamemap(100,40)
    gm.generate_rooms(20,5,15)
    gm.connect_all_rooms()
    if not gm.validate():
        print("Map Validation failed")
        return False
    
    ex=random.choice(gm.rooms[1:])
    gm.exit = ex.center()
    gm.set_tile(*gm.exit,"⇥")
    x,y= gm.rooms[0].center()
    
    
    pl=Player(x,y)
    en=spawn_enemies(gm,pl,5)
    occupied={(e.x,e.y)for e in en} | {(pl.x,pl.y)}
    gm.chests=spawn_chests(gm,occupied)
    
    combat_log=Combatlog()
    console=Console()
    
    kills=0
        
    layout= create_layout(pl,gm,en,combat_log,time_survived) 
    with Live(
        layout,
        console=console,
        screen=True,
        refresh_per_second=10
    ) as live:
            
        while True:
            time_survived= int(time.monotonic()-start_time)
            
            update_layout(layout,pl,gm,en,combat_log,time_survived)
            if msvcrt.kbhit():
                try: 
                    key = msvcrt.getch().decode("utf-8").lower()
                except UnicodeDecodeError:
                    continue
            else:
                time.sleep(0.1)
                continue
            
            turn_done=False
            
            moves={"w":(0,-1),"s":(0,1),"a":(-1,0),"d":(1,0)}
        
            if key in moves:
                dx,dy=moves[key]
                chest=next((c for c in gm.chests if (c.x,c.y)==(pl.x+dx,pl.y+dy)and not c.opened),None)
                if chest:
                    itms=chest.open(pl)
                    combat_log.add(f"You open a chest and find : {', '.join(itms)}","cyan")
                    turn_done=True
                else:
                    turn_done=pl.move(dx,dy,gm,en)

                    if turn_done and (pl.x,pl.y)==gm.exit:
                        combat_log.add("YOU FOUND THE DUNGEON EXIT!","bold yellow")
                        
                        save_run(player_name,kills,time_survived)
                        show_game_won(layout,kills,time_survived)
                        live.refresh()
                        
                        while True:
                            try:
                                choice=msvcrt.getch().decode("utf-8").lower()
                            except UnicodeDecodeError:
                                continue
                            
                            if choice=="q":
                                return False
                            elif choice=="r":
                                return True
                            elif choice=="l":
                                show_lb(layout)
                                live.refresh()
                                
                                
                        
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
                        turn_done=True
                        
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
                        update_layout(layout,pl,gm,en,combat_log,time_survived)
                        live.refresh()
                        break
                en = [enemy for enemy in en if enemy.hp>0]
                
                if pl.hp <= 0:
                    show_game_over(layout,kills,time_survived)
                    live.refresh()
                
                    while True:
                        try:
                            choice=msvcrt.getch().decode("utf-8").lower()
                        except UnicodeDecodeError:
                            continue
                        if choice=="l":
                            show_lb(layout)
                            live.refresh()
                        if choice== "q":
                            return False
                        if choice== "r":
                            return True
    if pl.hp <= 0:
        pa=Align.center(
            Panel.fit(
                    "[red] \n YOU DIED [/red] \n [dim] your journey ends here.... [/dim]",border_style="red"))
        console.print(pa,justify="center")
        
def main(player_name):
    while True:
        restart= run_game(player_name)
        if not restart:
            break
            
            
if __name__ == "__main__":
    player_name=input("Enter your username: ")
    while not player_name:
        print("Player name cannot be empty")
        player_name=input("Enter your username: ")
    main(player_name)