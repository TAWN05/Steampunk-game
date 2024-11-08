import random


# Character class to define different types of characters with unique attributes and steampunk themes
class CharacterClass:
    def __init__(self, name, strength, agility, magic):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.magic = magic


# Player class to hold player stats, inventory, and methods
class Player:
    def __init__(self, char_class):
        self.character_class = char_class
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.equipment = {
            'weapon': None,
            'armor': None,
            'gadget': None,
            'artifact': None
        }
        self.level = 1
        self.story_path = []  # Stores story choices

    def show_inventory(self):
        print("\nInventory:")
        if not self.inventory:
            print("  (empty)")
        else:
            for i, item in enumerate(self.inventory, 1):
                print(f"  {i}. {item['name']}")

    def show_equipment(self):
        print("\nCurrent Equipment:")
        for slot, item in self.equipment.items():
            item_name = item['name'] if item else "(empty)"
            print(f"  {slot.capitalize()}: {item_name}")

    def equip_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory.pop(item_index)
            if item['type'] in self.equipment:
                print(f"\nEquipping {item['name']}...")
                self.equipment[item['type']] = item
                print(f"{item['name']} equipped in {item['type']} slot.")
            else:
                print("\nCannot equip this item.")
        else:
            print("\nInvalid item selection.")

    def use_gadget(self):
        if self.equipment['gadget']:
            gadget = self.equipment['gadget']
            gadget_damage = random.randint(8, 15) + self.character_class.magic
            print(f"\nYou use {gadget['name']} and deal {gadget_damage} magic damage.")
            return gadget_damage
        else:
            print("\nYou have no gadget equipped.")
            return 0  # No damage if no gadget equipped

    def attack(self):
        if self.equipment['weapon']:
            weapon = self.equipment['weapon']
            damage_roll = random.randint(weapon['damage_min'], weapon['damage_max']) + self.character_class.strength
            print(f"\nYou attack with {weapon['name']} and deal {damage_roll} damage.")
            return damage_roll
        else:
            print("\nYou have no weapon equipped and deal 1 damage.")
            return 1  # Base damage if no weapon


