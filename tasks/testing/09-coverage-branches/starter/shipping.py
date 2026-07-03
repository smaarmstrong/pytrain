"""A correct implementation of the spec in prompt.md — write tests for it."""


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
