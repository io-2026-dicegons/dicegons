import pytest

from game.army import Army
from game.unit import UnitType

@pytest.fixture
def unit_a():
    return UnitType(
        id_unit_type = 1,
        name = "Unit A",
        attack_dice = 6,
        attack_modifier = 0,
        defensive_dice = 6,
        defense_modifier = 0,
        max_quantity = 5,
        price = 2
    )

@pytest.fixture
def unit_b():
    return UnitType(
        id_unit_type = 2,
        name = "Unit B",
        attack_dice = 3,
        attack_modifier = 0,
        defensive_dice = 3,
        defense_modifier = 0,
        max_quantity = 1,
        price = 3
    )

@pytest.fixture
def unit_c():
    return UnitType(
        id_unit_type = 3,
        name = "Unit C",
        attack_dice = 3,
        attack_modifier = 0,
        defensive_dice = 3,
        defense_modifier = 0,
        max_quantity = 2,
        price = 3
    )

def test_initial_army_creation():
    empty_army = Army()
    
    assert None == empty_army.get_squad(1)
    assert None == empty_army.get_squad(2)
    
    
def test_buy_unit(unit_a):
    simple_army = Army()
    
    example_unit_type = unit_a
    assert True == simple_army.check_can_buy_unit(example_unit_type)
    assert True == simple_army.buy_unit(example_unit_type.id_unit_type, example_unit_type)
    
    first_squad = simple_army.get_squad(1)
    assert None != first_squad
    assert first_squad.quantity == 1
    assert first_squad.squad_type == 1
    assert None == simple_army.get_squad(2)
    
    
def test_buy_same_unit_twice(unit_a):
    simple_army = Army()    
    assert True == simple_army.check_can_buy_unit(unit_a)
    assert True == simple_army.buy_unit(unit_a.id_unit_type, unit_a)
    assert True == simple_army.check_can_buy_unit(unit_a)
    assert True == simple_army.buy_unit(unit_a.id_unit_type, unit_a)
    
    first_squad = simple_army.get_squad(1)
    assert None != first_squad
    assert first_squad.quantity == 2
    assert first_squad.squad_type == 1
    assert None == simple_army.get_squad(2)


def test_buy_different_units(unit_a, unit_b):
    simple_army = Army()
    assert True == simple_army.check_can_buy_unit(unit_b)
    assert True == simple_army.buy_unit(unit_b.id_unit_type, unit_b)
    assert True == simple_army.check_can_buy_unit(unit_a)
    assert True == simple_army.buy_unit(unit_a.id_unit_type, unit_a)

    first_squad = simple_army.get_squad(1)
    assert None != first_squad
    assert first_squad.quantity == 1
    assert first_squad.squad_type == 2
    second_squad = simple_army.get_squad(2)
    assert None != second_squad
    assert second_squad.squad_type == 1
    assert second_squad.quantity == 1
    
def test_buy_over_limit(unit_a, unit_b, unit_c):
    simple_army = Army()
    assert True == simple_army.check_can_buy_unit(unit_b)
    assert True == simple_army.buy_unit(unit_b.id_unit_type, unit_b)
    assert True == simple_army.check_can_buy_unit(unit_a)
    assert True == simple_army.buy_unit(unit_a.id_unit_type, unit_a)
    
    assert False == simple_army.check_can_buy_unit(unit_b)
    assert False == simple_army.buy_unit(unit_b.id_unit_type, unit_b)

    
    
def test_try_buying_3rd_type_of_unit_in_the_army(unit_a, unit_b, unit_c):
    simple_army = Army()    
    assert True == simple_army.check_can_buy_unit(unit_a)
    assert True == simple_army.buy_unit(unit_a.id_unit_type, unit_a)
    
    assert True == simple_army.check_can_buy_unit(unit_b)
    assert True == simple_army.buy_unit(unit_b.id_unit_type, unit_b)
    
    
    assert False == simple_army.check_can_buy_unit(unit_c)
    assert False == simple_army.check_can_buy_unit(unit_c)
    
    
