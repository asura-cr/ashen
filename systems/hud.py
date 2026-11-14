from colorama import Fore,Style

def vwalls(text,width):
    print(f"║ {text:<{width-2}} ║")


def display_hud(player):
    hearts=""
    width=35
    top =  "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    print("║" + " " * (width + 2) + "║")
    
    print(top)
    for i in range(player.max_hp):
        if i < player.hp:
            hearts += Fore.RED + "♥"
        else:
            hearts +=Fore.WHITE + "♡"
            
    print(f"║ HP: {hearts}{Style.RESET_ALL} ║")
    
    barl=20
    filled=int(player.stam/player.max_stam*barl)
    
    bar = Fore.GREEN + "█" * filled
    bar += Fore.WHITE + "░" * (barl-filled)
    
    print(f"║ Stamina: {bar}{Style.RESET_ALL} {player.stam}/{player.max_stam} ║" )
    
    print(bottom)
    