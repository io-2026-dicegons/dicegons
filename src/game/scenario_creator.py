
from game.squad import Squad
from game.player import Player
from game.province import Province
from game.army import Army
from game.building import Building
from game.terrain import TerrainType

import random

class ScenarioCreator:

    def add_empty_province(self, game_controller, id, player, Hex, terrain):
        province = Province( id )
        
        province.player_id = player
  
        province.terrain = terrain

        for i, j in (Hex):
            province.add_hexagon( [i,j] )


        buildings_id = [0, 0, 1, 2, 3, 4]
        province.building = random.choice(buildings_id)
        province.terrain = terrain



        squad_one_type = random.randint(-2, 3)
        if(squad_one_type >= 0):
            squad_1 = Squad( 0, squad_one_type, random.randint(1, 10))

        squad_two_type = random.randint(-2, 3)
        if(squad_two_type >= 0):
            squad_2 = Squad( 1, squad_two_type, random.randint(1, 10))

        if( (squad_one_type >= 0 ) or ( squad_two_type >= 0)):
            army = Army()
            if(squad_one_type >= 0):
                army.set_squad( 1, squad_1 )
            if(squad_two_type >= 0):
                army.set_squad( 2, squad_2 )

            province.set_army( army )



        game_controller.map.add_province( province )


    def scenario_1( self, game_controller ):

        player_1 = Player( 1, "Gracz 1", 0 )
        player_1.player_color = (255,0,0)
        player_2 = Player( 2, "Gracz 2", 1000 )
        player_2.player_color = (0,255,0)

        game_controller.add_player(player_1)
        game_controller.add_player(player_2)

        for i in range(0,20):
            for j in range(0,5):

                province = Province( i * 5 + j )

                if i < 10 :
                    province.player_id = player_1.player_id
                else:
                    province.player_id = player_2.player_id

                province.terrain = 1
                province.add_hexagon( [i,j*3] )
                province.add_hexagon( [i,j*3+1] )
                province.add_hexagon( [i,j*3+2] )

                squad_1 = Squad( 0, 0, 1 )
                squad_2 = Squad( 0, 1, 2 )

                army = Army()
                army.set_squad( 1, squad_1 )
                army.set_squad( 2, squad_2 )

                province.set_army( army )

                province.building = 1
                if( i % 2 == 0 ):
                    province.terrain = 1
                else:
                    province.terrain = 2


                game_controller.map.add_province( province )

        return game_controller
    
    def scenario_2( self, game_controller ):

        player_1 = Player( 1, "Player 1", 0 )
        player_1.player_color = (255,0,0)
        player_2 = Player( 2, "Player 2", 0 )
        player_2.player_color = (0,255,0)

        game_controller.add_player(player_1)
        game_controller.add_player(player_2)

        self.add_empty_province(game_controller, 0, player_1.player_id, [[16, 12], [16, 13], [16, 14]], 5)
        self.add_empty_province(game_controller, 1, player_2.player_id, [[15, 12], [14, 12], [13, 12]], 3)
        self.add_empty_province(game_controller, 2, player_1.player_id, [[15, 11], [14, 11], [13, 11], [12, 11], [15, 10]], 3)
        self.add_empty_province(game_controller, 3, player_1.player_id, [[12, 12], [11, 11], [10, 11], [11, 12], [11, 13]], 3)
        self.add_empty_province(game_controller, 4, player_2.player_id, [[10, 12], [9, 11], [8, 11], [9, 10]], 2)
        self.add_empty_province(game_controller, 5, player_2.player_id, [[10, 10], [9, 9], [11, 10], [10, 9], [11, 9]], 3)
        self.add_empty_province(game_controller, 6, player_1.player_id, [[12, 10],[12, 9],[13, 10],[13, 9],[14, 10],[14, 9]], 3)
        self.add_empty_province(game_controller, 7, player_1.player_id, [[16, 11],[17, 11],[18, 11],[18, 10]], 1)
        self.add_empty_province(game_controller, 8, player_1.player_id, [[18, 9], [17, 9],[17, 10],[16, 10],[16, 9],[15, 9]], 1)
        self.add_empty_province(game_controller, 9, player_2.player_id, [[16, 8],[15, 7],[16, 7],[17, 7]], 2)
        self.add_empty_province(game_controller, 10, player_2.player_id, [[17, 6],[16, 6],[16, 5],[15, 5],[15, 6]], 2)
        self.add_empty_province(game_controller, 11, player_2.player_id, [[14, 5],[14, 6],[13, 5],[13, 6]], 1)
        self.add_empty_province(game_controller, 12, player_1.player_id, [[12, 5],[13, 4],[12, 4],[12, 3],[11, 3],[12, 2]], 1)
        self.add_empty_province(game_controller, 13, player_1.player_id, [[12, 6],[11, 7],[11, 6],[10, 7],[10, 6],[12, 8]], 2)
        self.add_empty_province(game_controller, 14, player_2.player_id, [[11, 5],[11, 4],[10, 5],[10, 4],[10, 3],[9, 3],[11, 2]], 1)
        self.add_empty_province(game_controller, 15, player_1.player_id, [[10, 2],[9, 2],[9, 1],[8, 1],[9, 0], [10, 0]], 6)
        self.add_empty_province(game_controller, 16, player_2.player_id, [[9, 5],[9, 4],[8, 3],[8, 4],[8, 5],[9, 6]], 1)
        self.add_empty_province(game_controller, 17, player_2.player_id, [[9, 7],[8, 7],[8, 6],[7, 7],[7, 5]], 1)
        self.add_empty_province(game_controller, 18, player_1.player_id, [[8, 0],[7, 1],[8, 2],[7, 2],[6, 1],[6, 2]], 6)
        self.add_empty_province(game_controller, 19, player_2.player_id, [[5, 2],[4, 2],[4, 3],[3, 3],[3, 2], [2,3]], 6)
        self.add_empty_province(game_controller, 20, player_2.player_id, [[3, 4],[4, 4],[3, 5],[2, 4],[1, 4]], 2)
        self.add_empty_province(game_controller, 21, player_1.player_id, [[5, 3],[6, 3],[7, 3],[7, 4],[6, 4],[5, 4],[6, 5]], 2)
        self.add_empty_province(game_controller, 22, player_1.player_id, [[4, 5],[5, 5],[7, 6],[6, 6],[4, 6],[6, 7], [5, 6]], 1)



        return game_controller