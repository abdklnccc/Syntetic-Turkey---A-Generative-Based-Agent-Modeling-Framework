# Synthetic Turkey — Simulation-Ready Framework

**Companion to:** `Synthetic-Turkey-Voter-Archetypes-for-Political-Simulation-2019-2024.md`
**Prototype scale:** 50 agents, 12 archetypes
**Output convention:** values are research-informed estimates; not statistically representative of the Turkish electorate. All assumptions are flagged.

---

## Task 1 — Overlap Analysis

All 12 archetypes are kept separate. No archetype is merged. Two clarifier tags are recommended for code-level disambiguation. Six overlap clusters were identified; each is resolved by an explicit distinguishing variable that the simulation must keep distinct.

| Overlap Pair | Decision | Distinguishing Variable(s) | Reason |
|---|---|---|---|
| A1 Devout Anatolian Loyalist ↔ A10 Earthquake Zone Loyalist | Keep separate | `geographic_zone`, `disaster_response_sensitivity`, `patronage_dependency`, `economic_grievance` | A10 is the empirically critical "disaster did not punish incumbent" case (Kahramanmaraş 72%, Adıyaman 66%, Malatya 69%). Merging would erase the central counter-intuitive finding. |
| A1 Devout Anatolian Loyalist ↔ A8 Pious Disillusioned Islamist | Keep separate | `government_approval`, `leader_loyalty`, `milli_gorus_identification`, vote intention | A8 is the YRP defection mechanism — the entire 2024 Islamist fracture. Merging would destroy that signal. |
| A3 Conservative Economically Disillusioned ↔ A11 Retired Protest Voter | Keep separate | `age`, `employment_status`, `economic_sensitivity`, `turnout_likelihood` | Pensioners were named by Betimar/Optimar/Sonar as the decisive 2024 bloc. A3 defects via abstention; A11 via protest vote. |
| A2 Secular Urban Professional ↔ A12 Cosmopolitan Liberal | Keep separate | `nationalist_cosmopolitan`, `kurdish_rights_support`, `international_exit_option`, `income_level` | A2 ≈ Çevik's Boxer/Pragmatist Kemalist core; A12 ≈ her Visionary. They diverge sharply on Kurdish rights and EU/cosmopolitan framing. |
| A6 Nationalist Grey Wolf ↔ A7 Moderate Nationalist (İYİ) | Keep separate | `secular_religious`, `government_approval`, `democratic_rights_priority`, `pro_eu_orientation` | Kadir Has data: 74.4% of İYİ pro-EU, MHP/Grey Wolf anti-EU. Real cleavage. |
| A5 Kurdish Political Voter ↔ A9 Young Urban Protest Voter | Keep separate | `identity_salience`, `kurdish_rights_support`, geography, vote intention | They share allies but not core identity. A5 reacts strongly to trustee removals; A9 reacts only sympathetically. |

**Recommended clarifier tags** (no rename, just code-level disambiguation):
- A6 → tag as `MHP_core_Peoples_Alliance` (makes alliance dependency explicit)
- A10 → tag as `Quake_belt_AKP_patronage` (makes the geography × archetype interaction explicit)

**No new archetype needed.** The HÜDA-PAR Kurdish-Islamist sub-segment mentioned in A5/A8 is too small (<2% nationally) to justify a 13th archetype at N=50 and is absorbed into A5 as a low-weight probability tag in the JSON.

---

## Task 2 — Simulation Weights for 50-Agent Prototype

