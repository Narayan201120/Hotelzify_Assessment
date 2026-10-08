"""Task 2: debug the two functions."""


def last_n_days_revenue(daily, n):
    """Sum the last n days. Fix: daily[-n:-1] dropped the newest day, now daily[-n:]."""
    if n <= 0:
        return 0
    return sum(daily[-n:])


def cancellation_rate(bookings):
    """Cancelled share in [0, 1]. Fix: empty list returns 0.0, matches cancel* case-insensitively. Does not dedupe ids."""
    if not bookings:
        return 0.0
    cancelled = len(
        [
            b
            for b in bookings
            if str(b.get("status", "")).strip().lower().startswith("cancel")
        ]
    )
    return cancelled / len(bookings)


if __name__ == "__main__":
    print(last_n_days_revenue([10, 20, 30, 40], 2))  # 70, old code gave 30
    print(last_n_days_revenue([10, 20, 30, 40], 10))  # 100
    print(cancellation_rate([]))  # 0.0, old code crashed
    print(cancellation_rate([{"status": "canceled"}, {"status": "Confirmed"}]))  # 0.5
