import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import requests
from sklearn.metrics import r2_score

url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv'
response = requests.get(url)
if response.status_code == 200:
    with open('hw_200.csv', 'wb') as f:
        f.write(response.content)

# Load the CSV file into a DataFrame
data = pd.read_csv('hw_200.csv')

# Extract the independent variable (x) and dependent variable (y) from the DataFrame
x = data.iloc[:, 1].values.reshape(-1, 1)  # Assuming the independent variable is in 'Column1'
y = data.iloc[:, 2].values  # Assuming the dependent variable is in 'Column2'

# Create a linear regression model
model = LinearRegression()

# Fit the model to the data
model.fit(x, y)

# Get the parameters a (slope) and b (intercept)
a = model.coef_[0]
b = model.intercept_ * -1

# Calculate the predicted values
predicted_y = model.predict(x)

# Calculate the mean squared error
mse = mean_squared_error(y, predicted_y)
r2 = r2_score(y, predicted_y)

plt.scatter(x, y, color='blue', label='Tatsächliche Daten')
plt.plot(x, predicted_y, color='red', label='Regression')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression')
plt.legend()

formula_text = f'y = {a:.2f}x + {b:.2f}'
plt.text(x.max() * 0.95, y.min() * 1.1, formula_text, color='black', fontsize=12)
plt.text(x.max() * 0.95, y.min() * 1.05, f'mse = {mse:.2f}', color='black', fontsize=12)
plt.text(x.max() * 0.95, y.min() * 1.0, f'r^2 = {r2:.2f}', color='black', fontsize=12)

plt.show()