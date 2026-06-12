# Mode-vote sensitivity to tie handling

Computed from `outputs/agent_trajectories.csv`. Random tie-break uses 10,000 Monte Carlo samples (seed=42).

- **First-round agents tied at top (T030A):** 50 of 300 (16.7%)
- **Runoff agents tied at top (T035A):** 54 of 300 (18.0%)

## T030A_first_round_vote_decision (first round)

| Candidate | Actual (YSK) % | Rule 1: canonical (Erdoğan first) % | Rule 2: reverse (Erdoğan last) % | Rule 3: random tie-break — mean % [95% interval] |
| --- | --- | --- | --- | --- |
| Erdoğan | 49.52 | 54.67 | 41.00 | 46.56  [44.67, 48.67] |
| Kılıçdaroğlu | 44.88 | 45.33 | 46.67 | 48.34  [46.33, 50.33] |
| S. Oğan | 5.17 | 0.00 | 0.33 | 0.39  [0.00, 1.00] |
| M. İnce | 0.43 | 0.00 | 0.00 | 0.00  [0.00, 0.00] |
| Other | — | 0.00 | 0.33 | 0.17  [0.00, 0.33] |
| Undecided | — | 0.00 | 11.67 | 4.55  [2.67, 6.33] |

*Winner under rule 1:* **Erdoğan** — *rule 2:* **Kılıçdaroğlu** — *rule 3 (mean):* **Kılıçdaroğlu**.

### Tied-agent breakdown (50 agents)

| Tied candidates | Tie size | Agents |
| --- | --- | --- |
| Erdoğan + Kılıçdaroğlu + Undecided | 3 | 21 |
| Erdoğan + Kılıçdaroğlu | 2 | 13 |
| Kılıçdaroğlu + Undecided | 2 | 8 |
| Erdoğan + Undecided | 2 | 4 |
| Erdoğan + S. Oğan + Undecided | 3 | 2 |
| Erdoğan + S. Oğan | 2 | 1 |
| Kılıçdaroğlu + Other | 2 | 1 |

## T035A_runoff_vote_decision (runoff)

| Candidate | Actual (YSK) % | Rule 1: canonical (Erdoğan first) % | Rule 2: reverse (Erdoğan last) % | Rule 3: random tie-break — mean % [95% interval] |
| --- | --- | --- | --- | --- |
| Erdoğan | 52.18 | 55.33 | 40.33 | 46.45  [44.33, 48.67] |
| Kılıçdaroğlu | 47.82 | 44.33 | 43.33 | 46.60  [44.67, 48.67] |
| Abstain / Invalid / Undec. | — | 0.33 | 16.33 | 6.95  [4.67, 9.33] |

*Winner under rule 1:* **Erdoğan** — *rule 2:* **Kılıçdaroğlu** — *rule 3 (mean):* **Kılıçdaroğlu**.

### Tied-agent breakdown (54 agents)

| Tied candidates | Tie size | Agents |
| --- | --- | --- |
| Abstain / Invalid / Undec. + Erdoğan + Kılıçdaroğlu | 3 | 25 |
| Abstain / Invalid / Undec. + Erdoğan | 2 | 14 |
| Abstain / Invalid / Undec. + Kılıçdaroğlu | 2 | 9 |
| Erdoğan + Kılıçdaroğlu | 2 | 6 |

## Notes

- Rule 1 (canonical order) is the rule used by `validation/metrics.py`. It corresponds to `max(distribution, key=distribution.get)` on a dict whose insertion order is `[Erdoğan, Kılıçdaroğlu, Sinan Oğan, M. İnce, Other, Undecided]` for the first round and `[Erdoğan, Kılıçdaroğlu, Abstain/Invalid/Undecided]` for the runoff.
- Rule 2 reverses this ordering, so Erdoğan loses every tie he is part of.
- Rule 3 is a Monte Carlo random tie-break: each tied agent independently picks one of their tied candidates uniformly at random; the table reports the mean and 2.5 / 97.5 percentile of each candidate's share across the simulation runs.
- Untied agents are unaffected by any of these rules. Differences across rules are driven only by the tied agents enumerated above.
