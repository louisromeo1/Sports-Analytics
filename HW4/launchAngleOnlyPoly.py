# Louis Romeo
# CSC 496 HW4
# launchAngleOnlyPoly.py
import sys
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

if len(sys.argv) < 2:
    print("Usage: python launchAngleOnlyPoly.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
data = pd.read_csv(input_file)

# Ensure necessary columns are present
required_columns = ['launch_angle', 'hit_distance_sc']
for col in required_columns:
    if col not in data.columns:
        print(f"Error: Missing column {col} in the input file.")
        sys.exit(1)

# Drop rows with NaN values
data = data.dropna(subset=['launch_angle', 'hit_distance_sc'])

# Select features and target
X = data[['launch_angle']]
y = data['hit_distance_sc']

# Apply polynomial features (degree 2)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Fit polynomial regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions and calculate metrics
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Output the results
print(mse)
print(r2)
for coef in model.coef_:
    print(coef)
print(model.intercept_)
