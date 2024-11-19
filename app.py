from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import random

app = Flask(__name__)
app.secret_key = "very_secret"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return "Passwords do not match", 400
        
        with open('users.json', 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            data[username] = {'email': email, 'password': password}
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.json', 'r') as f:
            data = json.load(f)
            if data.get(username) and data[username]['password'] == password:
                session['username'] = username
                session['email'] = data[username]['email']
                return redirect(url_for('home'))
    return render_template('login.html')  

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/inventory')
def inventory():
    with open('save.json', 'r') as f:
        data = json.load(f)
        inventory_data = data['inventory']
        if inventory_data:
            return render_template('inventory.html', inventory_data=inventory_data)
        else:
            return "Empty"
        
@app.route('/balance')
def balance():
    with open('save.json', 'r') as f:
        data = json.load(f)
        balance_data = data['balance']
        return f"Balance: {balance_data}"
    
@app.route('/harvest')
def harvest():
    crops = ['wheat', 'carrots', 'potatoes']
    harvested_crops = {}
    
    # Read the multiplier from the save file
    with open('save.json', 'r') as f:
        data = json.load(f)
        multiplier = data.get('multiplier', 1)

    for crop in crops:
        if random.random() < 0.5:
            amount = random.randint(1, 5)
            harvested_crops[crop] = amount * multiplier

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
        return harvested_crops
    else:
        return "No crops harvested."
    
@app.route('/sell_crops')
def sell_crops():
    with open('save.json', 'r+') as f:
        data = json.load(f)
        total = 0
        for crop, amount in data['inventory'].items():
            price = {
                'carrots': 1,
                'potatoes': 2,
                'wheat': 3
            }.get(crop, 0)
            total += price * amount
        data['balance'] += total
        data['inventory'] = {}
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    return f"Sold crops for {total}. Balance: {data['balance']}"

@app.route('/game')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)