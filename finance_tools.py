import pandas as pd


# -----------------------------------------
# LOAD TRANSACTION DATA
# -----------------------------------------

df = pd.read_csv(
    "transactions.csv"
)


# Convert date into proper date format
df["date"] = pd.to_datetime(
    df["date"]
)


# -----------------------------------------
# TOOL 1: REVENUE
# -----------------------------------------

def get_revenue():
    """
    Calculate total revenue from
    successful payments.
    """

    successful = df[
        df["status"] == "success"
    ]

    revenue = successful[
        "amount"
    ].sum()

    return {

        "total_revenue":
            float(revenue),

        "successful_transactions":
            int(len(successful))
    }


# -----------------------------------------
# TOOL 2: TOP CUSTOMERS
# -----------------------------------------

def get_top_customers():
    """
    Find the top 10 customers
    based on total spending.
    """

    successful = df[
        df["status"] == "success"
    ]

    result = (
        successful
        .groupby("customer")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    return result.to_dict()


# -----------------------------------------
# TOOL 3: FAILED PAYMENTS
# -----------------------------------------

def get_failed_payments():
    """
    Find failed payment statistics.
    """

    failed = df[
        df["status"] == "failed"
    ]

    return {

        "failed_transactions":
            int(len(failed)),

        "failed_amount":
            float(
                failed["amount"].sum()
            )
    }


# -----------------------------------------
# TOOL 4: PRODUCT PERFORMANCE
# -----------------------------------------

def get_product_performance():
    """
    Calculate revenue for each product.
    """

    successful = df[
        df["status"] == "success"
    ]

    result = (
        successful
        .groupby("product")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    return result.to_dict()


# -----------------------------------------
# TOOL 5: SUSPICIOUS TRANSACTIONS
# -----------------------------------------

def detect_suspicious_transactions():
    """
    Find unusually large transactions.

    This is only a simple anomaly detector.
    It is NOT a real fraud detection system.
    """

    successful = df[
        df["status"] == "success"
    ]

    suspicious = successful[
        successful["amount"] >= 9000
    ]

    return suspicious[
        [
            "transaction_id",
            "date",
            "customer",
            "product",
            "amount"
        ]
    ].to_dict(
        orient="records"
    )