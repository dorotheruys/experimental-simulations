import pandas as pd

from Corrections.Support_tare_correction import strut_correction
from Corrections.Lift_interference import lift_interference
from Corrections.Blockages import *
from General.Pathfinder import get_file_path
from General.Drag_coefficients import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def corrections_combined(df):
    df_dragthrust_coefficients = CD_CT(df)

    df_with_strut = strut_correction(df_dragthrust_coefficients)
    #print(df_with_strut)

    df_with_bcor = Full_blockage(df_with_strut)

    lift_interference_cor = lift_interference(df_with_bcor)
    #print(lift_interference_cor)


def main():
    filename = "bal_sorted2.csv"
    folder = "Sort_data"

    df = pd.read_csv(get_file_path(filename=filename, folder=folder))

    corrections_combined(df)


if __name__ == "__main__":
    main()
