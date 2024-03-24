import pandas as pd
from General.Pathfinder import get_file_path

def strut_correction():
    file = get_file_path("modelOffData.xlsx", folder="Corrections")
    df = pd.read_excel(file, header=10, skipfooter=4, usecols="A:H")
    return df
