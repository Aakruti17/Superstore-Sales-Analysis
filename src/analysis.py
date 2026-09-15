from pathlib import Path

def generate_analysis(df):
    analysis = {}

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()

    analysis["Total Orders"] = int(total_orders)
    analysis["Total Sales"] = float(total_sales)
    analysis["Total Profit"] = float(total_profit)
    analysis["Average Order Value"] = float(
        df.groupby("Order_ID")["Sales"].sum().mean()
    )
    analysis["Average Discount"] = float(df["Discount"].mean() * 100)
    analysis["Profit Margin"] = float(
        (total_profit / total_sales * 100) if total_sales else 0
    )

    region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)

    analysis["Top Performing Region"] = region_profit.index[0]
    analysis["Top Sales Region"] = region_sales.index[0]
    analysis["Best Sales Category"] = category_sales.index[0]
    analysis["Most Profitable Category"] = category_profit.index[0]

    product_sales = df.groupby("Product_Name")["Sales"].sum().sort_values(ascending=False)
    product_profit = df.groupby("Product_Name")["Profit"].sum().sort_values()

    analysis["Top Selling Product"] = product_sales.index[0]
    analysis["Least Profitable Product"] = product_profit.index[0]

    customer_sales = df.groupby("Customer_Name")["Sales"].sum().sort_values(ascending=False)
    analysis["Top Customer"] = customer_sales.index[0]

    analysis["Most Preferred Shipping Mode"] = df["Ship_Mode"].mode().iloc[0]

    loss_rows = int((df["Profit"] < 0).sum())
    analysis["Loss-making Rows"] = loss_rows

    high_discount_profit = df.loc[df["Discount"] >= 0.30, "Profit"].mean()
    no_discount_profit = df.loc[df["Discount"] == 0, "Profit"].mean()
    analysis["Average Profit at 30%+ Discount"] = float(high_discount_profit)
    analysis["Average Profit with No Discount"] = float(no_discount_profit)

    return analysis

def save_business_insights(analysis, file_path):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("SUPERSTORE SALES & PROFIT ANALYSIS - BUSINESS INSIGHTS\n")
        f.write("=" * 60 + "\n\n")
        for key, value in analysis.items():
            if isinstance(value, float):
                value = round(value, 2)
            f.write(f"{key}: {value}\n")
