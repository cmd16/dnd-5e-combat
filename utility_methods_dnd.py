import random
import warnings

def ability_to_mod(score):
    if score < 1:
        ValueError("Ability score too low (did you input a modifier?)")
    elif score > 30:
        ValueError("Ability score too high (did you add an extra digit?)")
    return (score -10) // 2

def roll_dice(dice_type, num=1, modifier=0, adv=0, critable=0):  # -1 for disadvantage, 0 for normal, 1 for advantage
    roll_val = 0
    nat_roll = 0
    crit = 0
    if num > 1 and critable:
        warnings.warn("Rolling multiple critable dice in one go is currently not supported. "
                      "Crit information will match the last die rolled.")
    for i in range(num):
        nat_roll = random.randint(1, dice_type)
        if adv:
            roll_2 = random.randint(1, dice_type)
            if adv == 1:
                nat_roll = max(nat_roll, roll_2)
            else:
                nat_roll = min(nat_roll, roll_2)
        crit = 0
        if critable:
            if nat_roll == dice_type:
                crit = 1  # crit success
            elif nat_roll == 1:
                crit = -1  # crit fail. WARNING: -1 evaluates to true. Use this method appropriately.
        roll_val += nat_roll
    return nat_roll + modifier, crit
