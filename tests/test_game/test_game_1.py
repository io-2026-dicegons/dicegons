import pytest

from game import *

@pytest.fixture
def game_controller( tmp_path ):

    unit_file = tmp_path / "unit.json"

    unit_file.write_text("""
    {
      "unit_types": [
        {
          "ID_Typu_Jednostki": 1,
          "name": "Peasant",
          "Atak_Kostka": 3,
          "Atak_Modifier": 3,
          "Obrona_Kostka": 3,
          "Obrona_Modifier": 3,
          "Max_Stos": 300,
          "Price": 30,
          "Max_Obronny_Rzut": 6,
          "Min_Obronny_Rzut": 3,
          "Max_Atakujacy_Rzut": 6,
          "Min_Atakujacy_Rzut": 3,
          "symbol": "A",
          "symbol_code": 0
        },
        {
          "ID_Typu_Jednostki": 2,
          "name": "Peasant",
          "Atak_Kostka": 2,
          "Atak_Modifier": 0,
          "Obrona_Kostka": 2,
          "Obrona_Modifier": 0,
          "Max_Stos": 100,
          "Price": 50,
          "Max_Obronny_Rzut": 2,
          "Min_Obronny_Rzut": 0,
          "Max_Atakujacy_Rzut": 2,
          "Min_Atakujacy_Rzut": 0,
          "symbol": "A",
          "symbol_code": 0        
        }
        
      ]
    }
    """)

    building_file = tmp_path / "building.json"

    building_file.write_text("""
    {
        "building_types":
        [
            {
                "name": "Placeholder",
                "id": 0,
                "defence_modifier": 0,
                "income_modifier": 0,
                "symbol": "A",
                "symbol_code": 0
            },
            {
                "name": "Wall",
                "id": 1,
                "defence_modifier": 3,
                "income_modifier": 0,
                "symbol": "B",
                "symbol_code": 0
            },
            {
                "name": "Farms",
                "id": 2,
                "defence_modifier": 0,
                "income_modifier": 3,
                "symbol": "B",
                "symbol_code": 0
            }        
        ]
    }
    """)

    terrain_file = tmp_path / "terrain.json"

    terrain_file.write_text("""
    {
        "terrain_types":
        [
            {
                "terrain_name": "Water",
                "id": 0,
                "defence_modifier": 0,
                "income_modifier": 0,
                "color": [38, 64, 171]
            },
            {
                "terrain_name": "Plains",
                "id": 1,
                "defence_modifier": 0,
                "income_modifier": 2,
                "color": [0, 255, 0, 255]
            },
            {
                "terrain_name": "Mountains",
                "id": 2,
                "defence_modifier": 3,
                "income_modifier": 0,
                "color": [0, 0, 255, 255]
            },
            {
                "terrain_name": "Desert",
                "id": 3,
                "defence_modifier": 2,
                "income_modifier": 0,
                "color": [255, 255, 0, 255]
            },
            {
                "terrain_name": "Forest",
                "id": 4,
                "defence_modifier": 1,
                "income_modifier": 1,
                "color": [0, 255, 0, 255]
            },
            {
                "terrain_name": "Swamp",
                "id": 5,
                "defence_modifier": 2,
                "income_modifier": 1,
                "color": [0, 255, 200, 255]
            }
        ]
    }
    """)

    rm = ResourceManager()

    rm.load_terrain_types( terrain_file )
    rm.load_building_types( building_file )
    rm.load_unit_types( unit_file )

    gc = GameController( rm )
    sc = ScenarioCreator()

    sc.scenario_1( gc )

    return gc

def test_game_init():
    rm = ResourceManager()
    gc = GameController( rm )

