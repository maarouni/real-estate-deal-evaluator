def calculate_metrics(purchase_price, monthly_rent, down_payment_pct, interest_rate, loan_term,
                      monthly_expenses, vacancy_rate, appreciation_rate, rent_growth_rate):
    loan_amount = purchase_price * (1 - down_payment_pct / 100)
    monthly_interest_rate = interest_rate / 100 / 12
    number_of_payments = loan_term * 12

    if monthly_interest_rate > 0:
        monthly_mortgage = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) /                            ((1 + monthly_interest_rate) ** number_of_payments - 1)
    else:
        monthly_mortgage = loan_amount / number_of_payments

    effective_rent = monthly_rent * (1 - vacancy_rate / 100)
    annual_rent = effective_rent * 12
    annual_expenses = monthly_expenses * 12
    annual_mortgage = monthly_mortgage * 12
    annual_cash_flow = annual_rent - annual_expenses - annual_mortgage

    cap_rate = (annual_rent - annual_expenses) / purchase_price * 100
    coc_return = annual_cash_flow / (purchase_price * down_payment_pct / 100) * 100
    roi = coc_return  # Simplified ROI for illustration

    # Grade based on CoC Return
    if coc_return >= 15:
        grade = "A"
    elif coc_return >= 12:
        grade = "B"
    elif coc_return >= 9:
        grade = "C"
    elif coc_return >= 6:
        grade = "D"
    else:
        grade = "F"

    # Cash flow & rent projection logic
    annual_cash_flows = []
    rents = []

    current_rent = monthly_rent
    for year in range(1, 11):
        effective_rent = current_rent * (1 - vacancy_rate / 100)
        annual_rent = effective_rent * 12
        annual_expenses = monthly_expenses * 12
        annual_mortgage = monthly_mortgage * 12

        annual_cash_flow = annual_rent - annual_expenses - annual_mortgage
        annual_cash_flows.append(round(annual_cash_flow, 2))
        rents.append(round(current_rent, 2))

        current_rent *= (1 + rent_growth_rate / 100)

    return {
        "Cap Rate (%)": round(cap_rate, 2),
        "Cash-on-Cash Return (%)": round(coc_return, 2),
        "ROI (%)": round(roi, 2),
        "Annual Cash Flow ($)": round(annual_cash_flows[0], 2),
        "Monthly Mortgage ($)": round(monthly_mortgage, 2),
        "Grade": grade,
        "10yr Cash Flow": annual_cash_flows,
        "10yr Rents": rents
    }
