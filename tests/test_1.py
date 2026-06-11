import pytest

from game.unit import UnitType
from game.squad import Squad
from game.player import Player
from game.army import Army
from game.province import Province
from game.terrain import TerrainType

@pytest.fixture
def unit_type():
    return UnitType(
        id_unit_type=1,
        name="Peasants",
        attack_dice=6,
        attack_modifier=1,
        defensive_dice=6,
        defense_modifier=1,
        max_quantity=10,
        price=100
    )


@pytest.fixture
def squad(unit_type):
    return Squad(
        squad_id=1,
        squad_type=unit_type,
        quantity=5
    )


@pytest.fixture
def army(squad):
    squad2 = Squad(
        squad_id=2,
        squad_type=squad.squad_type,
        quantity=3
    )
    
    army = Army()
    army.set_squad(1,squad)
    army.set_squad(2,squad2)
    return army

@pytest.fixture
def army_with_one_squad(squad):
    army = Army()
    army.set_squad(1, squad)
    return army


@pytest.fixture
def player():
    return Player(
        player_id=1,
        nick="Test",
        gold=500
    )


@pytest.fixture
def province(player, army):
    p = Province(province_id=1)
    p.set_player_id(player.player_id)
    p.set_army(army)
    p.set_terrain(0)
    return p


# ====== TESTY ======

# --- Typ jednostki ---

def test_unit_type_getters(unit_type):
    assert unit_type.GetID() == 1
    assert unit_type.GetName() == "Peasants"
    assert unit_type.GetAttackDice() == 6
    assert unit_type.GetAttackModifier() == 1
    assert unit_type.GetDefenseDice() == 6
    assert unit_type.GetDefenseModifier() == 1
    assert unit_type.GetMaxQuantity() == 10
    assert unit_type.GetPrice() == 100
    assert unit_type.GetMaxOffensiveRoll() == 7
    assert unit_type.GetMinOffensiveRoll() == 2
    assert unit_type.GetMaxDefensiveRoll() == 7
    assert unit_type.GetMinDefensiveRoll() == 2


# --- Oddział ---

def test_squad_quantity(squad):
    assert squad.quantity == 5


def test_squad_unit_type(squad, unit_type):
    assert squad.squad_type == unit_type


# --- Armia ---


def test_army_squads_not_none(army):
    assert army.get_squad(1) is not None
    assert army.get_squad(2) is not None

def test_army_with_one_squad_none(army_with_one_squad):
    assert army_with_one_squad.get_squad(1) is not None
    assert army_with_one_squad.get_squad(2) is None

# --- Province ---

def test_province_owner(province, player):
    assert province.player_id == player.player_id


def test_province_army(province, army):
    assert province.army == army

# --- Gra główna ---

def test_main_game_turn_progression():
    game = Main_Game()

    start_turn = game.GetTurn()
    game.NextTurn()

    assert game.GetTurn() == start_turn + 1


def test_main_game_phase_change():
    game = Main_Game()

    start_phase = game.GetPhase()
    game.NextPhase()

    assert game.GetPhase() != start_phase


# --- Ruch jednostki ---

def test_move_unit_changes_position():
    game = Main_Game()

    from_province = 0
    to_province = 1

    result = game.Move( from_province, to_province)

    assert result == 1
    assert game.GetUnitPosition( unit_id ) == to_province


# --- Atak ---

def test_attack_result():
    game = Main_Game()

    from_province = 0
    to_province = 1

    result = game.Attack( from_province, to_province )

    assert result == 1


# --- AI stuff ---

def test_get_squad_mean(squad):

    if squad == None:
        assert 0
    
    squadType = squad.GetUnitType()
    attackDice = squadType.GetAttackDice()
    count = squad.GetQuantity()
    maxRoll = squadType.GetMaxAttackRoll()
    minRoll = squadType.GetMinAttackRoll()
    modifier = squadType.GetAttackModifier()

    mean = ((max(1 + modifier, minRoll) + min(attackDice + modifier, maxRoll))/2)*count #wzorek

    assert mean == 20

def test_get_army_mean(army):
    if army == None:
        assert 0

    squadOne = army.GetFirstSquad()
    squadTwo = army.GetSecondSquad()
    count = army.getSquadCount()

    mean = (squadOne.GetSquadMean() + squadTwo.GetSquadMean()) / count

    assert mean == 20

def test_get_army_defence(province):

    defenderArmy = province.GetArmy()
    provinceModifier = province.GetModifier()
    building = province.GetBuilding()

    if building == None:
        buildingModifier = 0
    else:
        buildingModifier = building.GetModifier()
    
    armyCount = defenderArmy.GetSquadCount()
    squadOne = defenderArmy.GetFirstSquad()
    squadTwo = defenderArmy.GetSecondSquad()

    firstSquadType = squadOne.GetUnitType()
    secondSquadType = squadTwo.GetUnitType()

    firstDefenceDice = firstSquadType.GetDefenceDice()
    firstCount = squadOne.GetQuantity()
    firstMaxRoll = firstSquadType.GetMaxDefenceRoll()
    firstMinRoll = firstSquadType.GetMinDefenceRoll()
    
    secondDefenceDice = secondSquadType.GetDefenceDice()
    secondCount = squadTwo.GetQuantity()
    secondMaxRoll = secondSquadType.GetMaxDefenceRoll()
    secondMinRoll = secondSquadType.GetMinDefenceRoll()    


    modifier = provinceModifier + buildingModifier

    meanSquadOne = ((max(1 + modifier, firstMinRoll) + min(firstDefenceDice + modifier, firstMaxRoll))/2)*firstCount 
    meanSqudTwo = ((max(1 + modifier, secondMinRoll) + min(secondDefenceDice + modifier, secondMaxRoll))/2)*secondCount 

    mean = (meanSquadOne + meanSqudTwo)/armyCount

    assert mean == 20
