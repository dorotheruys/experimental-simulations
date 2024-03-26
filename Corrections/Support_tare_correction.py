import pandas as pd
from General.Pathfinder import get_file_path

def strut_correction():
    file = get_file_path("modelOffData.xlsx", folder="Corrections")
    df = pd.read_excel(file, header=10, skipfooter=4, usecols="A:H")
    df = df.rename(columns={"AoA [deg]": "AoA"})
    return df

def get_uncor_data(file, folder)

def main():
    path = get_file_path("bal_sorted2.csv", folder="Sort_data")
    df = pd.read_csv(path)
    print(df)

if __name__ == "__main__":
    main()