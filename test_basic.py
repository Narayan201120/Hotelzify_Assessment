"""Basic checks for Task 1 and Task 2. Run with: python test_basic.py"""
import os
import tempfile

from debug_fixes import cancellation_rate, last_n_days_revenue
from revenue import (
    is_cancelled,
    load_unique_bookings,
    normalize_channel,
    parse_date,
    summarize,
)

# 1. All four date formats in the brief parse to the right month and day.
assert (parse_date("2026-10-13").month, parse_date("2026-10-13").day) == (10, 13)
assert (parse_date("12/10/2026").month, parse_date("12/10/2026").day) == (10, 12)
assert (parse_date("15-10-2026").month, parse_date("15-10-2026").day) == (10, 15)
assert (parse_date("Oct 14 2026").month, parse_date("Oct 14 2026").day) == (10, 14)

# 2. Channel aliases map to one canonical name.
assert normalize_channel("BDC") == "Booking.com"
assert normalize_channel("booking com") == "Booking.com"
assert normalize_channel("Booking.com") == "Booking.com"
assert normalize_channel("EXPEDIA") == "Expedia"

# 3. Duplicate ids count once against the real loader.
csv_text = (
    "id,check_in,channel,amount,status\n"
    "B1,2026-10-12,Direct,100,confirmed\n"
    "B1,2026-10-12,Direct,100,confirmed\n"
    "B2,2026-10-13,Direct,50,cancelled\n"
)
with tempfile.NamedTemporaryFile(
    "w", suffix=".csv", delete=False, encoding="utf-8"
) as tmp:
    tmp.write(csv_text)
    tmp_path = tmp.name
bookings, rows_read, dupes_dropped = load_unique_bookings(tmp_path)
os.unlink(tmp_path)
assert (rows_read, dupes_dropped, len(bookings)) == (3, 1, 2)

# 4. Empty input never divides by zero.
assert cancellation_rate([]) == 0.0
assert summarize([]) == {}

# 5. Day-window edges: n=0 gives 0, oversized n sums everything.
assert last_n_days_revenue([10, 20, 30, 40], 0) == 0
assert last_n_days_revenue([10, 20, 30, 40], 2) == 70
assert last_n_days_revenue([10, 20, 30, 40], 10) == 100

# 6. Both spellings and cases count as cancelled.
assert is_cancelled("canceled")
assert is_cancelled("Cancelled")
assert cancellation_rate(
    [{"status": "canceled"}, {"status": "Cancelled"}, {"status": "confirmed"}]
) == 2 / 3

print("All basic checks passed.")
