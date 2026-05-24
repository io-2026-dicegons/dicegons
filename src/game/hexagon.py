
class Hexagon:
    def __init__(self, coordinate ):
        self.coordinate = coordinate

    def __repr__(self):
        x = self.coordinate[0]
        y = self.coordinate[1]
        return "("+str(x)+","+str(y)+")"
    
    def get_adjacent_hexes_list(self, ):
        x = self.coordinate[0]
        y = self.coordinate[1]

        coordinates = []

        coordinates.append( [x+1,y] )
        coordinates.append( [x-1,y] )
        coordinates.append( [x,y+1] )
        coordinates.append( [x,y-1] )

        if( y % 2 == 0 ):
            coordinates.append( [x-1,y+1] )
            coordinates.append( [x-1,y-1] )
        else:
            coordinates.append( [x+1,y+1] )
            coordinates.append( [x+1,y-1] )

        return coordinates