print("This will be a program to compute compound interest.")

balance = 10000
interest_rate = 0.13
years = 30
tax_rate = 0.25
deposit = 1000

total_interest_earned = 0
print(f"At the start you have {balance:.2f}")
for year in range(1, years + 1):
    interest_earned = balance * interest_rate
    total_interest_earned += interest_earned
    balance += interest_earned
    balance += deposit
taxes = total_interest_earned * tax_rate
balance -= taxes
print(f"After {year} years and after taxes, you have {balance:.2f}")
