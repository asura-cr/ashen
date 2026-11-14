from rich.panel import Panel
from rich.text import Text

class Combatlog:
    def __init__(self):
        self.msgs=[]
        
    def add(self,msg):
        self.msgs.append(msg)
        
        if len(self.msgs)>5:
            self.msgs.pop(0)
        
    def display(self):
        c=Text("\n".join(self.msgs))
        return Panel(c,title="COMBAT LOG",border_style="blue")
        