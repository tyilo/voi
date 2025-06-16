from dataclasses import dataclass
from z4 import minimize, Int, If

@dataclass
class Deal:
    minutes: int
    price: int

    def __str__(self) -> str:
        return f"deal_{self.minutes}"

DEALS = [
    Deal(5, 10),
    Deal(30, 39),
    Deal(60, 69),
    Deal(120, 119),
    Deal(300, 269),
]

vars = []
constraints = []
price = 0
minutes = 0
for deal in DEALS:
    v = Int(str(deal))
    vars.append(v)
    constraints.append(0 <= v)
    minutes += v * deal.minutes
    price += v * deal.price * 100

has_deal = sum(vars) > 0
no_deal_minutes = Int("no_deal_minutes")
vars.append(no_deal_minutes)
constraints.append(0 <= no_deal_minutes)
price += 220 * no_deal_minutes + If(has_deal, 0, 10 * 100)
minutes += no_deal_minutes


for goal in range(1, 100 + 1):
    print(f"{goal} mins: ", end="")
    solution_price, solution_vals = minimize(price, constraints + [minutes >= goal])
    print(f"{solution_price.as_long() / 100} kr.")

    for var in vars:
        v = solution_vals[var].as_long()
        if v != 0:
            print(f"  {var} x {v}")

    print()
