import warnings
from utility_methods_dnd import roll_dice, validate_dice, calc_advantage, time_to_rounds
import weapons

class Attack:
    """damage_dice=None, attack_mod=0, damage_mod=0, damage_type="", range=0, melee_range=0, adv=0, name="",
                 weapon=None, copy=None"""
    def __init__(self, **kwargs):
        # print("init Attack")
        name = kwargs.get("name")
        copy = kwargs.get("copy")
        if copy:
            self.copy_constructor(other=copy, name=name)
            return
        self._damage_dice = validate_dice(kwargs.get("damage_dice"))  # providing no dice will be handled by validate_dice
        attack_mod = kwargs.get("attack_mod", 0)
        if not isinstance(attack_mod, int):
            raise ValueError("Attack mod should be an integer")
        self._attack_mod = attack_mod
        damage_mod = kwargs.get("damage_mod", 0)
        if not isinstance(damage_mod, int):
            raise ValueError("Damage mod should be an integer")
        self._damage_mod = damage_mod
        damage_type = kwargs.get("damage_type", "")
        if not isinstance(damage_type, str):
            raise ValueError("Damage type should be a string")
        self._damage_type = damage_type
        if not isinstance(name, str):
            raise ValueError("Name should be a string")
        range = kwargs.get("range", 0)
        if isinstance(range, int):  # TODO: handle various formats of range
            self._range = range
        else:  # TODO: give a warning?
            warnings.warn("Non-integer value for range provided")
            self._range = range
        melee_range = kwargs.get("melee_range", 0)
        if isinstance(melee_range, int):
            self._melee_range = melee_range
        else:
            self._melee_range = 0
        if not self._range and not self._melee_range:  # assume this is a melee attack if not otherwise specified
            self._melee_range = 5
        adv = kwargs.get("adv", 0)
        if adv in [-1, 0, 1]:
            self._adv = adv
        else:
            raise ValueError("Advantage must be -1, 0, or 1")
        name = kwargs.get("name")
        self._name = name
        if not isinstance(name, str):
            raise ValueError("Name should be a string")
        weapon = kwargs.get("weapon")
        if isinstance(weapon, weapons.Weapon):
            self._weapon = weapon
        elif weapon:
            raise ValueError("Weapon should be a Weapon object")
        else:
            self._weapon = None

    def copy_constructor(self, other, name=""):
        if other == self:  # don't bother copying yourself
            return
        if not isinstance(other, Attack):
            raise ValueError("Cannot make self a copy of something that is not an Attack")

        if other.get_weapon():
            warnings.warn("Not recommended to copy an attack tied to a weapon. Copy the weapon itself and assign it to a person.")

        if not name or not isinstance(name, str):
            name = other.get_name()

        Attack.__init__(self=self, damage_dice=other.get_damage_dice(), attack_mod=other.get_attack_mod(), damage_mod=other.get_damage_mod(),
                      damage_type=other.get_damage_type(), range=other.get_range(), melee_range=other.get_melee_range(),
                      adv=other.get_adv(), name=name, weapon=other.get_weapon())

    def get_damage_dice(self):
        return self._damage_dice

    def get_attack_mod(self):
        return self._attack_mod

    def get_damage_mod(self):
        return self._damage_mod

    def get_damage_type(self):
        return self._damage_type

    def get_range(self):
        return self._range

    def get_melee_range(self):
        return self._melee_range

    def get_adv(self):
        return self._adv

    def get_name(self):
        return self._name

    def get_weapon(self):
        return self._weapon

    def set_attack_mod(self, attack_mod):
        if isinstance(attack_mod, int):
            self._attack_mod = attack_mod
        else:
            raise ValueError("Attack mod must be an integer")

    def roll_attack(self, adv=0):  # adv is the additional advantage afforded by circumstance
        return roll_dice(20, adv=calc_advantage([self._adv, adv]), modifier=self._attack_mod, critable=True)

    def roll_damage(self, crit=0):
        num = self._damage_dice[0]
        if crit:
            num *= 2
        return roll_dice(dice_type=self._damage_dice[1], num=num, modifier=self._damage_mod, critable=False)[0]  # don't need crit info

    def make_attack(self, source, target, adv=0):
        result = self.roll_attack(adv=adv)
        verbose = source.get_verbose()
        try:
            if verbose:
                print("%s attacks %s with %s and rolls a %d." % (source.get_name(), target.get_name(), self._name,
                                                                  result[0]), end=" ")
            if target.take_attack(result):  # take_attack returns True if attack hits
                if verbose:
                    if result[1] == 1:
                        print("Critical hit!", end=" ")  # leave room for damage info
                    else:
                        print("Hit!", end=" ")
                self.send_damage(target, crit=result[1])
            else:
                if verbose:
                    if result[1] == -1:
                        print("Critical miss.")
                    else:
                        print("Miss.")
        except NameError:
            raise ValueError("%s tried to attack something that can't take attacks" % source._name)

    def send_damage(self, target, crit=0):
        damage = self.roll_damage(crit=crit)
        target.take_damage(damage)

