import pandas as pd
from Data_sorting import df

columns_to_display = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'FX', 'FY', 'FZ', 'MX', 'MY', 'MZ']

pd.set_option('display.max_columns', None)

print(df[columns_to_display])