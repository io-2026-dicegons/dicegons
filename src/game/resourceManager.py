from pathlib import Path
import json 

from game.terrain import TerrainType
from game.building import Building
from game.unit import UnitType

class ResourceManager:
    def __init__(self):
        self.building_types = {} 
        self.terrain_types = {}
        self.unit_types = {} 
        pass

    def load_definitions(self):
        # load units, building, terrain types from appropriate files
        self.load_terrain_types(Path("terrain_types.json"))
        self.load_building_types(Path("building_types.json"))
        self.load_unit_types(Path("units.json"))
        # filenames should be configurable
        return

    def load_unit_types(self, file_path):
        try:
            with open(file_path, 'r') as fi:
                try:
                    data = json.load(fi)
                except json.JSONDecodeError:
                    print ("Invalid JSON within file describing units")
                    self.unit_types = { UnitType() }
                    return
        
            try:
                for item in data["unit_types"]:
                    current = UnitType(
                        id_unit_type = item["ID_Typu_Jednostki"],
                        name = item["name"],
                        attack_dice = item["Atak_Kostka"],
                        attack_modifier = item["Atak_Modifier"],
                        defensive_dice = item["Obrona_Kostka"],
                        defense_modifier = item["Obrona_Modifier"],
                        max_quantity = item["Max_Stos"],
                        price = item["Price"],
                        max_defensive_result = item["Max_Obronny_Rzut"],
                        min_defensive_result = item["Min_Obronny_Rzut"],
                        max_offensive_result = item["Max_Atakujacy_Rzut"],
                        min_offensive_result = item["Min_Atakujacy_Rzut"],
                        symbol = item["symbol"],
                        symbol_code = item["symbol_code"]
                    )
                    self.unit_types[current.id_unit_type] = current
            except KeyError:
                print ("File with unit types definitions malformed. Loading placeholder unit and aborting")
                self.unit_types = { UnitType() }   
                
        except (FileNotFoundError, PermissionError) as exc:
            # todo different warning log
            print ("File with unit types definitions missing or unreadable. Loading placeholder unit")
            self.unit_types = { UnitType() }
        return
        
    def load_building_types(self, file_path):
        
        try:
            with open(file_path, 'r') as fi:
                try:
                    data = json.load(fi)
                except json.JSONDecodeError:
                    print ("Invalid JSON within file describing buildings")
                    self.building_types = { Building() }
                    return
            try:
                for item in data["building_types"]:
                    current = Building(
                        name = item["name"],
                        id = item["id"],
                        defence_modifier = item["defence_modifier"],
                        income_modifier = item["income_modifier"],
                        symbol = item["symbol"],
                        symbol_code = item["symbol_code"]
                    )
                    self.building_types[current.id] = current
            except KeyError:
                print ("File with buildings types definitions malformed. Loading placeholder building with id and aborting")
                self.building_types = { Building() }
        except (FileNotFoundError, PermissionError) as exc:
            print ("File with building types definitions missing or unreadable. Loading placeholder building with id0")
            self.building_types = { Building() }
        return
    
    def load_terrain_types(self, file_path):
        
        try:
            with open(file_path, 'r') as fi:                
                try:
                    data = json.load(fi)
                except json.JSONDecodeError:
                    print ("Invalid JSON within file describing terrain")
                    self.terrain_types = { TerrainType() }
                    return
            try:
                # or maybe it should be simply dict from json?
                for item in data["terrain_types"]:
                    current_terrain = TerrainType(
                        name = item["terrain_name"],
                        id = item["id"],
                        defence_modifier = item["defence_modifier"],
                        income_modifier = item["income_modifier"],
                        color = item["color"]
                    )
                    self.terrain_types[current_terrain.id] = current_terrain
            except KeyError:
                print ("File with terrain types definitions malformed.  Loading placeholder terrain with id 0 and aborting")
                self.terrain_types = { TerrainType() }
        
        except (FileNotFoundError, PermissionError) as exc:
            print ("File with terrain types definitions missing or unreadable. Loading placeholder terrain with id0")
            self.terrain_types = { TerrainType() }
        return
                    
    def get_unit_types(self):
        return self.unit_types

    def get_unit_by_id(self, unit_id):
        if unit_id in self.unit_types:
            return self.unit_types[unit_id]
        else:
            return None
    
    def get_building_types(self):
        return self.building_types

    def get_building_by_id(self, b_id):
        if b_id in self.building_types:
            return self.building_types[b_id]
        else:
            return None
        
    def get_terrain_types(self):
        return self.terrain_types
        
    def get_terrain_by_id(self, t_id):
        if t_id in self.terrain_types:
            return self.terrain_types[t_id]
        else:
            return None