class SavingThrowAttack(Attack):
    """copy=None, damage_dice=None, dc=None, save_type="", damage_on_success=False,
                 damage_mod=0, damage_type="", range=0, melee_range=0, adv=0, name="", weapon=None"""
    def __init__(self, **kwargs):
        # print("init SavingThrowAttack")
        name = kwargs.get("name")
        copy = kwargs.get("copy")
        if copy:
            self.copy_constructor(other=copy, name=name)
            return

        super().__init__(**kwargs)  # irrelevant keyword arguments will be ignored
        dc = kwargs.get("dc")
        if not dc or not isinstance(dc, int):
            raise ValueError("Must provide DC (an int)")
        self._dc = dc
        save_type = kwargs.get("save_type")
        if save_type in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            self._save_type = save_type
        else:
            raise ValueError("Save type must be strength, dexterity, constitution, intelligence, wisdom, or charisma")
        damage_on_success = kwargs.get("damage_on_success")
        self._damage_on_success = damage_on_success  # half damage on successful save

    def copy_constructor(self, other, name=""):
        super().copy_constructor(other, name)
        dc = other.get_dc()
        if not dc or not isinstance(dc, int):
            raise ValueError("Must provide DC (an int)")
        self._dc = dc
        save_type = other.get_save_type()
        if save_type in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            self._save_type = save_type
        else:
            raise ValueError("Save type must be strength, dexterity, constitution, intelligence, wisdom, or charisma")
        self._damage_on_success = other.get_damage_on_success()  # half damage on successful save

    def get_dc(self):
        return self._dc

    def get_save_type(self):
        return self._save_type

    def get_damage_on_success(self):
        return self._damage_on_success

    def make_attack(self, source, target, adv=0):
        verbose = source.get_verbose()
        try:
            if verbose:
                print("%s attacks %s with %s." % (source.get_name(), target.get_name(), self._name), end=" ")
            if target.take_saving_throw(self._save_type, self._dc, self):  # take_saving_throw returns True if target made the save
                if verbose:
                    print("%s saves." % target.get_name())
                self.send_damage(target, saved=True)
            else:
                if verbose:
                    print("%s fails!" % target.get_name())
                self.send_damage(target)

        except NameError:
            raise ValueError("%s tried to attack something that can't take attacks" % source._name)

    def send_damage(self, target, saved=False):
        damage = self.roll_damage()
        if not saved:
            target.take_damage(damage)
        elif self._damage_on_success:
            target.take_damage(damage//2)

class Spell(Attack):
    """level=None, school=None, casting_time=None, components=None, duration=None,  damage_dice=None,
                 attack_mod=0, damage_mod=0, damage_type="", range=0, melee_range=0, adv=0, name="",
                 copy=None"""
    def __init__(self, **kwargs):
        # print("init Spell")
        copy = kwargs.get("copy")
        name = kwargs.get("name")
        if copy:
            self.copy_constructor(copy, name)
            return
        super().__init__(**kwargs)
        level = kwargs.get("level")
        if isinstance(level, int) and 0 <= level < 10:
            self._level = level
        else:
            raise ValueError("Level must be an integer between 0 and 9")
        school = kwargs.get("school")
        self._school = school  # TODO: validation
        casting_time = kwargs.get("casting_time")
        if casting_time == "1 action" or casting_time == "1 bonus action" or casting_time == "1 reaction":
            self._casting_time = casting_time
        else:
            self._casting_time = time_to_rounds(casting_time)
        components = kwargs.get("components")
        if not isinstance(components, (list, tuple)):
            raise ValueError("Components must be a list or tuple")
        self._components = []
        if "v" in components:
            self._components.append("v")
        if "s" in components:
            self._components.append("s")
        if "m" in components:
            self._components.append("m")
        duration = kwargs.get("duration")
        self._duration = duration  # TODO: validation

    def copy_constructor(self, other, name=""):
        super().copy_constructor(other, name)
        self._level = other.get_level()
        self._school = other.get_school()  # TODO: validation
        self._casting_time = other.get_casting_time()
        self._components = other.get_components()[:]
        self._duration = other.get_duration()  # TODO: validation

    def get_level(self):
        return self._level

    def get_school(self):
        return self._school

    def get_casting_time(self):
        return self._casting_time

    def get_components(self):
        return self._components

    def get_duration(self):
        return self._duration

    def make_attack(self, source, target, adv=0, level=None):
        if level is None:
            level = self._level
        if source.get_level_spell_slots(level) or level == 0:
            source.spend_slot(level)  # TODO: check cantrip logic
        else:
            if source.get_verbose():
                print("%s tried to cast a level %d spell even though they have no slots left for it" % (source.get_name(), level))
            return False
        super().make_attack(source=source, target=target, adv=adv)  # To be overridden in subclasses

class SavingThrowSpell(Spell, SavingThrowAttack):
    """level=None, school=None, casting_time=None, components=None, duration=None,
                 dc=None, save_type="", damage_on_success=False, damage_dice=None, damage_mod=0,
                 damage_type="", range=0, melee_range=0, adv=0, name="", copy=None"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
