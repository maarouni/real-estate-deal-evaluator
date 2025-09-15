
import streamlit as st
from calculations import calculate_metrics
from pdf_generator import generate_pdf
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Real Estate Evaluator", layout="centered")
st.title("🏠 Real Estate Evaluator")
st.markdown("Quickly assess if a property is a good investment using simple inputs. No login required.")

# --- Input Section ---
st.header("🔢 Property & Financing Info")
purchase_price = st.number_input("Purchase Price ($)", min_value=0, value=300000)
monthly_rent = st.number_input("Expected Monthly Rent ($)", min_value=0, value=2000)
down_payment_pct = st.slider("Down Payment (%)", min_value=0, max_value=100, value=20)
interest_rate = st.number_input("Loan Interest Rate (%)", min_value=0.0, value=6.5)
loan_term = st.selectbox("Loan Term (years)", [15, 20, 30], index=2)
monthly_expenses = st.number_input("Monthly Operating Expenses ($)", min_value=0, value=500)
vacancy_rate = st.slider("Vacancy Rate (%)", min_value=0, max_value=100, value=5)
appreciation_rate = st.slider("Annual Appreciation Rate (%)", min_value=0, max_value=10, value=3)

# Rent Growth Toggle
rent_growth_rate = st.slider("📈 Simulate x% Annual Rent Growth", 0.0, 10.0, 3.0)

# --- Button ---
load_dotenv()

if st.button("📊 Evaluate Deal"):
    results = calculate_metrics(
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

    st.success("📈 Deal Evaluation Results")
    for key in ["Cap Rate (%)", "Cash-on-Cash Return (%)", "ROI (%)", "Annual Cash Flow ($)", "Monthly Mortgage ($)"]:
        st.write(f"**{key}**: {results[key]}")

    st.subheader(f"🏅 Deal Grade: **{results['Grade']}**")

    # Plot 10-Year Cash Flow
    st.subheader("📊 10-Year Cash Flow Projection")
    fig, ax = plt.subplots()
    years = list(range(1, 11))
    ax.plot(years, results["10yr Cash Flow"], marker='o', linestyle='-', label="Annual Cash Flow ($)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cash Flow ($)")
    ax.set_title("Projected Cash Flow Over 10 Years")
    ax.grid(True)
    st.pyplot(fig)

    # PDF download
    st.subheader("📥 Export Report")
    pdf_bytes = generate_pdf(results)
    st.download_button(

    # Optional email form
    )
    st.subheader("✉️ Email This Report")
    recipient_email = st.text_input("Enter email address to send the report")
    if st.button("Send Email") and recipient_email:
        msg = EmailMessage()
        msg['Subject'] = "Your Real Estate Deal Report"
        msg['From'] = os.getenv('GMAIL_USER')
        msg['To'] = recipient_email
        msg.set_content("Attached is your property evaluation report.")

        msg.add_attachment(pdf_bytes.read(), maintype='application', subtype='pdf', filename='real_estate_report.pdf')
        pdf_bytes.seek(0)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'))
                smtp.send_message(msg)
            st.success(f"✅ Email sent to {recipient_email}!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

    # Reload PDF bytes for download button
    pdf_bytes.seek(0)

    st.download_button(
        label="📄 Download PDF Summary",
        data=pdf_bytes,
        file_name="real_estate_evaluation_report.pdf",
        mime="application/pdf"
    )

# --- Footer ---
st.markdown("---")
st.caption("🚀 MVP v0.4 | Now includes deal grading, cash flow chart, and PDF export.")
