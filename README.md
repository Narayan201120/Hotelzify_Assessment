# Hotelzify assessment - Narayan

How to run:

```
python revenue.py
python debug_fixes.py
python test_basic.py
```

Files:
- `bookings.csv` - input data from the brief
- `revenue.py` - Task 1 solution
- `debug_fixes.py` - Task 2 fixed functions with explanations
- `test_basic.py` - checks for Tasks 1 and 2
- `owner_message.txt` - Task 3, 123 words

## 1. Results

Assumptions (noted in code):
- Slash and dash dates are day-first (`12/10/2026` = 12 Oct). The proof is in the data: `15-10-2026` and `18/10/2026` are only valid day-first, since month 15 and month 18 do not exist.
- Duplicates: keep first occurrence of each booking id. B1003 and B1008 each appear twice.
- Channels normalised case-insensitively: `BDC`, `bdc`, `booking com`, `Booking.com` all map to `Booking.com`. `expedia` variants map to `Expedia`.
- Status accepts both spellings: `cancelled` and `canceled` count as cancelled. Unknown statuses are logged to stderr and treated as revenue.

Output from `python revenue.py`:

| month | channel | bookings | cancelled | net revenue | cancellation rate |
| --- | --- | --- | --- | --- | --- |
| 2026-10 | Booking.com | 3 | 1 | 260 | 33.33% |
| 2026-10 | Direct | 1 | 0 | 110 | 0.00% |
| 2026-10 | Expedia | 2 | 1 | 200 | 50.00% |
| 2026-11 | Booking.com | 2 | 0 | 310 | 0.00% |
| 2026-11 | Direct | 2 | 1 | 130 | 50.00% |
| 2026-11 | Expedia | 1 | 0 | 175 | 0.00% |

Insight: Direct is $240 of $1,185 net (about 20%). The hotel keeps only a fifth of its revenue commission-free, which is exactly the OTA dependence the owner message addresses.

## 2. Debug notes

`last_n_days_revenue`: the original slice `daily[-n:-1]` excludes the last element, since slice stop is exclusive. So for `[10, 20, 30, 40]` with `n=2` it returned 30 instead of 70. Fixed to `daily[-n:]`, with a guard for `n <= 0` (returns 0). The original snippet was also missing indentation on the return.

`cancellation_rate`: the original divides by `len(bookings)` with no empty-list guard, so `[]` raises `ZeroDivisionError`. Fixed to return `0.0` for empty input. Also matches any status starting with "cancel" after strip and lower, so `"Cancelled"` and `"canceled"` count, and uses `.get()` so missing keys do not break. Note it counts list entries and does not dedupe ids, so dedupe before calling if the input can hold duplicates.

## 3. Message to hotel owner (123 words)

See `owner_message.txt`:

When most bookings come from travel sites, you pay commission on every room, often 15 to 25 percent, about $30 on a $150 night. That money leaves before you see it. You also lose control. These sites decide how your hotel looks, which price shows first, and who finds you. Guests remember the site, not you, so they return there next time.

You can shift this. Keep your website and Google profile updated, with clear photos and a working book button. Offer a perk for booking direct, like breakfast or flexible check-in. Ask happy guests to book direct next time. You do not need to leave these sites. You just need direct bookings to grow, so you keep more of what you earn.

## 4. Voice note

Voice note: LINK_TO_ADD (Google Drive, shared as anyone with the link can view).

## 5. Scaling this up

- Alias table in an editable CSV so non-engineers can add channel mappings without code changes.
- Fuzzy match new channel names, with a review queue for unknowns instead of silent title-casing.
- Log duplicate ids with conflicting data instead of silently keeping the first row.
