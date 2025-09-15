
import streamlit as st
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import matplotlib.pyplot as plt
from calculations import calculate_metrics
from pdf_generator import generate_pdf

# Title
#st.markdown("<h1 style='text-align: center;'>🏡 Real Estate Deal Evaluator</h1>", unsafe_allow_html=True)
st.markdown("""<div style='text-align: center; margin-top: -40px;'><h1>🏡 Real Estate Deal Evaluator</h1></div>""", unsafe_allow_html=True)
#st.markdown("### 🧾 Property & Loan Inputs")

load_dotenv()

# Sidebar inputs
st.sidebar.header("📊 Property & Loan Inputs")
purchase_price = st.sidebar.number_input("Purchase Price ($)", value=300000)
monthly_rent = st.sidebar.number_input("Expected Monthly Rent ($)", value=2000)
down_payment_pct = st.sidebar.slider("Down Payment (%)", min_value=0, max_value=100, value=20)
interest_rate = st.sidebar.slider("Interest Rate (%)", min_value=0.0, max_value=10.0, value=6.5)
loan_term = st.sidebar.number_input("Loan Term (years)", value=30)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ($)", value=400)
vacancy_rate = st.sidebar.slider("Vacancy Rate (%)", min_value=0, max_value=100, value=5)
appreciation_rate = st.sidebar.slider("Annual Appreciation Rate (%)", min_value=0, max_value=10, value=3)
rent_growth_rate = st.sidebar.slider("Annual Rent Growth Rate (%)", min_value=0, max_value=10, value=3)

# Calculate metrics
metrics = calculate_metrics(
    purchase_price,
    monthly_rent,
    down_payment_pct,
    interest_rate,
    loan_term,
    monthly_expenses,
    vacancy_rate,
    appreciation_rate,
    rent_growth_rate
)

# Prepare property_data
property_data = {
    "Purchase Price": purchase_price,
    "Monthly Rent": monthly_rent,
    "Down Payment (%)": down_payment_pct,
    "Interest Rate (%)": interest_rate,
    "Loan Term": loan_term,
    "Monthly Expenses": monthly_expenses,
    "Vacancy Rate (%)": vacancy_rate,
    "Appreciation Rate (%)": appreciation_rate,
    "Rent Growth Rate (%)": rent_growth_rate
}

# Generate PDF
summary_text = f"This is a {metrics['Grade']}-grade rental with upside potential"
pdf_bytes = generate_pdf(property_data, metrics, summary_text)

# Plotting
st.subheader("📈 10-Year Cash Flow Projection")
fig, ax = plt.subplots()
ax.plot(range(1, 11), metrics["10yr Cash Flow"], marker='o', linestyle='-', label="Annual Cash Flow ($)")
ax.plot(range(1, 11), metrics["10yr Rents"], marker='s', linestyle='--', label="Projected Rent ($)")
ax.set_xlabel("Year")
ax.set_ylabel("Projected Cash Flow Over 10 Years")
ax.set_title("10-Year Projected Cash Flow")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Download
st.download_button(
    label="📄 Download PDF Report",
    data=pdf_bytes,
    file_name="real_estate_report.pdf",
    mime="application/pdf"
)

# Email Section
st.markdown("### 📨 Email This Report")
recipient_email = st.text_input("Enter email address to send the report", placeholder="you@example.com")

# Debug diagnostics

if st.button("Send Email Report") and recipient_email:
    # ✅ UI-level validation of malformed email inputs
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", recipient_email):
        st.error("❌ Please enter a valid email address.")
        st.stop()
    try:
        st.write("📤 Attempting to send email...")
        msg = EmailMessage()
        msg["Subject"] = "Your Real Estate Evaluation Report"
        msg["From"] = os.getenv("GMAIL_USER")
        msg["To"] = recipient_email
        msg.set_content("Please find attached your real estate evaluation report.")
        pdf_bytes.seek(0)
        msg.add_attachment(pdf_bytes.read(), maintype='application', subtype='pdf', filename="real_estate_report.pdf")

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASSWORD"))
            smtp.send_message(msg)

        st.success(f"✅ Report sent to {recipient_email}!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