| ID | Archetype | Agents | % | Uncertainty | Reason |
|----|-----------|:-:|:-:|:-:|--------|
| A1 | Devout Anatolian Loyalist | 7 | 14% | low | Core AKP loyalist bloc; KONDA dindar+sofu ~58% of population, ~25% of those are this hard loyalist type |
| A2 | Secular Urban Professional | 6 | 12% | low | Kemalist CHP core; stable urban backbone (İzmir, Beşiktaş, Kadıköy, Çankaya) |
| A3 | Conservative Economically Disillusioned | 6 | 12% | medium | Swing bloc the 2024 analysis hinges on; pollster consensus 10–15% of electorate |
| A4 | Alevi-CHP Loyalist | 4 | 8% | medium | Alevi share 10–25%; ~87% backed İmamoğlu; high partisan cohesion |
| A5 | Kurdish Political Voter | 5 | 10% | medium | Kurds ~15–20% of population, only ~half vote Kurdish-political parties |
| A6 | Nationalist Grey Wolf (MHP core) | 3 | 6% | medium | MHP fell to ~5% in 2024 local; 6% captures committed core |
| A7 | Moderate Nationalist (İYİ) | 2 | 4% | high | İYİ collapsed 9.9% → 3.77%; high uncertainty after migration to CHP |
| A8 | Pious Disillusioned Islamist | 3 | 6% | low | YRP got 6.19% in 2024 — direct empirical anchor |
| A9 | Young Urban Protest Voter | 4 | 8% | medium | 18–30 metropolitan opposition-leaning ~8–10% of electorate |
| A10 | Earthquake Zone Loyalist | 3 | 6% | medium | 11 quake provinces ≈ 16% of population; AKP-loyal sub-segment ~6% |
| A11 | Retired Protest Voter | 4 | 8% | low | Pensioners ~20% of voting-age; protest sub-segment named 2024 kingmakers |
| A12 | Cosmopolitan Liberal | 3 | 6% | medium | Concentrated in Avrupa Yakası / Çankaya / Alsancak; ~5–7% |
| **Total** | | **50** | **100%** | | |

**Validation against published vote shares:**
- Implied AKP-base (A1+A8+A10) = 26% of agents — within bracket of AKP's 35% 2023 first-round once swing/MHP-coalition flows are layered on
- Implied CHP-base (A2+A4+A9+A12) = 34% — within bracket of CHP's 37.7% 2024
- Implied Kurdish-political (A5) = 10% — above DEM's 5.7% to reflect Kurdish identity beyond party vote
- Implied 2024 swing bloc (A3+A11) = 20% — matches pollster narrative of the decisive defection mass

---

## Task 3 — Numeric Simulation Variables

Full per-archetype vectors are in `synthetic_turkey_simulation.json`. Summary tables below for readability.

### Political worldview (1–10)

| ID | Auth↔Lib | Sec↔Rel | Nat↔Cosmo | EconSat | InstTrust | GovApp | OppTrust | KurdRts | DemRts | RefAnx | CorrSens | EconGrv |
|----|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A1 | 9 | 10 | 9 | 4 | 8 | 9 | 2 | 2 | 3 | 5 | 3 | 5 |
| A2 | 3 | 2 | 5 | 4 | 3 | 2 | 7 | 5 | 9 | 6 | 9 | 6 |
| A3 | 6 | 7 | 8 | 2 | 4 | 4 | 5 | 3 | 4 | 9 | 7 | 9 |
| A4 | 3 | 2 | 5 | 4 | 2 | 1 | 8 | 7 | 9 | 5 | 9 | 7 |
| A5 | 3 | 4 | 4 | 3 | 1 | 1 | 6 | 10 | 9 | 4 | 8 | 8 |
| A6 | 10 | 7 | 10 | 4 | 6 | 7 | 2 | 1 | 2 | 10 | 4 | 6 |
| A7 | 5 | 4 | 7 | 3 | 4 | 3 | 5 | 4 | 7 | 8 | 7 | 7 |
| A8 | 8 | 10 | 7 | 2 | 4 | 4 | 3 | 4 | 4 | 6 | 8 | 9 |
| A9 | 2 | 3 | 4 | 2 | 2 | 2 | 5 | 7 | 8 | 6 | 8 | 9 |
| A10 | 8 | 9 | 8 | 2 | 6 | 7 | 3 | 3 | 3 | 5 | 5 | 9 |
| A11 | 6 | 6 | 6 | 1 | 3 | 3 | 5 | 3 | 5 | 8 | 8 | 10 |
| A12 | 1 | 1 | 2 | 6 | 2 | 1 | 6 | 9 | 10 | 3 | 10 | 5 |

Anchors: 1 = libertarian/secular/cosmopolitan/no-trust/welcoming/tolerates; 10 = authoritarian/devout/nationalist/full-trust/anti-refugee/primary-driver.

### Emotional baseline (0–1)

