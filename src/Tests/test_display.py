import pytest
from program import *
import logging
logging.basicConfig(level=logging.DEBUG, force=True)

@pytest.fixture
def duct():
    return Duct(10)

def itemPos(r):
    return Display.prefLen + 3*r.pos + 1

def directionPos(r):
    return itemPos(r) + r.dir    

def test_01_normal(duct):    
    r0 = duct.add(Robot(), 2)
    r1 = duct.add(Robot(), 6.5)

    line = duct.display.showLine(0, 1)
    pos = [itemPos(r0), itemPos(r1)]
    assert pos[0] ==  line.find(r0.name())
    assert line[pos[1]] == r1.name()
    assert directionPos(r0) == line.find('>')
    assert line[directionPos(r1)] == '<'

def test_02_close(duct):
    r0 = duct.add(Robot(), 4.5)
    r1 = duct.add(Robot(), 5)
    line = duct.display.showLine(0, 2)

    assert line[itemPos(r0)] == r0.name()
    assert line[itemPos(r1)] == r1.name()
    assert line[directionPos(r0)] == '>'
    assert line[directionPos(r1)] == '<'

def test_03_collsion(duct):  
    r0 = duct.add(Robot(), 8).turn()
    r1 = duct.add(Robot(), 8) # collision  
    line = duct.display.showLine(0, 3)

    pos = itemPos(r0)-1
    assert line[pos:pos+3] == f'{r1.name()}X{r0.name()}'

def test_04_log(duct):

    logging.debug(duct.display.showLine(2, 0))
    logging.debug(duct.display.showLine(1, 0))

    r0 = duct.add(Robot(), 2)
    r1 = duct.add(Robot(), 6.5)
    logging.debug(duct.display.showLine(0, 1/2))

    r0 = duct.add(Robot(), 4.5)
    r1 = duct.add(Robot(), 5)
    logging.debug(duct.display.showLine(0, 2/2))
    
    r0 = duct.add(Robot(), 8)
    r1 = duct.add(Robot(), 8).turn() # collision  
    logging.debug(duct.display.showLine(0, 3/2))
