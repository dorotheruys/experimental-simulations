# Old file as this has been done
# from General.Data_sorting import *
#
# non_windmill = (df['rounded_J'] != 17)
#
# # Filter the DataFrame based on the condition
# filtered_df = df[non_windmill]
#
# file_path = 'bal_sorted3.csv'
#
# # Save the DataFrame as a CSV file
# filtered_df.to_csv(file_path, index=False)
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
#
# # Original data
# x = np.array([1, 2, 3, 4, 5])
# y = np.array([1, np.sqrt(2)+0.1, np.sqrt(3)+0.1, np.sqrt(4)+0.1, np.sqrt(5)])  # Example data for square root fit
#
# for deg in degree:
#     # Define the square root function
# sqrt_func = lambda x, a: a * x**(deg)
#
# # Perform the curve fit
# params, covariance = curve_fit(sqrt_func, x, y)
#
# # Plot the original data
# plt.scatter(x, y, label='Original Data')
#
# # Plot the square root fit
# x_fit = np.linspace(min(x), max(x), 100)
# y_fit = sqrt_func(x_fit, *params)
#     plt.plot(x_fit, y_fit, color='red', label='Square Root Fit')
#
#     plt.xlabel('X-axis')
#     plt.ylabel('Y-axis')
#     plt.title('Square Root Fit')
#     plt.legend()
#     plt.grid(True)
# plt.show()
#
# print("Square root fit parameter (a):", params)