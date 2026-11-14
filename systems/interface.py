from rich.layout import Layout
from rich import print
from hud import display_hud

class TestPlayer:
    hp = 7
    max_hp = 10
    stam = 75
    max_stam = 100

def create_layout(player):
    layout=Layout()
    
    sidebar=Layout(name="sidebar")
    
    sidebar.split_column(
        Layout(name="HUD",size=8),
        Layout(name="empty",visible=False)
    )
    
    
    layout.split_row(
        Layout(name="dungeon",ratio=3),
        sidebar
    )
    
    layout["HUD"].update(display_hud(player))
    return layout

player = TestPlayer()
layout=create_layout(player)
print(layout)