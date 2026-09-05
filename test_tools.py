from finance_tools import (
    get_revenue,
    get_top_customers,
    get_failed_payments,
    get_product_performance,
    detect_suspicious_transactions
)


print("\n========== REVENUE ==========")

print(
    get_revenue()
)


print("\n========== TOP CUSTOMERS ==========")

print(
    get_top_customers()
)


print("\n========== FAILED PAYMENTS ==========")

print(
    get_failed_payments()
)


print("\n========== PRODUCT PERFORMANCE ==========")

print(
    get_product_performance()
)


print("\n========== SUSPICIOUS TRANSACTIONS ==========")

print(
    detect_suspicious_transactions()[:5]
)