from collections import defaultdict
from datetime import date


def analyze(data):
    daily, weekly, rides = data["daily_cap"], data["weekly_cap"], data["rides"]
    if any(type(cap) is not int or cap < 0 for cap in (daily, weekly)) or not isinstance(rides, list):
        raise ValueError("Use nonnegative integer caps and provide a ride list")
    events = []
    for day, cost in rides:
        parsed = date.fromisoformat(day)
        if parsed.isoformat() != day or type(cost) is not int or cost < 0:
            raise ValueError("Use YYYY-MM-DD and a nonnegative fare in cents")
        events.append((parsed, cost))
    events.sort(key=lambda ride: ride[0])
    day_total, week_total = defaultdict(int), defaultdict(int)
    charges = []
    for day, cost in events:
        year, week, _ = day.isocalendar()
        week_key = (year, week)
        charge = min(cost, daily-day_total[day], weekly-week_total[week_key])
        charges.append(charge)
        day_total[day] += charge
        week_total[week_key] += charge
    return {"charges": charges, "paid": sum(charges), "saved": sum(cost for _, cost in events)-sum(charges)}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
