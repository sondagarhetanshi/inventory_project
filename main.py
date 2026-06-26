from data import inventory, orders
from analysis import run_analysis
from visual import run_visuals

print("===== INVENTORY ANALYTICS SYSTEM =====")

run_analysis(inventory, orders)
run_visuals(inventory, orders)