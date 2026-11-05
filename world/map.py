import random
from colorama import Fore,Style,init
import heapq
import os
import msvcrt
init()

RESET=Fore.RESET
RED=Fore.RED
YELLOW=Fore.YELLOW
BLACK=Fore.BLACK
CYAN=Fore.CYAN
GREEN=Fore.GREEN
WHITE=Fore.WHITE

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
    
    def get_entrance(self,direction):
        if direction=="right":
            return self.x + self.width - 1,self.y + self.height//2
        elif direction == "left":
            return self.x, self.y + self.height//2
        elif direction == "up":
            return self.x + self.width//2 , self.y
        elif direction == "down":
            return self.x + self.width//2, self.y + self.height -1
    
class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def move(self, dx, dy, game_map):
        nx = self.x + dx
        ny = self.y + dy

        if game_map.is_walkable(nx, ny):
            self.x = nx
            self.y = ny

class Gamemap:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.rooms=[]
        self.tiles= [[" " for _ in range(width)] for _ in range(height)]
        self.colors=[[None for _ in range(width)]for _ in range(height)]

    def set_tile(self,x,y,tile,color=None):
        if 0 <=x<self.width and 0<=y<self.height:
            self.tiles[y][x]=tile
            self.colors[y][x]=color

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
                
                self.set_tile(col,row,".",YELLOW) 
                    
                self.set_tile(x,row,'|',RED)
                self.set_tile(x+width-1,row,'|',RED)
                self.set_tile(col,y,'-',RED)
                self.set_tile(col,y+height-1,'-',RED)
                    
                self.set_tile(x,y,"+",RED)
        
        self.set_tile(x,y,"+",RED)
        self.set_tile(x,y+height-1,'+',RED)
        self.set_tile(x+width-1,y,"+",RED)
        self.set_tile(x+width-1,y+height-1,"+",RED)
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
    
    def find_path(self, start, end):
        sx, sy = start
        ex, ey = end

        queue = [(0, start)]
        came_from = {start: None}
        cost = {start: 0}

        while queue:
            _, current = heapq.heappop(queue)

            if current == end:
                break

            x, y = current

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue

                # Allow the destination wall, but avoid other rooms.
                if next_pos != end and self.colors[ny][nx] in (RED, YELLOW):
                    continue

                new_cost = cost[current] + 1

                if next_pos not in cost or new_cost < cost[next_pos]:
                    cost[next_pos] = new_cost
                    priority = new_cost + abs(ex - nx) + abs(ey - ny)
                    heapq.heappush(queue, (priority, next_pos))
                    came_from[next_pos] = current

        if end not in came_from:
            return None

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = came_from[current]

        return path[::-1]
    
    def can_see(self,x,y,player,radius=6):
        dx=x-player.x
        dy=y-player.y
        
        return dx*dx+dy*dy<=radius * radius

    
    def create_corridor(self,x1,x2,y1,y2):
        start = (x1,y1)
        end = (x2,y2)
        
        path=self.find_path(start,end)
    
        
        if path is None:
            print("No path found between", start, "and", end)
            return
        for x,y in path:
            if self.get_tile(x,y) not in (".",):
                self.set_tile(x,y,".",CYAN)
            elif self.colors[y][x] is None:
                self.set_tile(x,y,".",CYAN)
        self.create_corridor_walls(path)
    
    def is_protected_tile(self,x,y):
        if x<0 or x>=self.width or y<0 or y>=self.height:
            return True
            
        if (self.colors[y][x]) not in (YELLOW,RED,CYAN):
            return False
        else:
            return True

    def create_corridor_walls(self,path):
        path_tiles=set(path)

        for x,y in path:
            neighbours=[(x,y-1,"-"),(x,y+1,"-"),(x-1,y,"|"),(x+1,y,"|")]
            
            for nx,ny,wall in neighbours:
                if not (0 <= nx < self.width and 0 <= ny <self.height):
                    continue
                if (nx,ny) in path_tiles:
                    continue
                if self.colors[ny][nx] is None:
                    self.set_tile(nx,ny,wall,GREEN)
            

    def create_entrance(self,x,y):
        self.set_tile(x,y,".")
        

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
        
        dx=x2-x1
        dy=y2-y1
        
        if abs(dx)>abs(dy):
            if dx>0:
                start = room1.get_entrance("right")
                end = room2.get_entrance("left")
            else:
                start = room1.get_entrance("left")
                end = room2.get_entrance('right')
        else:
            if dy>0:
                start=room1.get_entrance("down")
                end=room2.get_entrance('up')
            else:
                start=room1.get_entrance("up")
                end=room2.get_entrance("down")
        self.create_entrance(*start)
        self.create_entrance(*end)
        self.create_corridor(start[0],end[0],start[1],end[1])
        
        
            

    def connect_all_rooms(self):
        for i in range(1,len(self.rooms)):
            self.connect_rooms(self.rooms[i-1],self.rooms[i])
            
    
    def is_walkable(self,x,y):
        return self.get_tile(x,y)=="."
            
    def validate(self):
        if not self.rooms:
            return False
        checked=[[False for _ in range(self.width)]for _ in range(self.height)]
        start_x,start_y = self.rooms[0].center()
        queue = [(start_x,start_y)]
        checked[start_y][start_x]= True
        
        while queue:
            x,y = queue.pop(0)
            directions = [(0,-1),(0,1),(-1,0),(1,0)]
            for a,b in directions:
                c = a+x
                d = b+y
                if 0 <= c<self.width and 0<=d<self.height:
                    if self.is_walkable(c,d) and not checked[d][c]:
                        checked[d][c] = True
                        queue.append((c,d))
        
        for room in self.rooms:
            x,y=room.center()
            
            if not checked[y][x]:
                print(x,y)
                print(self.get_tile(x,y))
                return False
                
        return True

            
    def display(self, player=None,view_width=40 , view_height=20):
        camera_x = player.x - view_width//2
        camera_y = player.y - view_height//2
        
        camera_x=max(0,min(camera_x,self.width-view_width))
        camera_y=max(0,min(camera_y,self.height-view_height))
        
        for y in range(camera_y, min(camera_y+view_height,self.height)):
            for x in range(camera_x, min(camera_x+view_width,self.width)):
                
                if not self.can_see(x,y,player):
                    print(" ",end="")
                    continue
                
                if player.x==x and player.y==y:
                    print(WHITE + "@" + RESET,end="")
                    continue
                
                title= self.tiles[y][x]
                color = self.colors[y][x]
                
                if color:
                    print(color+title+RESET,end="")
                else:
                    print(title,end="")
            print()
            
              

if __name__=="__main__":
    game_map = Gamemap(80, 50)

    game_map.generate_rooms(10, 5, 10)
    game_map.connect_all_rooms()
    if not game_map.validate():
        print("Map validation failed.")
        exit()
    x,y = game_map.rooms[0].center()
    player = Player(x,y)
    while True:
        os.system("cls")
        game_map.display(player)
        print("Use WASD to move, Q to quit")
        
        key = msvcrt.getch().decode("utf-8").lower()
        
        if key=="w":
            player.move(0,-1,game_map)
        if key=="s":
            player.move(0,1,game_map)
        if key=="a":
            player.move(-1,0,game_map)
        if key=="d":
            player.move(1,0,game_map)
        if key=="q":
            break
            