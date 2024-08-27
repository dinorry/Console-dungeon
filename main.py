#only one room(no doors), without graphic interface
import json
from random import randrange, randint


class Room() :
    def __init__ (self) :
        self.chest_generator_int = randrange(10)
        self.monster_generator_int = randrange(10)
        self.contains_chest = False
        self.contains_monster = False
        if self.monster_generator_int >2 :
            if self.chest_generator_int > 5 :
                self.contains_chest = True
        else :
            if self.chest_generator_int > 7 :
                self.contains_chest = True



class Chest() :
    def __init__(self):
        self.amount_of_gold = randint(1,5)

class Monster() :
    max_gold = 30
    max_xp = 25
    max_hp =20
    max_armor = 3
    max_attack = 8
    product_of_stats = max_hp * max_attack * max_armor

    def __init__(self):
        self.max_hp = randint(5, Monster.max_hp)
        self.curr_hp = self.max_hp
        self.armor = randint(1,Monster.max_armor)
        self.attack = randint(2,Monster.max_attack)
        self.coefficient  = self.max_hp * self.armor * self.attack / Monster.product_of_stats
        self.gold = int(self.coefficient * Monster.max_gold)
        self.xp = int(self.coefficient * Monster.max_xp)

    def is_alive(self):
        if self.curr_hp > 0 :
            return True
        else :
            return False

class Character () :


    #arrays for lvlups
    attack_list = [3]
    armor_list = [1]
    hp_list = [10]
    for i in range(19) :
        attack_list.append(attack_list[i] * 1.09)
        armor_list.append(armor_list[i] * 1.11)
        hp_list.append(hp_list[i] * 1.1)

    for i in range(len(attack_list)) :
        attack_list[i]  = int(attack_list[i])
        armor_list[i] = int(armor_list[i])
        hp_list[i] = int(hp_list[i])

    armor_list[14]  = 3
    armor = armor_list[:15]

    for i in range(5) :
        armor.insert(0,0)

    #XP
    first_lvlup_cost = 10
    change_of_xp_for_lvlup = 1.15
    last_lvl = 20

    xp_list = [first_lvlup_cost]
    for i in range(last_lvl-2) :
        xp_list.append(int(xp_list[i] * change_of_xp_for_lvlup))
    xp_list.append(90)
    #==> end
    total_xp = sum(xp_list)



    def __init__(self):
        self.score = 0
        self.lvl_next_round = 1
        self.lvl = 1
        self.max_hp = 10
        self.curr_hp = self.max_hp
        self.attack = self.attack_list[self.lvl-1]
        self.armor = self.armor_list[self.lvl-1]
        self.gold = 0
        self.xp = 0
    def __repr__(self):
        return 'lvl: {},\nmax_hp: {},\nattack: {}\narmor: {}'.format(self.lvl, self.max_hp, self.attack, self.armor)

    def is_alive(self) :
        if self.curr_hp > 0 :
            return True
        else :
            return False

    def set_lvl_to(self, lvl) :
        self.lvl = lvl
        self.update_stats_for_new_lvl()

    def update_stats_for_new_lvl (self) :
        self.max_hp = self.hp_list[self.lvl-1]
        self.armor = self.armor_list[self.lvl - 1]
        self.attack = self.attack_list[self.lvl-1]
        self.xp = 0

    def lvlup(self):
        self.lvl += 1
        self.update_stats_for_new_lvl()

    def  calculate_score(self):
        self.score = self.xp + self.gold

    def  calculate_lvl_in_next_game(self) :
        self.lvl_next_round = int(self.score / Character.total_xp * 20 *0.8)





def fight(monster, character) :
    c_damage = character.attack - monster.armor
    m_damage = monster.attack-character.armor

    #returns True if monster is still alive
    def attack_monster() :
        monster.curr_hp -= c_damage
        if monster.curr_hp < 0:
            print('You defeated the monster with your last blow of {} damage'.format_map(c_damage))
            return False
        else :
            print('You attack the monster dealing him {} points of damage. He now has {} HP'.format(c_damage, monster.curr_hp))
            return True

    # returns True if character is still alive
    def attack_character()  :
        character.curr_hp -= m_damage
        if character.curr_hp <= 0:
            print('You lost your last {} HPs.'.format(m_damage))
        else:
            print('Monster attacks you dealing yourself {} points of damage. Your HP reduced to {}.'.format(m_damage, character.curr_hp))

    while True :
        input()
        attack_monster()
        if not monster.is_alive() :
            input()
            defeat_monster(monster, character)
            return True
        input()
        attack_character()
        if not character.is_alive() :
            return False



# returns true if reply contains reply_one
# false if reply two
def ask_question(question, reply_one, reply_two=None) :
    user_input = input(question)
    if reply_one in user_input[:len(reply_one)] :
        return True
    elif not reply_two is None and reply_two in user_input[:len(reply_two)] :
        return False
    else :
        ask_question(question, reply_one, reply_two)


def save_lost(character) :
    with open('Save.txt', 'w')  as save :
        dic ={"Level" : character.lvl_next_round}
        save.write(str(dic))

def defeat_monster(monster, character) :
    character.xp += monster.xp
    character.gold += monster.gold


def kill_character (character) :
    character.calculate_score()
    character.calculate_lvl_in_next_game()
    print('Unfortunately you are dead now :<\nWell played though.\nYou have reached a score of {} this time'.format(character.score))
    if character.lvl_next_round > 1 :
        print("Next time your starting level will be {} because of you score.".format(character.score, character.lvl_next_round))


input("Press enter to create your character...")
main_character = Character()


with open('save.json') as save_file :
    dic_of_file = json.load(save_file)
    if dic_of_file['LVL_NEXT_ROUND'] > 1 :
        main_character.set_lvl_to(dic_of_file['LVL_NEXT_ROUND'])
        print('You start with level {}.'.format(main_character.lvl))

print('Your stats are :\n', main_character)


print("You wake up in a dark place, your back hearts. Apparently you fell down into a cave. You see a door before you "
      "\n")
input_1 = input('Press enter key to enter the door...')

rooms = [Room()]
rooms[0].contains_monster = True
print('You enter the room', end = '')


while main_character.is_alive():
    if rooms[-1].contains_monster :
        print(', you see a monster in front of you.')
        monster = Monster()
        print('The monster has {} hit points,\n his attack is {},\n his armor is {}.'.format(monster.max_hp, monster.attack, monster.armor))
        print('Would you like to fight him or runaway')
        want_to_fight = ask_question('Press f and hit enter to fight,\nhit r followed by enter to runaway\n', 'f', 'r')

        character_won_the_fight = fight(monster, main_character)

        if not character_won_the_fight :
            break
        else:
            print("You won the fight.\n Monster is defeated.")
            print("You get {} XP and {} gold.".format(monster.xp, monster.gold))
            print("There is a door on the back wall of the room.")
    else :
       print(". The room is empty.\n But there is a door on the back wall.")

    input('Press enter to continue...')
    print('You enter a new room', end = '')

kill_character(main_character)
if main_character.lvl_next_round > 1 :
    print('Your you will start next game with the level {}.')

save_file_dict = {"LVL_NEXT_ROUND" : main_character.lvl_next_round}
with open("save.json", 'w') as save_file :
    save_file.write(json.dumps(save_file_dict))