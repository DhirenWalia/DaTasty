import pandas as pd
import numpy as np
import random

from faker import Faker
from datetime import datetime


fake = Faker("en_IN")

NUM_RECORDS = 100000

cities = [
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Chennai",
    "Kolkata",
    "Hyderabad",
    "Pune",
    "Ahmedabad",
    "Jaipur",
    "Lucknow"
]


states = {
    "Delhi": "Delhi",
    "Mumbai": "Maharashtra",
    "Bengaluru": "Karnataka",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Hyderabad": "Telangana",
    "Pune": "Maharashtra",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh"
}


genders = [
    "Male",
    "Female",
    "Other"
]


segments = [
    "Premium",
    "Standard",
    "Basic"
]

data = []

for i in range(NUM_RECORDS):

    city = random.choice(cities)

    join_date = fake.date_between(
        start_date="-10y",
        end_date="today"
    )

    last_purchase = fake.date_between(
        start_date=join_date,
        end_date="today"
    )


    data.append({

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
            city,

        "State":
            states[city],

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
    })


df = pd.DataFrame(data)

print("Clean enterprise dataset created.")

def inject_missing(column, percentage):

    count = int(
        len(df) * percentage
    )

    rows = np.random.choice(
        df.index,
        count,
        replace=False
    )

    df.loc[rows, column] = np.nan


inject_missing("Email", 0.15)
inject_missing("Phone", 0.10)
inject_missing("Annual_Income", 0.05)


print("Missing values injected.")
email_rows = np.random.choice(
    df.index,
    3000,
    replace=False
)

invalid_emails = [
    "abc.com",
    "hello@",
    "user@@gmail.com"
]


df.loc[
    email_rows,
    "Email"
] = np.random.choice(
    invalid_emails,
    len(email_rows)
)

age_rows = np.random.choice(
    df.index,
    2000,
    replace=False
)

df.loc[
    age_rows,
    "Age"
] = np.random.choice(
    [-5, 150, 200],
    len(age_rows)
)

print("Invalid data injected.")

city_rows = np.random.choice(
    df.index,
    8000,
    replace=False
)


for idx in city_rows:

    value = df.loc[idx, "City"]

    df.loc[idx, "City"] = random.choice([
        value.lower(),
        value.upper(),
        f" {value} "
    ])

country_rows = np.random.choice(
    df.index,
    10000,
    replace=False
)


df.loc[
    country_rows,
    "Country"
] = np.random.choice(
    [
        "india",
        "INDIA",
        " India "
    ],
    len(country_rows)
)

segment_rows = np.random.choice(
    df.index,
    5000,
    replace=False
)


for idx in segment_rows:

    value = df.loc[idx, "Customer_Segment"]

    df.loc[idx, "Customer_Segment"] = random.choice([
        value.lower(),
        value.upper(),
        f" {value} "
    ])


print("Consistency issues injected.")

duplicate_ids = np.random.choice(
    df["Customer_ID"],
    3000,
    replace=False
)


duplicate_rows = []


for customer_id in duplicate_ids:

    city = random.choice(cities)

    duplicate_rows.append({

        "Customer_ID":
            customer_id,

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
            city,

        "State":
            states[city],

        "Country":
            "India",

        "Join_Date":
            fake.date_between("-10y","today"),

        "Last_Purchase_Date":
            fake.date_between("-5y","today"),

        "Customer_Segment":
            random.choice(segments),

        "Annual_Income":
            random.randint(
                300000,
                2000000
            ),

        "Transaction_Count":
            random.randint(1,500),

        "Customer_Score":
            random.randint(1,100)
    })


duplicate_df = pd.DataFrame(
    duplicate_rows
)


df = pd.concat(
    [df, duplicate_df],
    ignore_index=True
)


print("Business duplicates injected.")

available = df[
    ~df["Customer_ID"].isin(
        duplicate_ids
    )
]


exact_duplicates = available.sample(
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

income_rows = np.random.choice(
    df.index,
    500,
    replace=False
)


df.loc[
    income_rows,
    "Annual_Income"
] = 1000000000


transaction_rows = np.random.choice(
    df.index,
    300,
    replace=False
)


df.loc[
    transaction_rows,
    "Transaction_Count"
] = 100000


print("Outliers injected.")

date_rows = np.random.choice(
    df.index,
    2500,
    replace=False
)


formats = [
    "%d/%m/%Y",
    "%d-%b-%y",
    "%b %d, %Y"
]


for idx in date_rows:

    date = pd.to_datetime(
        df.loc[idx, "Join_Date"]
    )

    df.loc[idx, "Join_Date"] = date.strftime(
        random.choice(formats)
    )


print("Date formatting issues injected.")

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


path = (
    "data/benchmark/"
    "DATATSTY_Enterprise_Benchmark_v1_1.csv"
)


df.to_csv(
    path,
    index=False
)


print("\nDATATSTY Benchmark v1.1 Created Successfully!")

print(
    f"Shape: {df.shape}"
)

print(
    f"Saved to: {path}"
)

