import pandas as pd

def load_product_data(csv_path: str = "../data/Product_Information_Dataset.csv") -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.fillna("", inplace=True)
    return df
