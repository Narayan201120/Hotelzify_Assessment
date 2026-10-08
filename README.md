# Hotelzify assessment - Narayan

How to run:

```
python revenue.py
python debug_fixes.py
```

Files:
- `bookings.csv` - input data from the brief
- `revenue.py` - Task 1 solution
- `debug_fixes.py` - Task 2 fixed functions with explanations
- `owner_message.txt` - Task 3, 117 words
- `voice_note_script.txt` - Task 4 script (record on your phone, ~2 min)

## 1. Results

Assumptions (noted in code):
- Slash and dash dates are day-first (`12/10/2026` = 12 Oct). This matches the Indian format and rows like `15-10-2026`, where month-first would be invalid.
- Duplicates: keep first occurrence of each booking id. B1003 and B1008 each appear twice.
- Channels normalised case-insensitively: `BDC`, `bdc`, `booking com`, `Booking.com` all map to `Booking.com`. `expedia` variants map to `Expedia`.

Output from `python revenue.py`:

| month | channel | bookings | cancelled | net revenue | cancellation rate |
| --- | --- | --- | --- | --- | --- |
| 2026-10 | Booking.com | 3 | 1 | 260 | 33.33% |
| 2026-10 | Direct | 1 | 0 | 110 | 0.00% |
| 2026-10 | Expedia | 2 | 1 | 200 | 50.00% |
| 2026-11 | Booking.com | 2 | 0 | 310 | 0.00% |
| 2026-11 | Direct | 2 | 1 | 130 | 50.00% |
| 2026-11 | Expedia | 1 | 0 | 175 | 0.00% |

11 unique bookings (13 rows minus 2 duplicates). Net revenue excludes cancelled bookings.

## 2. Debug notes

`last_n_days_revenue`: the original slice `daily[-n:-1]` excludes the last element, since slice stop is exclusive. So for `[10, 20, 30, 40]` with `n=2` it returned 30 instead of 70. Fixed to `daily[-n:]`, with guards for `n <= 0` (returns 0) and `n >= len(daily)` (sums all). The original snippet was also missing indentation on the return.

`cancellation_rate`: the original divides by `len(bookings)` with no empty-list guard, so `[]` raises `ZeroDivisionError`. Fixed to return `0.0` for empty input. Also normalised status with `.get("status", "")` plus strip and lower, so `"Cancelled"` and missing keys do not break or miscount.

## 3. Message to hotel owner (117 words)

See `owner_message.txt`. Pasted here for easy sending:

When most bookings come from travel sites, you pay commission on every room, often 15 to 25 percent. That money leaves before you see it. You also lose control. These sites decide how your hotel looks, which price shows first, and who finds you. Guests remember the site, not you, so they return there next time.

You can shift this. Keep your website and Google profile updated, with clear photos and a working book button. Offer a perk for booking direct, like breakfast or flexible check-in. Ask happy guests to book direct next time. You do not need to leave these sites. You just need direct bookings to grow, so you keep more of what you earn.

## 4. Voice note

Script is in `voice_note_script.txt` (228 words, about 2 minutes). Record it on your phone in a quiet room and upload the mp3/m4a to Drive. I did not generate AI audio, since they asked for your voice.

Suggested reply to Anirudh:

> Hi Anirudh, thanks for the exercise. Here is my work: [GitHub link], written message is in the repo and pasted below, voice note here: [Drive link]. Happy to walk through my approach on a call. Best, Narayan
