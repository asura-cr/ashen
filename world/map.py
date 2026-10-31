import random

class Room:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height


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
    
    def create_corridor(self,x,y,length,horizontal=True):
        if horizontal==True:
            self.create_room(x,y,length,3)
        else:
            self.create_room(x,y,3,length)
        
    def create_entrance(self,x,y):
        self.set_tile(x,y," ")
        
    def generate_map(self,max_rooms,min_size,max_size):
        for _ in range(max_rooms):
            width = random.randint(min_size,max_size)
            height = random.randint(min_size,max_size)
            
            x=random.randint(1,self.width-width-1)
            y=random.randint(1,self.height-height-1)
            
            n_room=self.create_room(x,y,width,height)
        
        
            
    def display(self):
        for i in self.tiles:
            print("".join(i))

if __name__=="__main__":
    game_map=Gamemap(50,50)
    game_map.create_room(2,2,5,4)
    game_map.create_corridor(9,4,5,horizontal=True)
    game_map.create_corridor(10,6,7,horizontal=False)
    game_map.display()