import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_sales():

    # Dummy historical data
    data = pd.DataFrame({
        "MonthNo": [1,2,3,4,5,6],
        "Sales": [10000,12000,15000,17000,20000,23000]
    })

    X = data[["MonthNo"]]
    y = data["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict next month
    next_month = [[7]]
    prediction = model.predict(next_month)

    return prediction[0]
