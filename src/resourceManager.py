from pathlib import Path
import json 

from terrain import TerrainType
from building import Building

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
        self.load_unit_types(Path("terrain_types.json"))

        return

    def load_unit_types(self, file_path):
        pass
        
    def load_building_types(self, file_path):
        
        with open(file_path, 'r') as fi:
            data = json.load(fi)
        
        try:
            for item in data["building_types"]:
                current = Building(
                    name = item["name"],
                    id = item["id"],
                    defence_modifier = item["defence_modifier"],
                    income_modifier = item["income_modifier"]
                )
                self.building_types[current.id] = current
        except KeyError:
            self.building_types = { Building() }        
        pass
    
    def load_terrain_types(self, file_path):
        with open(file_path, 'r') as fi:
            data = json.load(fi)
        
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
            self.terrain_types = { TerrainType() }
        
        return
                    
    def get_unit_types(self):
        return self.unit_types

    def get_unit_by_id(self, unit_id):
        if unit_id in self.unit_types:
            return self.unit_types[unit_id]
        #else:
            #return UnitType()
        pass
    
    def get_building_types(self):
        return self.building_types

    def get_building_by_id(self, b_id):
        if b_id in self.building_types:
            return self.building_types[b_id]
        else:
            return Building()
        
    def get_terrain_types(self):
        return self.terrain_types
        
    def get_terrain_by_id(self, t_id):
        if t_id in self.terrain_types:
            return self.terrain_types[t_id]
        else:
            # should we raise hell?
            # for now returns default terrain
            defafult_terrain = TerrainType()
            return defafult_terrain

