# Kill every mutant: branch coverage

Your workspace contains `shipping.py`:

```python
def quote(weight, zone, express=False, member=False):
    if weight <= 0:                                    # B1
        raise ValueError("weight must be positive")
    if zone not in ("A", "B", "C"):                    # B2
        raise ValueError(f"unknown zone: {zone}")
    base = {"A": 5.0, "B": 8.0, "C": 12.0}[zone]
    if weight > 20:                                    # B3: heavy tier
        cost = base + 20 * 0.5 + (weight - 20) * 0.25
    else:                                              # B4: light tier
        cost = base + weight * 0.5
    if express:                                        # B5: express multiplier
        cost *= 1.75
        if zone == "C":                                # B6: remote surcharge
            cost += 10.0
    if member:                                         # B7: capped discount
        cost -= min(5.0, cost * 0.1)
    return round(cost, 2)
```

Branches to reach:

- **B1** non-positive weight → `ValueError`
- **B2** unknown zone → `ValueError`
- **B3** heavy parcels (> 20 kg): first 20 kg at 0.50/kg, the rest at 0.25/kg
- **B4** light parcels: 0.50/kg
- **B5** express multiplies the cost by 1.75
- **B6** express **to zone C** adds a 10.00 surcharge (after the multiplier)
- **B7** members get 10% off, **capped at 5.00** — the cap only matters once
  the pre-discount cost exceeds 50.00, so you'll need an expensive scenario
  *and* a cheap one

## Your job

Write `test_shipping.py` whose tests reach **every branch above, on both
sides where relevant**. Think like a coverage tool: which inputs drive
execution down each path? Which combinations (heavy + express + C + member)
distinguish the cap from plain 10%?

## How it is graded

Your `test_shipping.py` is copied — alone — next to the correct
implementation (must pass) and **seven mutants**, each with exactly one
branch broken (B1..B7: check removed, wrong rate, missing surcharge, uncapped
discount, ...). A mutant that survives your suite means that branch isn't
really tested. Develop with `python -m pytest -q`.
