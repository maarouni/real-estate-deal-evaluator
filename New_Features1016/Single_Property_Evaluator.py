
import streamlit as st
from calculations import calculate_metrics
from pdf_generator_single import generate_pdf

st.set_page_config(page_title="🏡 Single Property Evaluator", layout="centered")

st.title("🏡 Real Estate Deal Evaluator")

st.markdown("Analyze the investment potential of a single property.")

# --- Sidebar Inputs ---
st.sidebar.header("📌 Property Information")
address = st.sidebar.text_input("Street Address (optional)")
zip_code = st.sidebar.text_input("ZIP Code (optional)")

purchase_price = st.sidebar.number_input("Purchase Price ($)", min_value=10000, step=1000, value=300000)
monthly_rent = st.sidebar.number_input("Expected Monthly Rent ($)", min_value=0, step=50, value=2000)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ($: property tax, insurance, miscellaneous)", min_value=0, step=50, value=300)

st.sidebar.header("💰 Financing & Growth")
down_payment_pct = st.sidebar.slider("Down Payment (%)", 0, 100, 20)
interest_rate = st.sidebar.slider("Interest Rate (%)", 0.0, 15.0, 6.5)
loan_term = st.sidebar.number_input("Loan Term (years)", min_value=1, value=30)
vacancy_rate = st.sidebar.slider("Vacancy Rate (%)", 0, 100, 5)
appreciation_rate = st.sidebar.slider("Appreciation Rate (%)", 0, 15, 3)
rent_growth_rate = st.sidebar.slider("Annual Rent Growth Rate (%)", 0, 10, 2)
time_horizon = st.sidebar.slider("Investment Horizon (years)", 1, 30, 10)

# --- Calculate Metrics ---
metrics = calculate_metrics(purchase_price, monthly_rent, down_payment_pct, interest_rate,
                            loan_term, monthly_expenses, vacancy_rate, appreciation_rate,
                            rent_growth_rate, time_horizon)

# --- Display Results ---
st.subheader("📈 Long-Term Metrics")
col1, col2 = st.columns(2)
col1.metric("IRR (%)", f"{metrics.get('irr (%)', 0):.2f}")
col2.metric("Equity Multiple", f"{metrics.get('equity_multiple', 0):.2f}")

st.subheader("💵 First Year Cash Flow")
st.metric("First Year Cash Flow ($)", f"{metrics.get('First Year Cash Flow ($)', 0):,.0f}")
st.metric("Cap Rate (%)", f"{metrics.get('Cap Rate (%)', 0):.2f}")
st.metric("Cash-on-Cash Return (%)", f"{metrics.get('Cash-on-Cash Return (%)', 0):.2f}")
st.metric("Monthly Mortgage ($)", f"{metrics.get('Monthly Mortgage ($)', 0):,.0f}")
st.metric("Grade", metrics.get("Grade", "N/A"))

# --- Download User Manual ---
st.markdown("---")
with open("User_Manual_Investment_Metrics_Explained_Styled_Final.pdf", "rb") as f:
    st.download_button(
        label="📘 Download User Manual (PDF)",
        data=f,
        file_name="Investment_Metrics_User_Guide.pdf",
        mime="application/pdf"
    )

# --- Export to PDF ---
if st.button("📄 Generate PDF Report"):
    generate_pdf(metrics, address, zip_code)
    st.success("✅ PDF generated successfully.")