# Enemy class to handle enemy stats and actions with steampunk themes
class Enemy:
    def __init__(self, level, name, special_ability=None):
        self.name = name
        self.level = level
        self.health = 50 + (level * 15)  # Increased scaling for dark fantasy steampunk setting
        self.damage = 6 + (level * 3)
        self.special_ability = special_ability

    def attack(self):
        damage = random.randint(4, 10) + (self.level // 2)  # Higher base roll
        print(f"\nThe {self.name} attacks with a whir of gears and deals {damage} damage.")
        return damage


# Create a list of character classes with steampunk themes
char_classes = {
    'engineer': CharacterClass('Engineer', strength=4, agility=3, magic=2),
    'clockwork mage': CharacterClass('Clockwork Mage', strength=2, agility=3, magic=6),
    'gearbound rogue': CharacterClass('Gearbound Rogue', strength=3, agility=5, magic=3)
}


# Function to handle player's choice of character class
def choose_character_class():
    print("\nChoose your character class:")
    for class_name in char_classes:
        print(
            f"  {class_name.capitalize()} (Strength: {char_classes[class_name].strength}, Agility: {char_classes[class_name].agility}, Magic: {char_classes[class_name].magic})")
    while True:
        choice = input("\nEnter your class (engineer, clockwork mage, gearbound rogue): ").lower()
        if choice in char_classes:
            return char_classes[choice]
        else:
            print("\nInvalid choice. Please choose a valid character class.")


# Function to create steampunk-themed loot
def generate_loot(level):
    loot_table = [
        {'name': 'Cogblade', 'type': 'weapon', 'damage_min': 4, 'damage_max': 10 + level},
        {'name': 'Brass Shield', 'type': 'armor', 'armor_value': 7},
        {'name': 'Steam Rifle', 'type': 'weapon', 'damage_min': 5, 'damage_max': 12 + level},
        {'name': 'Arcane Gauntlet', 'type': 'gadget', 'magic_bonus': 3},
        {'name': 'Restorative Elixir', 'type': 'potion', 'heal': 30}
    ]
    return random.choice(loot_table)


# Function for turn-based combat with steampunk twists
def combat(player, enemy):
    while enemy.health > 0 and player.health > 0:
        print(f"\n--- Current Health: {player.health} ---")
        print(f"\n{enemy.name} - Health: {enemy.health}")
        print("Choose an action: attack, defend, use gadget, inventory, equipment, run")
        action = input("Your choice: ").lower()

        if action == 'attack':
            damage = player.attack()
            enemy.health -= damage
            if enemy.health <= 0:
                print(f"\nYou dismantled the {enemy.name}!")
                loot = generate_loot(player.level)
                print(f"\nYou found loot: {loot['name']}")
                player.inventory.append(loot)
                break
            else:
                damage_taken = enemy.attack()
                player.health -= damage_taken

        elif action == 'defend':
            print("\nYou raise your brass shield to defend.")
            reduced_damage = max(0, enemy.attack() - (player.character_class.agility + 2))
            player.health -= reduced_damage
            print(f"You take {reduced_damage} damage after defending.")

        elif action == 'use gadget':
            gadget_damage = player.use_gadget()
            if gadget_damage > 0:
                enemy.health -= gadget_damage
                if enemy.health <= 0:
                    print(f"\nYou overpowered the {enemy.name} with your gadget!")
                    break

        elif action == 'inventory':
            player.show_inventory()

        elif action == 'equipment':
            player.show_equipment()

        elif action == 'run':
            if random.random() < 0.5:
                print("\nYou escaped into the steam-filled shadows!")
                return False  # Combat not resolved, but player escaped
            else:
                print("\nYou failed to escape and the enemy strikes!")
                damage_taken = enemy.attack()
                player.health -= damage_taken

        else:
            print("\nInvalid action. Try again.")

        if player.health <= 0:
            print("\nYour gears grind to a halt. You have been defeated.")
            return False

    return True  # Combat resolved


# Main game loop with steampunk locations
def main_game():
    print("Welcome to the Dark Fantasy Steampunk Adventure!")
    char_class = choose_character_class()
    player = Player(char_class)

    scenarios = ["The Clockwork Graveyard", "The Steam-Powered Citadel", "The Rusted Laboratory"]
    for scenario in scenarios:
        print(f"\n--- You enter {scenario} ---")
        enemy = Enemy(player.level, f"{random.choice(['Clockwork Sentinel', 'Brass Golem', 'Steam Phantom'])}")

        combat_result = combat(player, enemy)
        if not combat_result:
            break  # Exit game loop if player is defeated

        # Decision points with steampunk-themed outcomes
        decision = input(
            "\nYou find an ancient steam engine with gears still turning. Do you repair or sabotage it? (repair/sabotage): ").lower()
        if decision == 'repair':
            print("\nYou restore the engine to life, unlocking new paths in the mechanical underworld.")
            player.story_path.append("repair")
        elif decision == 'sabotage':
            print(
                "\nYou sabotage the engine, causing a chain reaction of explosions. You gain notoriety among rogue inventors.")
            player.story_path.append("sabotage")
        else:
            print("\nYou ignore the engine and move on, missing an opportunity.")
            player.story_path.append("neutral")

        player.level += 1
        player.health = player.max_health  # Restore health at the end of each level

    # Determine the ending based on story choices
    if 'repair' in player.story_path and 'sabotage' not in player.story_path:
        print("\nYour journey ends as the Architect of Progress.")
    elif 'sabotage' in player.story_path:
        print("\nYour legacy is one of chaos as the Rebel Engineer.")
    else:
        print("\nYou remain an enigmatic figure, remembered only in whispers.")

    print("\n--- Game Over ---")


# Run the game
if __name__ == "__main__":
    main_game()