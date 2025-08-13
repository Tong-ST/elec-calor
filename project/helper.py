import requests
from flask import redirect, render_template, session

location_array = [
    ["custom", "Custom unit rate 🌐", 1.00],
    ["th", "Thailand 🇹🇭", 4.00],       
    ["us", "United States 🇺🇸", 0.15],  
    ["uk", "United Kingdom 🇬🇧", 0.34], 
    ["au", "Australia 🇦🇺", 0.30],      
    ["jp", "Japan 🇯🇵", 27.00],         
    ["sg", "Singapore 🇸🇬", 0.30],      
    ["de", "Germany 🇩🇪", 0.40],       
    ["in", "India 🇮🇳", 8.00],
    ["cn", "China 🇨🇳", 0.55],
]

appliance_array = [
    ['default', 'Custom Appliance', None, None, 'Hour per day', 1.0],

    # Cooling / Heating
    ['air', 'Air Conditioner', 2000, 8, 'Hour per day', 0.9],
    ['fan', 'Electric Fan', 75, 6, 'Hour per day', 0.9],
    ['heater', 'Space Heater', 1500, 4, 'Hour per day', 1.0],
    ['fridge', 'Refrigerator', 150, 24, 'Hour per day', 0.8],

    # Kitchen
    ['microwave', 'Microwave Oven', 1200, 15, 'Minute per day', 1.0],
    ['rice', 'Rice Cooker', 700, 1, 'Hour per day', 1.0],
    ['toaster', 'Toaster', 800, 5, 'Minute per day', 1.0],
    ['kettle', 'Electric Kettle', 1500, 10, 'Minute per day', 1.0],
    ['blender', 'Blender', 300, 5, 'Minute per day', 1.0],
    ['coffee', 'Coffee Maker', 1000, 10, 'Minute per day', 1.0],

    # Laundry
    ['washer', 'Washing Machine', 500, 1, 'Hour per day', 0.9],
    ['dryer', 'Clothes Dryer', 3000, 1, 'Hour per day', 0.9],
    ['iron', 'Electric Iron', 1200, 30, 'Minute per day', 1.0],

    # Entertainment / Electronics
    ['tv', 'LED TV (42 inch)', 80, 4, 'Hour per day', 0.95],
    ['laptop', 'Laptop', 60, 6, 'Hour per day', 0.95],
    ['desktop', 'Desktop PC', 250, 6, 'Hour per day', 0.95],
    ['console', 'Game Console', 200, 2, 'Hour per day', 0.95],
    ['speaker', 'Home Speaker System', 100, 2, 'Hour per day', 0.95],
    ['tablet', 'Tablet', 15, 3, 'Hour per day', 0.95],
    ['phone', 'Smartphone Charging', 5, 2, 'Hour per day', 0.95],
    ['smartwatch', 'Smartwatch Charging', 2, 1, 'Hour per day', 0.95],

    # Lighting
    ['led', 'LED Light Bulb', 10, 5, 'Hour per day', 0.95],
    ['cfl', 'CFL Light Bulb', 15, 5, 'Hour per day', 0.95],
    ['incandescent', 'Incandescent Bulb', 60, 5, 'Hour per day', 1.0],
    ['lamp', 'Desk Lamp (LED)', 8, 4, 'Hour per day', 0.95],

    # Misc
    ['vacuum', 'Vacuum Cleaner', 1000, 20, 'Minute per day', 0.9],
    ['hairdryer', 'Hair Dryer', 1500, 10, 'Minute per day', 1.0],
    ['shower', 'Electric Shower Heater', 3500, 15, 'Minute per day', 1.0],
    ['pump', 'Water Pump', 750, 10, 'Minute per day', 0.9],
    ['purifier', 'Air Purifier', 50, 8, 'Hour per day', 0.95],
]

watt_to_kWh = 1000.0

def calculate_unit(amount, power_usage, usage_per_day, power_factor):
    total_watt = amount * (power_usage * power_factor)
    unit_per_day = (total_watt / watt_to_kWh) * (usage_per_day / 60)
    
    return unit_per_day

def update_format(value):
    return f"{value:,.2f}"

def apology(message, next_link="/", code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message), redirect_link=next_link), code 

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False