import os
import pandas as pd
from sklearn.model_selection import train_test_split

files = {
    "Bicarbonate": "D:\GitHub\Dataset\Water\Bicarbonate.csv",
    "Calcium": "D:\GitHub\Dataset\Water\Calcium.csv",
    "Chloride": "D:\GitHub\Dataset\Water\Chloride.csv",
    "Electrical_Conductance": "D:\GitHub\Dataset\Water\Electrical_Conductance.csv",
    "Magnesium": "D:\GitHub\Dataset\Water\Magnesium.csv",
    "Ph": "D:\GitHub\Dataset\Water\pH.csv",
    "Potassium": "D:\GitHub\Dataset\Water\Potassium.csv",
    "Sodium": "D:\GitHub\Dataset\Water\Sodium.csv",
    "Sulfur": "D:\GitHub\Dataset\Water\Sulfur.csv",
    "Tds": "D:\GitHub\Dataset\Water\Tds.csv",
    "Temperature": "D:\GitHub\Dataset\Water\Temperature.csv",
}

def prepare_df(file_path, param_name):
    df = pd.read_csv(file_path, encoding="ISO-8859-1", sep=";")
    df_clean = df[["GEMS.Station.Number", "Sample.Date", "Sample.Time", "Value"]].copy()
    df_clean["Parameter"] = param_name
    return df_clean

# Read all files and stack them
all_dfs = []
for param, file in files.items():
    all_dfs.append(prepare_df(file, param))

long_df = pd.concat(all_dfs, ignore_index=True)

# Pivot to wide format
wide_df = long_df.pivot_table(
    index=["GEMS.Station.Number", "Sample.Date", "Sample.Time"],
    columns="Parameter",
    values="Value",
    aggfunc="first"   # or 'mean' if duplicates exist
).reset_index()

# Split the data into training and testing sets (80% train, 20% test)
train_data, test_data = train_test_split(wide_df, test_size=0.2, random_state=42)

# Save the split datasets to CSV files in the 'data/raw' directory
os.makedirs("data/raw", exist_ok=True)  # Ensure the directory exists   
train_data.to_csv("data/raw/train.csv", index=False)
test_data.to_csv("data/raw/test.csv", index=False)