"""Task 2: debug the two functions."""


def last_n_days_revenue(daily, n):
    """Sum revenue of the last n days.

    Bug in original: daily[-n:-1] drops the most recent day.
    Python slices exclude the stop index, so [:-1] stops one
    element early. It also breaks when n <= 0.

    Fix: use daily[-n:] and guard bad n.
    """
    if n <= 0:
        return 0
    if n >= len(daily):
        return sum(daily)
    return sum(daily[-n:])


def cancellation_rate(bookings):
    """Return cancelled / total as a float in [0, 1].

    Bug in original: len(bookings) == 0 raises ZeroDivisionError.
    It also misses "Cancelled" vs "cancelled" and rows without
    a status key.

    Fix: return 0.0 for empty input, normalise case, use .get().
    """
    if not bookings:
        return 0.0
    cancelled = len(
        [
            b
            for b in bookings
            if str(b.get("status", "")).strip().lower() == "cancelled"
        ]
    )
    return cancelled / len(bookings)


if __name__ == "__main__":
    # Quick sanity check (not a test suite, just a demo run).
    print(last_n_days_revenue([10, 20, 30, 40], 2))  # 70, old code gave 30
    print(last_n_days_revenue([10, 20, 30, 40], 10))  # 100
    print(cancellation_rate([]))  # 0.0, old code crashed
    print(cancellation_rate([{"status": "cancelled"}, {"status": "Confirmed"}]))  # 0.5
