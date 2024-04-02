import pandas as pd


def max_val(column: str):
    df_15 = pd.read_csv('../Sort_data/cor_data_15.csv')
    df_0 = pd.read_csv('../Sort_data/cor_data_0.csv')
    df_min15 = pd.read_csv('../Sort_data/cor_data_min15.csv')
    df = pd.concat((df_0[column], df_15[column], df_min15[column]))
    max_val = max(df)
    max_val_sci = "{:.3e}".format(max_val)
    return max_val, max_val_sci


def main():
    max_Re, max_Re_sci = max_val("Re")
    print(f"Max Reynolds: {max_Re_sci}")


if __name__ == "__main__":
    main()
