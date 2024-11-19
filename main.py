import json
import os
import random
from time import sleep
from colored import fg, attr

def startup():
    print("Finding save file...")
    sleep(1)
    if os.path.exists('save.json'):
        print("Save file found.")
    else:
        print("Save file not found.")
        print("Creating save file...")
        sleep(1)
        with open('save.json', 'w') as f:
            f.write('{"name": "Farm", "balance": 100, "inventory": {}}')
        print("Save file created.")

def inventory():
    os.system('cls' if os.name == 'nt' else 'clear')
    with open('save.json', 'r') as f:
        data = json.load(f)
        inventory_data = data['inventory']
        print("Inventory data:")
        if inventory_data:
            for item, amount in inventory_data.items():
                color = {
                    'carrots': 'orange_1',
                    'potatoes': 'yellow',
                    'wheat': 'gold_1'
                }.get(item, 'white')
                print(f"{fg(color)}{item.capitalize()}: {amount}{attr('reset')}")
        else:
            print("Empty")
        input("Press enter to continue...")

def balance():
    os.system('cls' if os.name == 'nt' else 'clear')
    with open('save.json', 'r') as f:
        data = json.load(f)
        balance_data = data['balance']
        print(f"{fg('green')}Balance: {balance_data}{attr('reset')}")
        input("Press enter to continue...")

def harvest():
    crops = ['wheat', 'carrots', 'potatoes']
    harvested_crops = {}
    
    # Read the multiplier from the save file
    with open('save.json', 'r') as f:
        data = json.load(f)
        multiplier = data.get('multiplier', 1)  # Default to 1 if no multiplier is found
    
    for crop in crops:
        if random.random() < 0.5:  # 50% chance to harvest each crop
            amount = random.randint(1, 5)
            harvested_crops[crop] = amount * multiplier  # Apply the multiplier
    
    if harvested_crops:
        with open('save.json', 'r+') as f:
            data = json.load(f)
            for crop, amount in harvested_crops.items():
                if crop in data['inventory']:
                    data['inventory'][crop] += amount
                else:
                    data['inventory'][crop] = amount
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        print("Harvested crops:")
        for crop, amount in harvested_crops.items():
            print(f" - {crop.capitalize()}: {amount}")
    else:
        print("No crops harvested.")
    input("Press enter to continue...")

def sell_crops():
    prices = {'wheat': 4, 'carrots': 2, 'potatoes': 3}
    with open('save.json', 'r+') as f:
        data = json.load(f)
        total_earnings = 0
        for crop, price in prices.items():
            if crop in data['inventory'] and data['inventory'][crop] > 0:
                amount = data['inventory'][crop]
                earnings = amount * price
                total_earnings += earnings
                data['inventory'][crop] = 0
                print(f"Sold {amount} {crop} for {earnings} coins.")
        data['balance'] += total_earnings
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    print(f"Total earnings: {total_earnings} coins.")
    input("Press enter to continue...")

def shop():
    upgrades = {
        'wooden hoe': {'cost': 500, 'multiplier': 1.5},
        'stone hoe': {'cost': 1000, 'multiplier': 2},
        'iron hoe': {'cost': 2000, 'multiplier': 3}
    }
    
    with open('save.json', 'r+') as f:
        data = json.load(f)
        balance = data['balance']
        current_multiplier = data.get('multiplier', 1)
        
        print(f"{fg('blue')}Welcome to the shop!{attr('reset')}")
        print(f"{fg('green')}Your balance: {balance} coins{attr('reset')}")
        print("Available upgrades:")
        for upgrade, info in upgrades.items():
            status = "Owned" if current_multiplier == info['multiplier'] else f"{info['cost']} coins (x{info['multiplier']} multiplier)"
            print(f" - {upgrade.capitalize()}: {status}")
        
        choice = input("Enter the name of the upgrade you want to buy (or 'exit' to leave): ").lower()
        if choice in upgrades:
            if current_multiplier == upgrades[choice]['multiplier']:
                print(f"You already own the {choice.capitalize()}.")
            elif balance >= upgrades[choice]['cost']:
                balance -= upgrades[choice]['cost']
                current_multiplier = upgrades[choice]['multiplier']
                data['balance'] = balance
                data['multiplier'] = current_multiplier
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                print(f"You bought a {choice.capitalize()}! Your new multiplier is x{current_multiplier}.")
            else:
                print("You don't have enough coins.")
        elif choice == 'exit':
            return
        else:
            print("Invalid choice.")
    input("Press enter to continue...")

if __name__ == '__main__':
    startup()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input("1. Inventory\n2. Balance\n3. Harvest\n4. Sell Crops\n5. Shop\n6. Exit\n")
        match choice:
            case "1":
                inventory()
            case "2":
                balance()
            case "3":
                harvest()
            case "4":
                sell_crops()
            case "5":
                shop()
            case "6":
                break
            case _:
                print("Invalid choice.")
                sleep(1)