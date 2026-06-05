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
          "Min_Atakujacy_Rzut": 3
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
          "Min_Atakujacy_Rzut": 0
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
                "income_modifier": 0
            },
            {
                "name": "Wall",
                "id": 1,
                "defence_modifier": 3,
                "income_modifier": 0
            },
            {
                "name": "Farms",
                "id": 2,
                "defence_modifier": 0,
                "income_modifier": 3
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

def test_game_get_player_hexes( game_controller ):
    hexagons_list = game_controller.get_player_hexes( 1 )
    assert len( hexagons_list ) == 150

def test_game_get_player_hexes_wrong_player_id( game_controller ):
    hexagons_list = game_controller.get_player_hexes( 0 )
    assert len( hexagons_list ) == 0

def test_game_get_player_provinces( game_controller ):
    provinces_id_list = game_controller.get_player_provinces( 1 )
    assert len( provinces_id_list ) == 50

def test_game_get_player_provinces_wrong_player_id( game_controller ):
    provinces_id_list = game_controller.get_player_provinces( 0 )
    assert len( provinces_id_list ) == 0