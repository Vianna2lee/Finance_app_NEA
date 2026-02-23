inputs = {
    "Option Type": option_type,
    "Option Kind": option_kind,
    "Current Stock Price (S0)": s0,
    "Strike Price": strike_price,
    "Volatility": volatility_of_stock,
    "Start Date": start_date,
    "End Date": end_date,
    "Risk-Free Interest Rate": risk_free_interest_rate
}

# 2. Identify which ones are None
missing_fields = [name for name, value in inputs.items() if value is None]

# 3. Display specific errors
if missing_fields:
    for field in missing_fields:
        st.error(f"The field '{field}' is required.")