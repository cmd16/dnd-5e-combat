import combatant
import weapons

t0 = combatant.Combatant(ac=12, max_hp=20, current_hp=20, temp_hp=2, hit_dice='3d6', speed=20, vision='darkvision',
                         strength=14, dexterity=16, constitution=9, intelligence=12, wisdom=11, charisma=8, name='t0')
assert(t0._name == 't0')
assert(t0._ac == 12)
assert(t0._max_hp == 20)
assert(t0._current_hp == 20)
assert(t0._temp_hp == 2)
assert(t0._hit_dice == '3d6')
assert(t0._speed == 20)
assert(t0._vision == 'darkvision')
assert(t0._strength == 2)
assert(t0._dexterity == 3)
assert(t0._constitution == -1)
assert(t0._intelligence == 1)
assert(t0._wisdom == 0)
assert(t0._charisma == -1)
assert(not t0._proficiencies)
assert(not t0._features)
assert(not t0._death_saves)
assert(not t0._conditions)
assert(not t0._weapons)
assert(not t0._items)
assert(not t0._spells)
assert(not t0._spell_slots)

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
assert(dagger._name == "dagger")
assert(dagger._finesse)
assert(dagger._light)
assert(dagger._range == "20/60")
assert(dagger._melee_range == 5)
assert(dagger._damage_dice == "1d4")
assert(not dagger._heavy)
assert(not dagger._load)
assert(not dagger._reach)
assert(not dagger._two_handed)
assert(not dagger._versatile)

t0.add_weapon(dagger)
assert(t0._weapons == [dagger])
assert(dagger._owner == t0)

try:
    t0.add_weapon('stuff')
    raise Exception("Add weapon succeeded for non-weapon")
except ValueError:
    pass
