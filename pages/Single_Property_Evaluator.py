
import streamlit as st
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import matplotlib.pyplot as plt
from calculations import calculate_metrics
from pdf_generator_single import generate_pdf
from pdf_generator_single import generate_ai_verdict

# 🔐 Password Gate — load from .env or fallback
load_dotenv()
# Default password (can be overridden by .env)
APP_PASSWORD = os.getenv("APP_PASSWORD", "SmartInvest1!")

# Use session state to remember successful login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Show password input only if not yet authenticated
if not st.session_state.authenticated:
    st.title("🏠 Real Estate Deal Evaluator")
    password = st.text_input("🔒 Please enter access password", type="password")

    if password == APP_PASSWORD:
        st.session_state.authenticated = True
        st.rerun()  # 🔁 Clear the password input and reload
    elif password:
        st.error("❌ Incorrect password. Please try again.")
    st.stop()  # 🔒 Block access until correct
    
# ✅ MAIN APP STARTS HERE — only shown after password is correct
#st.title("🏠 Real Estate Deal Evaluator")    


# Title
#st.markdown("<h1 style='text-align: center;'>🏡 Real Estate Deal Evaluator</h1>", unsafe_allow_html=True)
st.markdown("""<div style='text-align: center; margin-top: -40px;'><h1>🏡 Real Estate Deal Evaluator</h1></div>""", unsafe_allow_html=True)
#st.markdown("""<div style='width: 100%; padding-left: 10%;'><h1 style='text-align: left;'>🏡 Real Estate Deal Evaluator</h1></div>""", unsafe_allow_html=True)
#st.markdown("### 🧾 Property & Loan Inputs")

load_dotenv()

# Sidebar inputs
st.sidebar.header("📊 Property, Loan & Investment Settings")
purchase_price = st.sidebar.number_input("Purchase Price ($)", value=300000)
monthly_rent = st.sidebar.number_input("Expected Monthly Rent ($)", value=2000)
down_payment_pct = st.sidebar.slider("Down Payment (%)", min_value=0, max_value=100, value=20)
interest_rate = st.sidebar.slider("Interest Rate (%)", min_value=0.0, max_value=10.0, value=6.5)
loan_term = st.sidebar.number_input("Loan Term (years)", value=30)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ($)", value=400)
vacancy_rate = st.sidebar.slider("Vacancy Rate (%)", min_value=0, max_value=100, value=5)
appreciation_rate = st.sidebar.slider("Annual Appreciation Rate (%)", min_value=0, max_value=10, value=3)
rent_growth_rate = st.sidebar.slider("Annual Rent Growth Rate (%)", min_value=0, max_value=10, value=3)
time_horizon = st.sidebar.slider("⏳ Investment Time Horizon (Years)", min_value=1, max_value=30, value=10)

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
    rent_growth_rate,
    time_horizon
)
irr_value = metrics.get("irr (%)", 0)
#st.metric("IRR (%)", round(irr_value, 2))

# Prepare inputs and call AI verdict generator
verdict_input = {
    "ROI (%)": metrics.get("ROI (%)"),
    "Multi-Year Cash Flow": metrics.get("Multi-Year Cash Flow", []),
    "Cap Rate (%)": metrics.get("Cap Rate (%)"),
    "Cash-on-Cash Return (%)": metrics.get("Cash-on-Cash Return (%)"),
    # this dict can be expanded as needed for future AI grading refinements
}

summary_text, grade = generate_ai_verdict(metrics)

# Add verdict to metrics so pdf_generator can consume it
metrics["AI Verdict"] = summary_text
metrics["Grade"] = grade

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

# IRR and Equity Multiple
st.subheader("📈 Long-Term Metrics")
col1, col2 = st.columns(2)
col1.metric("IRR (%)", f"{metrics.get('irr (%)', 0):.2f}")
col2.metric("Equity Multiple", f"{metrics.get('equity_multiple', 0):.2f}")

#if pdf_bytes is not None:
    #st.download_button(
        #label="📄 Download PDF Report",
        #data=pdf_bytes,
        #file_name="real_estate_report.pdf",
        #mime="application/pdf"
    #)
#else:
    #st.error("⚠️ PDF generation failed. Please check your input or logs.")

# Plotting
# 📈 10-Year Cash Flow Projection
st.subheader("📈 Multi-Year Cash Flow Projection")
fig, ax = plt.subplots()

# Define common x-axis values — always based on time_horizon
years = list(range(1, time_horizon + 1))

# Plot primary y-axis: Cash Flow & Rent
ax.plot(years, metrics["Multi-Year Cash Flow"], marker='o', linestyle='-', label="Multi-Year Cash Flow ($)")
ax.plot(years, metrics["Annual Rents $ (by year)"], marker='s', linestyle='--', label="Projected Rent ($)")
ax.set_xlabel("Year")
ax.set_ylabel("Projected Cash Flow / Rent ($)")
ax.grid(True)

# Add second y-axis for ROI
ax2 = ax.twinx()
ax2.plot(years, metrics["Annual ROI % (by year)"], color='green', marker='^', linestyle='-', label="ROI (%)")
ax2.set_ylabel("ROI (%)", color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Combine legends from both axes
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, loc="upper left")

# Title and Show Plot
ax.set_title("Multi - Year Projected Cash Flow & ROI")
st.pyplot(fig)

# PDF Download Button
if pdf_bytes is not None:
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name="real_estate_report.pdf",
        mime="application/pdf",
        key="download_pdf_unique"   # ✅ Prevents collision
    )
else:
    st.error("⚠️ PDF generation failed. Please check your input or logs.")

# Download
#st.download_button(
    #label="📄 Download PDF Report",
    #data=pdf_bytes,
    #file_name="real_estate_report.pdf",
    #mime="application/pdf"
#)

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
        msg["From"] = os.getenv("EMAIL_USER")  # ✅ From address
        msg["To"] = recipient_email
        msg.set_content("Please find attached your real estate evaluation report.")
        pdf_bytes.seek(0)
        msg.add_attachment(pdf_bytes.read(), maintype='application', subtype='pdf', filename="real_estate_report.pdf")

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD")) # GMAIL was changed to EMAIL!!!
            smtp.send_message(msg)

        st.success(f"✅ Report sent to {recipient_email}!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
