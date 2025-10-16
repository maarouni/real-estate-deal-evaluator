
import streamlit as st
from io import BytesIO
import os
import sys  # ✅ Move this before using sys
sys.path.append(os.path.abspath(".."))  # ✅ Now valid
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import matplotlib.pyplot as plt
import pandas as pd
from calculations import calculate_metrics
from pdf_generator_dual import generate_pdf , generate_comparison_pdf , generate_comparison_pdf_table_style
load_dotenv()

#from pdf_generator import generate_comparison_pdf_table_style
 #✅ Add this right below the imports — before any Streamlit UI code
st.set_page_config(
    page_title="Dual Property Comparison Evaluator",
    layout="wide",
    initial_sidebar_state="expanded"
)
from pdf_generator_dual import generate_ai_verdict

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

    
# ✅ Titles shown only after succesful login
st.markdown("## 🏡 Real Estate Deal Evaluator")
#st.markdown("### 📈 Multi-Year Cash Flow Projection")
st.header("🔄 Side-by-Side Deal Comparison")

st.markdown(
    "<p style='font-size:18px; color:white; font-weight:bold;'>🔍 Compare investment options side-by-side to optimize ROI, cash flow, and equity growth.</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='font-size:18px; color:white; font-weight:bold;'>Input real numbers for Property A & B to model ROI, cash flow, and appreciation.</p>",
    unsafe_allow_html=True
)
st.markdown("---")
with open("User_Manual_Investment_Metrics_Explained_Styled_Final.pdf", "rb") as f:
    st.download_button(
        label="📘 Download User Manual (PDF)",
        data=f,
        file_name="Investment_Metrics_User_Guide.pdf",
        mime="application/pdf"
    )

    # Sidebar Title
#sidebar.markdown("## 🧾 Shared Financial Inputs")
st.sidebar.markdown("<h2 style='color:white; font-size:24px;'>🧾 Shared Financial Inputs</h2>", unsafe_allow_html=True)

# Explanatory Text - in white

st.sidebar.markdown(
    "<p style='color:white; font-size:16px;'>These settings apply to both Property A and Property B</p>",
    unsafe_allow_html=True
)


# Styled Sliders with slightly larger font via label formatting
interest_rate = st.sidebar.slider("📈 Interest Rate (%)", 0.0, 15.0, 5.5, 0.1)
loan_term = st.sidebar.slider("📆 Loan Term (years)", 5, 40, 30)
vacancy_rate = st.sidebar.slider("🏠 Vacancy Rate (%)", 0.0, 20.0, 5.0, 0.5)

# 👇 DO NOT include shared Down Payment slider here
    

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Property A")
    purchase_price_a = st.number_input("Purchase Price A", value=300000)
    down_payment_pct_a = st.slider("Down Payment A (%)", 0.0, 100.0, value=20.0, step=1.0)
    rent_a = st.number_input("Monthly Rent A", value=2000)
    monthly_expenses_a = st.number_input("Monthly Expenses A", value=300, key="monthly_expenses_a")
    appreciation_rate_a = st.slider("Annual Appreciation A (%)", 0.0, 10.0, value=3.0, step=0.1, key="appreciation_rate_a")
    rent_growth_rate_a = st.slider("Annual Rent Growth A (%)", 0.0, 10.0, value=2.0, step=0.1, key="rent_growth_rate_a")
    time_horizon_a = st.slider("Time Horizon A (Years)", 1, 30, value=10, key="time_horizon_a")
    # ...add other inputs like interest rate, years, etc.

with col2:
    st.subheader("🏘️ Property B")
    purchase_price_b = st.number_input("Purchase Price B", value=320000)
    down_payment_pct_b = st.slider("Down Payment B (%)", 0.0, 100.0, value=20.0, step=1.0)
    rent_b = st.number_input("Monthly Rent B", value=2100)
    monthly_expenses_b = st.number_input("Monthly Expenses B", value=300, key="monthly_expenses_b")
    appreciation_rate_b = st.slider("Annual Appreciation B (%)", 0.0, 10.0, value=3.0, step=0.1, key="appreciation_rate_b")
    rent_growth_rate_b = st.slider("Annual Rent Growth B (%)", 0.0, 10.0, value=2.0, step=0.1, key="rent_growth_rate_b")
    time_horizon_b = st.slider("Time Horizon A (Years)", 1, 30, value=10, key="time_horizon_b")
    # ...same structure

