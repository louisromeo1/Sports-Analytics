# Louis Romeo
# CSC 496 HW4
# launchLogitLinear.py

import sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

if len(sys.argv) < 2:
    print("Usage: python launchLogitLinear.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
data = pd.read_csv(input_file)

# Ensure necessary columns are present
required_columns = ['launch_speed', 'launch_angle', 'woba_value']
for col in required_columns:
    if col not in data.columns:
        print(f"Error: Missing column {col} in the input file.")
        sys.exit(1)

# Create a binary target: 1 if woba_value > 0, else 0 (proxy for home run)
data['is_home_run'] = data['woba_value'].apply(lambda x: 1 if x > 0 else 0)

# Drop rows with NaN values
data = data.dropna(subset=['launch_speed', 'launch_angle'])

# Select features and target
X = data[['launch_speed', 'launch_angle']]
y = data['is_home_run']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions and calculate metrics
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Output the results
print(mse)
print(r2)
for coef in model.coef_[0]:
    print(coef)
