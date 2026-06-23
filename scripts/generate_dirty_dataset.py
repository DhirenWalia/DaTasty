import pandas as pd
import numpy as np


SOURCE_FILE = (
    "data/benchmark/"
    "DATATSTY_Enterprise_Benchmark_v1_1.csv"
)

OUTPUT_FILE = (
    "data/benchmark/"
    "DATATSTY_Dirty_Demo_Dataset.csv"
)


df = pd.read_csv(
    SOURCE_FILE
)
df["Phone"] = df["Phone"].astype(str)
## dts 86
# ====================================
# MASSIVE MISSING VALUES
# ====================================

for col in [
    "Email",
    "Phone",
    "Annual_Income",
    "City",
    "Customer_Segment"
]:

    idx = df.sample(
        frac=0.90,
        random_state=42
    ).index

    df.loc[idx, col] = np.nan


# ====================================
# INVALID EMAILS
# ====================================

idx = df.sample(
    frac=0.90,
    random_state=43
).index

df.loc[idx, "Email"] = (
    "invalid_email"
)


# ====================================
# INVALID AGE
# ====================================

idx = df.sample(
    frac=0.90,
    random_state=44
).index

df.loc[idx, "Age"] = 999


# ====================================
# INVALID PHONE
# ====================================

idx = df.sample(
    frac=0.90,
    random_state=45
).index

df.loc[idx, "Phone"] = (
    "ABC123XYZ"
)


# ====================================
# CONSISTENCY CHAOS
# ====================================

idx = df.sample(
    frac=0.90,
    random_state=46
).index

df.loc[idx, "City"] = (
    df.loc[idx, "City"]
    .astype(str)
    .str.upper()
)

idx = df.sample(
    frac=0.90,
    random_state=47
).index

df.loc[idx, "State"] = (
    df.loc[idx, "State"]
    .astype(str)
    .str.lower()
)


# ====================================
# HUGE OUTLIERS
# ====================================

idx = df.sample(
    frac=0.70,
    random_state=48
).index

df.loc[idx, "Annual_Income"] = (
    9999999999
)

idx = df.sample(
    frac=0.95,
    random_state=49
).index

df.loc[idx, "Transaction_Count"] = (
    100000
)


# ====================================
# DUPLICATE RECORDS
# ====================================

duplicates = df.sample(
    frac=0.90,
    random_state=50
)

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)


# ====================================
# BUSINESS KEY COLLISION
# ====================================

idx = df.sample(
    frac=0.90,
    random_state=51
).index

df.loc[idx, "Customer_ID"] = (
    "CUST000001"
)
# ====================================
# Save
# ====================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"Dirty dataset saved: "
    f"{OUTPUT_FILE}"
)

print(
    f"Rows: {len(df):,}"
)

# Destroy uniqueness

df["Customer_ID"] = "CUST000001"

# Destroy consistency

df["City"] = np.where(
    np.random.rand(len(df)) > 0.5,
    df["City"].astype(str).str.upper(),
    df["City"].astype(str).str.lower()
)

# Destroy validity

df["Email"] = "bad_email"