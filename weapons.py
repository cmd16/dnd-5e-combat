from utility_methods_dnd import validate_dice

class Weapon:
    def __init__(self, **kwargs):
        self._finesse = kwargs.get('finesse', 0)
        self._light = kwargs.get('light', 0)
        self._heavy = kwargs.get('heavy', 0)
        self._load = kwargs.get('load', 0)
        self._range = kwargs.get('range', 0)  # range is 0 or a tuple. For our purposes it's the same property as thrown
        self._melee_range = kwargs.get('melee_range', 0)
        if not self._range and not self._melee_range:  # assume it is a melee weapon
            self._melee_range = 5
        self._reach = kwargs.get('reach', 0)
        self._two_handed = kwargs.get('two_handed', 0)
        self._versatile = kwargs.get('versatile', 0)
        self._damage_dice = validate_dice(kwargs.get('damage_dice'))
        self._name = kwargs.get('name')  # needed for verbose output
        if not self._name:
            raise ValueError("Must provide name")
        self._owner = kwargs.get('owner', None)
        self._hit_bonus = kwargs.get('hit_bonus', 0)
        self._damage_bonus = kwargs.get('damage_bonus', 0)

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

    def get_range(self):
        return self._range

    def get_melee_range(self):
        return self._melee_range

    def get_damage_dice(self):
        return self._damage_dice

    def get_name(self):
        return self._name

    def get_owner(self):
        return self._owner

    def set_name(self, name):
        self._name = name

    def set_owner(self, owner):
        self._owner = owner
