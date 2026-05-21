
from game.province import Province
from game.hexagon import Hexagon
from game.coordinate import Coordinate

class Map:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.province_list = []

    def __repr__(self):
        pass

    def is_hex_on_map(self, coordinate):
        c = coordinate
        if( c.x < 0 or c.x >= self.width ):
            return False
        elif( c.y < 0 or c.y >= self.height ):
            return False
        return True
    
    def get_adjacent_hexes_list(self, coordinate):
        x = coordinate.x
        y = coordinate.y

        coordinates = []

        coordinates.append(Coordinate(x+1,y))
        coordinates.append(Coordinate(x-1,y))
        coordinates.append(Coordinate(x,y+1))
        coordinates.append(Coordinate(x,y-1))

        if( y % 2 == 0 ):
            coordinates.append(Coordinate(x-1,y+1))
            coordinates.append(Coordinate(x-1,y-1))
        else:
            coordinates.append(Coordinate(x+1,y+1))
            coordinates.append(Coordinate(x+1,y-1))

        coordinates = [ c for c in coordinates if self.is_hex_on_map(c) ]

        return coordinates
    
    #funkcje add

    def add_province(self, province):
        self.province_list.append(province)

    #funkcje get

    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
    
    def get_province_list(self):
        return self.province_list