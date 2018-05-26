import combatant
import weapons
import attack_class
from utility_methods_dnd import ability_to_mod, validate_dice
from nltk import FreqDist

def test_all():
    test_utility()
    test_combatant()
    test_creature()
    test_character()
    test_weapon()
    test_attack()

def test_utility():
    # testing utility methods
    try:
        ability_to_mod(-5)
        raise Exception("Allowed low ability score")
    except ValueError:
        pass

    try:
        ability_to_mod(70)
        raise Exception("Allowed high ability score")
    except ValueError:
        pass

    try:
        validate_dice(5.2)
    except ValueError:
        pass

    try:
        validate_dice((1, 2, 3))
        raise Exception("Allowed list of len != 2")
    except ValueError:
        pass

    try:
        validate_dice(("a", "b"))
        raise Exception("Allowed list of non-integers")
    except ValueError:
        pass

    try:
        validate_dice(("xdz"))
        raise Exception("Allowed dice with non-integers in string")
    except ValueError:
        pass

    try:
        validate_dice(("1d4d20"))
        raise Exception("Allowed dice with multiple d in string")
    except ValueError:
        pass

    assert(validate_dice((2, 3)) == (2, 3))
    assert(validate_dice("3d4") == (3, 4))

def test_combatant():
    # testing Combatant construction

    t0 = combatant.Combatant(ac=12, max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name='t0')
    assert(t0.get_name() == 't0')
    assert(t0.get_ac() == 12)
    assert(t0.get_max_hp() == 20)
    assert(t0.get_current_hp() == 20)
    assert(t0.get_temp_hp() == 2)
    assert(t0.get_hit_dice() == (3, 6))
    assert(t0.get_speed() == 20)
    assert(t0.get_vision() == 'darkvision')
    assert(t0.get_strength() == 2)
    assert(t0.get_dexterity() == 3)
    assert(t0.get_constitution() == -1)
    assert(t0.get_intelligence() == 1)
    assert(t0.get_wisdom() == 0)
    assert(t0.get_charisma() == -1)
    assert(not t0.get_proficiencies())
    assert(not t0.get_features())
    assert(not t0.get_death_saves())
    assert(not t0.get_conditions())
    assert(not t0.get_weapons())
    assert(not t0.get_items())
    assert(not t0.get_spells())
    assert(not t0.get_spell_slots())

    try:
        t1 = combatant.Combatant(name="bob")
        raise Exception("Create combatant succeeded without ability scores")
    except ValueError:
        pass

    try:
        t1 = combatant.Combatant(max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="t1")
        raise Exception("Create combatant succeeded without AC")
    except ValueError:
        pass

    try:
        t1 = combatant.Combatant(ac="10", max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="t1")
        raise Exception("Create combatant succeeded with non-integer AC")
    except ValueError:
        pass

    try:
        t1 = combatant.Combatant(max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, conditions="dog",
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="t1")
        raise Exception("Create combatant succeeded with non-list conditions")
    except ValueError:
        pass

    try:
        t1 = combatant.Combatant(ac=18, current_hp=5, temp_hp=2, hit_dice='1d4', speed=20, vision='blindsight',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="t1")
        raise Exception("Create combatant succeeded without max hp")
    except ValueError:
        pass

    try:
        t1 = combatant.Combatant(ac=18, max_hp=30, current_hp=35, temp_hp=2, hit_dice='1d4', speed=20, vision='blindsight',
                                 strength=9, dexterity=10, constitution=9, intelligence=12, wisdom=11, charisma=8,
                                 name="t1")
        raise Exception("Create combatant succeeded with current hp greater than max hp")
    except ValueError:
        pass

    t1 = combatant.Combatant(ac=18, max_hp=30, current_hp=-5, temp_hp=2, hit_dice='1d4', speed=20, vision='blindsight',
                                 strength=9, dexterity=10, constitution=9, intelligence=12, wisdom=11, charisma=8,
                                 name="t1")  # should give warning that combatant was created unconscious

    try:
        t1 = combatant.Combatant(ac=18, max_hp=30, current_hp=5, temp_hp=2, hit_dice='1d4', speed=20, vision='blindsight',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8)
        raise Exception("Create combatant succeeded without name")
    except ValueError:
        pass

    try:
        t1 = combatant.Combatant(ac=18, max_hp=30, current_hp=5, temp_hp=2, hit_dice='1d4', speed=20, vision='blindsight',
                             strength=-1, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="t1")
        raise Exception("Create combatant succeeded with low ability score")
    except ValueError:
        pass

    try:
        t1 = combatant.Combatant(ac=18, max_hp=30, current_hp=5, temp_hp=2, hit_dice='1d4', speed=20, vision='blindsight',
                             strength=7, dexterity=50, constitution=9, intelligence=12, wisdom=11, charisma=8, name="t1")
        raise Exception("Create combatant succeeded with high ability score")
    except ValueError:
        pass

    # testing Combatant vision

    t2 = combatant.Combatant(ac=18, max_hp=30, current_hp=5, temp_hp=2, hit_dice='1d4', speed=20, vision='normal',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="t1")
    assert(t2.can_see("normal"))
    assert(not t2.can_see("dark"))
    assert(not t2.can_see("magic"))
    t2.add_condition("blinded")
    assert(not t2.can_see("normal"))
    assert(not t2.can_see("dark"))
    assert(not t2.can_see("magic"))
    t2.remove_condition("blinded")
    assert(not t2.has_condition("blinded"))

    t2.change_vision("blindsight")
    assert(t2.can_see("normal"))
    assert(t2.can_see("dark"))
    assert(not t2.can_see("magic"))
    t2.add_condition("blinded")
    assert(t2.can_see("normal"))
    assert(t2.can_see("dark"))
    assert(not t2.can_see("magic"))
    t2.remove_condition("blinded")

    t2.change_vision("darkvision")
    assert(t2.can_see("normal"))
    assert(t2.can_see("dark"))
    assert(not t2.can_see("magic"))
    t2.add_condition("blinded")
    assert(not t2.can_see("normal"))
    assert(not t2.can_see("dark"))
    assert(not t2.can_see("magic"))
    t2.remove_condition("blinded")

    t2.change_vision("truesight")
    assert(t2.can_see("normal"))
    assert(t2.can_see("dark"))
    assert(t2.can_see("magic"))
    t2.add_condition("blinded")
    assert(not t2.can_see("normal"))
    assert(not t2.can_see("dark"))
    assert(not t2.can_see("magic"))
    t2.remove_condition("blinded")

    # testing Combatant damage and healing

    t2.take_damage(1)
    # take less than temp hp
    assert(t2.get_temp_hp() == 1)
    assert(t2.get_current_hp() == 5)
    # take more than temp hp
    t2.take_damage(2)
    assert(t2.get_temp_hp() == 0)
    assert(t2.get_current_hp() == 4)
    # take damage to current hp
    t2.take_damage(2)
    assert(t2.get_temp_hp() == 0)
    assert(t2.get_current_hp() == 2)
    # go unconscious but don't die
    t2.take_damage(10)
    assert(t2.get_temp_hp() == 0)
    assert(t2.get_current_hp() == 0)
    assert(t2.has_condition("unconscious"))
    # heal
    t2.take_healing(20)
    assert(t2.get_current_hp() == 20)
    assert(not t2.has_condition("unconscious"))
    # heal above max
    t2.take_healing(40)
    assert(t2.get_current_hp() == t2.get_max_hp() == 30)
    # die
    t2.take_damage(100)  # suuuper dead.
    assert(t2.get_conditions() == ["dead"])
    assert(t2.get_current_hp() == 0)
    assert(t2.get_temp_hp() == 0)

