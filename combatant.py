"""
ac
max_hp
temp_hp
current_hp
hit_dice
speed
vision - normal, dark, blind, true
strength
dexterity
constitution
intelligence
wisdom
charisma
death_saves
conditions
skill_proficiencies (add later)
spells (add later)
features (add later)
"""
import warnings
import weapons


def ability_to_mod(score):
    if score < 1:
        ValueError("Ability score too low (did you input a modifier?)")
    elif score > 30:
        ValueError("Ability score too high (did you add an extra digit?)")
    return (score -10) // 2

class Combatant:
    def __init__(self, **kwargs):
        self._ac = kwargs.get('ac')
        if not self._ac:
            raise ValueError("Must provide ac")
        self._max_hp = kwargs.get('max_hp')
        if not self._max_hp or self._max_hp <= 0:
            raise ValueError("Must provide positive max hp")
        self._temp_hp = kwargs.get('temp_hp', 0)

        self._conditions = kwargs.get('conditions', [])  # set this first in case current hp makes character unconscious

        self._current_hp = kwargs.get('current_hp', 0)
        if self._current_hp == 0:
            warnings.warn("Combatant created with 0 hp.")
            self.become_unconscious()
        self._hit_dice = kwargs.get('hit_dice')
        self._speed = kwargs.get('speed', 25)
        self._vision = kwargs.get('vision', 'normal')
        if self._vision not in ['normal', 'darkvision', 'blindsight', 'truesight']:
            print("%s not recognized as a valid vision. Setting vision to normal." % self._vision)
            self._vision = "normal"

        strength = kwargs.get('strength')
        if not strength:
            raise ValueError("Must provide strength score")
        self._strength = ability_to_mod(strength)
        dexterity = kwargs.get('dexterity')
        if not dexterity:
            raise ValueError("Must provide dexterity score")
        self._dexterity = ability_to_mod(dexterity)
        constitution = kwargs.get('constitution')
        if not constitution:
            raise ValueError("Must provide constitution score")
        self._constitution = ability_to_mod(constitution)
        intelligence = kwargs.get('intelligence')
        if not intelligence:
            raise ValueError("Must provide intelligence score")
        self._intelligence = ability_to_mod(intelligence)
        wisdom = kwargs.get('wisdom')
        if not wisdom:
            raise ValueError("Must provide wisdom score")
        self._wisdom = ability_to_mod(wisdom)
        charisma = kwargs.get('charisma')
        if not charisma:
            raise ValueError("Must provide charisma score")
        self._charisma = ability_to_mod(charisma)
        self._proficiencies = kwargs.get('proficiencies', {})  # TODO: implement
        self._features = kwargs.get('features', [])  # TODO: implement

        self._death_saves = kwargs.get('death_saves', [])

        self._weapons = kwargs.get('weapons', [])
        self._items = kwargs.get('items', [])  # TODO: implement
        self._spells = kwargs.get('spells', [])  # TODO: implement
        self._spell_slots = kwargs.get('spell_slots', [])

        self._attacks = []
        # for weapon in self._weapons:
        #     self._attacks.extend(weapon.getAttacks())

        self._name = kwargs.get('name')
        if not self._name:
            raise ValueError("Must provide a name")

    def get_ac(self):
        return self._ac

    def get_max_hp(self):
        return self._max_hp

    def get_temp_hp(self):
        return self._temp_hp

    def get_current_hp(self):
        return self._current_hp

    def is_bloodied(self):
        return self._current_hp <= self._max_hp

    def get_hit_dice(self):
        return self._hit_dice

    def get_speed(self):
        return self._speed

    def get_vision(self):
        return self._vision

    def can_see(self, light_src):
        if "blinded" in self._conditions:
            return self._vision == "blindsight" and light_src != "magic"
        if light_src == "normal":
            return True
        if self._vision == "normal":  # normal vision can't see anything better than normal light
            return False
        if light_src == "dark":  # darkvision, blindsight, and truesight can all see in the dark
            return True
        if light_src == "magic":
            return self._vision == "truesight"

    def get_strength(self):
        return self._strength

    def get_dexterity(self):
        return self._dexterity

    def get_constitution(self):
        return self._constitution

    def get_intelligence(self):
        return self._intelligence

    def get_wisdom(self):
        return self._wisdom

    def get_charisma(self):
        return self._charisma

    def get_proficiencies(self):
        return self._proficiencies

    def get_features(self):
        return self._features

    def get_death_saves(self):
        return self._death_saves

    def get_conditions(self):
        return self._conditions

    def has_condition(self, condition):
        return condition in self._conditions

    def get_weapons(self):
        return self._weapons

    def get_items(self):
        return self._items

    def get_spells(self):
        return self._spells

    def get_spell_slots(self):
        return self._spell_slots

    def get_attacks(self):
        return self._attacks

    def get_name(self):
        return self._name

    def add_weapon(self, weapon):
        if not isinstance(weapon, weapons.Weapon):
            raise ValueError("%s tried to add a non-weapon as a weapon" % self._name)
        self._weapons.append(weapon)
        weapon.set_owner(self)

    def add_condition(self, condition):
        # TODO: validate condition
        if condition not in self._conditions:
            self._conditions.append(condition)

    def remove_condition(self, condition):
        try:
            self._conditions.remove(condition)
        except ValueError:
            pass  # TODO: change later?

    def change_vision(self, vision):  # in case of special vision changing magic? also useful for testing
        self._vision = vision

    def become_unconscious(self):
        warnings.warn("Not implemented yet")  # TODO: become unconscious
