
BUYING_PHASE = 0
ATTACK_PHASE = 1
MOVEMENT_PHASE = 2
LAST_PHASE = 3

class Turn:

    def __init__(self, number_of_players=0):
        self.turn_number = 1
        self.turn_player = 0
        self.number_of_players = number_of_players
        self.turn_phase = 0

    #zwraca czy jest następna tura
    def next_phase(self):
        self.turn_phase = self.turn_phase + 1

        if self.turn_phase == LAST_PHASE:
            self.turn_player = self.turn_player + 1

            if self.turn_player == self.number_of_players:
                self.turn_number = self.turn_number + 1
                return True
        return False
    
    def get_current_player(self):
        return self.turn_player
    
    def get_phase(self):
        return self.turn_phase