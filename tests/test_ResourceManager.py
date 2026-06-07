import pytest

from pathlib import Path

from game.resourceManager import ResourceManager
from game.terrain import TerrainType
from game.building import Building

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
    assert loaded_unit.GetName() == "Peasant"
    assert loaded_unit.GetID() == 1
    assert loaded_unit.GetAttackDice() == 2
    assert loaded_unit.GetAttackModifier() == 0
    assert loaded_unit.GetDefenseDice() == 2
    assert loaded_unit.GetDefenseModifier() == 0
    assert loaded_unit.GetMaxQuantity() == 100
    assert loaded_unit.GetPrice() == 50
    


@pytest.fixture
def rs_with_multiple_units (tmp_path):
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
    return rm

def test_load_multiple_units (rs_with_multiple_units):
    rm = rs_with_multiple_units
    
    assert rm.get_unit_types() != None, "Expected at least some units loaded - get_unit_types() should not return None"
    t = len(rm.get_unit_types())
    assert t == 2, "Expected exactly 2 units loaded; got " + str(t)

def test_get_unit_by_id_consistent_with_direct_access_for_existing_entries (rs_with_multiple_units):
    rm = rs_with_multiple_units

    requested_unit_by_id = rm.get_unit_by_id(1)
    requested_unit_directly = rm.get_unit_types()[1]
    assert requested_unit_by_id == requested_unit_directly

    requested_unit_by_id2 = rm.get_unit_by_id(2)
    requested_unit_directly2 = rm.get_unit_types()[2]
    assert requested_unit_by_id2 == requested_unit_directly2

def test_get_unit_by_nonexisting_id (rs_with_multiple_units):    
    rm = rs_with_multiple_units

    requested_unit = rm.get_unit_by_id(0)
    assert requested_unit == None, "get_unit_types should return None for nonexisting unit type id 0"
    
    requested_unit2 = rm.get_unit_by_id(100)
    assert requested_unit2 == None, "get_building_by_id should return None for nonexisting unit type id 100"

def test_load_several_units (rs_with_multiple_units):    
    rm = rs_with_multiple_units   
    msg = "loaded unit have incorrect values"
    loaded_unit = rm.get_unit_by_id(1)
    assert loaded_unit.GetName() == "Peasant"
    assert loaded_unit.GetID() == 1
    assert loaded_unit.GetAttackDice() == 3
    assert loaded_unit.GetAttackModifier() == 3
    assert loaded_unit.GetDefenseDice() == 3
    assert loaded_unit.GetDefenseModifier() == 3
    assert loaded_unit.GetMaxQuantity() == 300
    assert loaded_unit.GetPrice() == 30    
    
    loaded_unit2 = rm.get_unit_by_id(2)
    assert loaded_unit2.GetName() == "Peasant" # only ids should be unique
    assert loaded_unit2.GetID() == 2
    assert loaded_unit2.GetAttackDice() == 2
    assert loaded_unit2.GetAttackModifier() == 0
    assert loaded_unit2.GetDefenseDice() == 2
    assert loaded_unit2.GetDefenseModifier() == 0
    assert loaded_unit2.GetMaxQuantity() == 100
    assert loaded_unit2.GetPrice() == 50 


def test_load_empty_unit_file (tmp_path):
    file = tmp_path / "units22.json"
    file.write_text(" ")
    rm = ResourceManager()
    rm.load_unit_types(file)
    # maybe it should be treated more seriously
    assert rm.get_unit_types() != None
    assert len(rm.get_unit_types()) == 1
    
def test_load_not_existing_unit_file (tmp_path):
    file = tmp_path / "units22.json"
    rm = ResourceManager()
    rm.load_unit_types(file)
    assert rm.get_unit_types() != None
    assert len(rm.get_unit_types()) == 1
         
def test_load_empty_buildings_file (tmp_path):
    file = tmp_path / "buildings22.json"
    file.write_text(" ")
    rm = ResourceManager()
    rm.load_building_types(file)
    assert rm.get_building_types() != None
    assert len(rm.get_building_types()) == 1
    
def test_load_not_existing_buildings_file (tmp_path):
    file = tmp_path / "buildings22.json"
    rm = ResourceManager()
    rm.load_building_types(file)
    assert rm.get_building_types() != None
    assert len(rm.get_building_types()) == 1

def test_load_empty_terrain_file (tmp_path):
    file = tmp_path / "terrain22.json"
    file.write_text(" ")
    rm = ResourceManager()
    rm.load_terrain_types(file)
    assert rm.get_terrain_types() != None
    assert len(rm.get_terrain_types()) == 1
    
def test_load_not_existing_terrain_file (tmp_path):
    file = tmp_path / "terrain22.json"
    rm = ResourceManager()
    rm.load_terrain_types(file)
    assert rm.get_terrain_types() != None
    assert len(rm.get_terrain_types()) == 1    

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


