import pandas as pd
from General.Pathfinder import get_file_path

def strut_correction():
    file = get_file_path("modelOffData.xlsx", folder="Corrections")
    df = pd.read_excel(file, header=10, skipfooter=4, usecols="A:H")
    df = df.rename(columns={"AoA [deg]": "AoA"})
    return df

def main():
    path = get_file_path("bal_sorted2.csv", folder="Sort_data")
    df_uncor = pd.read_csv(path)
    df_strut = strut_correction()


    for aoa in df_uncor["rounded_AoA"]:
        df_strut_aoa.loc[-1] = = df_strut[(df_strut["AoA"] == aoa)]
        df.loc[-1]

if __name__ == "__main__":
    main()