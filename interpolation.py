import matplotlib.pyplot as plt
import numpy as np

# X-axis: volumes from 100 ml to 1000 ml
volumes = [308.7, 408.7, 508.7, 608.7, 708.7, 808.7, 908.7, 1008.7, 1108.7, 1208.7]

# Y-axis: values from your provided list
values = [
    55.7, 73.1, 92.0, 110.6, 128.9, 146.6, 164.8, 183.5, 202.6, 219.7
]

# Fit a linear line to the data
slope, intercept = np.polyfit(volumes, values, 1)

# Create the linear model (y = mx + b)
def linear_model(x):
    return slope * x + intercept

# Generate fitted values based on the linear model
fitted_values = linear_model(np.array(volumes))

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(volumes, values, marker='o', linestyle='-', color='b', label='Original Data')
plt.plot(volumes, fitted_values, linestyle='--', color='r', label='Fitted Line')

# Adding titles and labels
plt.title('Volume vs Value with Linear Fit')
plt.xlabel('Volume (ml)')
plt.ylabel('Value')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()

# Save the linear model data to a .npy file
np.save('interpolation_data.npy', {'volumes': volumes, 'values': values, 'slope': slope, 'intercept': intercept})

print("Linear model and data saved to 'interpolation_data.npy'")

