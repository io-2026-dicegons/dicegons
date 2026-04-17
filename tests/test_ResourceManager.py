import pytest

from resourceManager import ResourceManager
from pathlib import Path

from terrain import TerrainType
from building import Building

def test_load_single_unit (tmp_path):
    file = tmp_path / "units.json"

    file.write_text("""
    {
      "unit_types": [
        {
          "ID_Typu_Jednostki": 1,
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

    rm = ResourceManager()
    rm.load_unit_types(file)
    assert rm.get_unit_types() != None, "Expected at least some units loaded - get_unit_types() should not return None"

    assert len(rm.get_unit_types()) == 1, "Expected exactly one unit loaded" 
    loaded_unit = rm.get_unit_by_id(1)
    
    msg = "loaded unit have incorrect values"
    assert loaded_unit.GetName() == "Peasant", msg
    assert loaded_unit.GetID() == 1
    assert loaded_unit.GetAttackDice() == 2
    assert loaded_unit.GetAttackModifier() == 0
    assert loaded_unit.GetDefenseDice() == 2
    assert loaded_unit.GetDefenseModifier() == 0
    assert loaded_unit.GetMaxQuantity() == 100
    assert loaded_unit.GetPrice() == 50
    

def test_load_several_units (tmp_path):
    file = tmp_path / "units.json"

    file.write_text("""
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

    rm = ResourceManager()
    rm.load_unit_types(file)
    pass
    assert rm.get_unit_types() != None, "Expected at least some units loaded - get_unit_types() should not return None"
    assert len(rm.get_unit_types()) == 2, "Expected exactly 2 units loaded" 
    
    msg = "loaded unit have incorrect values"
    loaded_unit = rm.get_unit_by_id(2)
    assert loaded_unit.GetName() == "Peasant"
    assert loaded_unit.GetID() == 1
    assert loaded_unit.GetAttackDice() == 3
    assert loaded_unit.GetAttackModifier() == 3
    assert loaded_unit.GetDefenseDice() == 3
    assert loaded_unit.GetDefenseModifier() == 3
    assert loaded_unit.GetMaxQuantity() == 300
    assert loaded_unit.GetPrice() == 30    
    
    loaded_unit = rm.get_unit_by_id(2)
    assert loaded_unit.GetName() == "Peasant" # only ids should be unique
    assert loaded_unit.GetID() == 2
    assert loaded_unit.GetAttackDice() == 2
    assert loaded_unit.GetAttackModifier() == 0
    assert loaded_unit.GetDefenseDice() == 2
    assert loaded_unit.GetDefenseModifier() == 0
    assert loaded_unit.GetMaxQuantity() == 100
    assert loaded_unit.GetPrice() == 50



def test_load_empty_unit_file (tmp_path):
    file = tmp_path / "units22.json"
    rm = ResourceManager()
    rm.load_unit_types(file)
    # maybe it should be treated more seriously
    assert rm.get_unit_types() != None
    assert len(rm.get_unit_types()) == 0
    

def test_load_single_building (tmp_path):
    file = tmp_path / "buildings.json"

    file.write_text("""
    {
      "building_types": [
        {
          "name": "TestBuilding",
          "id": 0,
          "defence_modifier": 1,
          "income_modifier": 2
        }
      ]
    }
    """)
    
    rm = ResourceManager()
    rm.load_building_types(file)
    msg = "Expected at least some buildings loaded - get_building_types() should not return None"
    assert rm.get_building_types() != None, msg

    assert len(rm.get_building_types()) == 1, "Expected exactly 1 building loaded"
    
    loaded_bulding = rm.get_building_types()[0]
    
    assert loaded_bulding.name == "TestBuilding"
    assert loaded_bulding.id == 0
    assert loaded_bulding.defence_modifier == 1
    assert loaded_bulding.income_modifier == 2
    
def test_load_single_terrain (tmp_path):
    file = tmp_path / "terrain.json"

    file.write_text("""
    {
      "terrain_types": [
        {
            "terrain_name": "Desert",
            "id": 1,
            "defence_modifier": 2,
            "income_modifier": 0,
            "color": [0, 255, 0, 100]
        }
      ]
    }
    """)

    rm = ResourceManager()
    rm.load_terrain_types(file)
    msg = "Expected at least some terrains' definitions loaded - get_terrain_types() should not return None"
    assert rm.get_terrain_types() != None, msg

    assert len(rm.get_terrain_types()) == 1, "Expected 1 terrain type loaded"
    
    loaded_terrain = rm.get_terrain_types()[1]
    assert loaded_terrain.terrain_name == "Desert"
    assert loaded_terrain.id == 1
    assert loaded_terrain.defence_modifier == 2
    assert loaded_terrain.income_modifier == 0
    
def test_get_terrain_by_id (tmp_path):
    file = tmp_path / "terrain.json"

    file.write_text("""
    {
      "terrain_types": [
        {
            "terrain_name": "Desert",
            "id": 1,
            "defence_modifier": 2,
            "income_modifier": 0,
            "color": [0, 255, 0, 100]
        },
        {
            "terrain_name": "Forest",
            "id": 3,
            "defence_modifier": 1,
            "income_modifier": 1,
            "color": [0, 255, 0, 100]
        }
      ]
    }
    """)

    rm = ResourceManager()
    rm.load_terrain_types(file)
    
    loaded_terrain = rm.get_terrain_by_id(1)
    assert loaded_terrain.terrain_name == "Desert"
    assert loaded_terrain.id == 1
    assert loaded_terrain.defence_modifier == 2
    assert loaded_terrain.income_modifier == 0    
    
    # re-work test
    loaded_terrain = rm.get_terrain_by_id(3)
    assert loaded_terrain.terrain_name == "Forest"
    assert loaded_terrain.id == 3
    assert loaded_terrain.defence_modifier == 1
    assert loaded_terrain.income_modifier == 1   
    

    


    
    
    
