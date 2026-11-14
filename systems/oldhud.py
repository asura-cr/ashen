from colorama import Fore,Style

def hudline(text,width):
    print(f"║ {text:<{width-2}} ║")


def display_hud(player):
    width=35
    top =  "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    
    hearts=""
    vhearts=""
    
    print(top)
    hudline("PLAYER STATUS",width)
    print("║" +( " " * (width)) + "║")
    
    for i in range(player.max_hp):
        if i < player.hp:
            hearts += Fore.RED + "♥ "
            vhearts += "♥ "
        else:
            hearts +=Fore.WHITE + "♡ "
            vhearts += "♡ "
            
            
    hudline("HEALTH",width)
    p=width-2- len(vhearts)
    print(f"║ {hearts}{Style.RESET_ALL}{' ' * (p+1) }║")
    
    barl=20
    filled=int(player.stam/player.max_stam*barl)
    
    bar = Fore.GREEN + "█" * filled
    bar += Fore.WHITE + "░" * (barl-filled)
    
    vbar= "█" * filled + "░" * (barl-filled)
    
    
    hudline("STAMINA",width)
    s=f"{vbar} {player.stam}/{player.max_stam}"
    padding= width - 2 -len(s)
    print(f"║ {bar}{Style.RESET_ALL} {player.stam}/{player.max_stam}{' ' * (padding)} ║" )
    
    print(bottom)
    