import numpy as np

class RateValue:
    """
    Custom class to hold a rate and a value.
    
    Attributes:
        rate (float): Interest rate
        value (float): Associated value
        n (int): Number of times compounded. Default = 1.
    """
    def __init__(self, rate:float, value: float, n: int = 1):
        self.rate = rate
        self.value = value
        self.n = n
        
    
    def __repr__(self):
        return f"RateValue(rate={self.rate}, value={self.value}, number={self.n})"

def compound_interest(rate, period):
    """
    Calculate compound interest given rate and period
    
    Parameters:
        rate (float): Interest rate (0.05 == 5%)
        period (int): Number of compounding periods

    Returns:
        float: Compound amount
    """
    return (1+(rate/period))**period

def pv_const_rate(rate, futureValues, n = 1):
    """
    Calculate present value based on interest rate and known future values at times t

    Args:
        rate (float): Interest rate (0.05 == 5%)
        futureValues (float[]): Array of known future values
    """
    total = 0
    for i, value in enumerate(futureValues):
        total += value / (1+rate/n)**(n*(i+1))
    return total

def pv_diff_rate(values):
    """
    Calculate present value when each value has own rate

    Args:
        values (list of RateValue): List of RateValue (rate, value, n = 1)

    Returns:
        float: Present value sum
    """
    if not isinstance(values, list) or not all(isinstance(v, RateValue) for v in values):
        return "Error: Input must be a list of RateValue objects."
    total = 0
    compoundRate = 1
    for rv in values:
        compoundRate *= (1+(rv.rate/rv.n))**rv.n
        total += (rv.value) / compoundRate
    return total

def fv_const_rate(rate, values, n = 1):
    """
    Calculate future value based on interest rate and values at times t

    Args:
        rate (float): Interest rate (0.05 == 5%)
        values (float[]): Array of known values at time t
    """
    total = 0
    for i, value in enumerate(values):
        total += value * (1+rate/n)**(n*(i+1))
    return total
# 100, .05, 100, .05, 100, .03
# 100 (1+.05)=x1, (x1+100) * (1+.05) = x2, (x2 +100) * (1+.03)

def fv_diff_rate(values):
    """
    Calculate future value when each value has own rate

    Args:
        values (list of RateValue): List of RateValue (rate, value, n = 1)

    Returns:
        float: Present value sum
    """
    if not isinstance(values, list) or not all(isinstance(v, RateValue) for v in values):
        return "Error: Input must be a list of RateValue objects."
    total = 0
    compoundRate = 1
    for rv in values:
        compoundRate *= (1+rv.rate/rv.n)**rv.n
        total += (rv.value) * compoundRate
    return total

if __name__ == "__main__":  
    values = [
        RateValue(0.05,100, 2),
        RateValue(0.05,100, 2),
        RateValue(0.05,100, 2)
    ]
    value = [100, 100, 100]
    print(fv_diff_rate(values))
    print(fv_const_rate(0.05,value, 2))