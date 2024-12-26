import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Louis Romeo
# CSC 496
# Assignment 1
def analyze_data(file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file)

    # Extract relevant columns
    stats = ['H', 'BA', 'OBP', 'SLG', 'OPS', 'OPS+']  # Adjust as necessary based on data format
    dependent_variable = 'R/G'  # Runs per Game column

    # Initialize a dictionary to store the correlation coefficients
    correlations = {}

    # Set up the plot
    plt.figure(figsize=(15, 10))

    for i, stat in enumerate(stats):
        # Prepare the data for regression
        X = df[[stat]].values  # Independent variable
        y = df[dependent_variable].values  # Dependent variable

        # Perform linear regression
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        # Calculate the correlation coefficient
        correlation = np.corrcoef(df[stat], df[dependent_variable])[0, 1]
        correlations[stat] = correlation

        # Print the correlation
        print(f"Correlation coefficient for {dependent_variable} vs {stat}: {correlation:.4f}")

        # Plot each regression
        plt.subplot(3, 2, i + 1)
        plt.scatter(X, y, label=f'Data: {stat} vs {dependent_variable}')
        plt.plot(X, y_pred, color='red', label='Regression Line')
        plt.xlabel(stat)
        plt.ylabel(dependent_variable)
        plt.title(f'{dependent_variable} vs {stat}')
        plt.legend()

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig('regression_plots.png')
    plt.show()

# Example usage
# File would be input manually, for example: "majors_2023.csv"
analyze_data('mlb_2023.csv')