| ID | Anger | Fear | Hope | Sadness | Pol. Fatigue |
|----|:-:|:-:|:-:|:-:|:-:|
| A1 | 0.40 | 0.55 | 0.65 | 0.35 | 0.25 |
| A2 | 0.80 | 0.70 | 0.50 | 0.70 | 0.55 |
| A3 | 0.80 | 0.70 | 0.35 | 0.65 | 0.60 |
| A4 | 0.85 | 0.75 | 0.55 | 0.75 | 0.40 |
| A5 | 0.90 | 0.80 | 0.45 | 0.80 | 0.55 |
| A6 | 0.70 | 0.55 | 0.50 | 0.30 | 0.30 |
| A7 | 0.65 | 0.55 | 0.35 | 0.60 | 0.75 |
| A8 | 0.75 | 0.65 | 0.50 | 0.60 | 0.25 |
| A9 | 0.80 | 0.65 | 0.45 | 0.70 | 0.65 |
| A10 | 0.55 | 0.80 | 0.55 | 0.90 | 0.45 |
| A11 | 0.90 | 0.85 | 0.25 | 0.80 | 0.50 |
| A12 | 0.80 | 0.75 | 0.45 | 0.80 | 0.70 |

### Media diet (0–1, intensity not share)

| ID | Pro-Govt | Opp. | Social | Local/Family | Alt./Independent |
|----|:-:|:-:|:-:|:-:|:-:|
| A1 | 0.85 | 0.05 | 0.40 | 0.85 | 0.05 |
| A2 | 0.05 | 0.80 | 0.75 | 0.45 | 0.60 |
| A3 | 0.45 | 0.40 | 0.65 | 0.75 | 0.20 |
| A4 | 0.02 | 0.80 | 0.70 | 0.80 | 0.65 |
| A5 | 0.05 | 0.55 | 0.80 | 0.90 | 0.85 |
| A6 | 0.70 | 0.20 | 0.60 | 0.75 | 0.20 |
| A7 | 0.20 | 0.60 | 0.65 | 0.55 | 0.45 |
| A8 | 0.45 | 0.15 | 0.60 | 0.85 | 0.35 |
| A9 | 0.05 | 0.45 | 0.95 | 0.35 | 0.75 |
| A10 | 0.75 | 0.10 | 0.55 | 0.90 | 0.15 |
| A11 | 0.50 | 0.40 | 0.35 | 0.85 | 0.20 |
| A12 | 0.02 | 0.55 | 0.90 | 0.30 | 0.90 |

### Behavioral variables (0–1)

| ID | Partisan | OpenPersuade | Protest | Turnout | Strategic | Boycott | NatBacklash | EconSens | DisasterSens | IdentSal | LeaderLoy |
|----|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A1 | 0.90 | 0.20 | 0.20 | 0.85 | 0.20 | 0.10 | 0.65 | 0.55 | 0.30 | 0.85 | 0.95 |
| A2 | 0.85 | 0.30 | 0.40 | 0.92 | 0.70 | 0.30 | 0.30 | 0.70 | 0.85 | 0.80 | 0.45 |
| A3 | 0.40 | 0.70 | 0.75 | 0.65 | 0.50 | 0.35 | 0.75 | 0.95 | 0.65 | 0.55 | 0.45 |
| A4 | 0.92 | 0.20 | 0.30 | 0.94 | 0.55 | 0.15 | 0.25 | 0.75 | 0.90 | 0.95 | 0.65 |
| A5 | 0.90 | 0.20 | 0.55 | 0.82 | 0.80 | 0.25 | 0.15 | 0.70 | 0.85 | 0.98 | 0.55 |
| A6 | 0.85 | 0.25 | 0.30 | 0.85 | 0.50 | 0.15 | 0.95 | 0.55 | 0.40 | 0.95 | 0.75 |
| A7 | 0.45 | 0.60 | 0.45 | 0.75 | 0.75 | 0.25 | 0.70 | 0.80 | 0.70 | 0.60 | 0.40 |
| A8 | 0.65 | 0.55 | 0.65 | 0.88 | 0.40 | 0.20 | 0.55 | 0.90 | 0.60 | 0.95 | 0.45 |
| A9 | 0.40 | 0.65 | 0.75 | 0.70 | 0.80 | 0.45 | 0.45 | 0.90 | 0.90 | 0.70 | 0.45 |
| A10 | 0.65 | 0.40 | 0.30 | 0.80 | 0.35 | 0.10 | 0.55 | 0.85 | 0.95 | 0.75 | 0.80 |
| A11 | 0.40 | 0.65 | 0.85 | 0.90 | 0.55 | 0.15 | 0.55 | 0.98 | 0.55 | 0.45 | 0.30 |
| A12 | 0.65 | 0.40 | 0.50 | 0.88 | 0.85 | 0.40 | 0.20 | 0.55 | 0.95 | 0.70 | 0.50 |