# Calculate metrics
# ---- Property A Metrics ----
metrics_a = calculate_metrics(
    purchase_price_a,
    rent_a,
    down_payment_pct_a,
    interest_rate,
    loan_term,
    monthly_expenses_a,
    vacancy_rate,
    appreciation_rate_a,
    rent_growth_rate_a,
    time_horizon_a
)

# ---- Property B Metrics ----
metrics_b = calculate_metrics(
    purchase_price_b,
    rent_b,
    down_payment_pct_b,
    interest_rate,
    loan_term,
    monthly_expenses_b,
    vacancy_rate,
    appreciation_rate_b,
    rent_growth_rate_b,
    time_horizon_b
)


if metrics_a and metrics_b:
    comparison_pdf = generate_comparison_pdf_table_style(metrics_a, metrics_b)
    st.download_button(
        label="📄 Download Comparison PDF",
        data=comparison_pdf,
        file_name="comparison_report.pdf",
        mime="application/pdf",
        key="download_comparison_pdf"
    )


# Title
#st.markdown("""<div style='text-align: center; margin-top: -40px;'><h1>🏡 Real Estate Deal Evaluator</h1></div>""", unsafe_allow_html=True)

load_dotenv()

# Prepare inputs and call AI verdict generator
verdict_input = {
    "ROI (%)": f"{metrics_a.get('ROI (%)', 0)} vs {metrics_b.get('ROI (%)', 0)}",
    "Multi-Year Cash Flow A": metrics_a.get("Multi-Year Cash Flow", []),
    "Multi-Year Cash Flow B": metrics_b.get("Multi-Year Cash Flow", []),
    "Cap Rate (%) A": metrics_a.get("Cap Rate (%)", 0),
    "Cap Rate (%) B": metrics_b.get("Cap Rate (%)", 0),
    "Cash-on-Cash Return (%) A": metrics_a.get("Cash-on-Cash Return (%)", 0),
    "Cash-on-Cash Return (%) B": metrics_b.get("Cash-on-Cash Return (%)", 0),
}

summary_text, grade = generate_ai_verdict(metrics_a, metrics_b)

# Add verdict to metrics so pdf_generator can consume it
metrics_a["AI Verdict"] = summary_text
metrics_a["Grade"] = grade
metrics_b["AI Verdict"] = summary_text
metrics_b["Grade"] = grade


# Prepare property_data
property_data = {
    "Purchase Price A": purchase_price_a,
    "Purchase Price B": purchase_price_b,
    "Monthly Rent A": rent_a,
    "Monthly Rent B": rent_b,
    "Down Payment (%) A": down_payment_pct_a,
    "Down Payment (%) B": down_payment_pct_b,
    "Monthly Expenses A": monthly_expenses_a,
    "Monthly Expenses B": monthly_expenses_b,
    "Appreciation Rate (%) A": appreciation_rate_a,
    "Appreciation Rate (%) B": appreciation_rate_b,
    "Rent Growth Rate (%) A": rent_growth_rate_a,
    "Rent Growth Rate (%) B": rent_growth_rate_b,
    
    # Shared inputs
    "Interest Rate (%)": interest_rate,
    "Loan Term (Years)": loan_term,
    "Vacancy Rate (%)": vacancy_rate,
}

# Generate PDF
summary_text = f"Property A is a {metrics_a['Grade']}-grade rental, and Property B is a {metrics_b['Grade']}-grade rental with upside potential"
pdf_bytes = generate_pdf(property_data, metrics_a, metrics_b, summary_text)

# ✅ Extract cash flow lists from metrics for plotting
cf_a = metrics_a.get("Multi-Year Cash Flow", [])
cf_b = metrics_b.get("Multi-Year Cash Flow", [])

# Ensure they are lists of numbers
if isinstance(cf_a, str):
    cf_a = [float(x.strip()) for x in cf_a.strip("[]").split(",") if x.strip()]
