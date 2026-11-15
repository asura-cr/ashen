from rich.layout import Layout
from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group
from rich.align import Align

from systems.hud import display_hud
from io import StringIO
from contextlib import redirect_stdout

    
def render_dungeon(game_map,player,enemies):
    buffer=StringIO()
    with redirect_stdout(buffer):
        game_map.display(player,enemies,80,30)
    return Text.from_ansi(buffer.getvalue())

def create_layout(player,game_map,enemies,combat_log):
    layout=Layout()
    
    sidebar=Layout(name="sidebar")
    
    sidebar.split_column(
        Layout(name="HUD",size=8),
        Layout(name="COMBAT LOG",ratio=1)
    )
    
    
    layout.split_row(
        Layout(name="dungeon",ratio=3),
        sidebar
    )
    
    layout["HUD"].update(display_hud(player))
    layout["COMBAT LOG"].update(combat_log.display())
    
    dg = render_dungeon(game_map,player,enemies)
    layout["dungeon"].update(
        Panel.fit(dg,title="DUNGEON",border_style="blue")
    )
    return layout

def update_layout(layout,player,game_map,enemies,combat_log):
    layout["HUD"].update(display_hud(player))
    layout["COMBAT LOG"].update(combat_log.display())
    dg=render_dungeon(game_map,player,enemies)
    
    layout["dungeon"].update(
        Panel(dg,title="DUNGEON",border_style="blue")
    )
    
def game_over(kills,stime):
    context=Group(
        Text("YOU DIED",style="bold red",justify="center"),
        Text("You journey ends here..... ",style="dim",justify="center"),
        Text(f"Enemies defeated : {kills}",style="yellow",justify="center"),
        Text(f"You survived {stime // 60}m and {stime % 60}s ",style="cyan",justify="center"),
        Text(""),
        Text(" [R] Restart     [Q] Quit ",style="bold white",justify="center")
        )
    return Panel(context,title="GAME OVER",border_style="red",padding=(2,6),width=45)

def show_game_over(layout,kills,stime):
    layout["dungeon"].update(Align.center(game_over(kills,stime),vertical="middle"))