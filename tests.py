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
    print("Testing utility methods")
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
    print("Passed!")

def test_combatant():
    print("Testing Combatant")

    t0 = combatant.Combatant(ac=12, max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                             proficiencies=["dexterity", "charisma"], proficiency_mod=2, name='t0')
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
    assert(t0.get_proficiencies() == ["dexterity", "charisma"])
    assert(t0.get_proficiency_mod() == 2)
    assert(t0.get_saving_throw("strength") == 2)
    assert (t0.get_saving_throw("dexterity") == 5)
    assert (t0.get_saving_throw("constitution") == -1)
    assert (t0.get_saving_throw("intelligence") == 1)
    assert (t0.get_saving_throw("wisdom") == 0)
    assert (t0.get_saving_throw("charisma") == 1)
    assert(not t0.get_features())
    assert(not t0.get_death_saves())
    assert(not t0.get_conditions())
    assert(not t0.get_weapons())
    assert(not t0.get_items())

    t10 = combatant.Combatant(copy=t0, name="t10")
    assert(t10.get_name() == 't10')
    assert(t10.get_ac() == 12)
    assert(t10.get_max_hp() == 20)
    assert(t10.get_current_hp() == 20)
    assert(t10.get_temp_hp() == 2)
    assert(t10.get_hit_dice() == (3, 6))
    assert(t10.get_speed() == 20)
    assert(t10.get_vision() == 'darkvision')
    assert(t10.get_strength() == 2)
    assert(t10.get_dexterity() == 3)
    assert(t10.get_constitution() == -1)
    assert(t10.get_intelligence() == 1)
    assert(t10.get_wisdom() == 0)
    assert(t10.get_charisma() == -1)
    assert(t10.get_proficiencies() == ["dexterity", "charisma"])
    assert(t10.get_proficiency_mod() == 2)
    assert(t10.get_saving_throw("strength") == 2)
    assert(t10.get_saving_throw("dexterity") == 5)
    assert(t10.get_saving_throw("constitution") == -1)
    assert(t10.get_saving_throw("intelligence") == 1)
    assert(t10.get_saving_throw("wisdom") == 0)
    assert(t10.get_saving_throw("charisma") == 1)
    assert(not t10.get_features())
    assert(not t10.get_death_saves())
    assert(not t10.get_conditions())
    assert(not t10.get_weapons())
    assert(not t10.get_items())
    assert(t10 is not t0)

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
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="t2")
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
    print("Passed!")

def test_creature():
    print("Testing Creature")
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

    c1 = combatant.Creature(copy=c0, name="c1")
    assert(c1.get_name() == "c1")
    assert(c1.get_max_hp() == 70)  # just check a stat lol
    assert(c1.get_cr() == 1/4)
    assert(c1.get_xp() == 50)
    assert(c0 is not c1)

    t2 = combatant.Combatant(ac=18, max_hp=30, current_hp=5, temp_hp=2, hit_dice='1d4', speed=20, vision='normal',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                             name="t2")
    c2 = combatant.Creature(copy=t2, name="c2", cr=1, xp=200)
    assert(c2.get_name() == "c2")
    assert(c2.get_ac() == 18)
    assert(c2.get_cr() == 1)
    assert(c2.get_xp() == 200)
    assert(c2 is not c0)

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
    print("Passed!")

def test_character():
    print("Testing Character")

    c0 = combatant.Character(ac=18, max_hp=70, current_hp=60, temp_hp=2, hit_dice='4d10', speed=30, vision='normal',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name="c0",
                            level=5)
    assert(c0.get_level() == 5)

    c1 = combatant.Character(copy=c0, name="c1")
    assert(c1.get_name() == "c1")
    assert(c1.get_temp_hp() == 2)
    assert(c1.get_level() == 5)
    assert(c1 is not c0)

    t0 = combatant.Combatant(ac=12, max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                             name='t0')

    c2 = combatant.Character(copy=t0, level=2, name="c2")
    assert(c2.get_name() == "c2")
    assert(c2.get_vision() == "darkvision")
    assert(c2.get_level() == 2)
    assert(c2 is not t0)

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
    print("Passed!")

