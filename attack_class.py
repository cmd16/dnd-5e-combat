from utility_methods_dnd import roll_dice, validate_dice

class Attack:
    def __init__(self, damage_dice, attack_mod=0, damage_mod=0, damage_type="", name=""):
        if not isinstance(attack_mod, int):
            raise ValueError("Attack mod should be an integer")
        self._attack_mod = attack_mod
        if not isinstance(damage_mod, int):
            raise ValueError("Damage mod should be an integer")
        self._damage_mod = damage_mod
        if not isinstance(damage_type, str):
            raise ValueError("Damage type should be a string")
        self._damage_type = damage_type
        self._damage_dice = validate_dice(damage_dice)
        if not isinstance(name, str):
            raise ValueError("Name should be a string")
        self._name = name
        if not isinstance(name, str):
            raise ValueError("Name should be a string")

    def roll_attack(self, adv=0):
        return roll_dice(20, adv=adv, modifier=self._attack_mod, critable=True)

    def roll_damage(self):
        return roll_dice(self._damage_dice[1], num=self._damage_dice[0], modifier=self._damage_mod, critable=False)

    def get_attack_mod(self):
        return self._attack_mod

    def get_damage_mod(self):
        return self._damage_mod

    def get_damage_type(self):
        return self._damage_type

    def get_damage_dice(self):
        return self._damage_dice

    def get_name(self):
        return self._name
