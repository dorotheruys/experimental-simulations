import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 25})

def average_tc():
    x = []
    y = []
    with open("wing airfoil coordinates DU 96-150.dat", "r") as file:
        for line in file:
            values = line.strip().split("\t")
            x.append(float(values[0]))
            y.append(float(values[1]))

    # Assuming you have the x-array and y-array
    x_array = np.array(x)
    y_array = np.array(y)

    # Initialize an empty list to store all differences
    all_differences = []

    # Iterate through unique x-values
    for x_val in np.unique(x_array):
        indices = np.where(x_array == x_val)[0]
        if len(indices) > 1:
            y_vals = y_array[indices]
            differences = abs(np.diff(np.sort(y_vals)))
            all_differences.extend(differences)

    # Calculate the average of all differences
    average_difference = np.mean(all_differences)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linewidth=2.5, label='DU 96 150 Airfoil')
    plt.xlabel('Chord [x/c]')
    plt.ylabel('Thickness [t/c]')
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()
    return average_difference

print(average_tc())