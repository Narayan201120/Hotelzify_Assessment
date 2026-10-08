"""Task 1: net revenue and cancellation rate per channel per month.

Rules from the brief:
- Net revenue excludes cancelled bookings.
- Duplicate booking ids count as one booking (keep first occurrence).
- "BDC" and "booking com" are Booking.com (case-insensitive normalisation).
- Dates come in mixed formats.
"""
import csv
from collections import defaultdict
from datetime import datetime

CHANNEL_MAP = {
    "booking.com": "Booking.com",
    "booking com": "Booking.com",
    "bdc": "Booking.com",
    "expedia": "Expedia",
    "direct": "Direct",
}

DATE_FORMATS = [
    "%Y-%m-%d",   # 2026-10-13
    "%d/%m/%Y",   # 12/10/2026 -> 12 Oct (day-first, Indian format)
    "%d-%m-%Y",   # 15-10-2026
    "%b %d %Y",   # Oct 14 2026
    "%B %d %Y",   # October 14 2026 (defensive)
]


def normalize_channel(raw: str) -> str:
    key = raw.strip().lower()
    if key in CHANNEL_MAP:
        return CHANNEL_MAP[key]
    # Fallback: title-case anything unexpected so it still groups.
    return raw.strip().title()


def parse_date(raw: str) -> datetime:
    raw = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognised date format: {raw!r}")


def load_unique_bookings(path: str = "bookings.csv") -> list[dict]:
    seen: dict[str, dict] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            bid = row["id"].strip()
            if bid in seen:
                continue  # duplicate id: count once, keep first
            seen[bid] = {
                "id": bid,
                "check_in": parse_date(row["check_in"]),
                "channel": normalize_channel(row["channel"]),
                "amount": float(row["amount"]),
                "status": row["status"].strip().lower(),
            }
    return list(seen.values())


def summarize(bookings: list[dict]) -> dict[tuple[str, str], dict]:
    # key: (month "YYYY-MM", channel) -> {total, cancelled, net_revenue}
    stats: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"total": 0, "cancelled": 0, "net_revenue": 0.0}
    )
    for b in bookings:
        month = b["check_in"].strftime("%Y-%m")
        key = (month, b["channel"])
        stats[key]["total"] += 1
        if b["status"] == "cancelled":
            stats[key]["cancelled"] += 1
        else:
            stats[key]["net_revenue"] += b["amount"]
    for v in stats.values():
        v["cancellation_rate"] = (
            v["cancelled"] / v["total"] if v["total"] else 0.0
        )
    return dict(stats)


def main() -> None:
    bookings = load_unique_bookings("bookings.csv")
    print(f"Unique bookings: {len(bookings)} (13 rows minus 2 duplicates)")
    summary = summarize(bookings)
    print("\nmonth,channel,bookings,cancelled,net_revenue,cancellation_rate")
    for (month, channel) in sorted(summary):
        s = summary[(month, channel)]
        print(
            f"{month},{channel},{s['total']},{s['cancelled']},"
            f"{s['net_revenue']:.0f},{s['cancellation_rate']:.2%}"
        )


if __name__ == "__main__":
    main()
