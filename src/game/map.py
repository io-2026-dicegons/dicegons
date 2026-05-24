
from game.province import Province
from game.hexagon import Hexagon

class Map:

    def __init__(self):
        self.province_list = {}

    def __repr__(self):
        pass
    
    #funkcje add

    def add_province(self, province):
        self.province_list[ province.province_id ] = province

    #funkcje get
    
    def get_province_list(self):
        return self.province_list
    
    def check_provine_by_id(self, provine_id):
        if self.province_list[ provine_id ] == None:
            return True
        return False
