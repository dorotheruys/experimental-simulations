import pandas as pd

from Corrections.Support_tare_correction import strut_correction
from Corrections.Lift_interference import lift_interference
from General.Pathfinder import get_file_path


def corrections_combined(df):
    df_with_strut = strut_correction(df)
    lift_interference_cor = lift_interference(df)
    print(df_with_strut)
    print(lift_interference_cor)


def main():
    filename = "bal_sorted2.csv"
    folder = "Sort_data"

    df = pd.read_csv(get_file_path(filename=filename, folder=folder))

    corrections_combined(df)


if __name__ == "__main__":
    main()
