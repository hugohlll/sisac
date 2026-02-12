import pytest
from decimal import Decimal
from datetime import date
from contracts.services.calculator import calculate_termination_fine
from contracts.models import Contract

@pytest.fixture
def typical_contract():
    return Contract(
        contract_type='TIPICO',
        start_date=date(2024, 1, 1),
        monthly_value=Decimal('1000.00'),
    )

def test_fine_after_12_months(typical_contract):
    # Termination exactly at 12 months
    termination_date = date(2025, 1, 1) # 2024-01-01 + 1 year
    fine = calculate_termination_fine(typical_contract, termination_date)
    assert fine == Decimal('0.00')

    # Termination after 13 months
    termination_date = date(2025, 2, 1)
    fine = calculate_termination_fine(typical_contract, termination_date)
    assert fine == Decimal('0.00')

def test_fine_before_12_months(typical_contract):
    # Termination at 6 months (approx)
    # Start: 2024-01-01. 12th month mark: 2025-01-01.
    # Terminate: 2024-07-01.
    # Remaining: 2024-07-01 to 2025-01-01.
    # Days: 31+31+30+31+30+31 = 184 days (approx)
    
    termination_date = date(2024, 7, 1)
    fine = calculate_termination_fine(typical_contract, termination_date)
    
    target_date = date(2025, 1, 1)
    days_remaining = (target_date - termination_date).days
    expected_fine = (Decimal('1000.00') / Decimal('30')) * Decimal(days_remaining)
    
    assert fine == expected_fine.quantize(Decimal('0.01'))


