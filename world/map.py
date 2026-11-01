import random

class Room:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
    def intersects(self,other):
        padding = 2
        return (
            
            self.x - padding < other.x +other.width and
            self.x + self.width + padding >other.x and
            self.y - padding < other.y + other.height and
            self.y + self.height + padding > other.y
        )
        
    def center(self):
        cx=self.x+self.width//2
        cy=self.y+self.height//2
        return cx,cy
    


class Gamemap:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.rooms=[]
        self.tiles= [[" " for _ in range(width)] for _ in range(height)]

    def set_tile(self,x,y,tile):
        if 0 <=x<self.width and 0<=y<self.height:
            self.tiles[y][x]=tile

    def get_tile(self,x,y):
        if 0 <=x<self.width and 0<=y<self.height:
            return self.tiles[y][x]
        return None

    def create_room(self,x,y,width,height):
        
        if x <0 or y<0 or width<3 or height<3:
            print("Room too small")
            return
        
        if x+width> self.width or y+height>self.height:
            print("Room is outside the map, make the room smaller")
            return
    
    
        for row in range(y,y+height):
            for col in range(x,x+width):
                
                self.set_tile(col,row,".") 
                    
                self.set_tile(x,row,'|')
                self.set_tile(x+width-1,row,'|')
                self.set_tile(col,y,'-')
                self.set_tile(col,y+height-1,'-')
                    
                self.set_tile(x,y,"+")
        
        self.set_tile(x,y,"+")
        self.set_tile(x,y+height-1,'+')
        self.set_tile(x+width-1,y,"+")
        self.set_tile(x+width-1,y+height-1,"+")
        self.rooms.append(Room(x,y,width,height))
                    

    """           
    FAILED ver
    def create_room(self,x,y,width,height):
    
    
        for row in range(y,y+height):

            for col in range(x,x+width):
                
                if (col==x)or (col==x+width-1):
                    self.set_tile(x,row,"|")
                    self.set_tile(x+width-1,row,"|")
               
                else:
                    self.set_tile(col,row,".") 
                    
                self.set_tile(x,row,'|')
                self.set_tile(x+width-1,row,'|')
                self.set_tile(col,y,'-')
                self.set_tile(col,y+height-1,'-')
                    
                self.set_tile(x,y,"+")
        
        self.set_tile(x,y,"+")
        self.set_tile(x,y+height-1,'+')
        self.set_tile(x+width-1,y,"+")
        self.set_tile(x+width-1,y+height-1,"+")
                    
    """
    
    def create_corridor(self,x1,x2,y1,y2):
        for x in range(min(x1,x2),max(x1,x2)+1):
            self.set_tile(x,y1,".")
            self.set_tile(x,y1-2,'-')
            self.set_tile(x,y1+2,'-')
        
        for y in range(min(y1,y2),max(y1,y2)+1):
            self.set_tile(x2,y,'.')
            self.set_tile(x2-1,y,'|')
            self.set_tile(x2+1,y,'|')
        
    def create_entrance(self,x,y):
        self.set_tile(x,y," ")
        

    def generate_rooms(self,max_rooms,min_size,max_size):
        for _ in range(max_rooms):
            width = random.randint(min_size,max_size)
            height = random.randint(min_size,max_size)
            
            x=random.randint(1,self.width-width-1)
            y=random.randint(1,self.height-height-1)
            
            n_room=Room(x,y,width,height) 
            ovrlap=False
            
            for room in self.rooms:
                if n_room.intersects(room):
                    ovrlap=True
                    break
                
            if not ovrlap:
                self.create_room(x,y,width,height)
                    
    def connect_rooms(self,room1,room2):
        x1,y1=room1.center()
        x2,y2=room2.center()
        
        self.create_corridor(x1,x2,y1,y2)
            

    def connect_all_rooms(self):
        for i in range(1,len(self.rooms)):
            self.connect_rooms(self.rooms[i-1],self.rooms[i])
            
        
            
    def display(self):
        for i in self.tiles:
            print("".join(i))

if __name__=="__main__":
    game_map = Gamemap(50, 50)

    game_map.generate_rooms(10, 5, 10)
    game_map.connect_all_rooms()
    game_map.display()