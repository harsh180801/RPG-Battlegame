from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# create black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 15, 250, "black")

# create white magic
cure = Spell("Cure", 20, 900, "white")
cura = Spell("Cura", 30, 1500, "white")
cureca = Spell("Cureca", 60, 3000, "white")
curecia = Spell("Curecia", 50, 1000, "white")

# add some items
potion = Item("Potion", "potion", "Heals 500 HP", 500)
hipotion = Item("Hi-potion", "potion", "Heals 1000 HP0", 1000)
superpotion = Item("Superpotion", "potion", "Heals 1500 HP", 1500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of any one party member", 99999)
hielixer = Item("Megaelixer", "elixer", "Fully restores HP/MP of the party", 99999)

grenade = Item("Grenade", "attack", "Deals 1500 damage", 1500)

player_spell = [fire, thunder, blizzard, meteor, quake, cure, cura, cureca]
enemy_spell = [fire, thunder, curecia]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 3}, {"item": grenade, "quantity": 3}]
# instantiate Person
player1 = Person("Harsh", 4200, 180, 300, 70, player_spell, player_items)
player2 = Person("Jon  ", 3500, 150, 360, 100, player_spell, player_items)
player3 = Person("Shiva", 4000, 200, 325, 80, player_spell, player_items)

enemy1 = Person("Thanos", 2500, 100, 300, 100, enemy_spell, [])
enemy2 = Person("Ravana", 12000, 500, 700, 25, enemy_spell, [])
enemy3 = Person("Stefan", 2500, 100, 500, 100, enemy_spell, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

defeated_enemies = 0
defeated_players = 0

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)

while running:

    print("\n")
    print("NAME                   HP                                           MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        if defeated_enemies == 3:
            print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
            running = False
            break
        else:
            player.choose_action()
            choice = input("   Choose action: ")
            index: int = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(bcolors.BOLD + player.name + " attacked " + enemies[enemy].name + " for", dmg, "points of damage."
                  + bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(bcolors.FAIL + enemies[enemy].name + " has died." + bcolors.ENDC)
                del enemies[enemy]
                defeated_enemies += 1

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("   Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYOU DO NOT HAVE ENOUGH MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "amount of damage to "
                      + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name + " has died." + bcolors.ENDC)
                    del enemies[enemy]
                    defeated_enemies += 1

        elif index == 2:
            player.choose_items()
            item_choice = int(input("   Choose Item: ")) - 1

            if item_choice == -1:
                continue

            Item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left because you used all of it." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if Item.type == "potion":
                player.heal(Item.prop)
                print(bcolors.OKGREEN + "\n" + Item.name + " heals for", str(Item.prop), "HP" + bcolors.ENDC)
            elif Item.type == "elixer":

                if Item.name == "Megaelixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + Item.name + " fully restored HP/MP" + bcolors.ENDC)
            elif Item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(Item.prop)

                print(bcolors.FAIL + "\n" + Item.name + " deals for", str(Item.prop), "points of damage to "
                      + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name + " has died." + bcolors.ENDC)
                    del enemies[enemy]
                    defeated_enemies += 1

    # check if we have won
    if defeated_enemies == 3:
        print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
        running = False
        break
    
    # enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # choose attack
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name + " attacks " + players[target].name + " for", enemy_dmg, "points of damage.")

            if players[target].get_hp() == 0:
                print(bcolors.FAIL + bcolors.BOLD + players[target].name + " has died!" + bcolors.ENDC)
                del players[target]
                defeated_players += 1

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + " for", str(magic_dmg), "HP."
                      + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, len(players))
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + enemy.name + "'s " + spell.name + " deals", str(magic_dmg),
                      "amount of damage to " + players[target].name + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD + players[target].name + " has died!")
                    del players[target]
                    defeated_players += 1

    # check if enemy has won
    if defeated_players == 3:
        print(bcolors.FAIL + "ENEMIES HAVE DEFEATED YOU" + bcolors.ENDC)
        running = False
        break