### Initial vote intention (probability distribution, sums to 1.0)

| ID | AKP | CHP | MHP | İYİ | HDP | YRP | Other | Undecided |
|----|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A1 | 0.85 | 0.00 | 0.05 | 0.00 | 0.00 | 0.05 | 0.00 | 0.05 |
| A2 | 0.00 | 0.85 | 0.00 | 0.08 | 0.02 | 0.00 | 0.02 | 0.03 |
| A3 | 0.60 | 0.10 | 0.15 | 0.05 | 0.00 | 0.05 | 0.00 | 0.05 |
| A4 | 0.00 | 0.85 | 0.00 | 0.02 | 0.10 | 0.00 | 0.01 | 0.02 |
| A5 | 0.05 | 0.05 | 0.00 | 0.00 | 0.80 | 0.00 | 0.05 | 0.05 |
| A6 | 0.25 | 0.00 | 0.65 | 0.03 | 0.00 | 0.02 | 0.02 | 0.03 |
| A7 | 0.05 | 0.15 | 0.05 | 0.60 | 0.00 | 0.02 | 0.05 | 0.08 |
| A8 | 0.55 | 0.00 | 0.02 | 0.00 | 0.00 | 0.35 | 0.03 | 0.05 |
| A9 | 0.05 | 0.55 | 0.02 | 0.10 | 0.10 | 0.02 | 0.06 | 0.10 |
| A10 | 0.70 | 0.10 | 0.05 | 0.02 | 0.02 | 0.05 | 0.03 | 0.03 |
| A11 | 0.50 | 0.25 | 0.08 | 0.05 | 0.02 | 0.05 | 0.02 | 0.03 |
| A12 | 0.00 | 0.80 | 0.00 | 0.05 | 0.08 | 0.00 | 0.04 | 0.03 |

### 2024 trajectory (probability distribution, sums to 1.0)

| ID | Stays | →CHP | →YRP | →DEM | Abstains | Undec. |
|----|:-:|:-:|:-:|:-:|:-:|:-:|
| A1 | 0.55 | 0.05 | 0.20 | 0.00 | 0.15 | 0.05 |
| A2 | 0.85 | 0.05 | 0.00 | 0.02 | 0.03 | 0.05 |
| A3 | 0.20 | 0.25 | 0.20 | 0.00 | 0.30 | 0.05 |
| A4 | 0.88 | 0.02 | 0.00 | 0.05 | 0.02 | 0.03 |
| A5 | 0.60 | 0.20 | 0.00 | 0.10 | 0.05 | 0.05 |
| A6 | 0.50 | 0.03 | 0.15 | 0.00 | 0.22 | 0.10 |
| A7 | 0.25 | 0.45 | 0.05 | 0.00 | 0.15 | 0.10 |
| A8 | 0.15 | 0.02 | 0.65 | 0.00 | 0.10 | 0.08 |
| A9 | 0.55 | 0.20 | 0.02 | 0.05 | 0.10 | 0.08 |
| A10 | 0.50 | 0.10 | 0.20 | 0.02 | 0.13 | 0.05 |
| A11 | 0.20 | 0.40 | 0.20 | 0.00 | 0.12 | 0.08 |
| A12 | 0.85 | 0.02 | 0.00 | 0.05 | 0.03 | 0.05 |

---

## Task 4 — Event Sensitivity Matrix

Deltas on −1.0..+1.0 for approval/trust/anger/hope; vote_shift_probability on 0..1. Full 12 × 10 matrix is in the JSON. Below: the highest-impact deltas only (one per event), to surface the simulation's main causal levers.

