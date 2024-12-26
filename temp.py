import streamlit as st

# App title
st.title("Razorpay Payment Gateway Test")

# Payment links
payment_links = {
    "₹10": "https://razorpay.me/@jstautomation?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
    "₹50": "https://razorpay.me/@jstautomation?amount=bMZtQmLjQWplBAmd%2FyQdEA%3D%3D"
}

# Create a dropdown for selecting amount
amount_choice = st.selectbox("Select Amount to Pay", options=list(payment_links.keys()))

st.header(f"Test Payment with {amount_choice}")

# Button to redirect to the payment link
if st.button(f"Pay {amount_choice} Now"):
    # Redirect to the appropriate Razorpay payment link
    st.markdown(f"[Click here to make payment of {amount_choice}]( {payment_links[amount_choice]} )")
