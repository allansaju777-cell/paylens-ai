import streamlit as st
import pandas as pd

from finance_tools import (
    get_product_performance
)

from ai_agent import ask_agent


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(

    page_title="PayLens AI",

    page_icon="💰",

    layout="wide"
)


# =========================================
# CUSTOM STYLING
# =========================================

st.markdown(

    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    </style>
    """,

    unsafe_allow_html=True
)


# =========================================
# TITLE
# =========================================

st.title("💰 PayLens AI")

st.caption(
    "AI-powered business finance assistant"
)


# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(
    "transactions.csv"
)


# =========================================
# SEPARATE SUCCESS / FAILED
# =========================================

successful = df[
    df["status"] == "success"
]


failed = df[
    df["status"] == "failed"
]


# =========================================
# CALCULATE DASHBOARD NUMBERS
# =========================================

revenue = successful[
    "amount"
].sum()


successful_count = len(
    successful
)


customer_count = successful[
    "customer"
].nunique()
    

failed_count = len(
    failed
)


# =========================================
# METRICS
# =========================================

col1, col2, col3, col4 = st.columns(4)


col1.metric(

    "💰 Revenue",

    f"₹{revenue:,.0f}"
)


col2.metric(

    "💳 Successful Payments",

    successful_count
)


col3.metric(

    "👥 Customers",

    customer_count
)


col4.metric(

    "❌ Failed Payments",

    failed_count
)


# =========================================
# BUSINESS SNAPSHOT
# =========================================

st.divider()

st.subheader(
    "🤖 Business Snapshot"
)


st.info(

    f"""
    Your business has generated
    ₹{revenue:,.0f} from
    {successful_count:,} successful payments.

    You currently have
    {failed_count:,} failed payments.

    Ask PayLens AI below to analyze
    your business data.
    """

)


# =========================================
# PRODUCT CHART
# =========================================

st.subheader(
    "📊 Revenue by Product"
)


product_data = (
    get_product_performance()
)


chart_df = pd.DataFrame(

    list(
        product_data.items()
    ),

    columns=[
        "Product",
        "Revenue"
    ]
)


st.bar_chart(

    chart_df.set_index(
        "Product"
    )
)


# =========================================
# AI CHAT
# =========================================

st.divider()

st.subheader(
    "🤖 Ask PayLens AI"
)


st.write(
    "Ask questions about your business "
    "payment data."
)


question = st.chat_input(

    "Example: Who are my top customers?"
)


if question:

    # USER MESSAGE

    with st.chat_message(
        "user"
    ):

        st.write(
            question
        )


    # AI MESSAGE

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Analyzing your business data..."
        ):

            try:

                answer = ask_agent(
                    question
                )

                st.write(
                    answer
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# =========================================
# RECENT TRANSACTIONS
# =========================================

st.divider()

st.subheader(
    "💳 Recent Transactions"
)


st.dataframe(

    df.sort_values(

        "date",

        ascending=False

    ).head(20),

    use_container_width=True
)