| Event | Highest-impact archetype | Approval Δ | Trust Δ | Anger Δ | Hope Δ | VoteShift p | Why |
|---|---|:-:|:-:|:-:|:-:|:-:|---|
| 2019 Istanbul local | A12 Cosmopolitan Liberal | -0.15 | +0.15 | -0.15 | +0.55 | 0.02 | Maximum institutional-reform investment |
| 2019 Istanbul rerun | A9 Young Urban Protest | -0.15 | +0.15 | -0.15 | +0.60 | 0.05 | KONDA: youth İmamoğlu support 37%→58% |
| COVID period | A12 Cosmopolitan Liberal | -0.25 | -0.15 | +0.35 | -0.15 | 0.02 | Sharp critique of govt communication |
| Lira/inflation 2021-22 | **A11 Retired Protest** | **-0.55** | **-0.30** | **+0.85** | **-0.50** | **0.45** | Pension below hunger threshold; breaking point |
| Refugee debate | A6 Grey Wolf | -0.10 | -0.05 | +0.45 | -0.10 | 0.10 | Strongest pro-deportation; 2024 riot involvement |
| HDP closure case | A5 Kurdish Political | -0.40 | -0.40 | +0.70 | -0.30 | 0.08 | Existential threat |
| Earthquake 2023 | A10 Quake-belt Loyalist | -0.30 | -0.30 | +0.70 | -0.40 | 0.15 | Direct catastrophic shock |
| Presidential 2023 | A10 Quake-belt Loyalist | **+0.25** | +0.15 | -0.30 | +0.30 | 0.10 | Reconstruction-pledge dependency dominates → Erdoğan vote |
| HDP/YSP/DEM transition | A5 Kurdish Political | -0.10 | -0.05 | +0.20 | +0.20 | 0.20 | Rebrand consolidates bloc |
| **2024 local elections** | **A11 Retired Protest** | **-0.55** | -0.20 | +0.70 | +0.10 | **0.70** | Three major polling firms: pensioners were kingmakers |

**Read this matrix as:** for each (archetype × event) pair the JSON contains the full Δ vector and a short qualitative explanation. The five pivotal mechanisms that the simulation must reproduce are:

1. **A11 inflation breaking point** (2021–2022) — pension protest is the strongest single-event shock in the system.
2. **A8 → YRP defection** at 2024 local (vote_shift_probability 0.65) — the YRP 6.19% outcome.
3. **A3 dual exit** at 2024 local — 25% to CHP, 20% to YRP, 30% to abstention (vote_shift_probability 0.55).
4. **A10 quake-belt loyalty paradox** — large negative deltas at the earthquake event, then positive approval delta at the May 2023 election (reconstruction-pledge dependency reverses the punishment).
5. **A5 mobilization** at HDP closure case and 2024 local — strategic voting + identity_salience keeps turnout high under repression.

---

## Task 5 — JSON Output

Machine-readable framework: `synthetic_turkey_simulation.json` (shared separately).

**Validation status:**
- 12 archetypes, all variables populated
- All vote-intention distributions sum to 1.000
- All 2024-trajectory distributions sum to 1.000
- All 12 archetypes have all 10 events in the sensitivity matrix
- 50 agents sum to 100%

**Implementation recipe (in JSON under `simulation_implementation_notes`):**

1. **Instantiate** N agents per archetype using the Task-2 distribution.
2. **Sample variable values** from N(mean, σ) with σ ≈ 0.05–0.10 for 0–1 scales and 0.5–0.8 for 1–10 scales; clip to bounds.
3. **Assign initial vote intention** from the categorical prior.
4. **Apply events in order**: 2019_local → 2019_rerun → covid → inflation → refugee → hdp_closure → earthquake → presidential → hdp_dem_transition → 2024_local.
5. **Update emotion** as: `new = clip(old + delta × (1 − 0.5 × political_fatigue), 0, 1)`.
6. **Update approval (1–10)** as: `new = clip(old + delta × 5, 1, 10)`.
7. **Resolve vote shift** with probability `vote_shift_probability`; on success, redraw vote from the `trajectory_2024` distribution.
8. **Sanity check 2024 simulated shares** against: AKP 30–40%, CHP 35–42%, MHP 3–7%, İYİ 2–5%, DEM 5–9%, YRP 5–9%, Other/Abstain 5–15%.

---

## Epistemic Warnings

- These values are research-informed estimates anchored to the published archetype document, not statistically representative of the Turkish electorate.
- No KONDA microdata or TÜİK individual-level data was used. All within-archetype distributions are interpretive bridges from published aggregates.
- Within-archetype variation is collapsed to a single mean vector. Simulation runs should add Gaussian noise at agent instantiation.
- Initial vote intention and 2024 trajectory are conditioned on the published vote-trajectory narrative in the base document, not on an independent reweighting of YSK results.
- Weights are academically defensible orders of magnitude, not precise population shares. Treat ±2 agents per archetype as a reasonable robustness band.
- The Task-4 deltas are calibrated for *plausibility and ordering*, not for predictive accuracy. Re-calibrate against a held-out empirical anchor (e.g., 2023 first-round YSK by province) before reporting simulation findings as evidence.
