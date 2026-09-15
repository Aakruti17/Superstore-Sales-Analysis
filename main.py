from pathlib import Path

from src.config import (
    PROCESSED_DATA_PATH,
    GRAPH_PATH,
    ANALYSIS_PATH,
    REPORT_PATH
)

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.data_transformation import transform_data
from src.analysis import (
    generate_analysis,
    save_business_insights
)
from src.visualization import create_visualizations
from src.report import create_report


def main():

    print("=" * 60)
    print("SUPERSTORE SALES & PROFIT ANALYSIS")
    print("=" * 60)

    # --------------------------------------------------
    # 1. LOAD DATA
    # --------------------------------------------------
    print("\nLoading data...")

    df_raw = load_data()

    print(f"\nRaw shape: {df_raw.shape}")

    print("\nColumns:")
    print(df_raw.columns.tolist())

    print("\nMissing values before cleaning:")
    print(df_raw.isna().sum())

    print(
        f"\nDuplicate rows before cleaning: "
        f"{df_raw.duplicated().sum()}"
    )

    # --------------------------------------------------
    # 2. CLEAN DATA
    # --------------------------------------------------
    print("\nCleaning data...")

    df = clean_data(df_raw)

    print(f"\nCleaned shape: {df.shape}")

    # --------------------------------------------------
    # 3. TRANSFORM DATA
    # --------------------------------------------------
    print("\nTransforming data...")

    df = transform_data(df)

    # Save processed dataset
    Path(PROCESSED_DATA_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print(
        f"\nProcessed dataset saved to: "
        f"{PROCESSED_DATA_PATH}"
    )

    # --------------------------------------------------
    # 4. BUSINESS ANALYSIS
    # --------------------------------------------------
    print("\nGenerating business analysis...")

    analysis_results = generate_analysis(df)

    # Create analysis folder
    Path(ANALYSIS_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    save_business_insights(
        analysis_results,
        ANALYSIS_PATH
    )

    print("\n--- KEY BUSINESS METRICS ---")

    for key, value in analysis_results.items():
        print(f"{key}: {value}")

    # --------------------------------------------------
    # 5. VISUALIZATIONS
    # --------------------------------------------------
    print("\nCreating visualizations...")

    graph_paths = create_visualizations(
        df,
        GRAPH_PATH
    )

    print(
        f"\nGenerated {len(graph_paths)} charts."
    )

    # --------------------------------------------------
    # 6. PDF REPORT
    # --------------------------------------------------
    print("\nCreating PDF report...")

    Path(REPORT_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    create_report(
        df,
        analysis_results,
        graph_paths,
        REPORT_PATH
    )

    print("\nPDF report created successfully.")

    # --------------------------------------------------
    # 7. OUTPUTS
    # --------------------------------------------------
    print("\n" + "=" * 60)
    print("OUTPUTS")
    print("=" * 60)

    print(
        f"\nProcessed dataset : "
        f"{PROCESSED_DATA_PATH}"
    )

    print(
        f"Charts            : "
        f"{GRAPH_PATH}"
    )

    print(
        f"Business insights : "
        f"{ANALYSIS_PATH}"
    )

    print(
        f"PDF report        : "
        f"{REPORT_PATH}"
    )

    print(
        "\nProject completed successfully."
    )


if __name__ == "__main__":
    main()