@pytest.fixture
def rs_with_multiple_buildings (tmp_path):
    file = tmp_path / "buildings.json"

    file.write_text("""
    {
      "building_types": [
        {
          "name": "TestBuilding",
          "id": 1,
          "defence_modifier": 1,
          "income_modifier": 2
        },
        {
          "name": "TestBuilding2",
          "id": 2,
          "defence_modifier": 3,
          "income_modifier": 4
        }
      ]
    }
    """)
    
    rm = ResourceManager()
    rm.load_building_types(file)
    return rm

def test_load_buildings (rs_with_multiple_buildings):    
    rm = rs_with_multiple_buildings
    msg = "Expected at least some buildings loaded - get_building_types() should not return None"
    assert rm.get_building_types() != None, msg
    assert len(rm.get_building_types()) == 2, "Expected exactly 2 buildings loaded"

def test_get_building_by_id_consistent_with_direct_access_for_existing_entries (rs_with_multiple_buildings):
    rm = rs_with_multiple_buildings

    loaded_bulding_by_get_id = rm.get_building_by_id(1)
    loaded_building_from_building_types = rm.get_building_types()[1]
    assert loaded_bulding_by_get_id == loaded_building_from_building_types


    loaded_bulding_by_get_id = rm.get_building_by_id(2)
    loaded_building_from_building_types = rm.get_building_types()[2]
    assert loaded_bulding_by_get_id == loaded_building_from_building_types

def test_get_building_by_nonexisting_id (rs_with_multiple_buildings):
    rm = rs_with_multiple_buildings

    loaded_bulding = rm.get_building_by_id(0)
    assert loaded_bulding == None, "get_building_by_id should return None for nonexisting building with id 0"
    
    loaded_bulding2 = rm.get_building_by_id(100)
    assert loaded_bulding2 == None, "get_building_by_id should return None for nonexisting building with id 100"

def test_get_building_by_id (rs_with_multiple_buildings):    
    rm = rs_with_multiple_buildings

    loaded_bulding1 = rm.get_building_by_id(1)
    
    assert loaded_bulding1.name == "TestBuilding"
    assert loaded_bulding1.id == 1
    assert loaded_bulding1.defence_modifier == 1
    assert loaded_bulding1.income_modifier == 2


    loaded_bulding2 = rm.get_building_by_id(2)
    assert loaded_bulding2.name == "TestBuilding2"
    assert loaded_bulding2.id == 2
    assert loaded_bulding2.defence_modifier == 3
    assert loaded_bulding2.income_modifier == 4


    
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
    assert loaded_terrain.color == [0, 255, 0, 100]




@pytest.fixture
def rs_with_multiple_terrains (tmp_path):
    file = tmp_path / "terrain.json"

    file.write_text("""
    {
      "terrain_types": [
        {
            "terrain_name": "Desert",
            "id": 1,
            "defence_modifier": 2,
            "income_modifier": 0,
            "color": [0, 100, 0, 100]
        },
        {
            "terrain_name": "Forest",
            "id": 3,
            "defence_modifier": 1,
            "income_modifier": 1,
            "color": [0, 10, 200, 100]
        }
      ]
    }
    """)

    rm = ResourceManager()
    rm.load_terrain_types(file)
    return rm


def test_load_terrain_types (rs_with_multiple_terrains):
    rm = rs_with_multiple_terrains
    assert rm.get_terrain_types() != None, "Expected some terrain types loaded - get_terrain_types() should not return None"
    assert len(rm.get_terrain_types()) == 2, "Expected exactly 2 terrain types loaded"

def test_get_terrain_by_id_consistent_with_direct_access_for_existing_entries (rs_with_multiple_terrains):
    rm = rs_with_multiple_terrains

    terrain_type_got_by_id = rm.get_terrain_by_id(1)
    terrain_type_got_directly = rm.get_terrain_types()[1]
    assert terrain_type_got_by_id == terrain_type_got_directly

    terrain_type_got_by_id2 = rm.get_terrain_by_id(3)
    terrain_type_got_directly2 = rm.get_terrain_types()[3]
    assert terrain_type_got_by_id2 == terrain_type_got_directly2


def test_get_terrain_type_by_nonexisting_id (rs_with_multiple_terrains):
    rm = rs_with_multiple_terrains

    requested_terrain = rm.get_terrain_by_id(0)
    assert requested_terrain == None, "get_terrain_by_id should return None for nonexisting terrain with id 0"
    
    requested_terrain2 = rm.get_terrain_by_id(10)
    assert requested_terrain2 == None, "get_terrain_by_id should return None for nonexisting terrain with id 10"


def test_get_terrain_by_id (rs_with_multiple_terrains):
    rm = rs_with_multiple_terrains

    loaded_terrain = rm.get_terrain_by_id(1)
    assert loaded_terrain.terrain_name == "Desert"
    assert loaded_terrain.id == 1
    assert loaded_terrain.defence_modifier == 2
    assert loaded_terrain.income_modifier == 0    
    assert loaded_terrain.color == [0, 100, 0, 100]
    
    loaded_terrain = rm.get_terrain_by_id(3)
    assert loaded_terrain.terrain_name == "Forest"
    assert loaded_terrain.id == 3
    assert loaded_terrain.defence_modifier == 1
    assert loaded_terrain.income_modifier == 1   
    assert loaded_terrain.color == [0, 10, 200, 100]



