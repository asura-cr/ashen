from rich.layout import Layout
from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group
from rich.align import Align
from rich.table import Table
from rich import box

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
        Layout(name="COMBAT LOG",ratio=1),
        Layout(name="CONTROLS GUIDE",ratio=1)
    )
    
    
    layout.split_row(
        Layout(name="dungeon",ratio=3),
        sidebar
    )
    
    layout["HUD"].update(display_hud(player))
    layout["COMBAT LOG"].update(combat_log.display())
    
    table=Table(expand=True, show_edge=False,border_style="blue",box=box.SQUARE,show_lines=True)
    table.add_column("Key",style="medium_spring_green",no_wrap=True)
    table.add_column("Dmg",style="medium_spring_green",no_wrap=True)
    table.add_column("Cost",style="medium_spring_green",no_wrap=True)
    table.add_column("Range",style="medium_spring_green",no_wrap=True)
    
    table.add_row("Z","3","5","1")
    table.add_row("X","5","25","1")
    table.add_row("C","5","10","2")
    table.add_row("V","7","15","3")
    table.add_row("B","1","3","5")
    
    content=Panel.fit(Group(
        table
    ),title="CONTROLS GUIDE",border_style="blue")
    
    layout["CONTROLS GUIDE"].update(content)
    
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