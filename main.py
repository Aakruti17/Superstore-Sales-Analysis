from pathlib import Path
import pandas as pd

from src.config import (
    PROCESSED_DATA_PATH, GRAPH_PATH, ANALYSIS_PATH, REPORT_PATH
)
from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.data_transformation import transform_data
from src.analysis import generate_analysis, save_business_insights
from src.visualization import create_visualizations
from src.report import create_report

def main():
    print("=" * 60)
    print("SUPERSTORE SALES & PROFIT ANALYSIS")
    print("=" * 60)

    # 1. Load
    df_raw = load_data()
    print(f"\nRaw shape: {df_raw.shape}")
    print("\nColumns:")
    print(df_raw.columns.tolist())

    # EDA before cleaning
    print("\nMissing values before cleaning:")
    print(df_raw.isna().sum())

    print(f"\nDuplicate rows before cleaning: {df_raw.duplicated().sum()}")

    # 2. Clean
    df = clean_data(df_raw)
    print(f"\nCleaned shape: {df.shape}")

    # 3. Transform / feature engineering
    df = transform_data(df)

    # Save transformed dataset
    Path(PROCESSED_DATA_PATH).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    # 4. Analysis
    analysis = generate_analysis(df)
    save_business_insights(analysis, ANALYSIS_PATH)

    print("\n--- KEY BUSINESS METRICS ---")
    for k, v in analysis.items():
        print(f"{k}: {v}")

    # 5. Visualizations
    graph_paths = create_visualizations(df, GRAPH_PATH)
    print(f"\nGenerated {len(graph_paths)} charts.")

    # 6. PDF report
    create_report(df, analysis, graph_paths, REPORT_PATH)

    print("\n--- OUTPUTS ---")
    print(f"Cleaned dataset : {PROCESSED_DATA_PATH}")
    print(f"Charts          : {GRAPH_PATH}")
    print(f"Insights        : {ANALYSIS_PATH}")
    print(f"PDF report      : {REPORT_PATH}")
    print("\nProject completed successfully.")

if __name__ == "__main__":
    main()
