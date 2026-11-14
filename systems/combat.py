from rich.panel import Panel
from rich.text import Text

class Combatlog:
    def __init__(self):
        self.msgs=[]
        
    def add(self,msg,style="white"):
        self.msgs.append((msg,style))
        
        if len(self.msgs)>10:
            self.msgs.pop(0)
        
    def display(self):
        c=Text()
        for msg,style in self.msgs:
            c.append(msg + "\n", style=style)
        return Panel(c,title="COMBAT LOG",border_style="blue")
        