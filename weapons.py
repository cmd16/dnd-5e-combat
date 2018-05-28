from utility_methods_dnd import validate_dice
import warnings

class Weapon:
    def __init__(self, **kwargs):
        copy_weapon = kwargs.get("copy")
        if copy_weapon:
            self.make_me_a_copy(copy_weapon, name=kwargs.get("name"))
            return
        self._finesse = kwargs.get('finesse', 0)
        self._light = kwargs.get('light', 0)
        self._heavy = kwargs.get('heavy', 0)
        self._load = kwargs.get('load', 0)
        self._range = kwargs.get('range', 0)  # range is 0 or a tuple. For our purposes it's the same property as thrown
        if isinstance(self._range, tuple):  # lists are mutable and that could be a problem
            if len(self._range) != 2:
                raise ValueError("Must provide exactly two values: normal range and disadvantage range")
            if not isinstance(self._range[0], int) or not isinstance(self._range[1], int):
                raise ValueError("Must provide exactly two integer values: normal range and disadvantage range")
        elif isinstance(self._range, str):
            try:
                self._range = tuple(int(x) for x in self._range.split("/"))
            except ValueError:
                raise ValueError("Must provide range in tuple of two ints (20, 60) or string format 20/60")
            if len(self._range) != 2:
                raise ValueError("Must provide range in tuple of two ints (20, 60) or string format 20/60")
        elif self._range != 0:
            raise ValueError("Must provide range in tuple of two ints (1, 6) or string format 1d6")
        self._melee_range = kwargs.get('melee_range', 0)
        if not self._range and not self._melee_range:  # assume this is a melee weapon if not otherwise specified
            self._melee_range = 5
        self._reach = kwargs.get('reach', 0)
        if self._reach and self._melee_range:
            self._melee_range += 5
        self._two_handed = kwargs.get('two_handed', 0)
        self._versatile = kwargs.get('versatile', 0)  # TODO: implement versatile (deal with damage)

        self._props = []
        if self._finesse:
            self._props.append("finesse")
        if self._light:
            self._props.append("light")
        elif self._heavy:
            self._props.append("heavy")
        if self._load:
            self._props.append("load")
        if self._range:
            self._props.append("range")
        if self._melee_range:
            self._props.append("melee")
        if self._reach:
            self._props.append("reach")
        if self._two_handed:
            self._props.append("two_handed")
        elif self._versatile:
            self._props.append("versatile")

        self._damage_dice = validate_dice(kwargs.get('damage_dice'))
        self._damage_type = kwargs.get("damage_type")
        if not isinstance(self._damage_type, str):
            raise ValueError("Damage type should be a string")
        self._name = kwargs.get('name')  # needed for verbose output
        if not self._name:
            raise ValueError("Must provide name")
        self._owner = kwargs.get('owner', None)
        self._hit_bonus = kwargs.get('hit_bonus', 0)
        self._damage_bonus = kwargs.get('damage_bonus', 0)

    def make_me_a_copy(self, other, name=""):
        """
        Sets instance variables from another Weapon. Warning: this overrides any existing values in self.
        :param other: another Weapon
        :return:
        """
        if other == self:  # don't bother copying yourself
            return
        if not isinstance(other, Weapon):
            raise ValueError("Cannot make self a copy of something that is not a Weapon")
        self._range = other.get_range()
        self._melee_range = other.get_melee_range()
        self._props = other.get_properties()
        self._finesse = 'finesse' in self._props
        self._light = "light" in self._props
        self._heavy = "heavy" in self._props
        self._load = "load" in self._props
        self._reach = "reach" in self._props
        self._two_handed = "two_handed" in self._props
        self._versatile = "versatile" in self._props
        self._damage_dice = other.get_damage_dice()
        self._damage_type = other.get_damage_type()
        if not name:
            self._name = other.get_name()  # TODO: keep same name?
        else:
            self._name = name
        self._owner = None
        self._hit_bonus = other.get_hit_bonus()
        self._damage_bonus = other.get_damage_bonus()

    def get_properties(self):
        props = []
        if self._finesse:
            props.append("finesse")
        if self._light:
            props.append("light")
        elif self._heavy:
            props.append("heavy")
        if self._load:
            props.append("load")
        if self._range:
            props.append("range")
        if self._melee_range:
            props.append("melee")
        if self._reach:
            props.append("reach")
        if self._two_handed:
            props.append("two_handed")
        elif self._versatile:
            props.append("versatile")
        return props

    def has_prop(self, prop):
        return prop in self._props

    def get_range(self):
        return self._range

    def get_melee_range(self):
        return self._melee_range

    def get_damage_dice(self):
        return self._damage_dice

    def get_damage_type(self):
        return self._damage_type

    def get_name(self):
        return self._name

    def get_owner(self):
        return self._owner

    def set_name(self, name):
        if name == self._name:
            return
        if self._owner:
            self._owner.remove_weapon_attacks(self)  # clear the attacks to avoid a name conflict
        self._name = name
        if self._owner:
            self._owner.add_weapon_attacks(self)

    def set_owner(self, owner):
        self._owner = owner

    def get_hit_bonus(self):
        return self._hit_bonus

    def get_damage_bonus(self):
        return self._damage_bonus
