from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


def create_visualizations(df, output_path):

    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # Store all generated chart paths
    graph_paths = []

    # --------------------------------------------------
    # 1. Sales Distribution Histogram
    # --------------------------------------------------
    graph_path = output_path / "01_sales_distribution.png"

    plt.figure(figsize=(9, 5))
    sns.histplot(df["Sales"], bins=40, kde=True)
    plt.title("Sales Distribution")
    plt.xlabel("Sales")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 2. Profit Distribution Histogram
    # --------------------------------------------------
    graph_path = output_path / "02_profit_distribution.png"

    plt.figure(figsize=(9, 5))
    sns.histplot(df["Profit"], bins=40, kde=True)
    plt.title("Profit Distribution")
    plt.xlabel("Profit")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 3. Category-wise Sales
    # --------------------------------------------------
    graph_path = output_path / "03_category_sales.png"

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))
    category_sales.plot(kind="bar")
    plt.title("Category-wise Sales")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 4. Region-wise Sales
    # --------------------------------------------------
    graph_path = output_path / "04_region_sales.png"

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))
    region_sales.plot(kind="bar")
    plt.title("Region-wise Sales")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 5. Shipping Mode Count Plot
    # --------------------------------------------------
    graph_path = output_path / "05_shipping_mode.png"

    plt.figure(figsize=(9, 5))
    sns.countplot(
        data=df,
        x="Ship_Mode",
        order=df["Ship_Mode"].value_counts().index
    )
    plt.title("Shipping Mode Count")
    plt.xlabel("Shipping Mode")
    plt.ylabel("Number of Records")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 6. Customer Segment Pie Chart
    # --------------------------------------------------
    graph_path = output_path / "06_customer_segment.png"

    segment_counts = df["Segment"].value_counts()

    plt.figure(figsize=(7, 7))
    plt.pie(
        segment_counts.values,
        labels=segment_counts.index,
        autopct="%1.1f%%"
    )
    plt.title("Customer Segment Distribution")
    plt.tight_layout()
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 7. Monthly Sales Line Chart
    # --------------------------------------------------
    graph_path = output_path / "07_monthly_sales.png"

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
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 8. Profit Box Plot
    # --------------------------------------------------
    graph_path = output_path / "08_profit_boxplot.png"

    plt.figure(figsize=(8, 5))
    sns.boxplot(y=df["Profit"])
    plt.title("Profit Distribution - Box Plot")
    plt.ylabel("Profit")
    plt.tight_layout()
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 9. Correlation Heatmap
    # --------------------------------------------------
    graph_path = output_path / "09_correlation_heatmap.png"

    numeric = df[
        [
            "Sales",
            "Quantity",
            "Discount",
            "Profit",
            "Profit_Margin",
            "Shipping_Days"
        ]
    ]

    plt.figure(figsize=(9, 7))
    sns.heatmap(
        numeric.corr(),
        annot=True,
        fmt=".2f",
        cmap="coolwarm"
    )
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(graph_path, dpi=150)
    plt.close()

    graph_paths.append(graph_path)

    # --------------------------------------------------
    # 10. Pair Plot
    # --------------------------------------------------
    graph_path = output_path / "10_pairplot.png"

    pair_df = df[
        ["Sales", "Quantity", "Discount", "Profit"]
    ].sample(
        min(1000, len(df)),
        random_state=42
    )

    g = sns.pairplot(pair_df)
    g.fig.suptitle(
        "Pair Plot - Sales, Quantity, Discount & Profit",
        y=1.02
    )
    g.savefig(graph_path, dpi=120)
    plt.close("all")

    graph_paths.append(graph_path)

    return graph_paths