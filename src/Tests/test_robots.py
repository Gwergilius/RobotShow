import pytest
from program import *
import logging
logfile = "{0}//RobotShow/logfile.log".format(os.environ.get('TEMP'))
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename=logfile, level=logging.DEBUG, force=True)

@pytest.mark.parametrize(
    argnames="l, n, bots, expected", 
    argvalues=[
        ( 10, 2, '2 6', 8 ), 
        ( 20, 7, '1 2 20 7 6 10 14', 20), 
        ( 103, 20, '87 19 72 59 22 74 89 30 33 3 66 77 15 23 58 82 56 98 1 84', 102),     
        ( 113, 50, 
            '42 38 102 73 106 15 51 8 72 66 112 95 87 90 1 104 25 43 14 29 57 98 33 '
            '58 55 16 49 60 105 71 18 12 28 86 4 101 63 36 22 31 45 17 75 85 32 61 '
            '62 30 107 13', 112), 
        ( 156, 78,
            '14 127 21 15 91 121 89 105 32 136 100 95 143 112 88 147 78 48 36 114 28 '
            '33 151 9 59 11 116 134 6 39 67 50 110 102 139 49 118 30 144 4 97 56 52 '
            '73 125 115 149 66 71 42 3 61 141 81 106 101 99 137 111 133 79 43 145 84 '
            '51 107 131 12 87 104 60 126 119 146 96 7 94 10', 153), 
        ( 14, 1, '7', 8), 

        ], ids=['01 Example', '02 Simple', '03 More bots', '04 Ping pong', 
                '05 Trafic jam', '06 Singular', ])
def test_acceptance(l, n, bots, expected):
    actual = main(str(l), str(n), bots)
    assert actual == expected