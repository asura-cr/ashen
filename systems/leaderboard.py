import json
from pathlib import Path
from datetime import datetime
from rich.table import Table
from rich.panel import Panel

Lb_file=Path(__file__).resolve().parent.parent / "leaderboard.json"

def load_lb():
    if not Lb_file.exists():
        return []
    
    try:
        with open(Lb_file,"r") as f:
            return json.load(f)
    except (json.JSONDecodeError,OSError):
        return []
    
def save_run(name,kills,time_survived):
    lb=load_lb()
    lb.append({
        "name":name,
        "kills":kills,
        "time_survived":time_survived,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    
    lb.sort(
        key=lambda run: (
            run["kills"],
            run["time_survived"]
        ),
        reverse=True
    )
    
    lb=lb[:10]
    
    with open(Lb_file,"w") as f:
        json.dump(lb,f,indent=4)
    return lb

def show_lb():
    lb=load_lb()
    
    table=Table(title="ASHEN LEADERBOARD",expand=True)
    
    table.add_column("#", justify="center",style="dim")
    table.add_column("Player Name",style="cyan",justify="center")
    table.add_column("Kills",justify="center")
    table.add_column("Time Survived",justify="center")    
    
    for pos,run in enumerate(lb,start=1):
        table.add_row(
            str(pos),
            str(run["name"]),
            str(run["kills"]),
            f"{run['time_survived']}s"
        )
        
    return Panel(table,border_style="yellow",subtitle=" [R] to Restart  [Q] to Quit")