from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(df, output_path):
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Sales Distribution Histogram
    plt.figure(figsize=(9, 5))
    sns.histplot(df["Sales"], bins=40, kde=True)
    plt.title("Sales Distribution")
    plt.xlabel("Sales")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path / "01_sales_distribution.png", dpi=150)
    plt.close()

    # 2. Profit Distribution Histogram
    plt.figure(figsize=(9, 5))
    sns.histplot(df["Profit"], bins=40, kde=True)
    plt.title("Profit Distribution")
    plt.xlabel("Profit")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path / "02_profit_distribution.png", dpi=150)
    plt.close()

    # 3. Category-wise Sales
    category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    category_sales.plot(kind="bar")
    plt.title("Category-wise Sales")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path / "03_category_sales.png", dpi=150)
    plt.close()

    # 4. Region-wise Sales
    region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    region_sales.plot(kind="bar")
    plt.title("Region-wise Sales")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path / "04_region_sales.png", dpi=150)
    plt.close()

    # 5. Shipping Mode Count Plot
    plt.figure(figsize=(9, 5))
    sns.countplot(data=df, x="Ship_Mode", order=df["Ship_Mode"].value_counts().index)
    plt.title("Shipping Mode Count")
    plt.xlabel("Shipping Mode")
    plt.ylabel("Number of Records")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_path / "05_shipping_mode.png", dpi=150)
    plt.close()

    # 6. Customer Segment Pie Chart
    segment_counts = df["Segment"].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(segment_counts.values, labels=segment_counts.index, autopct="%1.1f%%")
    plt.title("Customer Segment Distribution")
    plt.tight_layout()
    plt.savefig(output_path / "06_customer_segment.png", dpi=150)
    plt.close()

    # 7. Monthly Sales Line Chart
    monthly_sales = (
        df.groupby("Month_Start")["Sales"]
        .sum()
        .sort_index()
    )
    plt.figure(figsize=(11, 5))
    monthly_sales.plot(kind="line", marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(output_path / "07_monthly_sales.png", dpi=150)
    plt.close()

    # 8. Profit Box Plot
    plt.figure(figsize=(8, 5))
    sns.boxplot(y=df["Profit"])
    plt.title("Profit Distribution - Box Plot")
    plt.ylabel("Profit")
    plt.tight_layout()
    plt.savefig(output_path / "08_profit_boxplot.png", dpi=150)
    plt.close()

    # 9. Correlation Heatmap
    numeric = df[["Sales", "Quantity", "Discount", "Profit", "Profit_Margin", "Shipping_Days"]]
    plt.figure(figsize=(9, 7))
    sns.heatmap(numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(output_path / "09_correlation_heatmap.png", dpi=150)
    plt.close()

    # 10. Pair Plot
    pair_df = df[["Sales", "Quantity", "Discount", "Profit"]].sample(
        min(1000, len(df)), random_state=42
    )
    g = sns.pairplot(pair_df)
    g.fig.suptitle("Pair Plot - Sales, Quantity, Discount & Profit", y=1.02)
    g.savefig(output_path / "10_pairplot.png", dpi=120)
    plt.close("all")

    # Extra business chart: Discount vs Profit
    plt.figure(figsize=(9, 5))
    sns.scatterplot(data=df, x="Discount_Percent", y="Profit", alpha=0.5)
    plt.title("Discount vs Profit")
    plt.xlabel("Discount (%)")
    plt.ylabel("Profit")
    plt.tight_layout()
    plt.savefig(output_path / "11_discount_vs_profit.png", dpi=150)
    plt.close()

    # Extra business chart: Sub-category profit
    sub_profit = df.groupby("Sub-Category")["Profit"].sum().sort_values()
    plt.figure(figsize=(10, 7))
    sub_profit.plot(kind="barh")
    plt.title("Sub-category Profit Performance")
    plt.xlabel("Profit")
    plt.ylabel("Sub-category")
    plt.tight_layout()
    plt.savefig(output_path / "12_subcategory_profit.png", dpi=150)
    plt.close()

    return sorted(output_path.glob("*.png"))
