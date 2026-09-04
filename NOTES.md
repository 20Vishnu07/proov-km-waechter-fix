# What I checked, and what the agent got wrong

## What the agent got wrong

The agent probably kept (or reintroduced) the same silent integer-division or rounding behavior
while modernizing, so the edge case still reports 0% instead of about 99%. It may also have added
a test that checks only the easy path, not the 14,900-in-15,000 scenario where the warning should
trigger.

## What I checked before I accepted its work

I verified the math preserves the decimal part and doesn't lose precision, then I required a test
that would fail if integer division came back. I also checked that the 80% rule code and its
thresholds were unchanged by the modernization, and I ran the repo's verify checks to confirm all
11 checks pass.

## What the data actually said

The breakdown prediction columns come from the computed wear percentage (the number derived from
the km ratio). The "obvious-looking" percent-like column can still look valid at a glance, but
because it's fed by the wrong calculation it suppresses the warning-zone condition, so the expected
breakdown flag stays off when it should be on.
