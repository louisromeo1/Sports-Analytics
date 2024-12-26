# Louis Romeo
# CSC 496 HW4
# launchDistLinear.py
import sys
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

if len(sys.argv) < 2:
    print("Usage: python launchDistLinear.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
data = pd.read_csv(input_file)

required_columns = ['launch_angle', 'launch_speed', 'hit_distance_sc']
for col in required_columns:
    if col not in data.columns:
        print(f"Error: Missing column {col} in the input file.")
        sys.exit(1)

X = data[['launch_angle', 'launch_speed']]
y = data['hit_distance_sc']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(mse)
print(r2)
for coef in model.coef_:
    print(coef)
print(model.intercept_)
