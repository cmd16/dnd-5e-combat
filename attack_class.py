from utility_methods_dnd import roll_dice, validate_dice, calc_advantage
import weapons

class Attack:
    def __init__(self, damage_dice, attack_mod=0, damage_mod=0, damage_type="", range=0, melee_range=0, adv=0, name="",
                 weapon=None):
        self._damage_dice = validate_dice(damage_dice)
        if not isinstance(attack_mod, int):
            raise ValueError("Attack mod should be an integer")
        self._attack_mod = attack_mod
        if not isinstance(damage_mod, int):
            raise ValueError("Damage mod should be an integer")
        self._damage_mod = damage_mod
        if not isinstance(damage_type, str):
            raise ValueError("Damage type should be a string")
        self._damage_type = damage_type
        if not isinstance(name, str):
            raise ValueError("Name should be a string")
        if isinstance(range, int):
            self._range = range
        else:  # TODO: give a warning?
            self._range = 0
        if isinstance(melee_range, int):
            self._melee_range = melee_range
        else:
            self._melee_range = 0
        if not self._range and not self._melee_range:  # assume this is a melee attack if not otherwise specified
            self._melee_range = 5
        if adv in [-1, 0, 1]:
            self._adv = adv
        else:
            raise ValueError("Advantage must be -1, 0, or 1")
        self._name = name
        if not isinstance(name, str):
            raise ValueError("Name should be a string")
        if isinstance(weapon, weapons.Weapon):
            self._weapon = weapon
        elif weapon:
            raise ValueError("Weapon should be a Weapon object")
        else:
            self._weapon = None

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

    def roll_attack(self, adv=0):  # adv is the additional advantage afforded by circumstance
        return roll_dice(20, adv=calc_advantage([self._adv, adv]), modifier=self._attack_mod, critable=True)

    def roll_damage(self, crit=0):
        num = self._damage_dice[0]
        if crit:
            num *= 2
        return roll_dice(dice_type=self._damage_dice[1], num=num, modifier=self._damage_mod, critable=False)[0]  # don't need crit info
