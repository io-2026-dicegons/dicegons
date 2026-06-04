
from game.army import Army

class Province():
    def __init__(self, province_id ):
        self.province_id = province_id
        self.player_id = None
        self.army = Army()
        self.terrain = None
        self.building = None
        self.hexagons_list = []

    #funkcjie set
    def set_player_id(self, player_id):
        self.player_id = player_id

    def set_army(self, army):
        self.army = army

    def set_terrain(self, terrain):
        self.terrain = terrain;
    
    def set_building(self, building):
        self.building = building
    
    #funkcjie add
    def add_hexagon(self, hexagon):
        self.hexagons_list.append(hexagon)

    #funkcjie get

    def get_hexagons_list(self):
        return self.hexagons_list
    
    def get_attack(self):
        attack = 0



        return attack
    
    def get_defence(self):
        attack = 0



        return attack

