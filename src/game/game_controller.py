
from game.turn import *
from game.map import Map
from game.hexagon import Hexagon
from game.resourceManager import ResourceManager
from game.player import Player
from game.army import Army
from game.province import Province
from game.terrain import TerrainType

class GameController:

    def __init__(self, resource_manager):
        self.map = Map()
        self.player_list = {}
        self.turn = Turn()
        self.resource_manager = resource_manager

    #funkcje UI get
    def get_player_list(self):
        return self.player_list
    
    def get_player_provinces(self,player_id):
        provinces_id_list = []

        for province_id, province in self.map.get_province_list().items():
            if province.player_id == player_id:
                provinces_id_list.append( province_id )

        return provinces_id_list


    def get_player_hexes(self, player_id):
        heks = []
        for province_id, province in self.map.get_province_list().items():
            if province.player_id == player_id:
                for h in province.get_hexagons_list():
                    heks.append( h )
        
        return heks

    def get_terrain_color(self, terrain_type_id):
        return self.resource_manager.get_terrain_by_id( terrain_type_id ).color
    
    def get_terrain_defence_modifier(self, terrain_type_id):
        return self.resource_manager.get_terrain_by_id( terrain_type_id ).defence_modifier
    
    def get_terrain_income(self, terrain_type_id):
        return self.resource_manager.get_terrain_by_id( terrain_type_id ).income_modifier
    
    def get_terrain_name(self, terrain_type_id):
        return self.resource_manager.get_terrain_by_id( terrain_type_id ).terrain_name
    

    def get_unit_symbol(self, unit_id):
        return self.resource_manager.get_unit_by_id( unit_id ).symbol
    
    def get_unit_symbol_code(self, unit_id):
        return self.resource_manager.get_unit_by_id( unit_id ).symbol_code
    
    def get_unit_max_stack(self, unit_id):
        return self.resource_manager.get_unit_by_id( unit_id ).max_quantity
    
    def get_unit_attack_dice(self, unit_id):
        return self.resource_manager.get_unit_by_id( unit_id ).attack_dice
    
    def get_unit_defence_dice(self, unit_id):
        return self.resource_manager.get_unit_by_id( unit_id ).defensive_dice
    
    def get_unit_price(self, unit_id):
        return self.resource_manager.get_unit_by_id( unit_id ).price
    
    def get_unit_name(self, unit_id):
        return self.resource_manager.get_unit_by_id( unit_id ).name
    

    def get_building_symbol(self, building_id):
        return self.resource_manager.get_building_by_id( building_id ).symbol
    
    def get_building_symbol_code(self, building_id):
        return self.resource_manager.get_building_by_id( building_id ).symbol_code
    
    def get_building_income(self, building_id):
        return self.resource_manager.get_building_by_id( building_id ).income_modifier
    
    def get_building_defence(self, building_id):
        return self.resource_manager.get_building_by_id( building_id ).defence_modifier
    
    def get_building_name(self, building_id):
        return self.resource_manager.get_building_by_id( building_id ).name
    

    def get_army_squad_stack(self, province_id, squad_nr ):
        army = self.map.province_list[ province_id ].army
        squad = army.get_squad( squad_nr )
        return squad.quantity
    
    def get_army_squad_unit_type(self, province_id, squad_nr ):
        army = self.map.province_list[ province_id ].army
        squad = army.get_squad( squad_nr )
        return squad.squad_type
    
    def get_province_hex_list(self, province_id):
        return self.map.province_list[ province_id ].hexagons_list
    
    def get_province_owner(self, province_id):
        return self.map.province_list[ province_id ].player_id
    
    def get_province_building(self, province_id):
        return self.map.province_list[ province_id ].building
    
    def get_province_terrain(self, province_id):
        return self.map.province_list[ province_id ].terrain


    #funkcje load game set
    def add_player(self, player ):
        self.player_list[ player.player_id ] = player
        self.turn.number_of_players = len( self.player_list )

    def add_province(self, province):
        self.map.add_province(province)

    def add_hex_to_province(self, province_id, hexagon ):
        self.get_map().get_province_list()[ province_id ].append( hexagon )

    #funkcje sprawdzające poprawność

    def check_correctness(self):

        #czy liczba graczy w player_list jest równa liczbie w turn
        if len( self.player_list ) != self.turn.number_of_players:
            return False

        #czy nie ma dwóch prowincj o takim samym id
        #province_list jest tablicą asocjacyjną indeksowaną province_id

        #każda prowincja ma przynajmniej 3 heksagony
        for province_id, province in self.map.province_list.items():
            if len( province.hexagons_list ) < 3:
                return False

        #każdy skład ma istniejący typ
        for province_id, province in self.map.province_list.items():
            army = province.army
            if not self.resource_manager.get_unit_by_id( army.first_squad.squad_type ):
                return False
            
            if not self.resource_manager.get_unit_by_id( army.second_squad.squad_type ):
                return False
        
        #każdy skład ma prawidłową liczebność
        for province_id, province in self.map.province_list.items():
            army = province.army
            if not self.check_squad_quantity( army.first_squad ):
                return False
            
            if not self.check_squad_quantity( army.second_squad ):
                return False
        
        #każdy budynek ma istniejący typ
        for province_id, province in self.map.province_list.items():
            if not self.resource_manager.get_building_by_id( province.building ):
                return False
        
        #każda prowincja ma istniejący typ terenu
        for province_id, province in self.map.province_list.items():
            if not self.resource_manager.get_terrain_by_id( province.terrain ):
                return False

        #żaden heks nie należy do dwóch prowincji

        return True

    def check_squad_quantity(self, squad):

        squad_type = self.resource_manager.get_unit_by_id( squad.squad_type )

        if squad.quantity <= 0 :
            return False
        
        if squad.quantity > squad_type.max_quantity :
            return False
        
        return True
    

    #funkcje do gry
    def if_adjacent( self, province_from_id, province_to_id ):

        heks_from = []

        province_from = self.map.province_list[ province_from_id ]
        province_to = self.map.province_list[ province_to_id ]

        for h in province_from.get_hexagons_list():
            heks_from.append( h )

        heks_adjacent = []
        for h in heks_from:
            heks = Hexagon( h )

            for a in heks.get_adjacent_hexes_list():
                heks_adjacent.append( a )

        for h in province_to.get_hexagons_list():
            if h in heks_adjacent:
                return True

        return False

    def attack(self, province_from, province_to):

        player_id = list(self.player_list.keys())[ self.turn.get_current_player() ]
        player = self.player_list[player_id]

        #czy jest faza ataku
        if not self.turn.get_phase() == ATTACK_PHASE:
            return False
        
        #czy province_from istnieje
        if not self.map.check_province_by_id( province_from ):
            return False

        #czy province_to istnieje
        if not self.map.check_province_by_id( province_to ):
            return False

        #czy province_from należy do gracza który teraz wykonuje ruch
        attacker = self.map.province_list[ province_from ].player_id
        if player_id != attacker :
            return False

        #czy province_to nie należy do gracza który teraz wykonuje ruch
        defender = self.map.province_list[ province_to ].player_id
        if player_id == defender :
            return False

        #czy province_from sąsiaduje z province_to
        if not self.if_adjacent( province_from, province_to ):
            return False

        #czy province_from ma armie
        if self.map.province_list[ province_from ].army == None :
            return False

        #czy province_from ma armie z przynajmniej jednym oddziałem
        army = self.map.province_list[ province_from ].army
        if army.first_squad == None :
            return False
        
        if army.second_squad == None :
            return False

        # stoczenie bitwy

        attack = self.map.province_list[ province_from ].get_attack()
        defence = self.map.province_list[ province_to ].get_defence()

        if attack > defence :
            #atakujący wygrał
            self.map.province_list[ province_to ].army = None
            self.map.province_list[ province_to ].army = self.map.province_list[ province_from ].army
            self.map.province_list[ province_from ].army = Army()

            self.map.province_list[ province_to ].player_id = self.attacker
        else:
            self.map.province_list[ province_from ].army = None

        return True

    def move(self, province_from, squad_nr_from, province_to, squad_nr_to ):

        #czy jest faza ruchu
        if not self.turn.get_phase == MOVEMENT_PHASE:
            return False

        #czy province_from istnieje
        if not self.map.check_province_by_id( province_from ):
            return False

        #czy province_to istnieje
        if not self.map.check_province_by_id( province_to ):
            return False

        #czy province_from należy do gracza który teraz wykonuje ruch
        if self.player_list[ self.turn.get_current_player() ].player_id != self.map.province_list[ province_from ].player_id :
            return False

        #czy province_to należy do gracza który teraz wykonuje ruch
        if self.player_list[ self.turn.get_current_player() ].player_id != self.map.province_list[ province_to ].player_id :
            return False

        #czy province_from sąsiaduje z province_to
        if not self.if_adjacent( province_from, province_to ):
            return False

        #czy province_from ma armie
        if self.map.province_list[ province_from ].army == None :
            return False

        squad_from = self.map.province_list[ province_from ].army.get_squad( squad_nr_from )
        #czy province_from ma armie z oddziałem squad_nr_from
        if squad_from == None :
            return False

        squad_to = self.map.province_list[ province_from ].army.get_squad( squad_nr_to )
        squad_type = self.resource_manager.get_unit_by_id( squad_to.squad_type )
        #czy province_to ma wolne miejsce na jednostki
        if squad_to != None and squad_type == squad_from.squad_type and squad_type.max_quantity - squad_to.quantity >= squad_from.quantity :
            return False
        
        if squad_to == None :
            self.map.province_list[ province_from ].army.set_squad( squad_nr_to, squad_from )
        else:
            squad_to.quantity += squad_from.quantity

        self.map.province_list[ province_from ].army.set_squad( squad_nr_from, None )

        pass

    def buy_unit(self, unit_type_id, province_to):

        #czy jest faza kupowania
        if not self.turn.get_phase() == BUYING_PHASE:
            return False
        
        player_id = list(self.player_list.keys())[ self.turn.get_current_player() ]
        player = self.player_list[player_id]
        unit_type = self.resource_manager.get_unit_by_id( unit_type_id )

        #czy unit_type istnieje
        if not unit_type:
            return False

        #czy gracza stać na zakup
        if player.gold < unit_type.price :
            return False
        
        #czy province_to istnieje
        if not self.map.check_province_by_id( province_to ):
            return False
        
        #czy province_to należy do gracza który teraz wykonuje ruch
        if player.player_id != self.map.province_list[ province_to ].player_id :
            return False
        
        #czy province_to ma wolne miejsce na kupione jednostki
        if not self.map.province_list[ province_to ].army.check_can_buy_unit( unit_type ):
            return False
        
        self.map.province_list[ province_to ].army.buy_unit( unit_type )

        return True

    def __income_calculation(self):
        provinces = self.map.province_list
        for province_id, province in provinces.items():

            terrain = self.resource_manager.get_terrain_by_id( province.terrain )
            building = self.resource_manager.get_building_by_id( province.building )
            income = 0

            if terrain != None:
                income += terrain.income_modifier

            if building != None:
                income += building.income_modifier

            self.player_list[ province.player_id ].gold += income

    def next_phase(self):
        if self.turn.next_phase():
            self.__income_calculation()
