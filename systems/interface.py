from rich.layout import Layout
from rich import print
from rich.text import Text
from rich.panel import Panel
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