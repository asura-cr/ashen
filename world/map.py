class Gamemap:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.tiles= [[" " for _ in range(width)] for _ in range(height)]

    def set_tile(self,x,y,tile):
        if 0 <=x<self.width and 0<=y<self.height:
            self.tiles[y][x]=tile

    def get_tile(self,x,y):
        if 0 <=x<self.width and 0<=y<self.height:
            return self.tiles[y][x]
        return None

    def create_room(self,x,y,width,height):
        for i in range(y,y+height):

            for j in range(x,x+width):
                if (i ==y or i==y+height-1) or (j==x or j==x+width-1):
                   self.set_tile(j,i,"#")
                
                
                else:
                    self.set_tile(j,i,".") 

            if (i==y or i==y+height-1):
                self.set_tile(x,i,"+")
                self.set_tile(x+width-1,i,"+")

    def display(self):
        for i in self.tiles:
            print("".join(i))

if __name__=="__main__":
    game_map=Gamemap(20,10)
    game_map.create_room(2,2,5,4)
    game_map.display()