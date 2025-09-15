
import streamlit as st
from calculations import calculate_metrics
from pdf_generator import generate_pdf_report
import io
import re
import base64

# Title
st.markdown("<h1 style='text-align: center;'>🏡 Real Estate Deal Evaluator</h1>", unsafe_allow_html=True)
st.markdown("### 🧾 Property & Loan Inputs")

# Inputs
col1, col2 = st.columns(2)
with col1:
    purchase_price = st.number_input("Purchase Price ($)", value=300000, step=1000)
    monthly_rent = st.number_input("Expected Monthly Rent ($)", value=2000, step=100)
    down_payment_percent = st.slider("Down Payment (%)", min_value=0, max_value=100, value=20)
    interest_rate = st.slider("Interest Rate (%)", min_value=0.0, max_value=10.0, value=6.5)
with col2:
    loan_term_years = st.number_input("Loan Term (years)", value=30, step=1)
    monthly_expenses = st.number_input("Monthly Expenses ($)", value=300, step=50)
    vacancy_rate = st.slider("Vacancy Rate (%)", min_value=0, max_value=100, value=5)
    appreciation_rate = st.slider("Annual Appreciation Rate (%)", min_value=0, max_value=20, value=3)
    rent_growth_rate = st.slider("Annual Rent Growth Rate (%)", min_value=0, max_value=20, value=3)

email = st.text_input("Email Address")

# Button to calculate
if st.button("Calculate & Generate Report"):
    if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email):
        st.error("❌ Please enter a valid email address.")
    else:
        metrics = calculate_metrics(
            purchase_price=purchase_price,
            monthly_rent=monthly_rent,
            down_payment_percent=down_payment_percent,
            interest_rate=interest_rate,
            loan_term_years=loan_term_years,
            monthly_expenses=monthly_expenses,
            vacancy_rate=vacancy_rate,
            appreciation_rate=appreciation_rate,
            rent_growth_rate=rent_growth_rate,
        )

        st.success("✅ Calculation completed. See below:")
        st.write(metrics["summary"])
        st.pyplot(metrics["chart"])

        pdf = generate_pdf_report(metrics["summary"], metrics["chart_image"])

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name="real_estate_report.pdf",
            mime="application/pdf",
        )

        st.markdown("---")
        st.subheader("📨 Email This Report")
        st.text_input("Enter email address to send the report", value=email)
        st.info("📤 Email sending feature is stubbed in this demo.")

