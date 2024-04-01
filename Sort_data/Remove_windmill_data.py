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
import numpy as np
import matplotlib.pyplot as plt
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# def inverse_second_degree_polynomial(a, b, c, x_values):
#     def inverse_roots(x):
#         discriminant = b**2 - 4*a*(c - x)
#         if discriminant < 0:
#             return None, None  # No real roots
#         else:
#             root1 = (-b + np.sqrt(discriminant)) / (2*a)
#             root2 = (-b - np.sqrt(discriminant)) / (2*a)
#             return root1, root2
#
#     # Calculate the inverse roots for each x value
#     inverse_roots_list = [inverse_roots(x) for x in x_values]
#
#     # Filter out points with no real roots
#     inverse_roots_list = [(root1, root2) for root1, root2 in inverse_roots_list if root1 is not None and root2 is not None]
#
#     # Separate the roots into root1 and root2
#     root1_values = [roots[0] for roots in inverse_roots_list]
#     root2_values = [roots[1] for roots in inverse_roots_list]
#
#     return root1_values, root2_values
#
# def plot_inverse_second_degree_polynomial(a, b, c, x_range):
#     # Generate x values
#     x_values = np.linspace(x_range[0], x_range[-1], 100)
#     # Calculate the inverse function
#     root1_values, root2_values = inverse_second_degree_polynomial(a, b, c, x_range)
#     #print(root1_values,root2_values)
#     x_values1 = x_range[:len(root1_values)][::-1]
#     x_values2 = x_range[:len(root2_values)]
#     root1_values = root1_values[::-1]
#     x = []
#     for xv in x_values1:
#         x.append(xv)
#     for xv in x_values2:
#         x.append(xv)
#     y = []
#     for yv in root1_values:
#         y.append(yv)
#     for yv in root2_values:
#         y.append(yv)
#
#     plt.plot(x,y)
#
#     plt.xlabel('X-axis')
#     plt.ylabel('Y-axis')
#     plt.title('Inverse Function of a Second-Degree Polynomial')
#     plt.legend()
#     plt.grid(True)
#     #plt.show()

#plot_inverse_second_degree_polynomial(0.11319508, -0.0440425, 0.00109855, np.linspace(0,1,11))