if isinstance(cf_b, str):
    cf_b = [float(x.strip()) for x in cf_b.strip("[]").split(",") if x.strip()]


# 📊 New 6-Curve Dual-Y Comparison Plot
st.subheader("📈 Multi-Year ROI, Rent & Cash Flow Comparison (A vs B)")

# ✅ INSERT THE NEW BLOCK RIGHT AFTER THAT:
st.subheader("📈 Long-Term Metrics")
col1, col2 = st.columns(2)

with col1:
    st.metric("IRR A (%)", f"{metrics_a.get('irr (%)', 0):.2f}")
    st.metric("Equity Multiple A", f"{metrics_a.get('equity_multiple', 0):.2f}")

with col2:
    st.metric("IRR B (%)", f"{metrics_b.get('irr (%)', 0):.2f}")
    st.metric("Equity Multiple B", f"{metrics_b.get('equity_multiple', 0):.2f}")

# Extract data from metrics
# Pad shorter cash flow list with None or 0
max_years = max(len(cf_a), len(cf_b))
cf_a += [0] * (max_years - len(cf_a))
cf_b += [0] * (max_years - len(cf_b))

rent_a = metrics_a.get("Annual Rents $ (by year)", [])
rent_b = metrics_b.get("Annual Rents $ (by year)", [])
roi_a = metrics_a.get("Annual ROI % (by year)", [])
roi_b = metrics_b.get("Annual ROI % (by year)", [])

# Use longest time horizon
#years = list(range(1, max(len(cf_a), len(cf_b)) + 1))
fig, ax1 = plt.subplots()
#fig, ax1 = plt.subplots(figsize=(10, 5))  # ✅ Create figure and axes
years_a = list(range(1, len(cf_a) + 1))
years_b = list(range(1, len(cf_b) + 1))

# ✅ Step 3: Defensive trim to avoid x/y mismatch
years_a = years_a[:min(len(years_a), len(rent_a), len(roi_a), len(cf_a))]
years_b = years_b[:min(len(years_b), len(rent_b), len(roi_b), len(cf_b))]
cf_a = cf_a[:len(years_a)]
cf_b = cf_b[:len(years_b)]
rent_a = rent_a[:len(years_a)]
rent_b = rent_b[:len(years_b)]
roi_a = roi_a[:len(years_a)]
roi_b = roi_b[:len(years_b)]

#ax1.plot(years_a, cf_a, marker='o', label="Cash Flow A ($)", color='blue')
#ax1.plot(years_b, cf_b, marker='o', label="Cash Flow B ($)", color='skyblue')


# Primary Y-axis: Cash Flow & Rent
ax1.plot(years_a, cf_a, marker='o', label="Cash Flow A ($)", color='blue')
ax1.plot(years_b, cf_b, marker='o', label="Cash Flow B ($)", color='skyblue')
ax1.plot(years_a, rent_a, marker='s', linestyle='--', label="Rent A ($)", color='orange')
ax1.plot(years_b, rent_b, marker='s', linestyle='--', label="Rent B ($)", color='goldenrod')
ax1.set_xlabel("Year")
ax1.set_ylabel("Cash Flow / Rent ($)")
ax1.grid(True)

# Secondary Y-axis: ROI
ax2 = ax1.twinx()
ax2.plot(years_a, roi_a, marker='^', linestyle='-', label="ROI A (%)", color='green')
ax2.plot(years_b, roi_b, marker='^', linestyle='--', label="ROI B (%)", color='darkgreen')
ax2.set_ylabel("ROI (%)", color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Merge legends from both y-axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# Final layout
ax1.set_title("Projected Cash Flow, Rent, and ROI Over Time")
st.pyplot(fig)


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
                # ✅ Debug prints BEFORE login
            #st.write("🔐 EMAIL_USER:", os.getenv("EMAIL_USER"))
            #st.write("🔐 EMAIL_PASSWORD present:", bool(os.getenv("EMAIL_PASSWORD")))
            smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD")) # GMAIL was changed to EMAIL!!!
            smtp.send_message(msg)

        st.success(f"✅ Report sent to {recipient_email}!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
