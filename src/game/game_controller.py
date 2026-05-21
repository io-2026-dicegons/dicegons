
from game.turn import Turn
from game.map import Map
from game.hexagon import Hexagon
from game.coordinate import Coordinate

class GameController:

    def __init__(self):
        self.map = None
        self.player_list = []
        self.turn = Turn()

    def init_map(self, height, width ):
        self.map = Map(height, width)

    #funkcje UI get

    def get_map(self):
        return self.map

    #funkcje load game set

    def add_province(self, province):
        self.map.add_province(province)

    def add_hex_to_province(self, province_id, hexagon ):
        self.get_map().get_province_list()[ province_id ].append( hexagon )

    def check_correctness(self):

        #czy liczba graczy w player_list jest równa liczbie w turn
        if len( self.player_list ) != self.turn.number_of_players:
            pass

        #czy nie ma dwóch prowincj o takim samym id

    #funkcje do gry

    def attack(self, province_from, province_to):

        #czy province_from istnieje

        #czy province_to istnieje

        #czy province_from należy do gracza który teraz wykonuje ruch

        #czy province_to nie należy do gracza który teraz wykonuje ruch

        #czy province_from sąsiaduje z province_to

        #czy province_from ma armie

        #czy province_from ma armie z przynajmniej jednym oddziałem

        pass

    def move(self, province_from, province_to):

        #czy province_from istnieje

        #czy province_to istnieje

        #czy province_from należy do gracza który teraz wykonuje ruch

        #czy province_to należy do gracza który teraz wykonuje ruch

        #czy province_from sąsiaduje z province_to

        #czy province_from ma armie

        #czy province_from ma armie z przynajmniej jednym oddziałem

        #czy province_to ma wolne miejsce na jednostki

        pass

    def buy_unit(self, unit_type, province_to):

        #czy gracza stać na zakup

        #czy unit_type istnieje

        #czy province_to istnieje

        #czy province_to należy do gracza który teraz wykonuje ruch

        #czy province_to ma wolne miejsce na kupione jednostki

        pass

    def next_phase(self):
        self.turn.next_phase()