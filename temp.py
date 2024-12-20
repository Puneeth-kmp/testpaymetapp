import streamlit as st
import razorpay

# Razorpay API credentials
RAZORPAY_KEY_ID = "rzp_test_Gi6vQ4opJMDS5u"
RAZORPAY_KEY_SECRET = "bE7fdzTpU49kPXsMZNfc3MC6"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# App title
st.title("Razorpay Payment Gateway Test")
st.header("Test Payment with ₹10")

# Fixed test amount
amount = 10

if st.button("Pay ₹10 Now"):
    # Create Razorpay order
    try:
        order_data = {
            "amount": amount * 100,  # Convert amount to paise
            "currency": "INR",
            "payment_capture": 1
        }
        order = client.order.create(order_data)

        st.write("**Payment Details**")
        st.json(order)

        # Razorpay Checkout Script
        st.markdown(
            f"""
            <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
            <script>
                var options = {{
                    "key": "{RAZORPAY_KEY_ID}",
                    "amount": {order['amount']},  // Amount in paise
                    "currency": "INR",
                    "name": "Test Payment",
                    "description": "Pay ₹10",
                    "order_id": "{order['id']}",
                    "handler": function (response) {{
                        alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
                        // You can call your server here to verify the payment
                    }},
                    "prefill": {{
                        "name": "Test User",
                        "email": "test@example.com",
                        "contact": "9999999999"
                    }},
                    "theme": {{
                        "color": "#3399cc"
                    }}
                }};
                var rzp1 = new Razorpay(options);
                rzp1.open();
            </script>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
