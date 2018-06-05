import random
import warnings

def ability_to_mod(score):
    if score < 1:
        raise ValueError("Ability score too low (did you input a modifier?)")
    elif score > 30:
        raise ValueError("Ability score too high (did you add an extra digit?)")
    return (score -10) // 2

def validate_dice(dice):
    if isinstance(dice, tuple):  # lists are mutable and that could be a problem
        if len(dice) != 2:
            raise ValueError("Must provide exactly two values: number of dice and type of dice (1, 6)")
        if not isinstance(dice[0], int) or not isinstance(dice[1], int):
            raise ValueError("Must provide exactly two integer values: number of dice and type of dice (1, 6)")
    elif isinstance(dice, str):
        try:
            dice = tuple(int(x) for x in dice.split("d"))
        except ValueError:
            raise ValueError("Must provide damage dice in tuple of two ints (1, 6) or string format 1d6")
        if len(dice) != 2:
            raise ValueError("Must provide damage dice in tuple of two ints (1, 6) or string format 1d6")
    else:
        raise ValueError("Must provide damage dice in tuple of two ints (1, 6) or string format 1d6")
    return dice

def roll_dice(dice_type, num=1, modifier=0, adv=0, critable=False):  # -1 for disadvantage, 0 for normal, 1 for advantage
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
    return roll_val + modifier, crit

def cr_to_xp(cr):
    if not cr:
        return 10  # because this is combat simulation, assume these are the ones that have attacks and thus are worth 10xp
    return cr * 200

def calc_advantage(advs):  # Note: does not sanitize input. User must use appropriately
    sum = 0
    for adv in advs:
        sum += adv
    if sum == 0:
        return 0
    if sum > 0:
        return 1
    if sum < 0:
        return -1

def time_to_rounds(time_var):
    if isinstance(time_var, str):
        time_list = time_var.split(" ")
        try:
            time_list[0] = int(time_list[0])
            if time_list[0] <= 0:
                raise ValueError()
        except ValueError:
            raise ValueError("Time must be a positive integer")

    elif isinstance(time_var, (tuple, list)):
        time_list = time_var
    else:
        raise ValueError("Must provide string (\"1 minute\") or tuple/list (1, \"minute\")")
    if time_list[1] not in ["minute", "minutes", "hour", "hours", "round", "rounds"]:
        raise ValueError("Unit must be minutes, hours, or rounds; e.g., 1 minute")
    if "round" in time_list[1]:
        return time_list[0]
    if "minute" in time_list[1]:
        return time_list[0] * 10
    if "hour" in time_list[1]:
        return time_list[0] * 100
