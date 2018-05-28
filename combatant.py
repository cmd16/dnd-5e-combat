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
import attack_class
from utility_methods_dnd import ability_to_mod, validate_dice, cr_to_xp

class Combatant:
    def __init__(self, **kwargs):
        self._ac = kwargs.get('ac')
        if not self._ac or not isinstance(self._ac, int):  # TODO: include threshold
            raise ValueError("Must provide ac as an integer")
        self._max_hp = kwargs.get('max_hp')
        if not self._max_hp or not isinstance(self._max_hp, int) or self._max_hp <= 0:
            raise ValueError("Must provide positive max hp")
        self._temp_hp = kwargs.get('temp_hp', 0)

        self._conditions = kwargs.get('conditions', [])  # set this first in case current hp makes character unconscious
        if not isinstance(self._conditions, list):
            raise ValueError("If conditions provided, must be a list")

        self._current_hp = kwargs.get('current_hp', 0)
        if not isinstance(self._current_hp, int):
            raise ValueError("Must provide non-negative integer for current hp")
        if self._current_hp <= 0:
            warnings.warn("Combatant created with 0 or less hp. Going unconscious (and setting hp to 0).")
            self.become_unconscious()
        if self._current_hp > self._max_hp:
            raise ValueError("Current hp cannot be greater than max hp. Use temp hp if needed.")

        self._hit_dice = validate_dice(kwargs.get('hit_dice'))
        self._speed = kwargs.get('speed', 25)
        if not isinstance(self._speed, int) or self._speed <= 0:
            raise ValueError("Speed must be a positive integer")
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

        self._death_saves = kwargs.get('death_saves', [])  # TODO: implement

        self._weapons = []
        weapons = kwargs.get('weapons', [])
        if not isinstance(weapons, (list, tuple)):
            raise ValueError("Weapons must be a list or tuple of weapons")  # TODO: test
        for weapon in weapons:
            self.add_weapon(weapon)

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

    def get_conditions(self):
        return self._conditions

    def has_condition(self, condition):
        return condition in self._conditions

    def get_vision(self):
        return self._vision

    def can_see(self, light_src):
        if self.has_condition("blinded"):
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

    def set_ac(self, ac):
        self._ac = ac

    def set_temp_hp(self, hp):
        self._temp_hp = hp

    def take_damage(self, damage):   # assumes all pre-processing has been done (e.g., damage halved for successful saves)
        if self._temp_hp:
            if damage <= self._temp_hp:
                self._temp_hp -= damage
                return damage
            damage -= self._temp_hp  # empty out temp hp
            self._temp_hp = 0
        current_hp = self._current_hp
        self._current_hp -= damage
        if self._current_hp <= self._max_hp * -1:  # if remaining damage meets or exceeds your max hp
            self.die()
        elif self._current_hp <= 0:
            self.become_unconscious()

    def take_healing(self, healing):
        self._current_hp = min(self._current_hp + healing, self._max_hp)
        if self.has_condition("unconscious"):
            self.remove_condition("unconscious")

    def add_weapon(self, weapon):
        if not isinstance(weapon, weapons.Weapon):
            raise ValueError("%s tried to add a non-weapon as a weapon" % self._name)
        self._weapons.append(weapon)
        weapon.set_owner(self)

    def add_weapon_attacks(self, weapon):
        # Warning: if a Combatant has multiple weapons with the exact same name,
            # problems will arise because weapon attack names will not be unique
        if weapon.has_prop("finesse"):
            mod = max(self._strength, self._dexterity)
        else:
            mod = self._dexterity
        # TODO: add proficiency
        attack_mod = weapon.get_hit_bonus() + mod
        damage_mod = weapon.get_damage_bonus() + mod
        if weapon.get_range():
            self._attacks.append(attack_class.Attack(damage_dice=weapon.get_damage_dice(), attack_mod=attack_mod, damage_mod=damage_mod,
                                     name="%s_range" % weapon.get_name(), damage_type=weapon.get_damage_type(),
                                                range=weapon.get_range()[0]))
            self._attacks.append(attack_class.Attack(damage_dice=weapon.get_damage_dice(), attack_mod=attack_mod, damage_mod=damage_mod,
                                     name="%s_range_disadvantage" % weapon.get_name(), damage_type=weapon.get_damage_type(),
                                                range=weapon.get_range()[1], adv=-1))
        if weapon.get_melee_range():
            self._attacks.append(attack_class.Attack(damage_dice=weapon.get_damage_dice(), attack_mod=attack_mod, damage_mod=damage_mod,
                                     name="%s_melee" % weapon.get_name(), damage_type=weapon.get_damage_type(),
                                    melee_range=weapon.get_melee_range()))

    def remove_weapon_attacks(self, weapon):
        weapon_name = weapon.get_name()
        names_to_remove = []
        if weapon.get_range():
            names_to_remove.append("%s_range" % weapon_name)
            names_to_remove.append("%s_range_disadvantage" % weapon_name)
        if weapon.get_melee_range():
            names_to_remove.append("%s_melee" % weapon_name)
        # modify attack name in place
        self._attacks[:] = [attack for attack in self._attacks if attack.get_name() not in names_to_remove]

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
        warnings.warn("Becoming unconscious not fully implemented yet")  # TODO: become unconscious
        self.add_condition("unconscious")
        self._current_hp = 0

    def die(self):
        warnings.warn("Dying not fully implemented yet")  # TODO: die
        self._conditions = ["dead"]  # TODO: change death later?
        self._current_hp = 0
        self._temp_hp = 0

class Creature(Combatant):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cr = kwargs.get("cr", 0)
        if not isinstance(self._cr, (int, float)) or self._cr <= 0:
            raise ValueError("Challenge rating must be a non-negative number")
        self._xp = kwargs.get("xp", cr_to_xp(self._cr))

    def get_cr(self):
        return self._cr

    def get_xp(self):
        return self._xp

class Character(Combatant):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._level = kwargs.get("level")
        if not self._level:
            raise ValueError("No level provided or level is 0")
        if not isinstance(self._level, int) or self._level < 1 or self._level > 20:
            raise ValueError("Level must be an integer between 1 and 20")

    def get_level(self):
        return self._level
