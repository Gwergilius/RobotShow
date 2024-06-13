import math
import logging
import os
logfile = "{0}//RobotShow/logfile.log".format(os.environ.get('TEMP'))
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename=logfile, level=logging.DEBUG, force=True)
       
class Display:
    ordA  = ord('A')
    emptyCell = ' '*3
    collision = "lXr"
    border0 = "-+-"
    border1 = "---"
    prefixes = ["{0:5.1f} ", ' Time ', ' '*6 ]
    prefLen  = len(prefixes[2])

    def __init__(self, duct):
        self._length = duct.length
        self.reset()

    def reset(self):
        self._display = [
            [Display.emptyCell]*self._length, 
            [Display.border0+Display.border1]*(self._length >> 1) + [Display.border0],
            [self._displayNum(i)+Display.emptyCell for i in range(self._length >> 1)]+[self._displayNum(self._length>>1)],
        ]
        
    def put(self, r):
        if 0 <= r.pos and r.pos < self._length:
            self._display[0][r.pos] = str(r) if self._display[0][r.pos] == Display.emptyCell else self._showCollision(r)

    def showLine(self, idx, time):
        return Display.prefixes[idx].format(time) + ''.join(self._display[idx])

    def __str__(self):
        return '\n'.join([self.showLine(idx) for idx in range(3)])

    def _displayNum(self, i):
        return f"{i:#2} "

    def _showCollision(self, r):
        x = self._display[0][r.pos][1]
        y = r.name()
        if r.dir < 0: x,y = y,x
        return Display.collision.replace('l', x).replace('r', y)

class Robot:
    def __init__(self):
        self.id = None
        self.dir = 1
        self.pos = None

    def __str__(self):
        left = '<' if self.dir == -1 else ' '
        right = '>' if self.dir == 1 else ' '
        return f"{left}{self.name()}{right}"

    def name(self):
        return '*' if self.id is None else chr(Display.ordA+self.id)

    def move(self, pos):
        self.pos = pos
        return self

    def turn(self):
        self.dir = -self.dir
        return self

    def forward(self, dt=1):
        pos = self.pos + dt*self.dir
        self.move(pos)

    def collides(self, other):
        return self != other and self.pos == other.pos

class Duct:
    log = logging.getLogger("Duct")
    maxTime = 1000

    def __init__(self, length):
        self.length = (length * 2)
        self._robots = []
        self.display = Display(self)
        
    def add(self, r, pos, v=1):
        r.id = len(self._robots) 
        self._robots.append(r)
        pos = math.floor(pos*2)
        r.dir = 1 if pos < self.length // 2 else -1
        r.velocity = v
        r.move(pos)    
        self.display.put(r)
        return r
         
    def play(self):
        time = 0
        for i in reversed(range(3)):
            Duct.log.debug(self.display.showLine(i, time))
        while len(self._robots) > 0:
            time += 1
            self.display.reset()
            for r in self._robots: 
                r.forward()
            for r in reversed(self._robots):
                if r.pos < 0 or r.pos >= self.length:                    
                    self._robots.remove(r)
                else:
                    self.display.put(r)
                    for c in self._robots:
                       if r.collides(c): 
                           c.turn()
            Duct.log.debug(self.display.showLine(0, time/2))
        return time

def main(line1, line2, line3):
    duct = Duct(int(line1))
    
    for pos in line3.split():
        duct.add(Robot(), int(pos))
    time = duct.play()
    return(round(time/2))

# print( main(input(), input(), input()) )