def test_creature():
    # testing Creature construction
    c0 = combatant.Creature(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="c0",
                            cr=1/2, xp=100)
    assert(c0.get_cr() == 1/2)
    assert(c0.get_xp() == 100)

    c0 = combatant.Creature(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="c0",
                            cr=1/4)
    assert(c0.get_cr() == 1/4)
    assert(c0.get_xp() == 50)

    try:
        c0 = combatant.Creature(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="c0",
                            cr="dog")
        raise Exception("Create Creature succeeded for non-number cr")
    except ValueError:
        pass

    try:
        c0 = combatant.Creature(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="c0",
                            cr=-2)
        raise Exception("Create Creature succeeded for negative cr")
    except ValueError:
        pass

def test_character():
    # testing Character construction

    c0 = combatant.Character(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="c0",
                            level=5)
    assert c0.get_level() == 5

    try:
        c0 = combatant.Character(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                                 strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                                 name="c0",
                                 level=30)
        raise Exception("Create Character succeeded with level too high")
    except ValueError:
        pass

    try:
        c0 = combatant.Character(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                                 strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                                 name="c0",
                                 level=-2)
        raise Exception("Create Character succeeded with level too low")
    except ValueError:
        pass

    try:
        c0 = combatant.Character(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                                 strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                                 name="c0",
                                 level="stuff")
        raise Exception("Create Character succeeded with non-int level")
    except ValueError:
        pass

