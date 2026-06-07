   
class UnitType:
    def __init__(self, id_unit_type=0, name="Placeholder", attack_dice=0, attack_modifier=0, defensive_dice=0, 
    defense_modifier=0, max_quantity=1, price =0, max_defensive_result = None, 
    min_defensive_result  = None, max_offensive_result  = None, min_offensive_result = None,
    symbol = None, symbol_code = 0):
        self.id_unit_type = id_unit_type
        self.name = name
        self.attack_dice = attack_dice
        self.attack_modifier = attack_modifier
        self.defensive_dice = defensive_dice
        self.defense_modifier = defense_modifier
        self.max_quantity = max_quantity
        self.price = price
        self.max_defensive_result = max_defensive_result
        self.min_defensive_result = min_defensive_result
        self.max_offensive_result = max_offensive_result
        self.min_offensive_result = min_offensive_result
        if self.max_defensive_result is None:
            self.max_defensive_result = self.defensive_dice + self.defense_modifier
        if self.max_offensive_result is None:
            self.max_offensive_result = self.attack_dice + self.attack_modifier            
        if self.min_defensive_result is None:
            self.min_defensive_result = 1 + self.defense_modifier
        if self.min_offensive_result is None:
            self.min_offensive_result = 1 + self.attack_modifier
        self.symbol = symbol
        self.symbol_code = symbol_code

    # consider change: GetID->get_id:
    def GetID(self):        
        return self.id_unit_type

    def GetName(self):
        return self.name

    def GetAttackDice(self):
        return self.attack_dice

    def GetAttackModifier(self):
        return self.attack_modifier

    def GetDefenseDice(self):
        return self.defensive_dice

    def GetDefenseModifier(self):
        return self.defense_modifier

    def GetMaxQuantity(self):
        return self.max_quantity

    def GetPrice(self):
        return self.price
        
    def GetMaxOffensiveRoll(self):
        return self.max_offensive_result
        
    def GetMinOffensiveRoll(self):
        return self.min_offensive_result

    def GetMaxDefensiveRoll(self):
        return self.max_defensive_result
        
    def GetMinDefensiveRoll(self):
        return self.min_defensive_result
