import pandas as pd
from General.Pathfinder import get_file_path

def strut_correction():
    file = get_file_path("modelOffData.xlsx", folder="Corrections")
    df = pd.read_excel(file, header=10, skipfooter=4, usecols="A:H")
    df = df.rename(columns={"AoA [deg]": "AoA"})
    return df

def add_modeloff_corrections():
    df = pd.read_csv(get_file_path("bal_sorted2.csv", folder="Sort_data"))
    df_strut = strut_correction()

    df_strut_aoa = pd.DataFrame()  # Initialize as an empty DataFrame
    for aoa in df["rounded_AoA"]:
        df_strut_aoa = pd.concat([df_strut_aoa, df_strut[df_strut["AoA"] == aoa]], ignore_index=True)
    df_strut_aoa.reset_index(drop=True, inplace=True)

    df["CL_strut_cor"] = df["CL"] - df_strut_aoa["CL"]
    df["CD_strut_cor"] = df["CD"] - df_strut_aoa["CD"]
    df["CMpitch25c_strut_cor"] = df["CMpitch25c"] - df_strut_aoa["CMpitch"]
    return df

def main():
    add_modeloff_corrections()

if __name__ == "__main__":
    main()