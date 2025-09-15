
import streamlit as st
from calculations import calculate_metrics
from pdf_generator import generate_pdf_report
import re
import base64
import smtplib
from email.message import EmailMessage
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Real Estate Evaluator", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>🏡 Real Estate Deal Evaluator</h1>", unsafe_allow_html=True)
st.markdown("### 🧾 Property & Loan Inputs")

# --- Input fields
col1, col2 = st.columns(2)
with col1:
    purchase_price = st.number_input("Purchase Price ($)", min_value=0, value=300000)
    rent = st.number_input("Expected Monthly Rent ($)", min_value=0, value=2000)
    down_payment_percent = st.slider("Down Payment (%)", 0, 100, 20)
    interest_rate = st.slider("Interest Rate (%)", 0.0, 15.0, 6.5)
with col2:
    loan_term = st.number_input("Loan Term (years)", min_value=1, value=30)
    expenses = st.number_input("Monthly Expenses ($)", min_value=0, value=300)
    vacancy_rate = st.slider("Vacancy Rate (%)", 0, 100, 5)
    appreciation_rate = st.slider("Annual Appreciation Rate (%)", 0, 10, 3)
    rent_growth_rate = st.slider("Annual Rent Growth Rate (%)", 0, 10, 3)

# Email input
email = st.text_input("Email Address")

# Submit button
if st.button("Calculate & Generate Report"):
    # Basic email format validation
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        st.error("❌ Please enter a valid email address.")
    else:
        metrics = calculate_metrics(
            purchase_price=purchase_price,
            rent=rent,
            down_payment_percent=down_payment_percent,
            interest_rate=interest_rate,
            loan_term=loan_term,
            expenses=expenses,
            vacancy_rate=vacancy_rate,
            appreciation_rate=appreciation_rate,
            rent_growth_rate=rent_growth_rate
        )

        # --- PDF Generation
        summary_text = f"Annual Cash Flow: ${metrics['Annual Cash Flow ($)']:,}"
        pdf_buffer = generate_pdf_report(
            {
                "Purchase Price": f"${purchase_price:,}",
                "Down Payment": f"{down_payment_percent}%",
                "Loan Term": f"{loan_term} years",
                "Interest Rate": f"{interest_rate}%",
            },
            metrics,
            summary_text
        )

        # --- Display Matplotlib chart
        years = list(range(1, 11))
        cash_flow = metrics['10-Year Cash Flow Projection']['Annual Cash Flow ($)']
        rent_projection = metrics['10-Year Cash Flow Projection']['Projected Rent ($)']
        fig, ax = plt.subplots()
        ax.plot(years, cash_flow, label="Annual Cash Flow ($)", marker='o')
        ax.plot(years, rent_projection, label="Projected Rent ($)", linestyle='--')
        ax.set_title("📈 10-Year Cash Flow Projection")
        ax.set_xlabel("Year")
        ax.set_ylabel("Projected Cash Flow Over 10 Years")
        ax.legend()
        st.pyplot(fig)

        # --- PDF Download
        b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="report.pdf">📄 Download PDF Report</a>'
        st.markdown(href, unsafe_allow_html=True)

        # --- Email Section
        st.markdown("### 📤 Email This Report")
        st.write("Enter email address to send the report")
        try:
            msg = EmailMessage()
            msg["Subject"] = "Real Estate Deal Evaluation Report"
            msg["From"] = "your_email@gmail.com"
            msg["To"] = email
            msg.set_content("Attached is your Real Estate evaluation report.")
            msg.add_attachment(pdf_buffer.read(), maintype="application", subtype="pdf", filename="report.pdf")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login("your_email@gmail.com", "your_app_password")
                smtp.send_message(msg)
            st.success("✅ Email sent successfully.")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
