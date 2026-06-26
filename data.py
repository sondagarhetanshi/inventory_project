import pandas as pd

inventory = pd.DataFrame({
    "ProductID": [101,102,103,104,105],
    "ProductName": ["Laptop","Mouse","Keyboard","Chair","Table"],
    "Category": ["Electronic","Electronic","Electronic","Furniture","Furniture"],
    "Stock": [50,200,150,80,40],
    "Price": [50000,500,1000,3000,5000]
})

orders = pd.DataFrame({
    "OrderID": [1,2,3,4,5,6,7],
    "ProductID": [101,102,103,102,104,105,102],
    "Quantity": [2,10,5,20,3,2,15],
    "Month": ["Jan","Jan","Feb","Feb","Mar","Mar","Apr"]
})