def test_weapon():
    # testing Weapon construction

    try:
        weapon = weapons.Weapon(name='weapon')
        raise Exception("Create weapon succeeded without damage dice")
    except ValueError:
        pass

    try:
        weapon = weapons.Weapon(damage_dice=(1, 4))
        raise Exception("Create weapon succeeded without name")
    except ValueError:
        pass

    dagger = weapons.Weapon(finesse=1, light=1, range="20/60", melee_range=5, name="dagger", damage_dice=(1, 4),
                            hit_bonus=2, damage_bonus=1)
    assert(dagger.get_name() == "dagger")
    props = dagger.get_properties()
    assert("finesse" in props)
    assert("light" in props)
    assert("range" in props)
    assert(dagger.get_range() == "20/60")
    assert("melee" in props)
    assert(dagger.get_melee_range() == 5)
    assert(dagger.get_damage_dice() == (1, 4))
    assert("heavy" not in props)
    assert("load" not in props)
    assert("reach" not in props)
    assert("two_handed" not in props)
    assert("versatile" not in props)
    assert(dagger.has_prop("finesse"))
    assert(dagger.get_hit_bonus() == 2)
    assert(dagger.get_damage_bonus() == 1)

    t0 = combatant.Combatant(ac=12, max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                             name='t0')

    t0.add_weapon(dagger)
    assert(t0.get_weapons() == [dagger])
    assert(dagger.get_owner() == t0)

    try:
        t0.add_weapon('stuff')
        raise Exception("Add weapon succeeded for non-weapon")
    except ValueError:
        pass

def test_attack():
    # testing Attack construction

    try:
        a0 = attack_class.Attack(damage_dice=(1, 8), attack_mod=5.2)
        raise Exception("Create Attack succeeded with non-int attack mod")
    except ValueError:
        pass

    try:
        a0 = attack_class.Attack(damage_dice=(1, 8), damage_mod=["fail"])
        raise Exception("Create Attack succeeded with non-int damage mod")
    except ValueError:
        pass

    try:
        a0 = attack_class.Attack(damage_dice=(1, 8), name=1)
        raise Exception("Create Attack succeeded with non-string name")
    except ValueError:
        pass

    a0 = attack_class.Attack(damage_dice=(1, 8), attack_mod=5, damage_mod=2, name="a0")
    assert(a0.get_damage_dice() == (1, 8))
    assert(a0.get_attack_mod() == 5)
    assert(a0.get_damage_mod() == 2)
    assert(a0.get_name() == "a0")

    # testing attack rolls. Basically just make FreqDists and look to see if they check out

    # a0 = attack_class.Attack(damage_dice=(1, 8), name="a0")
    #
    # attack_roll_list = []
    # crit_list = []
    # for i in range(10000):
    #     result = a0.roll_attack()
    #     attack_roll_list.append(result[0])
    #     crit_list.append(result[1])
    # attack_roll_freqdist = FreqDist(attack_roll_list)
    # crit_freqdist = FreqDist(crit_list)
    # for key in sorted(attack_roll_freqdist.keys()):
    #     print("%d: %d" % (key, attack_roll_freqdist[key]), end=", ")
    # print()
    # print(crit_freqdist.most_common())

    # testing damage rolls (see above)

    # a1 = attack_class.Attack(damage_dice=(1, 8), damage_mod=1, name="a1")  # also check that modifiers work
    #
    # damage_roll_list = []
    # for i in range(10000):
    #     result = a1.roll_damage()
    #     damage_roll_list.append(result[0])
    # damage_roll_freqdist = FreqDist(damage_roll_list)
    # for key in sorted(damage_roll_freqdist.keys()):
    #     print("%d: %d" % (key, damage_roll_freqdist[key]), end=", ")
    # print()


