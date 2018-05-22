import combatant
import weapons

t0 = combatant.Combatant(ac=12, max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                         strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name='t0')
assert(t0.get_name() == 't0')
assert(t0.get_ac() == 12)
assert(t0.get_max_hp() == 20)
assert(t0.get_current_hp() == 20)
assert(t0.get_temp_hp() == 2)
assert(t0.get_hit_dice() == '3d6')
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
    weapon = weapons.Weapon(name='weapon')
    raise Exception("Create weapon succeeded without damage dice")
except ValueError:
    pass

try:
    weapon = weapons.Weapon(damage_dice='1d4')
    raise Exception("Create weapon succeeded without name")
except ValueError:
    pass

dagger = weapons.Weapon(finesse=1, light=1, range="20/60", melee_range=5, name="dagger", damage_dice="1d4")
assert(dagger.get_name() == "dagger")
props = dagger.get_properties()
assert("finesse" in props)
assert("light" in props)
assert("range" in props)
assert(dagger.get_range() == "20/60")
assert("melee" in props)
assert(dagger.get_melee_range() == 5)
assert(dagger.get_damage_dice() == "1d4")
assert("heavy" not in props)
assert("load" not in props)
assert("reach" not in props)
assert("two_handed" not in props)
assert("versatile" not in props)

t0.add_weapon(dagger)
assert(t0.get_weapons() == [dagger])
assert(dagger.get_owner() == t0)

try:
    t0.add_weapon('stuff')
    raise Exception("Add weapon succeeded for non-weapon")
except ValueError:
    pass
