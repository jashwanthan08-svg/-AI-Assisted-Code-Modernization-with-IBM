# What I checked, and what the agent got wrong
Bob fixed the failing tests, but it didn't add a test for the missing-last_service_km case that verify.py was checking for — I had to point that out and ask it to add that test separately.

In the risk analysis, I noticed one car with missing service history (VOS-1217) wasn't flagged as broken down. Instead of treating that as a data gap, the script just quietly treated "no data" the same as "low risk," which felt wrong.

Bob also deleted four dead functions from fleet_utils.py — a hand-rolled mean, a duplicate of logic already in km_wachter.py, and two functions tied to things that no longer exist. Rather than trust the docstrings saying they were unused, I opened the file myself afterward and confirmed only the three functions still in use were left, and reran the tests to make sure nothing broke.

I also double-checked that SERVICE_INTERVAL_KM, WARN_AT_PERCENT, and settings.cfg weren't touched by any of this, since those had to stay fixed.

## What the agent got wrong
The initial test suite Bob fixed only addressed the tests that were already failing — it didn't add a test for the missing-last_service_km scenario that verify.py specifically checks for. I had to point this out and ask Bob to add that test explicitly; it wasn't something it caught on its own.

Separately, in the breakdown-risk analysis, I noticed from the output that a car with missing service history (VOS-1217) wasn't flagged as broken down. Rather than being treated as a data-quality problem — a car we simply don't have full information on — it was silently treated the same as a car with a clean, complete history. I noted this as a real gap: missing data was being interpreted as "not at risk" instead of "unknown risk."

## What I checked before I accepted its work

Bob also removed four dead functions from fleet_utils.py — mean(), is_due(), parse_service_date(), and chunk_list(). Each had its own docstring admitting it was unused or duplicated (is_due duplicated logic already in km_wachter.py; parse_service_date referenced a form that "no longer exists"; chunk_list was flagged as "no longer called from anywhere"). Rather than take that at face value, I opened the updated fleet_utils.py myself and confirmed only the three functions still in active use — km_to_miles, format_number, format_percent — remained. I also confirmed the test suite still passed after the removal, which would have failed immediately if anything in the codebase still depended on the deleted functions.

I also specifically checked that SERVICE_INTERVAL_KM, WARN_AT_PERCENT, and settings.cfg were untouched by any of these changes, since those values needed to stay fixed throughout.


## What the data actually said

Comparing broke-down vs. non-broke-down cars, the two columns that separated the groups were km_since_service and load_factor — total mileage and age showed almost no difference between the groups. But I also noticed the analysis excludes cars missing service history from the "broke down" count entirely, rather than treating them as higher-risk or flagging them separately — which likely understates risk for cars like VOS-1217 where we simply don't have the data.
