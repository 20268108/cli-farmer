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
        if inventory_data:
            print("Inventory data:")
            for item, amount in inventory_data.items():
                if item == 'carrots':
                    print(f"{fg('orange_1')}{item.capitalize()}: {amount}{attr('reset')}")
                elif item == 'potatoes':
                    print(f"{fg('yellow')}{item.capitalize()}: {amount}{attr('reset')}")
                elif item == 'wheat':
                    print(f"{fg('gold_1')}{item.capitalize()}: {amount}{attr('reset')}")
                else:
                    print(f"{item.capitalize()}: {amount}")
        else:
            print("Inventory data: empty")
        print("Press enter to continue...")
        input("")

def balance():
    os.system('cls' if os.name == 'nt' else 'clear')
    with open('save.json', 'r') as f:
        data = json.load(f)
        balance_data = data['balance']
        print(f"{fg("green")}Balance data: {attr('reset')}", balance_data)
        print("Press enter to continue...")
        input("")

def harvest():
    crops = ['wheat', 'carrots', 'potatoes']
    harvested_crops = {}
    
    for crop in crops:
        if random.random() < 0.5:  # 50% chance to harvest each crop
            amount = random.randint(1, 5)
            harvested_crops[crop] = amount
    
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
        print("Harvested crops:", harvested_crops)
    else:
        print("No crops harvested.")
    print("Press enter to continue...")
    input("")

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
    print("Press enter to continue...")
    input("")

if __name__ == '__main__':
    startup()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input("1. Inventory\n2. Balance\n3. Harvest\n4. Sell Crops\n5. Exit\n")
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
                break
            case _:
                print("Invalid choice.")
                sleep(1)
