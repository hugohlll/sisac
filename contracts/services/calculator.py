from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta

def calculate_termination_fine(contract, termination_date: date) -> Decimal:
    """
    Calculates termination fine for Typical contracts (30 months).
    Rule:
    - If < 12 months elapsed: Fine = Sum of remaining rents to complete 12 months (pro-rata).
    - If >= 12 months elapsed: Fine = 0.
    
    For Atypical contracts, strictly follows the contract terms (logic not implemented here as it varies).
    """
    if contract.contract_type != 'TIPICO':
        return Decimal('0.00')

    start_date = contract.start_date
    twelfth_month_mark = start_date + relativedelta(months=12)
    
    if termination_date >= twelfth_month_mark:
        return Decimal('0.00')
    
    # Calculate finding: remaining rent to complete 12 months
    # We need to calculate how much is left from termination_date until twelfth_month_mark
    # Method: Pro-rata calculation used in legal contexts often counts days.
    # Simple approach: Calculate total days in the 12 month period vs days elapsed.
    
    # However, SPEC says: "soma dos aluguéis restantes para completar o 12º mês"
    # This implies we calculate the time difference and multiply by monthly_value.
    
    delta = twelfth_month_mark - termination_date
    days_remaining = delta.days
    
    # Cost per day based on 30-day month or actual days? 
    # Standard practice: Pro-rata die usually implies (Monthly Value / 30) * Days Remaining
    # OR (Monthly Value / Days in Month) * Days Remaining.
    # Let's use a standard 30-day base for simplicity unless specified otherwise, 
    # but exact day diff is more precise.
    # Let's use: (Monthly Value * Total Remaining Months including floats)
    # Remaining months = days_remaining / 30.4375 (avg) or just strictly days.
    
    # Let's check SPEC again: "calculado pro-rata die"
    # So: (daily_rate * days_remaining)
    
    daily_rate = contract.monthly_value / Decimal('30') # Standard commercial month
    fine = daily_rate * Decimal(days_remaining)
    
    return fine.quantize(Decimal('0.01'))

def calculate_deposit_installments(monthly_value: Decimal) -> tuple[Decimal, Decimal]:
    """
    Calculates the 2 installments for Security Deposit if payment_type is PARCELADO.
    - Installment 1: 1.5 * monthly_value
    - Installment 2: 0.5 * monthly_value
    """
    p1 = monthly_value * Decimal('1.5')
    p2 = monthly_value * Decimal('0.5')
    return p1.quantize(Decimal('0.01')), p2.quantize(Decimal('0.01'))
