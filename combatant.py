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
spells (subclass)
features (add later)
"""
import warnings
import weapons
import attack_class
from utility_methods_dnd import ability_to_mod, validate_dice, roll_dice, cr_to_xp

class Combatant:
    def __init__(self, **kwargs):
        combatant_copy = kwargs.get("copy")
        if combatant_copy:
            self.copy_constructor(combatant_copy, name=kwargs.get("name"))
            return

        self._verbose = kwargs.get("verbose", False)

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

        self._current_hp = kwargs.get('current_hp', self._max_hp)  # by default, start with max hp
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
            strength_mod = kwargs.get("strength_mod")  # modifiers also accepted
            if strength_mod is not None:
                if isinstance(strength_mod, int):
                    self._strength = strength_mod
                else:
                    raise ValueError("Strength mod must be an integer")
            else:
                raise ValueError("Must provide strength score or modifier")
        else:
            self._strength = ability_to_mod(strength)

        dexterity = kwargs.get('dexterity')
        if not dexterity:
            dexterity_mod = kwargs.get("dexterity_mod")
            if dexterity_mod is not None:
                if isinstance(dexterity_mod, int):
                    self._dexterity = dexterity_mod
                else:
                    raise ValueError("Dexterity mod must be an integer")
            else:
                raise ValueError("Must provide dexterity score or modifier")
        else:
            self._dexterity = ability_to_mod(dexterity)

        constitution = kwargs.get('constitution')
        if not constitution:
            constitution_mod = kwargs.get("constitution_mod")
            if constitution_mod is not None:
                if isinstance(constitution_mod, int):
                    self._constitution = constitution_mod
                else:
                    raise ValueError("Constitution mod must be an integer")
            else:
                raise ValueError("Must provide constitution score or modifier")
        else:
            self._constitution = ability_to_mod(constitution)

        intelligence = kwargs.get('intelligence')
        if not intelligence:
            intelligence_mod = kwargs.get("intelligence_mod")
            if intelligence_mod is not None:
                if isinstance(intelligence_mod, int):
                    self._intelligence = intelligence_mod
                else:
                    raise ValueError("Intelligence mod must be an integer")
            else:
                raise ValueError("Must provide intelligence score or modifier")
        else:
            self._intelligence = ability_to_mod(intelligence)

        wisdom = kwargs.get('wisdom')
        if not wisdom:
            wisdom_mod = kwargs.get("wisdom_mod")
            if wisdom_mod is not None:
                if isinstance(wisdom_mod, int):
                    self._wisdom = wisdom_mod
                else:
                    raise ValueError("Wisdom mod must be an integer")
            else:
                raise ValueError("Must provide wisdom score or modifier")
        else:
            self._wisdom = ability_to_mod(wisdom)

        charisma = kwargs.get('charisma')
        if not charisma:
            charisma_mod = kwargs.get("charisma_mod")
            if charisma_mod is not None:
                if isinstance(charisma_mod, int):
                    self._charisma = charisma_mod
                else:
                    raise ValueError("Charisma mod must be an integer")
            else:
                raise ValueError("Must provide charisma score or modifier")
        else:
            self._charisma = ability_to_mod(charisma)
        self._proficiencies = kwargs.get('proficiencies', [])  # TODO: implement
        if not isinstance(self._proficiencies, (list, tuple)):
            raise ValueError("Proficiencies must be provided as a list or tuple")

        self._proficiency_mod = kwargs.get("proficiency_mod", 0)

        self._saving_throws = {"strength": self._strength, "dexterity": self._dexterity, "constitution": self._constitution, "intelligence": self._intelligence,
                               "wisdom": self._wisdom, "charisma": self._charisma}
        for ability in self._saving_throws:
            if ability in self._proficiencies:
                self._saving_throws[ability] += self._proficiency_mod

        self._features = kwargs.get('features', [])  # TODO: implement

        self._death_saves = kwargs.get('death_saves', [])  # TODO: implement

        self._attacks = []

        self._weapons = []
        weapons = kwargs.get('weapons', [])
        if not isinstance(weapons, (list, tuple)):
            raise ValueError("Weapons must be a list or tuple of weapons")  # TODO: test
        for weapon in weapons:
            self.add_weapon(weapon)

        self._items = kwargs.get('items', [])  # TODO: implement

        self._name = kwargs.get('name')
        if not self._name:
            raise ValueError("Must provide a name")

    def copy_constructor(self, other, name=""):
        """
        Sets instance variables from another Combatant. Warning: this overrides any existing values in self.
        :param other: another Combatant
        :return:
        """
        if other == self:  # don't bother copying yourself
            return
        if not isinstance(other, Combatant):
            raise ValueError("Cannot make self a copy of something that is not a Combatant")

        if not name or not isinstance(name, str):
            name = other.get_name()

        Combatant.__init__(self=self, verbose=other.get_verbose(), max_hp=other.get_max_hp(), temp_hp=other.get_temp_hp(),
                      conditions=other.get_conditions()[:], current_hp=other.get_current_hp(), hit_dice=other.get_hit_dice(),
                      speed=other.get_speed(), vision=other.get_vision(), strength_mod=other.get_strength(),
                      dexterity_mod=other.get_dexterity(), constitution_mod=other.get_constitution(),
                      intelligence_mod=other.get_intelligence(), wisdom_mod=other.get_wisdom(), charisma_mod=other.get_charisma(),
                      proficiencies=other.get_proficiencies(), proficiency_mod=other.get_proficiency_mod(),
                      features=other.get_features(), death_saves=other.get_death_saves(), ac=other.get_ac(), name=name)

        for weapon in other.get_weapons():
            self.add_weapon(weapons.Weapon(copy=weapon))

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

    def get_ability(self, ability):
        if ability == "strength":
            return self._strength
        elif ability == "dexterity":
            return self._dexterity
        elif ability == "constitution":
            return self._constitution
        elif ability == "intelligence":
            return self._intelligence
        elif ability == "wisdom":
            return self._wisdom
        elif ability == "charisma":
            return self._charisma
        else:
            raise ValueError("Ability score must be strength, dexterity, constitution, intelligence, wisdom, or charisma")

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

    def get_proficiency_mod(self):
        return self._proficiency_mod

    def get_saving_throw(self, ability):
        try:
            return self._saving_throws[ability]
        except KeyError:
            raise ValueError("Asked for a saving throw that is not an ability score")

    def get_features(self):
        return self._features

    def get_death_saves(self):
        return self._death_saves

    def get_weapons(self):
        return self._weapons

    def get_items(self):
        return self._items

    def get_attacks(self):
        return self._attacks

    def get_name(self):
        return self._name

    def get_verbose(self):
        return self._verbose

    def set_ac(self, ac):
        self._ac = ac

    def set_temp_hp(self, hp):
        self._temp_hp = hp

    def set_verbose(self, val):
        self._verbose = bool(val)

    def add_weapon(self, weapon):
        if not isinstance(weapon, weapons.Weapon):
            raise ValueError("%s tried to add a non-weapon as a weapon" % self._name)
        if weapon in self._weapons:
            warnings.warn("You (%s) already owns weapon %s" %(self._name, weapon.get_name()))
        owner = weapon.get_owner()
        if owner:
            raise ValueError("Weapon %s is owned by %s. Remove it from them first." % (weapon.get_name(), owner.get_name()))
        self._weapons.append(weapon)
        weapon.set_owner(self)
        self.add_weapon_attacks(weapon)
        if self._verbose:
            print("%s adds %s weapon" % (self._name, weapon.get_name()))

    def remove_weapon(self, weapon):
        if weapon not in self._weapons:
            raise ValueError("%s tried to remove a weapon they don't have" % self._name)
        self._weapons.remove(weapon)
        weapon.set_owner(None)  # Dobby is a free weapon!
        self.remove_weapon_attacks(weapon)
        if self._verbose:
            print("%s removes %s weapon" % (self._name, weapon.get_name()))

    def remove_all_weapons(self):
        to_remove = self._weapons[:]  # make a copy so I can iterate through the list
        for weapon in to_remove:
            self.remove_weapon(weapon)

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
            self.add_attack(attack_class.Attack(damage_dice=weapon.get_damage_dice(), attack_mod=attack_mod, damage_mod=damage_mod,
                                     name="%s_range" % weapon.get_name(), damage_type=weapon.get_damage_type(),
                                                range=weapon.get_range()[0], weapon=weapon))
            self.add_attack(attack_class.Attack(damage_dice=weapon.get_damage_dice(), attack_mod=attack_mod, damage_mod=damage_mod,
                                     name="%s_range_disadvantage" % weapon.get_name(), damage_type=weapon.get_damage_type(),
                                                range=weapon.get_range()[1], adv=-1, weapon=weapon))
        if weapon.get_melee_range():
            self._attacks.append(attack_class.Attack(damage_dice=weapon.get_damage_dice(), attack_mod=attack_mod, damage_mod=damage_mod,
                                     name="%s_melee" % weapon.get_name(), damage_type=weapon.get_damage_type(),
                                    melee_range=weapon.get_melee_range(), weapon=weapon))

    def add_attack(self, attack):
        if attack in self._attacks:
            pass
        self._attacks.append(attack)

    def remove_weapon_attacks(self, weapon):
        self._attacks[:] = [attack for attack in self._attacks if attack.get_weapon() is not weapon]

    def add_condition(self, condition):
        # TODO: validate condition?
        if condition not in self._conditions:
            self._conditions.append(condition)
            if self._verbose:
                print("%s is now %s" % (self._name, condition))

    def remove_condition(self, condition):
        try:
            self._conditions.remove(condition)
            if self._verbose:
                print("%s is no longer %s" % (self._name, condition))
        except ValueError:
            pass  # TODO: change later?

    def change_vision(self, vision):  # in case of special vision changing magic? also useful for testing
        if vision in ["normal", "darkvision", "blindsight", "truesight"]:
            self._vision = vision
            if self._verbose:
                print("%s changes vision to %s" % (self._name, vision))
        else:
            raise ValueError("Vision type not recognized")

    def send_attack(self, target, attack, adv=0):
        try:
            attack.make_attack(self, target, adv=adv)
        except:
            raise ValueError("%s tried to make an attack with something that can't make attacks" % self._name)

    def take_attack(self, attack_result):
        hit_val, crit_val = attack_result
        if crit_val == -1:  # critical fails auto-miss
            return False
        return hit_val >= self._ac

    def take_saving_throw(self, save_type, dc, attack):  # attack just there in case it's useful later
        return self.make_saving_throw(save_type) >= dc

    def make_saving_throw(self, save_type):
        modifier = self.get_saving_throw(save_type)
        result = roll_dice(dice_type=20, modifier=modifier)[0]
        if self._verbose:
            print("%s rolls a %d." % (self._name, result), end=" ")
        return result

    def take_damage(self, damage):
        if self._verbose:
            print("%s takes %d damage" % (self._name, damage))
        if self._temp_hp:
            if damage <= self._temp_hp:
                self._temp_hp -= damage
                return damage
            damage -= self._temp_hp  # empty out temp hp
            self._temp_hp = 0
        self._current_hp -= damage
        if self._current_hp <= self._max_hp * -1:  # if remaining damage meets or exceeds your max hp
            self.die()
        elif self._current_hp <= 0:
            self.become_unconscious()

    def take_healing(self, healing):
        self._current_hp = min(self._current_hp + healing, self._max_hp)
        if self._verbose:
            print("%s is healed for %d" % (self._name, healing), end=" ")
        if self.has_condition("unconscious"):
            self.remove_condition("unconscious")

    def become_unconscious(self):
        warnings.warn("Becoming unconscious not fully implemented yet")  # TODO: become unconscious
        self.add_condition("unconscious")
        self._current_hp = 0

    def die(self):
        warnings.warn("Dying not fully implemented yet")  # TODO: die
        self._conditions = []
        self.add_condition("dead")  # TODO: change death later?
        self._current_hp = 0
        self._temp_hp = 0

class Creature(Combatant):
    def __init__(self, **kwargs):
        # do this before super so that there aren't multiple calls to copy_constructor
        copy_creature = kwargs.get("copy")
        if copy_creature:
            self.copy_constructor(copy_creature, name=kwargs.get("name"), cr=kwargs.get("cr"), xp=kwargs.get("xp"))
            return
        super().__init__(**kwargs)
        self._cr = kwargs.get("cr", 0)
        if not isinstance(self._cr, (int, float)) or self._cr <= 0:
            raise ValueError("Challenge rating must be a non-negative number")
        self._xp = kwargs.get("xp", cr_to_xp(self._cr))

    def copy_constructor(self, other, name="", cr=0, xp=0):
        super().copy_constructor(other, name)
        if isinstance(other, Creature):
            self._cr = other.get_cr()
            self._xp = other.get_xp()
        else:
            if not isinstance(cr, (int, float)) or cr < 0:
                raise ValueError("Challenge rating must be a non-negative number")
            self._cr = cr
            if xp:
                if not isinstance(xp, int) or xp < 0:
                    raise ValueError("XP must be a non-negative integer")
                self._xp = xp
            else:
                self._xp = cr_to_xp(self._cr)

    def get_cr(self):
        return self._cr

    def get_xp(self):
        return self._xp

class Character(Combatant):
    def __init__(self, **kwargs):
        copy_character = kwargs.get("copy")
        if copy_character:
            self.copy_constructor(copy_character, name=kwargs.get("name"), level=kwargs.get("level"))
            return
        super().__init__(**kwargs)
        self._level = kwargs.get("level")
        if not self._level:
            raise ValueError("No level provided or level is 0")
        if not isinstance(self._level, int) or self._level < 1 or self._level > 20:
            raise ValueError("Level must be an integer between 1 and 20")

    def copy_constructor(self, other, name="", level=0):
        super().copy_constructor(other, name)
        self._level = level
        if isinstance(other, Character):
            self._level = other.get_level()
        else:
            if not self._level:
                raise ValueError("No level provided or level is 0")
            if not isinstance(self._level, int) or self._level < 1 or self._level > 20:
                raise ValueError("Level must be an integer between 1 and 20")

    def get_level(self):
        return self._level

class SpellCaster(Combatant):
    def __init__(self, **kwargs):
        copy = kwargs.get("copy")
        if copy:
            self.copy_constructor(other=copy, **kwargs)
            return

        super().__init__(**kwargs)
        spell_ability = kwargs.get("spell_ability", "intelligence")
        try:
            self._spell_ability_mod = self.get_ability(spell_ability)
            self._spell_ability = spell_ability
        except ValueError:
            raise ValueError("Spell ability must be strength, dexterity, constitution, intelligence, wisdom, or charisma")
        self._spell_save_dc = 8 + self._proficiency_mod + self._spell_ability_mod
        self._spell_attack_mod = self._proficiency_mod + self._spell_ability_mod
        spell_slots = kwargs.get("spell_slots")
        if spell_slots and not isinstance(spell_slots, dict):
            raise ValueError("Spell slots must be a dictionary. {1: 3, 2:1} would mean 3 1st level spells and 1 2nd level spell")
        if not spell_slots:
            for i in range(1, 10):
                value = kwargs.get("level_%d" % i)
                if value:
                    if isinstance(value, int):
                        spell_slots[i] = value
                    else:
                        raise ValueError("Spell slot number for level %d must be an integer" % i)
        self._spell_slots = spell_slots
        self._full_spell_slots = dict()
        self._full_spell_slots.update(self._spell_slots)
        self._spells = []
        spells = kwargs.get("spells")
        if not spells:
            warnings.warn("Created a SpellCaster with no spells")
        elif not isinstance(spells, (list, tuple)):
            raise ValueError("Spells must be a list or tuple")
        else:
            for spell in spells:
                if not isinstance(spell, attack_class.Spell):
                    raise ValueError("Spells must contain only Spell objects")
                self.add_spell(spell)

    def copy_constructor(self, other, **kwargs):
        super().copy_constructor(other, name=kwargs.get("name"))
        if isinstance(other, SpellCaster):
            self._spell_ability = other.get_spell_ability()
            self._spell_ability_mod = other.get_spell_ability_mod()
            self._spell_save_dc = other.get_spell_save_dc()
            self._spell_attack_mod = other.get_spell_attack_mod()
            self._spell_slots = dict()
            self._spell_slots.update(other.get_spell_slots())
            self._spells = []
            for spell in other.get_spells():
                new_spell = attack_class.Spell(copy=spell)
                self._spells.append(new_spell)
        else:
            spell_ability = kwargs.get("spell_ability", "intelligence")
            try:
                self._spell_ability_mod = self.get_ability(spell_ability)
                self._spell_ability = spell_ability
            except ValueError:
                raise ValueError(
                    "Spell ability must be strength, dexterity, constitution, intelligence, wisdom, or charisma")
            self._spell_save_dc = 8 + self._proficiency_mod + self._spell_ability_mod
            self._spell_attack_mod = self._proficiency_mod + self._spell_ability_mod
            spell_slots = kwargs.get("spell_slots")
            if spell_slots and not isinstance(spell_slots, dict):
                raise ValueError(
                    "Spell slots must be a dictionary. {1: 3, 2:1} would mean 3 1st level spells and 1 2nd level spell")
            if not spell_slots:
                for i in range(1, 10):
                    value = kwargs.get("level_%d" % i)
                    if value:
                        if isinstance(value, int):
                            spell_slots[i] = value
                        else:
                            raise ValueError("Spell slot number for level %d must be an integer" % i)
            self._spell_slots = spell_slots
            self._spells = []
            spells = kwargs.get("spells")
            if not spells:
                warnings.warn("Created a SpellCaster with no spells")
            elif not isinstance(spells, (list, tuple)):
                raise ValueError("Spells must be a list or tuple")
            else:
                for spell in spells:
                    if not isinstance(spell, attack_class.Spell):
                        raise ValueError("Spells must contain only Spell objects")
                    self.add_spell(attack_class.Spell(copy=spell))

    def get_spell_ability(self):
        return self._spell_ability

    def get_spell_ability_mod(self):
        return self._spell_ability_mod

    def get_spell_save_dc(self):
        return self._spell_save_dc

    def get_spell_attack_mod(self):
        return self._spell_attack_mod

    def get_spell_slots(self):
        return self._spell_slots

    def get_level_slots(self, level):
        try:
            return self._spell_slots[level]
        except KeyError:
            return 0

    def get_spells(self):
        return self._spells

    def add_spell(self, spell):
        if isinstance(spell, attack_class.Spell):
            self._spells.append(spell)
            # TODO: finish this

    def spend_slot(self, level):
        if not isinstance(level, int) or not (0 < level < 10):
            raise ValueError("Level must be an int between 1 and 9")
        try:
            if self._spell_slots[level] > 0:
                self._spell_slots[level] -= 1
            else:
                raise ValueError()  # no need including a message because it is caught
        except (KeyError, ValueError):
            raise ValueError("%s tried to cast a level %d spell even though they don't have slots for it" % (self._name, level))

    def reset_slots(self):
        spell_slots = dict()
        spell_slots.update(self._full_spell_slots)
        self._spell_slots = spell_slots
