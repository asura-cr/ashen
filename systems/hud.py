from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console=Console()

def display_hud(player):
    health= " ".join(
        "[red]♡[/red] " if i < player.hp else "[dim]♡[/dim] "
        for i in range(player.max_hp)
    )
    
    barl=20
    filled=int(player.stam/player.max_stam * barl)
    
    stam= (
        f"[green]{'█' * filled}[/green]"
        f"[white]{'░' * (barl-filled)}[/white]"
    )
    
    content = (
        f"[bold]HEALTH[/bold]\n"
        f"{health}\n \n"
        f"[bold]STAMINA[/bold]\n"
        f"{stam} {player.stam}/{player.max_stam} \n"
    )
    
    panel=Panel.fit(content, title="Player Stats",border_style="blue")
    return panel