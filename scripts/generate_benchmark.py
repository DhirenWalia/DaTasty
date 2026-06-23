import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("en_IN")

NUM_RECORDS = 100000

data = []

segments = [
    "Premium",
    "Standard",
    "Basic"
]

genders = [
    "Male",
    "Female",
    "Other"
]


for i in range(NUM_RECORDS):

    join_date = fake.date_between(
        start_date="-10y",
        end_date="today"
    )

    last_purchase = fake.date_between(
        start_date=join_date,
        end_date="today"
    )


    row = {

        "Customer_ID":
            f"CUST{i+10000}",

        "Customer_Name":
            fake.name(),

        "Email":
            fake.email(),

        "Phone":
            fake.phone_number(),

        "Age":
            random.randint(18, 70),

        "Gender":
            random.choice(genders),

        "City":
            fake.city(),

        "State":
            fake.state(),

        "Country":
            "India",

        "Join_Date":
            join_date,

        "Last_Purchase_Date":
            last_purchase,

        "Customer_Segment":
            random.choice(segments),

        "Annual_Income":
            random.randint(
                300000,
                2000000
            ),

        "Transaction_Count":
            random.randint(1, 500),

        "Customer_Score":
            random.randint(1, 100)
    }

    data.append(row)


df = pd.DataFrame(data)

print("Clean dataset created.")
def inject_missing(column, percentage):

    rows = int(
        len(df) * percentage
    )

    indices = np.random.choice(
        df.index,
        rows,
        replace=False
    )

    df.loc[indices, column] = np.nan


inject_missing("Email", 0.15)
inject_missing("Phone", 0.10)
inject_missing("Annual_Income", 0.05)


print("Missing values injected.")

email_indices = np.random.choice(
    df.index,
    3000,
    replace=False
)


invalid_emails = [
    "abc.com",
    "hello@",
    "user@@gmail.com"
]


for idx in email_indices:

    df.loc[idx, "Email"] = (
        random.choice(invalid_emails)
    )


print("Invalid emails injected.")

age_indices = np.random.choice(
    df.index,
    2000,
    replace=False
)


invalid_ages = [
    -5,
    150,
    200
]


for idx in age_indices:

    df.loc[idx, "Age"] = (
        random.choice(invalid_ages)
    )


print("Invalid ages injected.")

city_indices = np.random.choice(
    df.index,
    8000,
    replace=False
)


for idx in city_indices:

    city = df.loc[idx, "City"]

    df.loc[idx, "City"] = random.choice([
        city.lower(),
        city.upper(),
        " " + city + " "
    ])


print("City formatting issues injected.")

country_indices = np.random.choice(
    df.index,
    10000,
    replace=False
)


for idx in country_indices:

    df.loc[idx, "Country"] = random.choice([
        "india",
        "INDIA",
        " India "
    ])


print("Country formatting issues injected.")

duplicate_ids = np.random.choice(
    df["Customer_ID"],
    3000,
    replace=False
)


new_rows = []


for customer_id in duplicate_ids:

    new_rows.append({
        "Customer_ID": customer_id,
        "Customer_Name": fake.name(),
        "Email": fake.email(),
        "Phone": fake.phone_number(),
        "Age": random.randint(18, 70),
        "Gender": random.choice(genders),
        "City": fake.city(),
        "State": fake.state(),
        "Country": "India",
        "Join_Date": fake.date_between("-10y", "today"),
        "Last_Purchase_Date": fake.date_between("-5y", "today"),
        "Customer_Segment": random.choice(segments),
        "Annual_Income": random.randint(300000, 2000000),
        "Transaction_Count": random.randint(1, 500),
        "Customer_Score": random.randint(1, 100)
    })


df = pd.concat(
    [
        df,
        pd.DataFrame(new_rows)
    ],
    ignore_index=True
)


print("Business duplicates injected.")

exact_duplicates = df.sample(
    3000,
    random_state=42
)


df = pd.concat(
    [
        df,
        exact_duplicates
    ],
    ignore_index=True
)


print("Exact duplicates injected.")

income_indices = np.random.choice(
    df.index,
    500,
    replace=False
)


df.loc[
    income_indices,
    "Annual_Income"
] = 1000000000


## Transaction Outliers

transaction_indices = np.random.choice(
    df.index,
    300,
    replace=False
)


df.loc[
    transaction_indices,
    "Transaction_Count"
] = 100000


print("Outliers injected.")

date_indices = np.random.choice(
    df.index,
    5000,
    replace=False
)


formats = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%b-%y",
    "%b %d, %Y"
]


for idx in date_indices:

    date = pd.to_datetime(
        df.loc[idx, "Join_Date"]
    )

    df.loc[idx, "Join_Date"] = (
        date.strftime(
            random.choice(formats)
        )
    )


print("Date inconsistencies injected.")

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

path = (
    "data/benchmark/"
    "DATATSTY_Enterprise_Benchmark_v1.csv"
)

df.to_csv(
    path,
    index=False
)

print("\nBenchmark dataset created successfully!")
print(f"Location: {path}")
print(f"Shape: {df.shape}")