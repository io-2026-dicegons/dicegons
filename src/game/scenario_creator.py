
from game.squad import Squad
from game.player import Player
from game.province import Province
from game.army import Army
from game.building import Building
from game.terrain import TerrainType

class ScenarioCreator:
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