import combatant
import attack_class

class Aboleth(combatant.Creature):
	def __init__(self, **kwargs):
		default_kwargs = {"ac": 17, "max_hp": 135, "speed": 10,
			"strength": 21, "dexterity": 9, "constitution": 15, "intelligence": 18, "wisdom": 15, "charisma": 18}
		default_kwargs.update({"saving_throws": {'intelligence': 8, 'constitution': 6, 'wisdom': 6}})
		default_kwargs.update({'vision': "darkvision", 'cr': 10})
		# the following lines are things that may be features or attacks. Refer to the original source to see what you want to incorporate.
		"""
		attack_class.Attack(dice=3d6, attack_mod=9, damage_mod=5, damage_type=bludgeoning, name=Tail)
		Amphibious
		attack_class.Attack(dice=2d6, attack_mod=9, damage_mod=5, damage_type=bludgeoning, name=Tentacle) # there is more to this attack. Refer to the original source
		Enslave (3/Day)
		Multiattack 
		Psychic Drain (Costs 2 Actions)
		Mucous Cloud
		Probing Telepathy
		Tail Swipe
		Detect 
		"""
		kwargs.update(default_kwargs)
		super().__init__(**kwargs)
