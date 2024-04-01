from Corrections.Support_tare_correction import strut_correction
from Corrections.Lift_interference import lift_interference
from Corrections.Blockages import *
from General.Thrust_calculation import CT_corrected
from General.Drag_coefficients import *
from General.Data_sorting import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def corrections_combined(df):
    df_with_strut = strut_correction(df)

    df_dragthrust_coefficients = CD_CT(df_with_strut)

    df_with_bcor = Full_blockage(df_dragthrust_coefficients)

    lift_interference_cor = lift_interference(df_with_bcor)

    thrust_cor = CT_corrected(lift_interference_cor)

    return thrust_cor


def main():
    #Get the data
    bal_sorted_min15 = pd.read_csv('../Sort_data/bal05_sorted_neg15.csv')
    bal_sorted_min15 = pd.concat([bal_sorted_min15, pd.DataFrame({'delta_e': [-15] * len(bal_sorted_min15)})], axis=1)
    data_corrected_min15 = corrections_combined(bal_sorted_min15)
    # data_corrected_min15.to_csv('cor_05data_min15.csv')
    #
    # bal_sorted_15 = pd.read_csv('../Sort_data/bal05_sorted_15.csv')
    # bal_sorted_15 = pd.concat([bal_sorted_15, pd.DataFrame({'delta_e': [15] * len(bal_sorted_15)})], axis=1)
    # data_corrected_15 = corrections_combined(bal_sorted_15)
    # data_corrected_15.to_csv('cor_05data_15.csv')
    #
    # bal_sorted_0 = pd.read_csv('../Sort_data/bal05_sorted_0.csv')
    # bal_sorted_0 = pd.concat([bal_sorted_0, pd.DataFrame({'delta_e': [0] * len(bal_sorted_0)})], axis=1)
    # data_corrected_0 = corrections_combined(bal_sorted_0)
    # data_corrected_0.to_csv('cor_05data_0.csv')
    #


if __name__ == "__main__":

    main()
