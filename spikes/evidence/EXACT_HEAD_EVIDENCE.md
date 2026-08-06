# Exact-head evidence rule

All automated candidate claims must refer to one pull-request head SHA and one workflow run. Evidence from superseded heads may diagnose failures but cannot satisfy acceptance.

The final report records the GitHub run and artifact identities outside committed source so that committing evidence metadata cannot create a self-referential head loop.
