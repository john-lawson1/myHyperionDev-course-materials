import math

"""
This program provides a user with 2 financial calculators.
  1) an investment calculator.
  2) a home loan repayment calculator.

The user chooses which calculator they want to use.
The user inputs the calculation parameter values.
The program outputs the calculated value.
"""

print("""
Please choose the financial calculator you would like to use:
investment: to calculate the amount of interest you'll earn on your investment
bond: to calculate the amount you'll have to pay on a home loan
""")
choice = input("""Enter either 'investment' or 'bond' \
from the menu above to proceed: """)

# Program checks for invalid calculator input values.
while choice.lower() != "investment" and choice.lower() != "bond":
    print(f"'{choice}' is not one of the options.\n")
    choice = input("""Please re-enter either 'investment' or 'bond'\
from the menu above to proceed: """)

# User inputs parameters for the bond calculation.
# Progam outputs the calculated bond repayment value.
if choice.lower() == "bond":
    print(f"\nYou chose: '{choice}'\n")
    pv = float(input("""Please enter the present value of the house, \
as an integer (eg: for £100,000, enter '100000': """))
    rate = float(input("""Please enter the interest rate, as a percentage, \
but only the number of the interest rate without the ‘%’ \
(eg: for 8.0%, enter '8.0'): """))
    months = float(input("""Please enter the number of months you are will \
take to repay the bond, as an integer (eg: for 120 months, enter '120'): """))
    repayment = round((rate/100/12 * pv)/(1 - (1 + rate/100/12)**(-months)),2)
    print(f"""
        {"_"*79}
        Your monthly repayments will be: {round(repayment,2)}\n
        This is based on the following inputs:
        * Present value: {pv}
        * Interest rate: {rate}%
        * Months to repay: {months}
        {"_"*79}
        """)

# User inputs parameters for the investment calculation.
if choice.lower() == "investment":
    print(f"\nYou chose '{choice}'\n")
    deposit = float(input("""Please enter the amount of money that they are \
depositing, as an integer (eg: for £100, enter '100'): """))
    rate = float(input("""Please enter the interest rate, as a percentage, \
but only the number of the interest rate without the ‘%’\
(eg: for 8.0%, enter '8.0'): """))
    years = float(input("""Please enter the number of years you are planning \
on investing, as an integer (eg: for 5 years, enter '5'): """))
    method = input("""Please choose the method of interest calculation to be \
applied by entering either 'simple' or 'compound': """)

    # Program checks for invalid interest method input values.
    while method.lower() != "simple" and method.lower() != "compound":
        print(f"'{method}' is not one of the methods.\n")
        method = input("""Please re-enter the method of interest calculation \
    to be applied by entering either simple' or 'compound': """)

    # Progam outputs the total amount with simple interest
    if method.lower() == "simple":
        total_simple = deposit * (1 + rate / 100 * years)
        print(f"""
        {"_"*79}
        The total amount including simple interest is: {round(total_simple,2)}\n
        This is based on the following inputs:
        * Deposit amount: {deposit}
        * Interest rate: {rate}%
        * Years of investment: {years}
        {"_"*79}
        """)

    # Progam outputs the total amount with compound interest
    elif method.lower() == "compound":
        total_compound = deposit * math.pow((1 + rate / 100),years)
        print(f"""
        {"_"*79}
        The total amount including compound interest is: {round(total_compound,2)}\n
        This is based on the following inputs:
        * Deposit amount: {deposit}
        * Interest rate: {rate}%
        * Years of investment: {years}
        {"_"*79}
        """)
