import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Louis Romeo
# CSC 496 HW2


# Load the data
data = pd.read_csv('win_probability_data.csv', header=None)
data.columns = ['outs', 'run_diff', 'first_base', 'second_base', 'third_base', 'winner']

# Split data into features and target
X = data[['outs', 'run_diff', 'first_base', 'second_base', 'third_base']]
y = data['winner']

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the logistic regression model
logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)

# Get predictions and print accuracy
y_pred = logistic_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Print the coefficients of the logistic regression model
print("Logistic Regression Coefficients:")
for feature, coef in zip(X.columns, logistic_model.coef_[0]):
    print(f"{feature}: {coef:.4f}")
