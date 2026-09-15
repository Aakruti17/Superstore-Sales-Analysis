import pandas as pd
from .config import RAW_DATA_PATH

def load_data():
    # The supplied Superstore CSV contains a non-UTF8 character in text data,
    # so latin1 is used for robust loading.
    df = pd.read_csv(RAW_DATA_PATH, encoding="latin1")
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_", regex=False)
    )
    return df
