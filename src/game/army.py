
from game.squad import Squad
from game.squad_type import SquadType

class Army:

    def __init__(self):
        self.first_squad = None
        self.second_squad = None

    def check_can_buy_unit(self, squad_type):
        if self.first_squad == None :
            return True
        
        if self.second_squad == None :
            return True
        
        if self.first_squad.squad_type == squad_type and self.first_squad.quantity < squad_type.max_quantity :
            return True
        
        if self.second_squad.squad_type == squad_type and self.second_squad.quantity < squad_type.max_quantity :
            return True
        
        return False
    
    def buy_unit(self, squad_type):
        if self.first_squad.squad_type == squad_type and self.first_squad.quantity < squad_type.max_quantity :
            self.first_squad.quantity = self.first_squad.quantity + 1
        
        if self.second_squad.squad_type == squad_type and self.second_squad.quantity < squad_type.max_quantity :
            self.second_squad.quantity = self.second_squad.quantity + 1
        
        if self.first_squad == None :
            self.first_squad = Squad(0,squad_type,1)
        
        if self.second_squad == None :
            self.second_squad = Squad(0,squad_type,1)
        
        return False

    def get_squad(self, squad_id ):

        if self.first_squad.squad_id == squad_id:
            return self.first_squad
        elif self.second_squad.squad_id == squad_id:
            return self.second_squad