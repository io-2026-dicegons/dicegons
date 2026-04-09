import pytest

@pytest.fixture
def unit_type():
    return UnitType(
        ID_Typu_Jednostki=1,
        name="Peasants",
        Atak_Kostka=6,
        Atak_Modifier=1,
        Obrona_Kostka=6,
        Obrona_Modifier=1,
        Max_Stos=10,
        Price=100
    )


@pytest.fixture
def squad(unit_type):
    return Squad(
        ID_Squad=1,
        Aktualna_Liczba=5,
        ID_Typu_Jednostki=unit_type
    )


@pytest.fixture
def army(squad):
    squad2 = Squad(
        ID_Squad=2,
        Aktualna_Liczba=3,
        ID_Typu_Jednostki=squad.GetUnitType()
    )
    return Army(
        ID_Squad=1,
        ID_Squad_1=squad,
        ID_Squad_2=squad2
    )

@pytest.fixture
def army_with_one_squad(squad):
    return Army(
        ID_Squad=1,
        ID_Squad_1=squad,
        ID_Squad_2=None
    )


@pytest.fixture
def player():
    return Player(
        ID_Player=1,
        Nick="Test",
        Gold=500
    )


@pytest.fixture
def province(player, army):
    return Province(
        ID_Prowincji=1,
        ID_Player=player,
        ID_Army=army,
        ID_Terenu=Teren("Plains", 0),
        Budynki=[],
        Sąsiedzi=[],
        Hex=[]
    )


# ====== TESTY ======

# --- Typ jednostki ---

def test_unit_type_getters(unit_type):
    assert unit_type.GetID() == 1
    assert unit_type.GetName() == "Peasants"
    assert unit_type.GetAttackDice() == 6
    assert unit_type.GetAttackModyfire() == 1
    assert unit_type.GetDefenseDice() == 6
    assert unit_type.GetDefenseModyfire() == 1
    assert unit_type.GetMaxQuantity() == 10
    assert unit_type.GetPrice() == 100
    assert unit_type.GetMaxRoll() == 6
    assert unit_type.GetMinRoll() == 1


# --- Oddział ---

def test_squad_quantity(squad):
    assert squad.GetQuantity() == 5


def test_squad_unit_type(squad, unit_type):
    assert squad.GetUnitType() == unit_type


# --- Armia ---

def test_army_squad_count(army):
    assert army.GetSquadCount() == 2


def test_army_squads_not_none(army):
    assert army.GetFirstSquad() is not None
    assert army.GetSecondSquad() is not None

def test_army_with_one_squad_count(army_with_one_squad):
    assert army_with_one_squad.GetSquadCount() == 1


def test_army_with_one_squad_none(army_with_one_squad):
    assert army_with_one_squad.GetFirstSquad() is not None
    assert army_with_one_squad.GetSecondSquad() is None

# --- Province ---

def test_province_owner(province, player):
    assert province.GetOwner() == player


def test_province_army(province, army):
    assert province.GetArmy() == army

def test_get_building_modifier(province):
    building = province.getBuilding()
    
    assert building.getBuildingModifier() == 0

def test_get_terrain_modifier(province):
    terrain = province.getTerrain()

    assert terrain.getTerrainModifier() == 1



def test_province_hex_list(province):
    assert isinstance(province.GetHexesList(), list)


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
