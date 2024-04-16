from pwn import *
import os
import json

# os.system('clear')

filename = './trading-firebase_bkup.json'
with open(filename, 'r') as f:
    content = json.load(f) # read the json data

# get the person with the highest profit percentage
highest_profit = max(content.values(), key=lambda x: x['profit_percentage'])

log.success(f"EMAIL ADDRESS: {highest_profit['email']}")
log.success(f"PROFIT PERCENTAGE: {highest_profit['profit_percentage']}")
