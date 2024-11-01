class FixedChaserStraight(MovableSprite):
    def __init__(self,win,height,width,blocks,maze,player):
        super().__init__(win, height, width, blocks)
        self.y, self.x = self.starty,self.startx = maze.get_start("fixed_chaser_start")
        self.endy, self.endx = maze.get_start("fixed_chaser_end")
        self.maze=maze
        self.player=player
        self.pastpath=[]        

    #using pastpath to check where the chaser come from (start or end)
    def check_direction(self):
        if self.pastpath[0]==(self.starty, self.startx):
            return True
        elif self.pastpath[0]==(self.endy, self.endx):
            return False
        return True
    #determine the move direction
    def check_step(self,dirction):
        available_steps=((1,0),(0,1),(-1,0),(0,-1))
        if direction:
            if self.endy-self.y>0 and self.endx-self.x==0:
                return available_steps[0]
            elif self.endy-self.y<0 and self.endx-self.x==0:
                return available_steps[2]
            elif self.endy-self.y==0 and self.endx-self.x>0:
                return available_steps[1]
            elif self.endy-self.y==0 and self.endx-self.x<0:
                return available_steps[3]
            
        else:
            if self.starty -self.y>0 and self.startx-self.x==0:
                return available_steps[0]
            elif self.starty-self.y<0 and self.startx-self.x==0:
                return available_steps[2]
            elif self.starty-self.y==0 and self.startx-self.x>0:
                return available_steps[1]
            elif self.starty-self.y==0 and self.startx-self.x<0:
                return available_steps[3]
        
        return(0,0)
    
    def move(self):
        self.pastpath.append((self.y,self.x))
        direction=check_direction()
        dy, dx = check_step(direction)
        super().move(dy,dx)
        if (self.y, self.x) in ((self.starty,self.startx),(self.endy,self.endx)):
            self.pastpath =[]#refresh the pastpath to record the latest initial point(start or end)
    
    def draw(self):
        block = self.blocks[0]
        block.draw(self.win,self.y,self.x)
    def check_lose(self):
        return (self.y,self.x) == (self.player.y,self.player.x)


class FixedChaserClockwise:
    #class a movablesprite which rotate clockwisely
    pass


class FixedChaserAclockwise:
    #class a movablesprite which rotate anti-clockwisely
    pass


#Plz check the Movable Blocks --wy
class MovableBlock(MovableSprite):
    def __init__(self,win, height, width, blocks, maze,player):
        super().__init__(win, height, width, blocks,maze)
        self.player = player
    
    def search_player(self):
        neighbours=self.maze.get_neighbours(self.y,self.x)
        for neighbour in neighbours:
            if (self.player.y,self.player.x)==neighbour:
                return True
        return False
    
    def move(self,player_new_y,player_new_x):
        if self.search_player():
            dy=player_new_y-self.player.y
            dx=player_new_x-self.player.x
            new_y=self.y+dy
            new_x=self.x+dx
            if maze.check_inrange(new_y,new_x) and not maze.check_solid(new_y,new_x):
                super().move(dy,dx)
