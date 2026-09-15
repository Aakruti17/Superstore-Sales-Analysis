import pandas as pd
from .config import PROCESSED_DATA_PATH

TEXT_COLUMNS = [
    "Ship_Mode", "Customer_ID", "Customer_Name", "Segment", "Country",
    "City", "State", "Region", "Product_ID", "Category", "Sub-Category",
    "Product_Name"
]

NUMERIC_COLUMNS = [
    "Row_ID", "Postal_Code", "Sales", "Quantity", "Discount", "Profit"
]

def clean_data(df):
    df = df.copy()

    # Remove exact duplicate records.
    df = df.drop_duplicates()

    # Standardize text fields.
    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Convert dates.
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"], errors="coerce")

    # Convert numeric fields.
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # The supplied dataset has no missing values, but these rules make the
    # pipeline robust if the file is changed later.
    if df["Quantity"].isna().any():
        df["Quantity"] = df["Quantity"].fillna(1)
    if df["Discount"].isna().any():
        df["Discount"] = df["Discount"].fillna(0)
    if df["Sales"].isna().any():
        df["Sales"] = df["Sales"].fillna(df["Sales"].median())
    if df["Profit"].isna().any():
        df["Profit"] = df["Profit"].fillna(df["Profit"].median())

    df = df.dropna(subset=["Order_Date", "Ship_Date", "Order_ID", "Product_ID"])

    # Remove impossible numeric records.
    df = df[df["Sales"] >= 0]
    df = df[df["Quantity"] > 0]
    df = df[df["Discount"].between(0, 1)]

    df = df.reset_index(drop=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    return df