def test_game_turn( game_controller ):
    assert game_controller.turn.turn_number == 1
    assert game_controller.turn.turn_phase == 0
    assert game_controller.turn.turn_player == 0

    game_controller.next_phase()

    assert game_controller.turn.turn_number == 1
    assert game_controller.turn.turn_phase == 1
    assert game_controller.turn.turn_player == 0

    game_controller.next_phase()

    assert game_controller.turn.turn_number == 1
    assert game_controller.turn.turn_phase == 2
    assert game_controller.turn.turn_player == 0

    game_controller.next_phase()

    assert game_controller.turn.turn_number == 1
    assert game_controller.turn.turn_phase == 0
    assert game_controller.turn.turn_player == 1

    game_controller.next_phase()
    game_controller.next_phase()
    game_controller.next_phase()

    assert game_controller.turn.turn_number == 2
    assert game_controller.turn.turn_phase == 0
    assert game_controller.turn.turn_player == 0

def test_game_income_from_terrain( game_controller ):

    province_id = 1
    player_id = 1

    assert game_controller.player_list[ player_id ].gold == 0

    terrain_type_id = game_controller.map.province_list[ province_id ].terrain

    assert terrain_type_id == 1
    assert game_controller.resource_manager.get_terrain_by_id( terrain_type_id ).income_modifier == 2

    game_controller.next_phase()
    game_controller.next_phase()
    game_controller.next_phase()
    game_controller.next_phase()
    game_controller.next_phase()
    game_controller.next_phase()

    assert game_controller.player_list[ player_id ].gold == 100

def test_game_buy_unit_without_money( game_controller ):

    province_id = 1

    squad = game_controller.map.province_list[ province_id ].army.get_squad( 1 )
    squad_type = game_controller.resource_manager.get_unit_by_id( squad.squad_type )

    assert squad.squad_type == 1
    assert squad.quantity == 1
    assert squad_type.max_quantity == 300
    assert squad_type.price == 30

    assert game_controller.buy_unit( province_id, squad.squad_type ) == False

    squad = game_controller.map.province_list[ province_id ].army.get_squad( 1 )

    assert squad.quantity == 1

def test_game_buy_unit_with_wrong_province( game_controller ):

    province_id = 51

    squad = game_controller.map.province_list[ province_id ].army.get_squad( 1 )
    squad_type = game_controller.resource_manager.get_unit_by_id( squad.squad_type )

    assert squad.squad_type == 1
    assert squad.quantity == 1
    assert squad_type.max_quantity == 300
    assert squad_type.price == 30

    assert game_controller.buy_unit( province_id, squad.squad_type ) == False

    squad = game_controller.map.province_list[ province_id ].army.get_squad( 1 )

    assert squad.quantity == 1

def test_game_buy_unit( game_controller ):

    province_id = 51

    game_controller.next_phase()
    game_controller.next_phase()
    game_controller.next_phase()

    squad = game_controller.map.province_list[ province_id ].army.get_squad( 1 )
    squad_type = game_controller.resource_manager.get_unit_by_id( squad.squad_type )

    assert game_controller.map.province_list[ province_id ].player_id == 2
    assert squad.squad_type == 1
    assert squad.quantity == 1
    assert squad_type.max_quantity == 300
    assert squad_type.price == 30

    assert game_controller.buy_unit( squad.squad_type, province_id ) == True

    squad = game_controller.map.province_list[ province_id ].army.get_squad( 1 )

    assert squad.quantity == 2

def test_game_attack_lose( game_controller ):

    province_from_id = 45
    province_to_id = 50

    game_controller.next_phase()

    assert game_controller.attack( province_from_id, province_to_id ) == True

    assert game_controller.map.province_list[ province_from_id ].army == None
    assert game_controller.map.province_list[ province_from_id ].player_id == 1
    assert game_controller.map.province_list[ province_to_id ].player_id == 2

def test_game_attack_win( game_controller ):

    province_from_id = 45
    province_to_id = 50

    game_controller.next_phase()

    assert game_controller.attack( province_from_id, province_to_id ) == True

    assert game_controller.map.province_list[ province_from_id ].army == None
    assert game_controller.map.province_list[ province_from_id ].player_id == 1
    assert game_controller.map.province_list[ province_to_id ].player_id == 1