def test_weapon():
    print("Testing Weapon")

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

    dagger = weapons.Weapon(finesse=1, light=1, range=(20, 60), melee_range=5, name="dagger", damage_dice=(1, 4),
                            hit_bonus=2, damage_bonus=1, damage_type="piercing")
    assert(dagger.get_name() == "dagger")
    props = dagger.get_properties()
    assert("finesse" in props)
    assert(dagger.has_prop("light"))
    assert(dagger.has_prop("range"))
    assert(dagger.get_range() == (20, 60))
    assert(dagger.has_prop("melee"))
    assert(dagger.get_melee_range() == 5)
    assert(dagger.get_damage_dice() == (1, 4))
    assert(not dagger.has_prop("heavy"))
    assert(not dagger.has_prop("load"))
    assert(not dagger.has_prop("reach"))
    assert(not dagger.has_prop("two_handed"))
    assert(not dagger.has_prop("versatile"))
    assert(dagger.get_hit_bonus() == 2)
    assert(dagger.get_damage_bonus() == 1)
    assert(dagger.get_damage_type() == "piercing")

    dagger_2 = weapons.Weapon(copy=dagger, name="dagger_2")
    assert(dagger_2.get_name() == "dagger_2")
    props = dagger_2.get_properties()
    assert("finesse" in props)
    assert(dagger_2.has_prop("light"))
    assert(dagger_2.has_prop("range"))
    assert(dagger_2.get_range() == (20, 60))
    assert(dagger_2.has_prop("melee"))
    assert(dagger_2.get_melee_range() == 5)
    assert(dagger_2.get_damage_dice() == (1, 4))
    assert(not dagger_2.has_prop("heavy"))
    assert(not dagger_2.has_prop("load"))
    assert(not dagger_2.has_prop("reach"))
    assert(not dagger_2.has_prop("two_handed"))
    assert(not dagger_2.has_prop("versatile"))
    assert(dagger_2.get_hit_bonus() == 2)
    assert(dagger_2.get_damage_bonus() == 1)
    assert(dagger_2.get_damage_type() == "piercing")
    assert(dagger is not dagger_2)  # make sure they aren't the same object

    t0 = combatant.Combatant(ac=12, max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                             name='t0')

    t0.add_weapon(dagger)
    assert(t0.get_weapons() == [dagger])
    assert(dagger.get_owner() is t0)

    t1 = combatant.Combatant(copy=t0, name="t1")
    assert(len(t1.get_weapons()) == 1)
    dagger_3 = t1.get_weapons()[0]
    assert (dagger_3.get_name() == "dagger")
    props = dagger_3.get_properties()
    assert ("finesse" in props)
    assert (dagger_3.has_prop("light"))
    assert (dagger_3.has_prop("range"))
    assert (dagger_3.get_range() == (20, 60))
    assert (dagger_3.has_prop("melee"))
    assert (dagger_3.get_melee_range() == 5)
    assert (dagger_3.get_damage_dice() == (1, 4))
    assert (not dagger_3.has_prop("heavy"))
    assert (not dagger_3.has_prop("load"))
    assert (not dagger_3.has_prop("reach"))
    assert (not dagger_3.has_prop("two_handed"))
    assert (not dagger_3.has_prop("versatile"))
    assert (dagger_3.get_hit_bonus() == 2)
    assert (dagger_3.get_damage_bonus() == 1)
    assert (dagger_3.get_damage_type() == "piercing")
    assert (dagger is not dagger_3)

    try:
        t0.add_weapon('stuff')
        raise Exception("Add weapon succeeded for non-weapon")
    except ValueError:
        pass

    print("Passed!")

