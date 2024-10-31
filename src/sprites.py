class Sprite:
    def __init__(self, win, height, width, blocks):
        self.win = win
        self.height = height
        self.width = width
        self.blocks = blocks
    
    def draw(self):
        raise NotImplementedError

class MovableSprite(Sprite):
    def move(self, dy, dx):
        self.y += dy
        self.x += dx

        # border check
        if self.y < 0:
            self.y = 0
        elif self.y > self.height - 1:
            self.y = self.height - 1
        elif self.x < 0:
            self.x = 0
        elif self.x > self.width - 1:
            self.x = self.width - 1
        
        # solid block check
        elif self.maze.check_solid(self.y, self.x):
            self.y -= dy
            self.x -= dx


class Maze(Sprite):
    def __init__(self, win, height, width, blocks, start, end):
        super().__init__(win, height, width, blocks)
        self.start = start
        self.end = end

    def get_start(self, name):
        return self.start[name]
    
    def get_end(self):
        return self.end

    def check_solid(self, y, x):
        index = y * self.width + x
        return self.blocks[index].is_solid
    
    def draw(self):
        for index, block in enumerate(self.blocks):
            y, x = divmod(index, self.width)
            block.draw(self.win, y, x)


class Player(MovableSprite):
    def __init__(self, win, height, width, blocks, maze):
        super().__init__(win, height, width, blocks)
        self.y, self.x = maze.get_start("player")
        self.maze = maze   

    def check_win(self):
        return (self.y, self.x) == self.maze.get_end()
    
    def draw(self):
        block = self.blocks[0]
        block.draw(self.win, self.y, self.x)

class Chaser(MovableSprite):
    def __init__(self, win, height, width, blocks, maze, player):
        super().__init__(win, height, width, blocks)
        self.y, self.x = maze.get_start("chaser")
        self.maze = maze
        self.player = player
    #plz check the following Astar
    def heuristic(self,a,b):
        return abs (a[0]-b[0])+abs[a[1]-b[1]]
    
    def get_neighbour(self,current):
        neighbours=[]
        for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx=current[0]+dy,current[1]+dx
            if 0<=ny<=self.height and 0<=nx<self.width and not self.maze.is_solid:
                neighbours.append(ny,nx)
            return neighbours

    def astar_search(self,chaser,player):
        temp_set = [(0,start)]
        come_from={}
        g_score={start: 0}
        f_score={start: self.heuristic(chaser,player)}
       
        while temp_set:
            temp_set.sort(key=lambda x: x[0])
            _, current=temp_set.pop(0)
            
            if current == player:
                path=[]
                while current in came_from:
                    path.append(current)
                    current=come_from[current]
                path.reverse()
            return path
            
            for neighbour in self.get_neighbour(current):
                new_g_score=g_score[current]+1
                
                if neighbour not in g_score or new_g_score<g_score[neighbour]:
                    came_from[neighbour]=current
                    g_score[neighbour]=new_g_score
                    f_score[neighbour]=new_g_score+self.heuristic(neighbour,player)
                    temp_set.append((f_score[neighbour],neighbour))
        
        return[]#copilot helps here -- Do we need to clarify?

    def move(self):
        chaser=(self.y,self.x)
        player=(self.player.y,self.player.x)
        path=self.astar_search(chaser,player)
        if path:
            next_move=path[0]
            dy,dx=next_move[0]-self.y,next_move[1]-self.x
            super().move(dy,dx)
            self.y,self.x=next_move
     
    def check_lose(self):
        return (self.y, self.x) == (self.player.y, self.player.x)
    
    def draw(self):
        block = self.blocks[0]
        block.draw(self.win, self.y, self.x)

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



