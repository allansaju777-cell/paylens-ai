import pandas as pd
import random
from datetime import datetime, timedelta


# Make the generated data repeatable
random.seed(42)


# -----------------------------------------
# FAKE CUSTOMERS
# -----------------------------------------

customers = [
    "Arjun Mehta",
    "Rahul Sharma",
    "Priya Nair",
    "Rohan Kumar",
    "Ananya Menon",
    "Vivek Rao",
    "Sneha Patel",
    "Karan Singh",
    "Neha Gupta",
    "Aditya Verma",
    "Aisha Khan",
    "Riya Thomas",
    "Akash Das",
    "Meera Iyer",
    "Varun Shah"
]


# -----------------------------------------
# FAKE PRODUCTS
# -----------------------------------------

products = [
    "Starter Plan",
    "Pro Plan",
    "Business Plan",
    "Enterprise Plan"
]


# -----------------------------------------
# CREATE TRANSACTIONS
# -----------------------------------------

rows = []

start_date = datetime(2026, 1, 1)


for i in range(1500):

    customer = random.choice(customers)

    date = start_date + timedelta(
        days=random.randint(0, 240)
    )

    product = random.choice(products)

    amount = random.choice([
        299,
        499,
        799,
        999,
        1499,
        2499,
        4999,
        9999
    ])

    status = random.choices(
        ["success", "failed"],
        weights=[90, 10]
    )[0]

    rows.append({

        "transaction_id":
            f"TX{i+1:05}",

        "date":
            date.strftime("%Y-%m-%d"),

        "customer":
            customer,

        "product":
            product,

        "amount":
            amount,

        "status":
            status
    })


# -----------------------------------------
# CREATE DATAFRAME
# -----------------------------------------

df = pd.DataFrame(rows)


# -----------------------------------------
# SAVE CSV
# -----------------------------------------

df.to_csv(
    "transactions.csv",
    index=False
)


print("================================")
print("SUCCESS!")
print("================================")

print(
    f"Created {len(df)} transactions."
)

print(
    "Saved as transactions.csv"
)