import pandas as pd

def transform_data(df):
    df = df.copy()

    # Superstore Sales already reflects the transaction sales amount.
    # Do NOT subtract discount from Sales again.
    df["Profit_Margin"] = (
        df["Profit"] / df["Sales"].replace(0, pd.NA) * 100
    ).fillna(0)

    df["Order_Year"] = df["Order_Date"].dt.year
    df["Order_Month"] = df["Order_Date"].dt.month
    df["Order_Month_Name"] = df["Order_Date"].dt.month_name()
    df["Order_Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)

    df["Month_Start"] = df["Order_Date"].dt.to_period("M").dt.to_timestamp()

    df["Discount_Percent"] = df["Discount"] * 100
    df["Discount_Category"] = pd.cut(
        df["Discount"],
        bins=[-0.001, 0, 0.10, 0.25, 1.0],
        labels=["No Discount", "Low Discount", "Medium Discount", "High Discount"]
    )

    df["Profit_Status"] = df["Profit"].apply(
        lambda x: "Profitable" if x > 0 else ("Break-even" if x == 0 else "Loss")
    )

    df["Shipping_Days"] = (
        df["Ship_Date"] - df["Order_Date"]
    ).dt.days

    return df
