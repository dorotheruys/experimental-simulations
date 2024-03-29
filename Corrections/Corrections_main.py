from Corrections.Support_tare_correction import strut_correction
from Corrections.Lift_interference import lift_interference
from Corrections.Blockages import *
from General.Drag_coefficients import *
from General.Data_sorting import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def corrections_combined(df):
    df_dragthrust_coefficients = CD_CT(df)

    df_with_strut = strut_correction(df_dragthrust_coefficients)

    df_with_bcor = Full_blockage(df_with_strut)

    lift_interference_cor = lift_interference(df_with_bcor)
    #1
    print(lift_interference_cor)
    return lift_interference_cor


def main():
    # The dataframe is now imported from Data_sorting
    # filename = "bal_sorted2.csv"
    # folder = "Sort_data"
    #
    # df = pd.read_csv(get_file_path(filename=filename, folder=folder))

    df_cor = corrections_combined(df)



if __name__ == "__main__":
    # Get the data
    bal_sorted_min15 = pd.read_csv('../Sort_data/bal_sorted1.csv')
    bal_sorted_min15 = pd.concat([bal_sorted_min15, pd.DataFrame({'delta_e': [-15]*len(bal_sorted_min15)})], axis=1)
    data_corrected_min15 = corrections_combined(bal_sorted_min15)
    data_corrected_min15.to_csv('data_cor_min15.csv')

    bal_sorted_0 = pd.read_csv('../Sort_data/bal_sorted2.csv')
    bal_sorted_0 = pd.concat([bal_sorted_0, pd.DataFrame({'delta_e': [0]*len(bal_sorted_0)})], axis=1)
    data_corrected_0 = corrections_combined(bal_sorted_0)
    data_corrected_0.to_csv('data_cor_0.csv')

    bal_sorted_15 = pd.read_csv('../Sort_data/bal_sorted3.csv')
    bal_sorted_15 = pd.concat([bal_sorted_15, pd.DataFrame({'delta_e': [15]*len(bal_sorted_15)})], axis=1)
    data_corrected_15 = corrections_combined(bal_sorted_15)
    data_corrected_15.to_csv('data_cor_15.csv')

    # main()
