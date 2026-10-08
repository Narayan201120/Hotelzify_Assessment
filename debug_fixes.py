"""Task 2: debug the two functions."""


def last_n_days_revenue(daily, n):
    """Sum revenue of the last n days.

    Bug in original: daily[-n:-1] drops the most recent day.
    Python slices exclude the stop index, so [:-1] stops one
    element early. It also breaks when n <= 0.

    Fix: use daily[-n:] and guard bad n. Oversized n needs no
    special case: daily[-n:] already returns the whole list.
    """
    if n <= 0:
        return 0
    return sum(daily[-n:])


def cancellation_rate(bookings):
    """Return cancelled / total as a float in [0, 1].

    Bug in original: len(bookings) == 0 raises ZeroDivisionError.
    It also misses "Cancelled" vs "cancelled", the US spelling
    "canceled", and rows without a status key.

    Fix: return 0.0 for empty input, match any status starting
    with "cancel" after strip/lower, and use .get().

    Note: this counts list entries, it does not dedupe booking
    ids. Dedupe before calling if the input can hold duplicates.
    """
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