def test_attack():
    print("Testing Attack")

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

    a0 = attack_class.Attack(damage_dice=(1, 8), attack_mod=5, damage_mod=2, damage_type="piercing", range=120, adv=-1,
                             melee_range=10, name="a0")
    assert(a0.get_damage_dice() == (1, 8))
    assert(a0.get_attack_mod() == 5)
    assert(a0.get_damage_mod() == 2)
    assert(a0.get_damage_type() == "piercing")
    assert(a0.get_range() == 120)
    assert(a0.get_melee_range() == 10)
    assert(a0.get_adv() == -1)
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

    dagger = weapons.Weapon(finesse=1, light=1, range=(20, 60), melee_range=5, name="dagger", damage_dice=(1, 4),
                            hit_bonus=2, damage_bonus=1, damage_type="piercing")  # cool damage thing

    t0 = combatant.Combatant(ac=12, max_hp=40, current_hp=40, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                             name='t0')

    t0.add_weapon(dagger)
    assert(dagger in t0.get_weapons())
    assert(dagger.get_owner() is t0)

    assert(len(t0.get_attacks()) == 3)  # melee and two ranged

    dagger_attacks = t0.get_attacks()

    dagger_attack = dagger_attacks[0]
    assert(dagger_attack.get_name() == "dagger_range")
    assert(dagger_attack.get_weapon() is dagger)
    assert(dagger_attack.get_damage_dice() == (1, 4))
    assert(dagger_attack.get_damage_type() == "piercing")
    assert(dagger_attack.get_attack_mod() == 5)  # 3 + 2
    assert(dagger_attack.get_damage_mod() == 4)  # 3 + 1
    assert(dagger_attack.get_range() == 20)
    assert(dagger_attack.get_melee_range() == 0)
    assert(dagger_attack.get_adv() == 0)

    dagger_attack = dagger_attacks[1]
    assert(dagger_attack.get_name() == "dagger_range_disadvantage")
    assert(dagger_attack.get_damage_dice() == (1, 4))
    assert(dagger_attack.get_damage_type() == "piercing")
    assert(dagger_attack.get_attack_mod() == 5)
    assert(dagger_attack.get_damage_mod() == 4)
    assert(dagger_attack.get_range() == 60)
    assert(dagger_attack.get_melee_range() == 0)
    assert(dagger_attack.get_adv() == -1)

    dagger_attack = dagger_attacks[2]
    assert(dagger_attack.get_name() == "dagger_melee")
    assert(dagger_attack.get_damage_dice() == (1, 4))
    assert(dagger_attack.get_damage_type() == "piercing")
    assert(dagger_attack.get_attack_mod() == 5)
    assert(dagger_attack.get_damage_mod() == 4)
    assert(dagger_attack.get_range() == 0)
    assert(dagger_attack.get_melee_range() == 5)
    assert(dagger_attack.get_adv() == 0)

    t0.remove_weapon_attacks(dagger)
    assert(len(t0.get_attacks()) == 0)
    
    t0.add_weapon_attacks(dagger)
    dagger.set_name("stabby")
    dagger_attacks = t0.get_attacks()
    assert(dagger_attacks[0].get_name() == "stabby_range")
    assert(dagger_attacks[1].get_name() == "stabby_range_disadvantage")
    assert(dagger_attacks[2].get_name() == "stabby_melee")

    t0.remove_weapon(dagger)
    assert(len(t0.get_weapons()) == 0)
    assert(len(t0.get_attacks()) == 0)

    dagger.set_name("dagger")

    mace = weapons.Weapon(name="mace", damage_dice=(1, 6), damage_type="bludgeoning")
    assert(mace.get_melee_range() == 5)

    t0.add_weapon(dagger)
    t0.add_weapon(mace)

    assert(len(t0.get_attacks()) == 4)
    t0.remove_weapon(mace)
    assert(len(t0.get_attacks()) == 3)

    attack_names = [attack.get_name() for attack in t0.get_attacks()]
    assert(attack_names[0] == "dagger_range")
    assert(attack_names[1] == "dagger_range_disadvantage")
    assert(attack_names[2] == "dagger_melee")

    t0.add_weapon(mace)
    t0.remove_weapon(dagger)
    assert(len(t0.get_attacks()) == 1)
    assert(t0.get_attacks()[0].get_name() == "mace_melee")
    t0.add_weapon(dagger)

    t0.remove_all_weapons()
    assert(len(t0.get_weapons()) == 0)
    assert(len(t0.get_attacks()) == 0)

    dagger.set_hit_bonus(0)
    dagger.set_damage_bonus(0)

    t0.add_weapon(dagger)
    t1 = combatant.Combatant(ac=10, max_hp=40, current_hp=40, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                             strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8,
                             name='t1')  # almost identical to t0, but easier to hit
    t1.add_weapon(mace)

    dagger_melee = t0.get_attacks()[2]
    mace_melee = t1.get_attacks()[0]

    t0.set_verbose(True)
    t1.set_verbose(True)

    for i in range(15):
        t0.send_attack(t1, dagger_melee)
        if t1.has_condition("unconscious") or t1.has_condition("dead"):
            break
        t1.send_attack(t0, mace_melee)
        if t0.has_condition("unconscious") or t0.has_condition("dead"):
            break

    t0.set_verbose(False)
    t1.set_verbose(False)

    print("Passed!")

test_combatant()
# test_attack()
