from bs4 import BeautifulSoup
import urllib.request

def read_from_open5e(url):
    soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
    soup = soup.body.div.section.div.div.find_all("div")[1].div.div
    name = soup.h1.get_text().replace("¶", "")
    print("name:", name)
    sections = soup.find_all("p")
    race_alignment, armor_class, hp, speed = sections

    print(sections)
    stuff = ["ac", "hp", "speed", "saving throws", "skills"]
    # print(soup.get_text())

def read_from_d20srd(url, outname=None):
    if outname:
        outfile = open(outname, "a")
    soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
    soup = soup.body
    name = soup.h1.get_text()
    if outname:
        outfile.write("class %s(combatant.Creature):\n" % name)
        outfile.write("\tdef __init__(self, **kwargs):\n")
        outfile.write("\t\tdefault_kwargs = {")
    else:
        print("Name:", name)
    paragraphs = soup.find_all("p")
    # print(paragraphs)
    ac_hp_speed = paragraphs[1].contents
    # print(ac_hp_speed)
    ac = 0
    hp = 0
    speed = 0
    for idx in range(len(ac_hp_speed)):
        line = ac_hp_speed[idx]
        if "Armor Class" in line:
            ac = ac_hp_speed[idx+1].strip()
            ac = ac.split()[0]  # get just the number
            ac = int(ac)
            if outname:
                outfile.write('"ac": %d, ' % ac)
            else:
                print("AC:", ac)
        elif "Hit Points" in line:
            hp = ac_hp_speed[idx+1].strip()
            hp = hp.split()[0]  # get just the number
            hp = int(hp)
            if outname:
                outfile.write('"max_hp": %d, ' % hp)
            else:
                print("HP:", hp)
        elif "Speed" in line:
            speed = int(ac_hp_speed[idx+1].strip().split()[0])  # TODO: figure out how to handle this data
            if outname:
                outfile.write('"speed": %d,\n' % speed)
            else:
                print("Speed:", speed)
    attribute_table = soup.table.tbody.tr
    scores = [int(x.get_text().split("(")[0]) for x in attribute_table.find_all("td")]
    strength, dexterity, constitution, intelligence, wisdom, charisma = scores
    if outname:
        outfile.write('\t\t\t"strength": %d, "dexterity": %d, "constitution": %d, "intelligence": %d, "wisdom": %d, "charisma": %d}\n' %
                      (strength, dexterity, constitution, intelligence, wisdom, charisma))
    else:
        print("Str:", strength)
        print("Dex:", dexterity)
        print("Con:", constitution)
        print("Int:", intelligence)
        print("Wis:", wisdom)
        print("Cha:", charisma)
    save_skill_sense_lang_challenge = paragraphs[2].contents
    saving_throws = {}
    vision = "normal"
    cr = 0
    for idx in range(len(save_skill_sense_lang_challenge)):
        line = save_skill_sense_lang_challenge[idx]
        if "Saving Throws" in line:
            saving_throw_str = save_skill_sense_lang_challenge[idx+1].strip()
            saving_throw_list = saving_throw_str.split(", ")
            for str_value in saving_throw_list:
                ability, mod = str_value.split()
                sign = mod[0]
                if sign == "+":
                    mod = int(mod[1:])
                elif sign == "-":
                    mod = int(mod[1:]) * -1
                if ability == "Str":
                    saving_throws.update({"strength": mod})
                elif ability == "Dex":
                    saving_throws.update({"dexterity": mod})
                elif ability == "Con":
                    saving_throws.update({"constitution": mod})
                elif ability == "Wis":
                    saving_throws.update({"wisdom": mod})
                elif ability == "Int":
                    saving_throws.update({"intelligence": mod})
                elif ability == "Cha":
                    saving_throws.update({"charisma": mod})
        elif "Senses" in line:
            vision_line = save_skill_sense_lang_challenge[idx+1]
            if "truesight" in vision_line:
                vision = "truesight"
            elif "blindsight" in vision_line:
                vision = "blindsight"
            elif "darkvision" in vision_line:
                vision = "darkvision"
        elif "Challenge" in line:
            challenge_line = save_skill_sense_lang_challenge[idx+1].strip()
            cr = int(challenge_line.split()[0])
    if outname:
        outfile.write("\t\tdefault_kwargs.update({\"saving_throws\": %s})\n" % str(saving_throws))
        outfile.write("\t\tdefault_kwargs.update({'vision': \"%s\", 'cr': %d})\n" % (vision, cr))
    else:
        print("Saving throws:", saving_throws)
        print("Vision:", vision)
        print("CR:", cr)
    attack_paragraphs = paragraphs[3:]
    attack_stats = {}
    for attack_stuff in attack_paragraphs:
        text = attack_stuff.get_text()
        try:
            attack_name = attack_stuff.em.strong.get_text().replace(".", "")
        except AttributeError:
            continue
        attack_stats[attack_name] = {}
        if "Melee Weapon Attack" in text:
            text = text.split("Melee Weapon Attack: ")[1]
            to_hit, reach = text.split(", ")[:2]  # TODO: care about number of targets
            to_hit = to_hit.split(" to hit")[0]
            sign = to_hit[0]
            if sign == "+":
                to_hit = int(to_hit[1:])
            elif sign == "-":
                to_hit = int(to_hit[1:]) * -1
            attack_stats[attack_name]["attack_mod"] = to_hit
            reach = reach.split("reach ")[1]
            reach = reach.split(" ft")[0]
            reach = int(reach)
            attack_stats[attack_name]["melee_range"] = reach
            damage_str = text[text.find("Hit: "): text.find("damage.")]
            damage_str = damage_str.replace("Hit: ", "").replace("(", "").replace(")","").replace(" + ", " ")
            avg_damage, dice, damage_mod, damage_type = damage_str.split()
            attack_stats[attack_name]["dice"] = dice
            attack_stats[attack_name]["damage_mod"] = int(damage_mod)
            attack_stats[attack_name]["damage_type"] = damage_type
            if text.find("damage.") + 8 < len(text):
                attack_stats[attack_name]["more_content"] = True
            else:
                attack_stats[attack_name]["more_content"] = False
    if outname:
        outfile.write("\t\t# the following lines are things that may be features or attacks. Refer to the original source to see what you want to incorporate.\n")
        outfile.write('\t\t"""\n')
        for attack_name in attack_stats:
            if attack_stats[attack_name]:
                outfile.write("\t\tattack_class.Attack(dice=%s, attack_mod=%d, damage_mod=%d, damage_type=%s, name=%s)" %
                              (attack_stats[attack_name]["dice"], attack_stats[attack_name]["attack_mod"],
                               attack_stats[attack_name]["damage_mod"], attack_stats[attack_name]["damage_type"],
                               attack_name))
                if attack_stats[attack_name]["more_content"]:
                    outfile.write(" # there is more to this attack. Refer to the original source\n")
                else:
                    outfile.write("\n")
            else:
                outfile.write("\t\t%s\n" % attack_name)
        outfile.write('\t\t"""\n')
        outfile.write("\t\tkwargs.update(default_kwargs)\n")
        outfile.write("\t\tsuper().__init__(**kwargs)\n")
    else:
        print(attack_stats)
    if outname:
        outfile.close()

read_from_d20srd("http://5e.d20srd.org/srd/monsters/aboleth.htm", "bestiary.py")