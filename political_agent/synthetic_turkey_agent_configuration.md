# Synthetic Turkey — Political Agent Configuration

**Simulation window:** January 2019 – April 2024
**Purpose:** Consolidated, simulation-ready political-agent configuration files for the Synthetic Turkey agent-based political simulation.
**Source of truth:** uploaded profile files (`profile_erdogan.md`, `profile_kilicdaroglu.md`, `profile_imamoglu.md`, `profile_bahceli.md`, `profile_aksener.md`, `synthetic_turkey_kurdish_movement.md`, `kurdish_personas_simulation.md`, `kurdish_personas.json`, `kurdish_persona_roles_by_period.json`).
**Conventions:**

- All 0–1 values are **source-grounded simulation calibration parameters**, not objective measurements.
- All message frames are paraphrased — no direct quotes.
- Sourced facts vs. simulation assumptions are kept distinct (see notes).
- IDs use snake_case and match the uploaded persona files where applicable.

---

## Output 1 — Agent Classification

| # | Actor | simulation_id | classification | active_agent | use_level | active period | broadcast vs. movement-channel | reason |
|---|---|---|---|---|---|---|---|---|
| 1 | Recep Tayyip Erdoğan | `erdogan_recep_tayyip` | individual_politician_agent | true | must_have | 2019-01 → 2024-04 | direct broadcast | President + AKP leader; dominant national agent; controls state media; sets agenda for every event in the window. |
| 2 | Kemal Kılıçdaroğlu | `kilicdaroglu_kemal` | individual_politician_agent | true | must_have | 2019-01 → 2024-04 (degraded post Nov 2023) | direct broadcast | CHP chair 2019 – Nov 2023; 2023 presidential candidate; downgraded but retained voice after losing leadership. |
| 3 | Ekrem İmamoğlu | `imamoglu_ekrem` | individual_politician_agent | true | must_have | 2019-03 → 2024-04 | direct broadcast | Istanbul mayor; cross-camp persuader; central to 2019 + 2024 local cycles. |
| 4 | Devlet Bahçeli | `bahceli_devlet` | individual_politician_agent | true | must_have | 2019-01 → 2024-04 | direct broadcast (low cadence, high impact) | MHP leader; nationalist agenda-setter inside People's Alliance; surprise-intervention dynamics. |
| 5 | Meral Akşener | `aksener_meral` | individual_politician_agent | true | must_have (degraded post Apr 2024) | 2019-01 → 2024-04 (collapse post 2024-03-31) | direct broadcast | İYİ leader; nationalist opposition pole; 2023 walkout; resigned April 2024. |
| 6 | Kurdish Political Movement | `kurdish_movement_agent` | movement_agent | true | must_have | 2019-01 → 2024-04 | movement-level broadcast; internal personas channel through it | Modeled as one dynamic actor passing through HDP → YSP → HEDEP → DEM under sustained legal pressure. State machine carries the variation. |
| 7 | Selahattin Demirtaş | `demirtas_selahattin` | symbolic_persona + legal_pressure_symbol | true (locked) | must_have | 2019-01 → 2024-04 (already imprisoned since 2016-11-04) | channels through movement | Locked symbolic resource: zero operational agency, maximum legitimacy generation. Personal popularity exceeds party brand. |
| 8 | Pervin Buldan | `buldan_pervin` | institutional_leader (HDP phase) | true | must_have | 2019-01 → 2023-08-27 (then advisory / Imrali Delegation Dec 2023+) | channels through movement | Primary institutional leader of HDP through closure case; authored 2024 own-candidates strategy. |
| 9 | Mithat Sancar | `sancar_mithat` | institutional_leader (HDP phase) | true | useful_secondary | 2020-02-23 → 2023-08-27 (then Imrali Delegation Dec 2023+) | channels through movement | Co-chair with Buldan; constitutional-law legitimacy; collapsible to Buldan–Sancar pair in low-resolution runs. |
| 10 | Sırrı Süreyya Önder | `onder_sirri_sureyya` | strategic_communicator + parliamentary_voice | true | useful_secondary | 2019-01 → 2024-04 (TBMM Deputy Speaker from 2023-07) | channels through movement | Peace-process interlocutor; Imrali Delegation; non-Kurd bridge figure. |
| 11 | Tülay Hatimoğulları Oruç | `hatimogullari_tulay` | institutional_leader (DEM phase) + strategic_communicator | true | must_have | 2023-10-15 → 2024-04 | channels through movement | DEM co-chair; "weaken AKP" faction; led 2024 Third Way doctrine and Van crisis response. |
| 12 | Tuncer Bakırhan | `bakirhan_tuncer` | institutional_leader (DEM phase) + local_democracy_figure | true | useful_secondary | 2023-10-15 → 2024-04 | channels through movement | DEM co-chair with Hatimoğulları; anti-kayyum lead; collapsible to Hatimoğulları–Bakırhan pair. |
| 13 | Abdullah Zeydan | `zeydan_abdullah` | local_democracy_figure + legal_pressure_symbol | true | must_have | 2023-Q4 → 2024-04 (Van mayor from 2024-04-03) | channels through movement; spikes as agent in P7 | Van crisis cannot be reproduced without him; full mandate_contestation_state pipeline. |
| 14 | Meral Danış Beştaş | `bestas_meral_danis` | parliamentary_voice + institutional_leader + legal_pressure_symbol | true | useful_secondary | 2019-01 → 2024-04 (DEM Istanbul co-candidate Feb–Mar 2024) | channels through movement | Closure-case legal lead; DEM Istanbul candidacy = identity-not-arithmetic signal. |
| 15 | Ahmet Türk | `turk_ahmet` | symbolic_persona + local_democracy_figure | true | useful_secondary | 2019-01 → 2024-04 | channels through movement | Faction-axis counterweight to Hatimoğulları ("dialogue with Erdoğan" pole); Mardin twice-removed mayor. |
| 16 | Gültan Kışanak | `kisanak_gultan` | legal_pressure_symbol + symbolic_persona | false (active only in P6 around symbolic Ankara candidacy) | useful_secondary | window-imprisoned (released 2024-05-16 — post-window) | channels through movement | Symbolic candidacy from prison Jan 2024; otherwise group with Tuncel as imprisoned-women cluster. |
| 17 | Çiğdem Kılıçgün Uçar | `kilicgun_ucar_cigdem` | strategic_communicator (transitional) | false | context_only | 2022-10 → 2023-10 | n/a | YSP interim spokesperson; role-fill rather than unique agent. |
| 18 | İbrahim Akın | `akin_ibrahim` | context_only | false | context_only | window | n/a (background `non_Kurdish_socialist_wing` variable) | Non-Kurdish socialist wing of YSP; role-ambiguity flagged in source. |
| 19 | Sebahat Tuncel | `tuncel_sebahat` | legal_pressure_symbol | false | context_only | imprisoned throughout window | n/a (cluster with Kışanak) | January 2019 hunger strike noted; otherwise background. |
| 20 | Başak Demirtaş | `basak_demirtas` | symbolic_persona (episode-specific) | false | context_only | event trigger Jan–Feb 2024 only | event trigger | Istanbul candidacy debate event trigger; not a continuous agent. |
| 21 | Sultan Özcan | `ozcan_sultan` | institutional_leader (HDP shell, with Kırkazak) | false | context_only | 2023-08-27 → window end | n/a (legal_continuity background) | HDP-shell maintenance leadership; preserves legal personhood. |
| 22 | Cahit Kırkazak | `kirkazak_cahit` | institutional_leader (HDP shell, with Özcan) | false | context_only | 2023-08-27 → window end | n/a (legal_continuity background) | Same role logic as Özcan — joint shell-leadership agent. |
| 23 | Figen Yüksekdağ | `yuksekdag_figen` | legal_pressure_symbol | false | context_only | window-pressured | n/a (cluster with Demirtaş) | Co-chair 2014–2017; legal-pressure cluster reinforcement only. |

**Active broadcasting agents (final list, 13 entities):**
`erdogan_recep_tayyip`, `kilicdaroglu_kemal`, `imamoglu_ekrem`, `bahceli_devlet`, `aksener_meral`, `kurdish_movement_agent` (with internal personas: `demirtas_selahattin` (locked), `buldan_pervin`, `sancar_mithat`, `onder_sirri_sureyya`, `hatimogullari_tulay`, `bakirhan_tuncer`, `bestas_meral_danis`, `turk_ahmet`, `zeydan_abdullah`).

`kisanak_gultan` is an episode-scoped active persona for P6 only.

---

## Output 2 — Political Agent Variables

All 0–1 communication and effects scores are source-grounded simulation calibration parameters derived from the uploaded profiles. Where the source profile provided a different scale (e.g. 1–10 ideological profiles for Kurdish personas), values have been normalized to 0–1 by dividing by 10. Where the source already used 0–1, the value is reproduced.

### 2.1 Erdoğan — `erdogan_recep_tayyip`

```
agent_kind: individual
party_or_movement: AKP (People's Alliance / Cumhur İttifakı)
active_start_date: 2019-01-01
active_end_date: 2024-04-30 (continues past window)
role_type: individual_politician_agent / institutional_leader
ideological_family: Turkish-Islamic synthesis · authoritarian-populist
alliance_position: People's Alliance leader (Cumhur İttifakı)

communication_profile:
  combative: 0.85
  nationalist: 0.80
  populist: 0.80
  hopeful: 0.55
  defensive: 0.60
  conciliatory: 0.15
  technocratic: 0.20
  religious_framing: 0.80
  democratic_framing: 0.55
  economic_framing: 0.75
  security_framing: 0.85
  anti_corruption_framing: 0.30
  local_governance_framing: 0.30
  refugee_framing: 0.65
  legal_rights_framing: 0.25
  identity_framing: 0.80
  feminist_ecological_framing: 0.10

simulation_effects:
  persuasion_strength: 0.58
  polarization_effect: 0.88
  mobilization_effect: 0.78
  cross_camp_reach: 0.25
  base_lock_in_effect: 0.85
  backlash_risk: 0.75
  media_amplification: 0.95
  crisis_responsiveness: 0.55
  institutional_continuity_signal: 0.70
```

### 2.2 Kılıçdaroğlu — `kilicdaroglu_kemal`

```
agent_kind: individual
party_or_movement: CHP (2019-01 → 2023-11) / CHP backbench elder (2023-11 → window end)
active_start_date: 2019-01-01
active_end_date: 2024-04-30
role_type: individual_politician_agent (broadcast power decreases sharply after 2023-11 CHP leadership loss)
ideological_family: social-democratic / Kemalist-coalition-builder
alliance_position: Nation Alliance leader 2019-2023; backbench post Nov 2023

communication_profile:
  combative: 0.45
  nationalist: 0.35
  populist: 0.65
  hopeful: 0.80
  defensive: 0.35
  conciliatory: 0.75
  technocratic: 0.30
  religious_framing: 0.35   # helalleşme outreach
  democratic_framing: 0.80
  economic_framing: 0.70
  security_framing: 0.25
  anti_corruption_framing: 0.75
  local_governance_framing: 0.40
  refugee_framing: 0.50     # runoff pivot raised this
  legal_rights_framing: 0.65
  identity_framing: 0.50
  feminist_ecological_framing: 0.35

simulation_effects:
  persuasion_strength: 0.52
  polarization_effect: 0.42
  mobilization_effect: 0.62
  cross_camp_reach: 0.55
  base_lock_in_effect: 0.65
  backlash_risk: 0.35
  media_amplification: 0.45
  crisis_responsiveness: 0.55
  institutional_continuity_signal: 0.55
  broadcast_power_multiplier_after_2023_11: 0.40   # apply globally from 2023-11
```

### 2.3 İmamoğlu — `imamoglu_ekrem`

```
agent_kind: individual
party_or_movement: CHP (Istanbul Metropolitan Mayor)
active_start_date: 2019-03-31
active_end_date: 2024-04-30
role_type: individual_politician_agent / local_democracy_figure
ideological_family: left-populist / Radical Love / social-democratic
alliance_position: Nation Alliance (2019-2023); CHP-led opposition (2024)

communication_profile:
  combative: 0.30
  nationalist: 0.30
  populist: 0.55
  hopeful: 0.80
  defensive: 0.30
  conciliatory: 0.75
  technocratic: 0.55
  religious_framing: 0.40   # respectful outreach
  democratic_framing: 0.75
  economic_framing: 0.55
  security_framing: 0.20
  anti_corruption_framing: 0.70
  local_governance_framing: 0.90
  refugee_framing: 0.35
  legal_rights_framing: 0.60
  identity_framing: 0.50
  feminist_ecological_framing: 0.40

simulation_effects:
  persuasion_strength: 0.68
  polarization_effect: 0.28
  mobilization_effect: 0.78
  cross_camp_reach: 0.72
  base_lock_in_effect: 0.70
  backlash_risk: 0.40   # AKP threat-perception of his popularity
  media_amplification: 0.55
  crisis_responsiveness: 0.75   # COVID + earthquake city role
  institutional_continuity_signal: 0.75
```

### 2.4 Bahçeli — `bahceli_devlet`

```
agent_kind: individual
party_or_movement: MHP (People's Alliance)
active_start_date: 2019-01-01
active_end_date: 2024-04-30
role_type: individual_politician_agent / institutional_leader
ideological_family: Turkish ultranationalist / state-centric
alliance_position: People's Alliance pillar

communication_profile:
  combative: 0.85
  nationalist: 0.85
  populist: 0.55
  hopeful: 0.40
  defensive: 0.60
  conciliatory: 0.20
  technocratic: 0.05
  religious_framing: 0.45
  democratic_framing: 0.25
  economic_framing: 0.20
  security_framing: 0.95
  anti_corruption_framing: 0.30
  local_governance_framing: 0.20
  refugee_framing: 0.50
  legal_rights_framing: 0.20
  identity_framing: 0.85
  feminist_ecological_framing: 0.05

simulation_effects:
  persuasion_strength: 0.52
  polarization_effect: 0.78
  mobilization_effect: 0.68
  cross_camp_reach: 0.18
  base_lock_in_effect: 0.85
  backlash_risk: 0.65
  media_amplification: 0.60   # weekly TBMM group speech as agenda-setter
  crisis_responsiveness: 0.40
  institutional_continuity_signal: 0.70
  agenda_setting_power: 0.80   # custom: low cadence high impact
```

### 2.5 Akşener — `aksener_meral`

```
agent_kind: individual
party_or_movement: İYİ Party
active_start_date: 2019-01-01
active_end_date: 2024-04 (resigned April 2024 after local collapse; influence collapses post 2024-03-31)
role_type: individual_politician_agent / institutional_leader
ideological_family: Republican nationalist / center-right secular nationalist
alliance_position: Nation Alliance (2019-2023); solo strategy 2024

communication_profile:
  combative: 0.80
  nationalist: 0.75
  populist: 0.75
  hopeful: 0.60
  defensive: 0.55
  conciliatory: 0.30
  technocratic: 0.20
  religious_framing: 0.30   # yemeni ritual / cultural Sunni
  democratic_framing: 0.55
  economic_framing: 0.60
  security_framing: 0.65
  anti_corruption_framing: 0.55
  local_governance_framing: 0.35
  refugee_framing: 0.75
  legal_rights_framing: 0.35
  identity_framing: 0.65
  feminist_ecological_framing: 0.40   # first-female-Interior-Minister symbolism

simulation_effects:
  persuasion_strength: 0.62
  polarization_effect: 0.65
  mobilization_effect: 0.58
  cross_camp_reach: 0.40
  base_lock_in_effect: 0.60
  backlash_risk: 0.45
  media_amplification: 0.45
  crisis_responsiveness: 0.45
  institutional_continuity_signal: 0.55
  broadcast_power_multiplier_after_2024_03_31: 0.30   # apply after local collapse
```

### 2.6 KurdishMovementAgent — `kurdish_movement_agent`

```
agent_kind: movement
party_or_movement: HDP → YSP (Green Left) → HEDEP → DEM Party (state-machine driven)
active_start_date: 2019-01-01
active_end_date: 2024-04-30
role_type: movement_agent
ideological_family: left-pluralist / Kurdish-democratic / Labour and Freedom Alliance
alliance_position: outside both formal alliances; informal anti-AKP 2019-2023; Third Way 2024

# Communication profile is computed as a weighted blend of active internal personas in the current period.
# Default blend below reflects the typical period-1-to-period-7 average. Use the state machine to override per period.
communication_profile:
  combative: 0.50
  nationalist: 0.10            # against; this is its anti-self
  populist: 0.55
  hopeful: 0.60
  defensive: 0.65
  conciliatory: 0.55
  technocratic: 0.40
  religious_framing: 0.25
  democratic_framing: 0.85
  economic_framing: 0.45
  security_framing: 0.15
  anti_corruption_framing: 0.50
  local_governance_framing: 0.80
  refugee_framing: 0.45
  legal_rights_framing: 0.85
  identity_framing: 0.80
  feminist_ecological_framing: 0.70

simulation_effects:
  persuasion_strength: 0.55     # mostly base-directed
  polarization_effect: 0.55     # mainly nationalist counter-mobilisation
  mobilization_effect: 0.75     # very high in Kurdish provinces
  cross_camp_reach: 0.40        # via Demirtaş + Önder
  base_lock_in_effect: 0.85
  backlash_risk: 0.70           # nationalist backlash structurally embedded
  media_amplification: 0.30     # under severe state-media suppression
  crisis_responsiveness: 0.65
  institutional_continuity_signal: 0.55   # rebrand-resilient

# Kurdish-specific extension fields (movement-level defaults; state machine overrides per period)
kurdish_rights_emphasis: 0.90
anti_trustee_kayyum_emphasis: 0.90
peace_process_emphasis: 0.65
strategic_voting_emphasis: 0.50   # period-dependent
independent_party_identity_signal: 0.75
symbolic_mobilization_power: 0.85   # via Demirtaş
```

### 2.7 Internal Kurdish personas (active)

Internal personas are not full broadcast agents. They modulate the movement-level signal. Their numeric fields are reproduced/normalized from `kurdish_personas.json` and `kurdish_personas_simulation.md`. Use them to (a) re-weight the movement's communication blend in periods where they are active, and (b) generate event-specific paraphrased frames.

#### 2.7.1 Demirtaş — `demirtas_selahattin`

```
agent_kind: symbolic_resource
role_type: symbolic_persona + legal_pressure_symbol
operational_agency: 0.00       # locked
legitimacy_generation: 1.00    # max
active_period: 2019-01 → 2024-04 (already imprisoned since 2016-11-04)

communication_profile:
  combative: 0.50
  nationalist: 0.05
  populist: 0.55
  hopeful: 0.65
  defensive: 0.55
  conciliatory: 0.55
  technocratic: 0.30
  religious_framing: 0.20
  democratic_framing: 0.95
  economic_framing: 0.40
  security_framing: 0.10
  anti_corruption_framing: 0.55
  local_governance_framing: 0.45
  refugee_framing: 0.40
  legal_rights_framing: 0.85
  identity_framing: 0.75
  feminist_ecological_framing: 0.55

simulation_effects:
  persuasion_strength: 0.70    # paraphrased frames have unusual cross-camp reach
  polarization_effect: 0.55
  mobilization_effect: 0.85
  cross_camp_reach: 0.65       # urban progressive + young
  base_lock_in_effect: 0.90
  backlash_risk: 0.75
  media_amplification: 0.45    # via international + opposition media
  crisis_responsiveness: 0.40
  institutional_continuity_signal: 0.60

kurdish_rights_emphasis: 0.90
anti_trustee_kayyum_emphasis: 0.80
peace_process_emphasis: 0.90
strategic_voting_emphasis: 0.75
independent_party_identity_signal: 0.55
symbolic_mobilization_power: 1.00
```

#### 2.7.2 Buldan — `buldan_pervin`

```
agent_kind: internal_persona
role_type: institutional_leader (HDP phase 2019 → Aug 2023; advisory thereafter)

communication_profile:
  combative: 0.45
  nationalist: 0.10
  populist: 0.55
  hopeful: 0.60
  defensive: 0.55
  conciliatory: 0.70
  technocratic: 0.45
  religious_framing: 0.20
  democratic_framing: 0.85
  economic_framing: 0.40
  security_framing: 0.10
  anti_corruption_framing: 0.45
  local_governance_framing: 0.65
  refugee_framing: 0.40
  legal_rights_framing: 0.70
  identity_framing: 0.70
  feminist_ecological_framing: 0.70

simulation_effects:
  persuasion_strength: 0.60
  polarization_effect: 0.50
  mobilization_effect: 0.70
  cross_camp_reach: 0.45
  base_lock_in_effect: 0.75
  backlash_risk: 0.50
  media_amplification: 0.40
  crisis_responsiveness: 0.65
  institutional_continuity_signal: 0.90

kurdish_rights_emphasis: 0.90
anti_trustee_kayyum_emphasis: 0.90
peace_process_emphasis: 1.00
strategic_voting_emphasis: 0.70
independent_party_identity_signal: 0.65
symbolic_mobilization_power: 0.70
```

#### 2.7.3 Sancar — `sancar_mithat`

```
agent_kind: internal_persona
role_type: institutional_leader (HDP phase 2020-02-23 → 2023-08-27)
communication_profile:
  combative: 0.35; nationalist: 0.05; populist: 0.40; hopeful: 0.50; defensive: 0.55
  conciliatory: 0.75; technocratic: 0.70
  religious_framing: 0.15; democratic_framing: 0.90; economic_framing: 0.45
  security_framing: 0.10; anti_corruption_framing: 0.50; local_governance_framing: 0.55
  refugee_framing: 0.45; legal_rights_framing: 0.95; identity_framing: 0.60
  feminist_ecological_framing: 0.50
simulation_effects:
  persuasion_strength: 0.50; polarization_effect: 0.35; mobilization_effect: 0.50
  cross_camp_reach: 0.55; base_lock_in_effect: 0.65; backlash_risk: 0.35
  media_amplification: 0.35; crisis_responsiveness: 0.55; institutional_continuity_signal: 0.90
kurdish_rights_emphasis: 0.80; anti_trustee_kayyum_emphasis: 0.80
peace_process_emphasis: 0.80; strategic_voting_emphasis: 0.65
independent_party_identity_signal: 0.60; symbolic_mobilization_power: 0.50
```

#### 2.7.4 Önder — `onder_sirri_sureyya`

```
agent_kind: internal_persona
role_type: strategic_communicator + parliamentary_voice + symbolic_persona
communication_profile:
  combative: 0.55; nationalist: 0.05; populist: 0.55; hopeful: 0.65; defensive: 0.45
  conciliatory: 0.60; technocratic: 0.45
  religious_framing: 0.20; democratic_framing: 0.85; economic_framing: 0.55
  security_framing: 0.10; anti_corruption_framing: 0.50; local_governance_framing: 0.50
  refugee_framing: 0.40; legal_rights_framing: 0.70; identity_framing: 0.75
  feminist_ecological_framing: 0.55
simulation_effects:
  persuasion_strength: 0.60; polarization_effect: 0.55; mobilization_effect: 0.85
  cross_camp_reach: 0.60; base_lock_in_effect: 0.70; backlash_risk: 0.60
  media_amplification: 0.45; crisis_responsiveness: 0.60; institutional_continuity_signal: 0.80
kurdish_rights_emphasis: 0.80; anti_trustee_kayyum_emphasis: 0.70
peace_process_emphasis: 1.00; strategic_voting_emphasis: 0.70
independent_party_identity_signal: 0.65; symbolic_mobilization_power: 0.80
```

#### 2.7.5 Hatimoğulları — `hatimogullari_tulay`

```
agent_kind: internal_persona
role_type: institutional_leader (DEM phase, from 2023-10-15)
communication_profile:
  combative: 0.60; nationalist: 0.05; populist: 0.55; hopeful: 0.55; defensive: 0.50
  conciliatory: 0.55; technocratic: 0.45
  religious_framing: 0.15; democratic_framing: 0.85; economic_framing: 0.50
  security_framing: 0.10; anti_corruption_framing: 0.65; local_governance_framing: 0.85
  refugee_framing: 0.40; legal_rights_framing: 0.80; identity_framing: 0.80
  feminist_ecological_framing: 0.75
simulation_effects:
  persuasion_strength: 0.60; polarization_effect: 0.55; mobilization_effect: 0.80
  cross_camp_reach: 0.35; base_lock_in_effect: 0.85; backlash_risk: 0.55
  media_amplification: 0.40; crisis_responsiveness: 0.85; institutional_continuity_signal: 0.85
kurdish_rights_emphasis: 0.90; anti_trustee_kayyum_emphasis: 1.00
peace_process_emphasis: 0.70; strategic_voting_emphasis: 0.25
independent_party_identity_signal: 0.95; symbolic_mobilization_power: 0.70
faction_id: weaken_AKP
```

#### 2.7.6 Bakırhan — `bakirhan_tuncer`

```
agent_kind: internal_persona
role_type: institutional_leader (DEM phase) + local_democracy_figure
communication_profile:
  combative: 0.55; nationalist: 0.05; populist: 0.50; hopeful: 0.55; defensive: 0.50
  conciliatory: 0.50; technocratic: 0.50
  religious_framing: 0.20; democratic_framing: 0.75; economic_framing: 0.45
  security_framing: 0.10; anti_corruption_framing: 0.65; local_governance_framing: 0.95
  refugee_framing: 0.35; legal_rights_framing: 0.70; identity_framing: 0.70
  feminist_ecological_framing: 0.45
simulation_effects:
  persuasion_strength: 0.55; polarization_effect: 0.45; mobilization_effect: 0.75
  cross_camp_reach: 0.30; base_lock_in_effect: 0.80; backlash_risk: 0.45
  media_amplification: 0.30; crisis_responsiveness: 0.75; institutional_continuity_signal: 0.90
kurdish_rights_emphasis: 0.90; anti_trustee_kayyum_emphasis: 1.00
peace_process_emphasis: 0.70; strategic_voting_emphasis: 0.25
independent_party_identity_signal: 0.95; symbolic_mobilization_power: 0.60
```

#### 2.7.7 Beştaş — `bestas_meral_danis`

```
agent_kind: internal_persona
role_type: parliamentary_voice + institutional_leader + legal_pressure_symbol
communication_profile:
  combative: 0.50; nationalist: 0.05; populist: 0.45; hopeful: 0.45; defensive: 0.55
  conciliatory: 0.45; technocratic: 0.65
  religious_framing: 0.15; democratic_framing: 0.90; economic_framing: 0.40
  security_framing: 0.10; anti_corruption_framing: 0.55; local_governance_framing: 0.65
  refugee_framing: 0.45; legal_rights_framing: 0.95; identity_framing: 0.60
  feminist_ecological_framing: 0.70
simulation_effects:
  persuasion_strength: 0.50; polarization_effect: 0.45; mobilization_effect: 0.70
  cross_camp_reach: 0.40; base_lock_in_effect: 0.70; backlash_risk: 0.40
  media_amplification: 0.35; crisis_responsiveness: 0.70; institutional_continuity_signal: 0.90
kurdish_rights_emphasis: 0.90; anti_trustee_kayyum_emphasis: 0.80
peace_process_emphasis: 0.70; strategic_voting_emphasis: 0.30
independent_party_identity_signal: 0.85; symbolic_mobilization_power: 0.60
```

#### 2.7.8 Türk — `turk_ahmet`

```
agent_kind: internal_persona
role_type: symbolic_persona + local_democracy_figure
communication_profile:
  combative: 0.25; nationalist: 0.05; populist: 0.40; hopeful: 0.55; defensive: 0.45
  conciliatory: 0.85; technocratic: 0.40
  religious_framing: 0.30; democratic_framing: 0.75; economic_framing: 0.35
  security_framing: 0.10; anti_corruption_framing: 0.40; local_governance_framing: 0.85
  refugee_framing: 0.30; legal_rights_framing: 0.70; identity_framing: 0.85
  feminist_ecological_framing: 0.40
simulation_effects:
  persuasion_strength: 0.55; polarization_effect: 0.30; mobilization_effect: 0.65
  cross_camp_reach: 0.55; base_lock_in_effect: 0.75; backlash_risk: 0.30
  media_amplification: 0.40; crisis_responsiveness: 0.55; institutional_continuity_signal: 0.85
kurdish_rights_emphasis: 1.00; anti_trustee_kayyum_emphasis: 1.00
peace_process_emphasis: 1.00; strategic_voting_emphasis: 0.40
independent_party_identity_signal: 0.70; symbolic_mobilization_power: 0.80
faction_id: dialogue_first
```

#### 2.7.9 Zeydan — `zeydan_abdullah`

```
agent_kind: internal_persona
role_type: local_democracy_figure + legal_pressure_symbol
communication_profile:
  combative: 0.70; nationalist: 0.05; populist: 0.55; hopeful: 0.55; defensive: 0.50
  conciliatory: 0.35; technocratic: 0.40
  religious_framing: 0.20; democratic_framing: 0.85; economic_framing: 0.45
  security_framing: 0.10; anti_corruption_framing: 0.60; local_governance_framing: 0.90
  refugee_framing: 0.30; legal_rights_framing: 0.80; identity_framing: 0.75
  feminist_ecological_framing: 0.30
simulation_effects:
  persuasion_strength: 0.55; polarization_effect: 0.55; mobilization_effect: 0.90
  cross_camp_reach: 0.35; base_lock_in_effect: 0.85; backlash_risk: 0.70
  media_amplification: 0.55; crisis_responsiveness: 0.95; institutional_continuity_signal: 0.80
kurdish_rights_emphasis: 0.90; anti_trustee_kayyum_emphasis: 1.00
peace_process_emphasis: 0.60; strategic_voting_emphasis: 0.15
independent_party_identity_signal: 0.90; symbolic_mobilization_power: 0.80
```

#### 2.7.10 Kışanak — `kisanak_gultan` (P6 only)

```
agent_kind: internal_persona (episode-active, P6 only)
role_type: legal_pressure_symbol + symbolic_persona
communication_profile:
  combative: 0.50; nationalist: 0.05; populist: 0.45; hopeful: 0.45; defensive: 0.55
  conciliatory: 0.45; technocratic: 0.35
  religious_framing: 0.15; democratic_framing: 0.85; economic_framing: 0.30
  security_framing: 0.10; anti_corruption_framing: 0.55; local_governance_framing: 0.85
  refugee_framing: 0.30; legal_rights_framing: 0.85; identity_framing: 0.85
  feminist_ecological_framing: 0.90
simulation_effects:
  persuasion_strength: 0.50; polarization_effect: 0.45; mobilization_effect: 0.70
  cross_camp_reach: 0.45; base_lock_in_effect: 0.80; backlash_risk: 0.50
  media_amplification: 0.55; crisis_responsiveness: 0.45; institutional_continuity_signal: 0.80
kurdish_rights_emphasis: 1.00; anti_trustee_kayyum_emphasis: 1.00
peace_process_emphasis: 0.70; strategic_voting_emphasis: 0.20
independent_party_identity_signal: 0.85; symbolic_mobilization_power: 0.90
```

---

## Output 3 — Credibility Matrix

Voter archetypes (12):

1. Devout Anatolian Loyalist (`devout_anatolian_loyalist`)
2. Secular Urban Professional (`secular_urban_professional`)
3. Conservative Economically Disillusioned (`conservative_economically_disillusioned`)
4. Alevi-CHP Loyalist (`alevi_chp_loyalist`)
5. Kurdish Political Voter (`kurdish_political_voter`)
6. Nationalist Grey Wolf Core (`nationalist_grey_wolf_core`)
7. Moderate Nationalist Opposition (`moderate_nationalist_opposition`)
8. Pious Disillusioned Islamist (`pious_disillusioned_islamist`)
9. Young Urban Protest Voter (`young_urban_protest_voter`)
10. Earthquake Zone Loyalist (`earthquake_zone_loyalist`)
11. Retired Protest Voter (`retired_protest_voter`)
12. Cosmopolitan Liberal Urban Professional (`cosmopolitan_liberal_urban_professional`)

Effect codes:

- `persuade` = moves persuadable voters to support
- `mobilize_base` = activates existing supporters / raises turnout
- `reinforce_existing_belief` = consolidates prior orientation
- `trigger_backlash` = activates counter-mobilization
- `ignored` = below salience threshold

### 3.1 Erdoğan × archetypes

| Archetype | credibility | likely_effect | explanation |
|---|---|---|---|
| devout_anatolian_loyalist | 0.85 | mobilize_base | Foundational base; religion + civilisational restoration frame. |
| secular_urban_professional | 0.10 | trigger_backlash | Net disapproval -20 to -30 (MetroPOLL 2021-22). |
| conservative_economically_disillusioned | 0.48 | reinforce_existing_belief | Welfare clientelism vs inflation; fragile loyalty. |
| alevi_chp_loyalist | 0.05 | trigger_backlash | Sectarian framing of Kılıçdaroğlu read as direct threat. |
| kurdish_political_voter | 0.15 | trigger_backlash | Peace-process collapse + kayyum operations; minority conservative Kurds reachable. |
| nationalist_grey_wolf_core | 0.70 | reinforce_existing_belief | People's Alliance structural; YRP/Zafer slight leakage. |
| moderate_nationalist_opposition | 0.30 | trigger_backlash | İYİ-aligned voters view him as authoritarian. |
| pious_disillusioned_islamist | 0.45 | reinforce_existing_belief | Some leakage to YRP/Saadet but cultural pull holds. |
| young_urban_protest_voter | 0.20 | trigger_backlash | #OyMoyYok generation; 25% youth unemployment. |
| earthquake_zone_loyalist | 0.55 | reinforce_existing_belief | AKP won 8 of 11 quake provinces in May 2023 despite criticism. |
| retired_protest_voter | 0.40 | reinforce_existing_belief | Pension erosion vs religious-identity loyalty; bifurcated. |
| cosmopolitan_liberal_urban_professional | 0.06 | trigger_backlash | Near-total alienation; democratic-rights frame. |

### 3.2 Kılıçdaroğlu × archetypes (apply 0.40 multiplier post 2023-11)

| Archetype | credibility | likely_effect | explanation |
|---|---|---|---|
| devout_anatolian_loyalist | 0.18 | ignored | Helalleşme partially heard; sectarian counter-frame dominates. |
| secular_urban_professional | 0.80 | mobilize_base | Historic CHP base; rule-of-law frame. |
| conservative_economically_disillusioned | 0.42 | persuade | Kitchen-table inflation video resonated; uptake partial. |
| alevi_chp_loyalist | 0.92 | mobilize_base | Identity congruence; Alevi disclosure video. |
| kurdish_political_voter | 0.63 | persuade | Tactical-not-enthusiastic; runoff refugee pivot eroded. |
| nationalist_grey_wolf_core | 0.10 | trigger_backlash | AKP deepfake PKK frame stuck. |
| moderate_nationalist_opposition | 0.35 | persuade | Through Table of Six and İYİ partnership. |
| pious_disillusioned_islamist | 0.30 | persuade | Headscarf apology + Saadet inclusion = limited inroads. |
| young_urban_protest_voter | 0.60 | persuade | ~50% first-round 18-24 support per pre-2023 polls. |
| earthquake_zone_loyalist | 0.40 | persuade | Accountability frame; AKP welfare network held. |
| retired_protest_voter | 0.65 | mobilize_base | Pension/inflation anger; secular cohort core. |
| cosmopolitan_liberal_urban_professional | 0.72 | mobilize_base | Rule-of-law / EU orientation. |

### 3.3 İmamoğlu × archetypes

| Archetype | credibility | likely_effect | explanation |
|---|---|---|---|
| devout_anatolian_loyalist | 0.32 | persuade | Religious outreach (mosque visits) opened ceiling. |
| secular_urban_professional | 0.87 | mobilize_base | Core constituency; service delivery + Radical Love. |
| conservative_economically_disillusioned | 0.62 | persuade | 2024 peripheral-Istanbul AKP defections. |
| alevi_chp_loyalist | 0.82 | mobilize_base | High but slightly below Kılıçdaroğlu identity affinity. |
| kurdish_political_voter | 0.58 | persuade | HDP tactical non-candidacy 2019; multicultural framing. |
| nationalist_grey_wolf_core | 0.25 | reinforce_existing_belief | Won >50% of 2018 MHP voters in June 2019 rerun (extraordinary); core MHP largely resistant. |
| moderate_nationalist_opposition | 0.55 | persuade | İYİ-aligned reachable via inclusive frame. |
| pious_disillusioned_islamist | 0.45 | persuade | Respectful religious register; ceiling on direct credibility. |
| young_urban_protest_voter | 0.80 | mobilize_base | Core youth credibility per MEI 2023. |
| earthquake_zone_loyalist | 0.55 | persuade | İBB earthquake response visible. |
| retired_protest_voter | 0.70 | mobilize_base | Service-delivery record + Istanbul pensioners. |
| cosmopolitan_liberal_urban_professional | 0.88 | mobilize_base | Highest cross-camp credibility in opposition. |

### 3.4 Bahçeli × archetypes

| Archetype | credibility | likely_effect | explanation |
|---|---|---|---|
| devout_anatolian_loyalist | 0.50 | reinforce_existing_belief | Turkish-Islamic synthesis overlap; not primary affinity. |
| secular_urban_professional | 0.10 | trigger_backlash | Anti-democratic, anti-rights framing rejected. |
| conservative_economically_disillusioned | 0.28 | ignored | Minimal economic content. |
| alevi_chp_loyalist | 0.05 | trigger_backlash | Hard nationalist register read as direct threat. |
| kurdish_political_voter | 0.05 | trigger_backlash | Closure demands + trustee endorsement. |
| nationalist_grey_wolf_core | 0.85 | mobilize_base | Ülkücü organizational network identity. |
| moderate_nationalist_opposition | 0.20 | trigger_backlash | İYİ defined itself against him. |
| pious_disillusioned_islamist | 0.30 | reinforce_existing_belief | Religion-nation overlap but state-centric distance. |
| young_urban_protest_voter | 0.10 | trigger_backlash | Anti-youth-protest record. |
| earthquake_zone_loyalist | 0.30 | ignored | Low local resonance. |
| retired_protest_voter | 0.35 | reinforce_existing_belief | Nationalist retirees retain affinity. |
| cosmopolitan_liberal_urban_professional | 0.04 | trigger_backlash | Maximally rejected. |

### 3.5 Akşener × archetypes (apply 0.30 multiplier post 2024-03-31)

| Archetype | credibility | likely_effect | explanation |
|---|---|---|---|
| devout_anatolian_loyalist | 0.32 | ignored | Cultural fluency (yemeni) softens; Kemalist frame caps. |
| secular_urban_professional | 0.70 | mobilize_base | EU-supportive Kemalist coalition. |
| conservative_economically_disillusioned | 0.50 | persuade | Economic populism; partial AKP defection target. |
| alevi_chp_loyalist | 0.40 | reinforce_existing_belief | Coalition-via-CHP affinity; identity distance. |
| kurdish_political_voter | 0.10 | trigger_backlash | 1990s Interior Ministry record; refugee rhetoric. |
| nationalist_grey_wolf_core | 0.45 | persuade | Recaptured ~10% from MHP in 2018, 2023 cycles. |
| moderate_nationalist_opposition | 0.78 | mobilize_base | Core electoral mandate. |
| pious_disillusioned_islamist | 0.30 | ignored | Limited religious register. |
| young_urban_protest_voter | 0.48 | persuade | Exam/education grievances; declining force post-2022. |
| earthquake_zone_loyalist | 0.40 | persuade | Accountability frame heard partially. |
| retired_protest_voter | 0.55 | persuade | Nationalist-secular retirees reachable. |
| cosmopolitan_liberal_urban_professional | 0.50 | persuade | Pro-EU + secular but nationalist register caps it. |

### 3.6 KurdishMovementAgent × archetypes (period-modulated)

Period multipliers (apply to each cell):

- HDP phase (P1–P4 up to 2023-08-27): baseline.
- YSP phase (electoral, Mar 2023 – Oct 2023): ×0.85 on `kurdish_political_voter` recognition (new brand effect); ×1.05 on cross-camp reach (Green Left socialist coalition).
- HEDEP phase (Oct 2023 – Dec 2023): ×0.80 on recognition (forced rename uncertainty).
- DEM phase (from Dec 2023): ×0.95 recognition, ×1.10 mobilization (Third Way).

| Archetype | credibility | likely_effect | explanation |
|---|---|---|---|
| devout_anatolian_loyalist | 0.05 | trigger_backlash | Nationalist counter-mobilization. |
| secular_urban_professional | 0.45 | persuade | Cross-camp reach via Demirtaş + Önder + Beştaş. |
| conservative_economically_disillusioned | 0.15 | ignored | Identity barrier dominates. |
| alevi_chp_loyalist | 0.45 | persuade | Hatay/Adana Arab-Alevi reach via Hatimoğulları. |
| kurdish_political_voter | 0.88 | mobilize_base | Movement-base affinity; near-ceiling. |
| nationalist_grey_wolf_core | 0.02 | trigger_backlash | Maximum backlash channel. |
| moderate_nationalist_opposition | 0.10 | trigger_backlash | İYİ explicitly defines itself against. |
| pious_disillusioned_islamist | 0.25 | persuade | Some pious Kurds reachable via legal-rights frame. |
| young_urban_protest_voter | 0.55 | mobilize_base | Demirtaş + feminist-ecological register. |
| earthquake_zone_loyalist | 0.35 | persuade | Hatay quake region overlaps Hatimoğulları base. |
| retired_protest_voter | 0.30 | reinforce_existing_belief | Pension salience low; democratic-rights frame heard. |
| cosmopolitan_liberal_urban_professional | 0.65 | persuade | Democratic-rights + international-rights audience. |

### 3.7 Demirtaş × archetypes (locked symbolic — operates only when invoked by movement)

| Archetype | credibility | likely_effect | explanation |
|---|---|---|---|
| devout_anatolian_loyalist | 0.10 | trigger_backlash | "Terrorist" counter-frame. |
| secular_urban_professional | 0.60 | persuade | Cross-camp legitimacy; rights symbol. |
| conservative_economically_disillusioned | 0.20 | ignored | Identity barrier. |
| alevi_chp_loyalist | 0.65 | persuade | Strong democratic-rights resonance. |
| kurdish_political_voter | 0.95 | mobilize_base | Highest credibility figure of the movement. |
| nationalist_grey_wolf_core | 0.02 | trigger_backlash | Strongest backlash target. |
| moderate_nationalist_opposition | 0.15 | trigger_backlash | İYİ rejection. |
| pious_disillusioned_islamist | 0.30 | persuade | Pious Kurds + some young pious reachable. |
| young_urban_protest_voter | 0.75 | mobilize_base | Generational symbol. |
| earthquake_zone_loyalist | 0.35 | persuade | Limited local resonance. |
| retired_protest_voter | 0.35 | persuade | Saturday Mothers / rights generation. |
| cosmopolitan_liberal_urban_professional | 0.80 | mobilize_base | International rights symbol. |

### 3.8 Other internal personas — credibility deltas

Internal personas inherit the KurdishMovementAgent credibility row and modify selected cells when invoked. Deltas (applied to movement-level cell, capped at [0,1]):

- `buldan_pervin`: +0.05 women_voters where applicable; +0.05 cosmopolitan_liberal_urban_professional.
- `sancar_mithat`: +0.10 cosmopolitan_liberal_urban_professional; +0.05 secular_urban_professional (legalistic register).
- `onder_sirri_sureyya`: +0.10 secular_urban_professional; +0.05 young_urban_protest_voter (Gezi-generation Istanbul reach); +0.05 cosmopolitan.
- `hatimogullari_tulay`: +0.10 alevi_chp_loyalist (Hatay Arab-Alevi); +0.05 kurdish_political_voter.
- `bakirhan_tuncer`: +0.05 kurdish_political_voter (DEHAP-to-DEM continuity).
- `bestas_meral_danis`: +0.05 cosmopolitan_liberal_urban_professional (legal register); +0.05 secular_urban_professional.
- `turk_ahmet`: -0.05 young_urban_protest_voter (perceived accommodationist); +0.10 retired_protest_voter (elder statesman); +0.05 devout_anatolian_loyalist (dialogue posture).
- `zeydan_abdullah`: +0.07 kurdish_political_voter; +0.05 cosmopolitan_liberal_urban_professional (post-Van mandate defence).
- `kisanak_gultan` (P6 only): +0.05 cosmopolitan; +0.07 young_urban_protest_voter (feminist symbol).

---

## Output 4 — Event-Specific Behavior Matrix

17 events × active agents. For each pair: `does_agent_broadcast`, `message_frame` (paraphrased), `emotional_tone`, `target_voter_groups`, `expected_positive_effect`, `expected_backlash`, `vote_shift_direction`, `movement_state_effect`, `confidence_level`.

Confidence: `low` = primarily INTERP / SIM-ASSUME, `medium` = supported by source profile interpretation, `high` = directly sourced.

### Event 1 — 2019 Istanbul local election (Mar 31, 2019)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Istanbul's transformation continues with us; opposition will return Istanbul to "dark days". | combative, nationalist | devout_anatolian_loyalist, conservative_economically_disillusioned | mobilize base | secular + young trigger | toward AKP | n/a | high |
| kilicdaroglu_kemal | true | Anti-corruption + service delivery alternative; opposition unity proves itself in city races. | hopeful, conciliatory | secular_urban_professional, alevi_chp_loyalist, retired_protest_voter | mobilize CHP base | mild AKP backlash | toward CHP | n/a | high |
| imamoglu_ekrem | true | "Everything will be very nice"; competent + inclusive mayoral candidacy bridging cultural divisions. | hopeful, conciliatory | secular_urban_professional, young_urban_protest_voter, kurdish_political_voter (Istanbul), conservative_economically_disillusioned | persuade across camps | AKP fear-mobilisation | toward CHP | n/a | high |
| bahceli_devlet | true | Vote AKP-MHP alliance to defeat terror-supporting opposition. | combative, nationalist | nationalist_grey_wolf_core | mobilize ülkücü | trigger backlash among Kurdish + secular | toward AKP-MHP | n/a | high |
| aksener_meral | true | "Winter is coming" for the AKP — alliance via non-candidacy in metros to stop one-man rule. | combative, hopeful | moderate_nationalist_opposition, secular_urban_professional | mobilize İYİ base + allow CHP win | mild nationalist defection risk | toward Nation Alliance | n/a | high |
| kurdish_movement_agent (HDP) | true | No HDP candidate in 7 metros — the vote that hurts AKP-MHP is the vote that defends democracy. | mobilizing | kurdish_political_voter (esp. Istanbul/Ankara diaspora), cosmopolitan_liberal_urban_professional | secures CHP wins; mobilizes Kurdish western diaspora | AKP "PKK-CHP collusion" frame | toward Nation Alliance metros, toward HDP southeast | strategy_state=hybrid; strategic_voting_signal=explicit | high |
| demirtas_selahattin (invoked) | true | From prison: vote that ends authoritarianism is the vote for peace. | hopeful, defiant | kurdish_political_voter, young_urban_protest_voter, cosmopolitan | locks tactical CHP vote | nationalist counter | toward Nation Alliance | n/a | medium |
| buldan_pervin | true | Non-candidacy in 7 metros is a political act of choosing where the vote ends authoritarianism. | conciliatory, mobilizing | kurdish_political_voter, secular_urban_professional | legitimises strategic vote | internal critique re: lost leverage | toward Nation Alliance | n/a | high |
| onder_sirri_sureyya | false (recently released; medium influence) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | medium |
| turk_ahmet | true | Mardin co-mayor candidacy — six-decade movement returns to local governance. | conciliatory, identity | kurdish_political_voter (Mardin) | wins Mardin 56% | trustee-removal vulnerability | toward HDP southeast | n/a | high |

### Event 2 — 2019 Istanbul rerun (Jun 23, 2019)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Procedural integrity required; "whoever wins Istanbul wins Turkey" reframed as patriotic vigilance. | combative, defensive | devout_anatolian_loyalist, nationalist_grey_wolf_core | base mobilisation | mass backlash from secular + Kurdish + youth | net toward CHP (backfire) | n/a | high |
| kilicdaroglu_kemal | true | Democratic mandate must be respected; this rerun is itself a referendum on the rule of law. | conciliatory, hopeful | secular_urban_professional, retired_protest_voter, cosmopolitan | mobilize anti-AKP coalition | mild | toward CHP | n/a | high |
| imamoglu_ekrem | true | Radical Love: inclusion of all Istanbul, refusal of polarisation, focus on service. | hopeful, conciliatory | all opposition + soft AKP voters; KONDA showed ~4% AKP switch | 775k vote margin | AKP fear-mobilisation | toward CHP | n/a | high |
| bahceli_devlet | true | Endorse AKP candidate; defend national unity against opposition collusion with PKK. | combative, nationalist | nationalist_grey_wolf_core | partial base hold | nationalist defections to İmamoğlu (KONDA ~50% of MHP voters switched) | toward CHP (backfire) | n/a | high |
| aksener_meral | true | "Winter is coming" — call all democrats to defend the ballot. | combative, hopeful | moderate_nationalist_opposition | İYİ nationalist support for İmamoğlu | nationalist defections | toward CHP | n/a | high |
| kurdish_movement_agent (HDP) | true | Defend the vote; the rerun is a test of whether elections still mean anything. | mobilizing | kurdish_political_voter (Istanbul) | locks Istanbul Kurdish vote behind İmamoğlu | nationalist counter | toward CHP | strategy_state=hybrid; strategic_voting_signal=explicit | high |
| demirtas_selahattin (invoked) | true | Choice is between continued one-man rule and a democratic restart. | hopeful, defiant | kurdish_political_voter, cosmopolitan | reinforces Kurdish CHP vote | nationalist counter | toward CHP | n/a | medium |
| buldan_pervin | true | Strategic non-candidacy was correct; defend the result. | conciliatory | kurdish_political_voter, cosmopolitan | reinforces strategic vote | n/a | toward CHP | n/a | high |

### Event 3 — 2019 trustee/kayyum appointments (Aug 19, 2019)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Trustees protect citizens from terror-linked municipalities — security overrides ballot. | combative, security | devout_anatolian_loyalist, nationalist_grey_wolf_core | base mobilisation | secular + Kurdish + cosmopolitan trigger | toward AKP-MHP | n/a | high |
| kilicdaroglu_kemal | true | Removing elected mayors is not security policy — it is democratic regression. | hopeful, defensive | secular_urban_professional, cosmopolitan, kurdish_political_voter | cross-camp solidarity signal | nationalist counter | toward CHP | n/a | medium |
| imamoglu_ekrem | true | The ballot must mean what it says; Istanbul stands in solidarity with cities whose mandates are cancelled. | conciliatory | secular_urban_professional, kurdish_political_voter | strengthens cross-camp coalition | nationalist counter | toward CHP | n/a | medium |
| bahceli_devlet | true | Trustees are correct because the elected officials served terror networks. | combative, nationalist | nationalist_grey_wolf_core | base reinforcement | maximum backlash from Kurdish + cosmopolitan | toward AKP-MHP | n/a | high |
| aksener_meral | true | The principle of the ballot must be defended even where one disagrees with the result. | conciliatory, defensive | moderate_nationalist_opposition | partial cross-camp credibility | nationalist defection risk | mixed | n/a | medium |
| kurdish_movement_agent (HDP) | true | Mass coordinated state operation, not three independent decisions; 418 detained across 29 provinces; defend the ballot. | mobilizing, defensive | kurdish_political_voter, cosmopolitan, secular_urban_professional | raises anti-trustee salience | nationalist backlash | n/a (off-cycle) | trustee_kayyum_salience=high; democratic_rights_salience=high | high |
| turk_ahmet | true | Voters chose me as Mardin's mayor; the President had other plans — is the ballot still the ballot? (Washington Post op-ed) | conciliatory, defiant | international audience, kurdish_political_voter (cross-gen) | internationalises kayyum critique | nationalist backlash | n/a | trustee_kayyum_salience→HIGH | high |
| buldan_pervin | true | Trustees do not erase mandates — the movement continues under any banner. | conciliatory, mobilizing | kurdish_political_voter | base hold | nationalist counter | n/a | institutional_continuity_signal=high | high |
| bakirhan_tuncer | true | Drawing on Siirt experience: kayyum is economic-political punishment, not security policy. | defensive | kurdish_political_voter (provincial) | anti-trustee salience | n/a | n/a | n/a | medium |

### Event 4 — COVID period (Mar 2020 – mid-2022)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Turkey's expert-led response is competent; opposition mayors and the medical association are politicising the crisis. | technocratic + combative | devout_anatolian_loyalist, conservative_economically_disillusioned | base hold | secular + young trigger; underreporting controversy | mild toward AKP early; erosion later | n/a | high |
| kilicdaroglu_kemal | true | Government transparency failure; CHP municipalities deliver. | conciliatory, technocratic | secular_urban_professional, alevi_chp_loyalist | base mobilisation | mild | toward CHP | n/a | medium |
| imamoglu_ekrem | true | Istanbul's parallel data + needs-cards solidarity show competent local governance. | technocratic, hopeful | all opposition + soft AKP defectors | high cross-camp credibility | central-govt counter-attack on donations | toward CHP | n/a | high |
| bahceli_devlet | true | Defend state authority; opposition mayors overstep their lane. | combative, security | nationalist_grey_wolf_core | base hold | n/a | none | n/a | medium |
| aksener_meral | true | Field-visit politics — market visits, local pressure on central government failure. | combative, hopeful | moderate_nationalist_opposition, secular_urban_professional | partial mobilisation | mild | toward İYİ | n/a | medium |
| kurdish_movement_agent (HDP) | true | COVID + loss of municipal platforms = double erasure; ECtHR Grand Chamber Dec 2020 = democratic vindication. | defensive | kurdish_political_voter, cosmopolitan | preserves base | mobilisation suppressed | none | strategy_state=strategic-silent-support; voter_mobilization_level=low | high |
| demirtas_selahattin (invoked, Dec 2020) | true | Grand Chamber ruling is a verdict on the state, not me. | defiant, hopeful | kurdish_political_voter, cosmopolitan, secular | raises democratic_rights_salience to HIGH | state-media reframe as foreign interference | none | n/a | high |
| buldan_pervin | true | Anti-kayyum + Demirtaş-release coalition. | defensive | kurdish_political_voter, cosmopolitan | base hold | n/a | none | n/a | medium |

### Event 5 — HDP closure case (Mar 17, 2021 – ongoing)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Constitutional court will determine — the AKP respects judicial independence (while implicitly endorsing closure). | nationalist, defensive | devout_anatolian_loyalist, nationalist_grey_wolf_core | base mobilisation | secular + Kurdish backlash | toward AKP-MHP base | n/a | high |
| kilicdaroglu_kemal | true | Party closures are not democratic remedies; HDP is a legitimate parliamentary actor. (Sept 2021 explicit validation) | conciliatory, democratic | secular_urban_professional, cosmopolitan, kurdish_political_voter | builds opposition alliance bridge to HDP | nationalist counter | toward Nation+HDP coalition | n/a | high |
| imamoglu_ekrem | partial (low cadence) | Defends democratic pluralism without becoming primary spokesperson. | conciliatory | secular_urban_professional, cosmopolitan | mild positive signal | mild AKP counter | none | n/a | medium |
| bahceli_devlet | true | HDP must be closed — it is the political wing of terror. | combative, nationalist | nationalist_grey_wolf_core | mobilizes base | maximum Kurdish + cosmopolitan backlash | toward MHP base | n/a | high |
| aksener_meral | true | Party closures via court are wrong in principle, but HDP must distance itself from terror. | conditional, nationalist | moderate_nationalist_opposition | mixed | Kurdish backlash | mild toward İYİ | n/a | medium |
| kurdish_movement_agent (HDP) | true | The case is fundamentally political, not legal — defence is for the historical archive. | legalistic, defiant | kurdish_political_voter, cosmopolitan, secular | preserves base + raises international salience | nationalist counter | none | closure_risk_level=critical; party_transition_state=preparing | high |
| sancar_mithat | true | The indictment fails Venice Commission standards. | technocratic, legalistic | cosmopolitan, legal/academic | sustains legitimacy | state-media dismissal | none | n/a | high |
| buldan_pervin | true | The movement existed before its acronyms and will exist after them. | conciliatory, defiant | kurdish_political_voter | lowers rebrand anxiety | state-media seizes on "continuity with closed parties" | none | institutional_continuity_signal=high | high |
| bestas_meral_danis | true | The 843-page indictment is a political case; defense is constitutional theatre on the record. | technocratic, defiant | cosmopolitan, kurdish_political_voter | stabilises voter confidence | n/a | none | n/a | high |

### Event 6 — 2021–2022 lira / inflation crisis

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Economic war of independence; "interest rate lobby" attacks Turkey; trust the lira. | combative, populist, nationalist | devout_anatolian_loyalist, working_class welfare recipients | base hold via blame-shift | secular + young + cosmopolitan trigger; conservative_economically_disillusioned erosion | erosion among economically disillusioned | n/a | high |
| kilicdaroglu_kemal | true | Kitchen-table economics videos — inflation as lived experience; orthodox policy needed. | hopeful, populist (economic) | conservative_economically_disillusioned, secular, alevi, retired | persuasion among undecideds | "doesn't sound like a leader" critique | toward CHP | n/a | high |
| imamoglu_ekrem | true | Istanbul service delivery offsets central-government economic failure; concrete cost-of-living interventions. | technocratic, populist | conservative_economically_disillusioned, secular, retired | high credibility on competence | central counterattack | toward CHP | n/a | high |
| bahceli_devlet | true | Defend national economic sovereignty; reject IMF / orthodox prescriptions. | nationalist, defensive | nationalist_grey_wolf_core | base hold | economic_disillusioned defection | mild toward AKP-MHP base; net erosion | n/a | medium |
| aksener_meral | true | The lira crisis is the bill for one-man rule. | combative, populist | moderate_nationalist_opposition, conservative_economically_disillusioned | partial persuasion | nationalist defection (refugee pivot ahead) | toward İYİ | n/a | high |
| kurdish_movement_agent (HDP) | true | Economic crisis layered onto democratic crisis — both have one cause. | defiant, legalistic | kurdish_political_voter, cosmopolitan | base hold | secondary salience vs closure | none | strategy_state=hybrid | medium |

### Event 7 — Refugee debate (escalating 2021–2023)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Voluntary and honourable return after 2022 pivot; opposition's deportation rhetoric is un-Islamic cruelty. | populist, religious | devout_anatolian_loyalist, refugee-skeptical conservative | retains base | hardliner defection to YRP/Zafer | mild erosion to YRP | n/a | high |
| kilicdaroglu_kemal | true | Pre-runoff: orderly return within 2 years (runoff pivot intensified anti-refugee tone). | combative (runoff), defensive | nationalist swing voters | nationalist persuasion attempt | Kurdish + cosmopolitan + alevi dissonance | mixed | n/a | high |
| imamoglu_ekrem | true | Pragmatic urban management; rejects scapegoating. | conciliatory, technocratic | cosmopolitan, secular, conservative_econ_disill | preserves cross-camp credibility | refugee-skeptical defection risk | mild toward İmamoğlu among urban | n/a | medium |
| bahceli_devlet | true | Refugees must be controlled; nationalist sovereignty paramount. | nationalist | nationalist_grey_wolf_core | base hold | mild | mild toward MHP-aligned | n/a | medium |
| aksener_meral | true | All refugees must return; sharp anti-refugee programme. | combative, nationalist, populist | moderate_nationalist_opposition, refugee-skeptical secular | mobilises İYİ base | kurdish + cosmopolitan + alevi trigger | toward İYİ + Zafer drain | n/a | high |
| kurdish_movement_agent | true | Rejects scapegoating; refugee question is rights question; condemns Özdağ Protocol. | defiant | kurdish_political_voter, cosmopolitan | preserves base distinction | nationalist counter | none | nationalist_backlash_risk=high (P4) | high |

### Event 8 — 2023 Kahramanmaraş earthquakes (Feb 6, 2023)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | "Not possible to be ready for a disaster like this"; God-given; rebuild quickly; critics are dishonorable. | defensive, religious, combative | devout_anatolian_loyalist, earthquake_zone_loyalist | retains 8 of 11 quake provinces in May 2023 | mass urban + young + cosmopolitan trigger | partial defence in quake region; net negative urban | n/a | high |
| kilicdaroglu_kemal | true | Government accountability; structural critique; CHP municipalities respond effectively. | combative (rare), defensive | secular_urban_professional, alevi, retired, cosmopolitan | base mobilisation | mild | toward CHP | n/a | high |
| imamoglu_ekrem | true | İBB rescue teams deployed quickly; transparency on aid; visible field presence. | technocratic, hopeful | all opposition + soft AKP | high credibility | central counter-attack on aid coordination | toward CHP | n/a | high |
| bahceli_devlet | true | National unity around the state; security-discipline framing. | nationalist | nationalist_grey_wolf_core | base hold | n/a | none | n/a | low |
| aksener_meral | true | Accountability; condemnation of building-amnesty laws. | combative | moderate_nationalist_opposition, secular | base mobilisation | n/a | toward İYİ | n/a | medium |
| kurdish_movement_agent | true | Hatay/Adana victims include Arab-Alevi communities; rights-based reconstruction; trustee municipalities cannot deliver. | defensive, mobilizing | kurdish_political_voter (region), alevi, cosmopolitan | regional credibility | nationalist counter | none | trustee_kayyum_salience=high | medium |
| hatimogullari_tulay (pre-leadership) | true | Hatay Arab-Alevi victims need rights-based response; AFAD-government accountability. | defensive | alevi_chp_loyalist (regional), kurdish_political_voter | regional credibility | n/a | mild positive for opposition | n/a | medium |

### Event 9 — 2023 presidential election first round (May 14, 2023)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Native and national; opposition is PKK-FETÖ-Western collusion; civilisational defence. | combative, nationalist, populist | devout_anatolian_loyalist, nationalist_grey_wolf_core, diaspora | 49.52% R1 | secular + young + Kurdish + cosmopolitan trigger | toward AKP | n/a | high |
| kilicdaroglu_kemal | true | Helalleşme; rule of law; "Bay Kemal" relatable figure; coalition of six + HDP/YSP. | hopeful, conciliatory | secular, alevi, kurdish, retired, young, cosmopolitan | 44.88% R1 | nationalist counter | toward Nation Alliance | n/a | high |
| imamoglu_ekrem | true | Supporting figure for Kılıçdaroğlu; mobilises Istanbul + young + cross-camp. | hopeful, conciliatory | cosmopolitan, young_urban_protest_voter, secular | base mobilisation | mild | toward Nation Alliance | n/a | high |
| bahceli_devlet | true | Nationalist defence of the state; MHP holds at 10.1%. | nationalist | nationalist_grey_wolf_core | base hold | n/a | toward AKP-MHP | n/a | high |
| aksener_meral | true | Backs Kılıçdaroğlu within Table of Six; nationalist legitimisation. | combative, hopeful | moderate_nationalist_opposition | İYİ ~10% | mild | toward Nation Alliance | n/a | high |
| kurdish_movement_agent (HDP→YSP) | true | End the one-man regime; YSP electoral switch is prophylactic, identity continuous. | mobilizing | kurdish_political_voter | YSP 8.82% / 61 seats; 60-75% for Kılıçdaroğlu in Kurdish provinces | nationalist counter | toward Nation Alliance | strategy_state=full-alliance; party_transition_state=transitioning | high |
| demirtas_selahattin (invoked) | true | Choice is between continued one-man rule and democratic restart; stay with Kılıçdaroğlu. | defiant, hopeful | kurdish_political_voter, cosmopolitan, young | locks Kurdish R1 turnout | nationalist counter | toward Nation Alliance | n/a | high |
| buldan_pervin / sancar_mithat | true | Joint endorsement of Kılıçdaroğlu; YSP coalition with Labour and Freedom Alliance. | mobilizing | kurdish_political_voter | base hold | n/a | toward Nation Alliance | n/a | high |
| onder_sirri_sureyya | true | Bridge figure: Istanbul + Kurdish + parliamentary peace-process horizon. | hopeful | cosmopolitan, secular, kurdish | mobilizes urban Kurdish + Gezi-generation | nationalist counter | toward Nation Alliance | n/a | medium |

### Event 10 — 2023 presidential runoff (May 28, 2023)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Doubles down on PKK-collusion + refugee-management; Sinan Oğan endorsement consolidates nationalists. | combative, nationalist | nationalist_grey_wolf_core, devout, diaspora | 52.18% win | secular + Kurdish trigger | toward AKP | n/a | high |
| kilicdaroglu_kemal | true | Combative pivot — anti-refugee, anti-foreign-meddling; nationalist register. (Özdağ Protocol May 18) | combative, nationalist (runoff) | nationalist swing voters | partial nationalist persuasion | Kurdish + cosmopolitan + alevi demobilisation (-4 to -6% Kurdish R2 turnout) | net inadequate | n/a | high |
| imamoglu_ekrem | true | Continues to back Kılıçdaroğlu publicly; quietly distances from refugee pivot. | hopeful, conciliatory | cosmopolitan, secular, kurdish | preserves own brand | n/a | toward Nation Alliance | n/a | medium |
| bahceli_devlet | true | Endorse Erdoğan; mobilise nationalist runoff turnout. | combative, nationalist | nationalist_grey_wolf_core | base mobilisation | n/a | toward AKP-MHP | n/a | high |
| aksener_meral | true | Endorse Kılıçdaroğlu R2; nationalist register against Erdoğan. | combative, nationalist | moderate_nationalist_opposition | İYİ R2 hold | mild | toward Nation Alliance | n/a | high |
| kurdish_movement_agent (YSP) | true | Stay with Kılıçdaroğlu R2 despite Özdağ Protocol — name the betrayal openly but defend democracy. | defiant, mobilizing | kurdish_political_voter | limits Kurdish R2 turnout drop to ~4-6% | soft boycott pressure within base | mostly toward Nation Alliance | strategy_state=full-alliance; nationalist_backlash_risk=high; trustee_kayyum_salience=high | high |
| demirtas_selahattin (invoked) | true | Endorses Kılıçdaroğlu R2 from prison; names the Özdağ Protocol problem explicitly. | defiant, conciliatory | kurdish_political_voter, cosmopolitan, young | limits R2 turnout drop | base reads endorsement as capitulation (contested) | toward Nation Alliance with leakage | n/a | high |
| buldan_pervin | true | Hold the line; the choice is still between one-man rule and democracy. | mobilizing | kurdish_political_voter | base hold | leakage | toward Nation Alliance | n/a | high |

### Event 11 — CHP leadership transition (Nov 2023)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Opposition internal chaos signals AKP stability. | combative | devout, nationalist | base reinforcement | mild | mild toward AKP | n/a | medium |
| kilicdaroglu_kemal | true (degraded post-Nov) | Continuity over confrontation; defends record but loses chair to Özgür Özel. | defensive | secular_urban_professional, alevi, retired | partial base retention | factional damage | mild toward CHP renewal | n/a | high |
| imamoglu_ekrem | true | Renewal of opposition leadership; municipal-success generation rises. | hopeful | secular, young, cross-camp | mobilises CHP renewal | factional tension | toward CHP renewal | n/a | high |
| bahceli_devlet | false | n/a (no MHP broadcast on internal CHP race). | n/a | n/a | n/a | n/a | none | n/a | medium |
| aksener_meral | partial | Comments on opposition cohesion; tensions with new CHP leadership begin. | combative | moderate_nationalist_opposition | partial | İYİ–CHP friction | mild negative for opposition cohesion | n/a | medium |
| kurdish_movement_agent | false | Movement focused on HEDEP→DEM transition; not primary actor in CHP race. | n/a | n/a | n/a | n/a | none | n/a | high |

### Event 12 — HDP/YSP transition for 2023 election (Mar 24, 2023)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | YSP is HDP under a new name — the closure case must proceed. | combative, security | devout, nationalist | base hold | secular + kurdish trigger | toward AKP-MHP | n/a | high |
| kilicdaroglu_kemal | true | Welcomes YSP into the Labour and Freedom Alliance; coalition formalises. | conciliatory | secular, kurdish, cosmopolitan | mobilises broad coalition | nationalist counter | toward Nation Alliance | n/a | high |
| bahceli_devlet | true | YSP is HDP's mask; closure case must continue. | combative, nationalist | nationalist_grey_wolf_core | base hold | n/a | toward MHP | n/a | high |
| aksener_meral | true | İYİ does not formally coordinate with YSP; tactical neutrality on closure case. | nationalist, defensive | moderate_nationalist_opposition | preserves İYİ identity | Kurdish trigger | none | n/a | medium |
| kurdish_movement_agent | true | YSP is the electoral vehicle; HDP retained as legal shell; identity continuous. | legalistic, mobilizing | kurdish_political_voter, cosmopolitan, secular | electoral viability preserved | nationalist counter | toward YSP | party_transition_state=transitioning; current_party_label=HDP (institutional) / YSP (electoral) | high |
| buldan_pervin / sancar_mithat | true | YSP transition is institutional continuity, not surrender. | conciliatory | kurdish_political_voter | base hold | n/a | toward YSP | n/a | high |
| bestas_meral_danis | true | HDP defence continues legally; YSP is the campaign vehicle. | technocratic | cosmopolitan, kurdish, secular | preserves base | n/a | toward YSP | n/a | high |

### Event 13 — HDP suspends activity / transfers center to YSP (Aug 27, 2023)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | partial | Treats the rebrand as confirmation that the original was illegitimate. | combative | devout, nationalist | base reinforcement | secular + Kurdish trigger | mild toward AKP-MHP | n/a | medium |
| kilicdaroglu_kemal | false | Post-2023 loss; CHP leadership crisis takes priority. | n/a | n/a | n/a | n/a | none | n/a | medium |
| bahceli_devlet | true | Closure must still proceed regardless of rebrand. | combative, nationalist | nationalist_grey_wolf_core | base hold | n/a | toward MHP | n/a | medium |
| aksener_meral | partial | Tactical neutrality; İYİ's own internal dynamics intensify. | n/a | n/a | n/a | n/a | none | n/a | medium |
| kurdish_movement_agent | true | HDP suspended at 4th Extraordinary Congress; Özcan/Kırkazak preserve legal shell; YSP is the operative center. Buldan announces July 1 strategy of own metro candidates in 2024. | legalistic, mobilizing | kurdish_political_voter, cosmopolitan | brand-discontinuity managed; Third Way doctrine activated | internal critique | toward YSP/DEM | party_transition_state=just-completed; strategy_state=independent-run (announced); institutional_continuity_signal=high | high |
| buldan_pervin | true | Steps down at Aug 27 congress; strategic announcement is the legacy. | conciliatory, mobilizing | kurdish_political_voter | base hold + new strategy lock | n/a | toward independent-run | n/a | high |
| sancar_mithat | true | Steps down; institutional continuity through transition. | conciliatory | kurdish_political_voter, cosmopolitan | base hold | n/a | toward independent-run | n/a | high |

### Event 14 — YSP → HEDEP → DEM transition (Oct 15, 2023 / Dec 11, 2023)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Forced acronym change is judicial discipline; opposition fragmenting. | combative | devout, nationalist | base hold | secular + Kurdish trigger | toward AKP-MHP | n/a | medium |
| kilicdaroglu_kemal | false (degraded) | n/a | n/a | n/a | n/a | n/a | none | n/a | high |
| bahceli_devlet | true | Rebrand does not change the substance; closure still warranted. | combative, nationalist | nationalist_grey_wolf_core | base hold | n/a | toward MHP | n/a | medium |
| aksener_meral | false | Internal İYİ campaign preparation dominates. | n/a | n/a | n/a | n/a | none | n/a | medium |
| kurdish_movement_agent | true | HEDEP congress Oct 15: Third Way doctrine, Öcalan-release demand, Kurdish-Palestinian solidarity; DEM brand finalised Dec 11. | symbolic, mobilizing | kurdish_political_voter, cosmopolitan | brand viability; pre-2024 mobilisation primer | nationalist counter; small "vote-splitting" concern from CHP-aligned commentators | toward DEM | current_party_label=HEDEP→DEM; strategy_state=independent-run; institutional_leadership=Hatimoğulları/Bakırhan | high |
| hatimogullari_tulay | true | Third Way: no subordination of identity to alliance arithmetic; mandate recovery non-negotiable. | mobilizing, defiant | kurdish_political_voter, cosmopolitan | locks independent-run strategy | CHP-aligned vote-splitting frame | toward DEM | faction=weaken_AKP active | high |
| bakirhan_tuncel | true | Operational renewal grounded in lived trustee experience. | mobilizing | kurdish_political_voter (provincial) | provincial mobilisation primer | n/a | toward DEM | n/a | high |
| turk_ahmet | true | Dialogue-faction commentary: dialogue with the state remains the path. | conciliatory | kurdish_political_voter (elder), international | stabilises dialogue-faction | younger base reads as accommodationist | mild | faction=dialogue_first active | medium |

### Event 15 — 2024 local election campaign (Jan – Mar 2024)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Local government is extension of national policy; opposition municipalities serve foreign interests. | combative, nationalist | devout, nationalist_grey_wolf_core | partial base hold | secular + young + earthquake_zone trigger | toward AKP base; insufficient | n/a | high |
| kilicdaroglu_kemal (degraded) | partial | Background CHP elder; limited mobilisation; effectively passes baton to İmamoğlu/Yavaş/Özel. | defensive | secular, alevi (residual) | minor base hold | factional drag | mild toward CHP renewal | n/a | high (degraded) |
| imamoglu_ekrem | true | Track record + Radical Love + service delivery; speaks to AKP defectors directly. | hopeful, conciliatory, populist | secular, young, conservative_econ_disill, alevi, kurdish, cosmopolitan | 51.14% reelection landslide | AKP fear-mobilisation | toward CHP | n/a | high |
| bahceli_devlet | true | Defend the alliance; nationalist discipline. | combative, nationalist | nationalist_grey_wolf_core | partial base hold | n/a | mild toward MHP base; net erosion in MHP | n/a | high |
| aksener_meral | true | Solo strategy — İYİ contests independently. | combative, nationalist | moderate_nationalist_opposition | İYİ identity preserved | catastrophic mobilisation loss; vote share halves | net negative for İYİ | n/a | high |
| kurdish_movement_agent (DEM) | true | "Free cities + local democracy"; resounding response to the trustee regime; mandate recovery campaign. | mobilizing | kurdish_political_voter, cosmopolitan, alevi (Hatay) | recovers 10 provincial capitals; 78 municipalities | nationalist counter; soft internal boycott concern | toward DEM independently | strategy_state=independent-run; voter_mobilization_level=high; trustee_kayyum_salience=high | high |
| hatimogullari_tulay | true | Free cities; refuse to trade mandates for alliance arithmetic. | mobilizing, defiant | kurdish_political_voter | mobilises southeast | CHP-aligned vote-splitting frame | toward DEM | n/a | high |
| bakirhan_tuncel | true | Concrete local-democracy programme; restore services + councils. | mobilizing | kurdish_political_voter (provincial) | 10/10 provincial capital recovery | n/a | toward DEM | n/a | high |
| bestas_meral_danis | true | Accepts DEM Istanbul co-candidacy Feb 9 — identity assertion, not arithmetic. | conciliatory | kurdish_political_voter (Istanbul), cosmopolitan, women | 2.12% Istanbul vote (by design) | CHP-aligned vote-splitting frame | toward DEM identity-preservation | n/a | high |
| kisanak_gultan (P6 only) | true | Symbolic Ankara candidacy from prison — continued imprisonment is the political content. | defiant | kurdish women, cosmopolitan, international | maximises legal_pressure_symbol salience (Le Monde etc.) | nationalist counter | n/a | n/a | high |
| zeydan_abdullah | true | Van: reverse 2019 trustee, restore municipal services. | mobilizing | kurdish_political_voter (Van) | 55.48% landslide | pre-election Justice Ministry letter | toward DEM Van | n/a | high |
| turk_ahmet | partial | Declines to run again Jan 2024; dialogue-faction commentary continues. | conciliatory | kurdish_political_voter (elder) | factional balance | n/a | mild | n/a | high |
| onder_sirri_sureyya | true | Bridge figure for Istanbul Kurdish + Gezi-generation; peace-process horizon. | hopeful | cosmopolitan, young, kurdish | partial Istanbul mobilisation | nationalist counter | toward DEM | n/a | medium |

### Event 16 — 2024 local election result (Mar 31, 2024)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | First defeat since 2002 acknowledged; "we will compensate for our mistakes" — unusually conciliatory balcony speech. | conciliatory (rare), defensive | devout, AKP base | base damage-control | low | net negative for AKP | n/a | high |
| kilicdaroglu_kemal | partial | Background commentary; CHP victory is institutional vindication. | defensive | secular_urban_professional (residual) | mild positive | factional irrelevance | mild positive for CHP | n/a | medium |
| imamoglu_ekrem | true | 51.14% reelection; CHP wins all 5 largest cities + 80% of municipal revenue. | hopeful | all opposition + AKP defectors | maximum cross-camp mobilisation | mild | toward CHP nationally | n/a | high |
| bahceli_devlet | partial | MHP losses; defence of alliance integrity. | nationalist, defensive | nationalist_grey_wolf_core | partial base hold | n/a | mild negative for MHP | n/a | medium |
| aksener_meral | true | İYİ collapse — vote share halved. Begin resignation trajectory. | defensive | İYİ base (declining) | none meaningful | factional revolt | catastrophic for İYİ | apply broadcast_power_multiplier_after_2024_03_31=0.30 | high |
| kurdish_movement_agent (DEM) | true | 10 provincial capitals + 78 municipalities; Third Way validated; trustee-regime answered. | mobilizing | kurdish_political_voter, cosmopolitan | structural victory in southeast | nationalist + AKP retaliation primed | toward DEM | strategy_state=hybrid (post-victory); trustee_kayyum_salience=critical (looming Van crisis) | high |
| hatimogullari_tulay | true | "Resounding response to the trustee regime." | mobilizing | kurdish_political_voter, cosmopolitan | base mobilisation | n/a | toward DEM | n/a | high |
| zeydan_abdullah | true | Van mandate is the voters'; defend it. | mobilizing | kurdish_political_voter (Van) | 55.48% lock | Justice Ministry letter (Mar 29) primes contestation | toward DEM Van | n/a | high |

### Event 17 — Van / Abdullah Zeydan mandate crisis (Apr 2–3, 2024)

| Agent | broadcast | message_frame | tone | target | + effect | – effect | vote_shift | movement_state | conf |
|---|---|---|---|---|---|---|---|---|---|
| erdogan_recep_tayyip | true | Protesters are "provocateurs" and "terrorists"; YSK is the lawful arbiter. | combative, security, defensive | devout, nationalist_grey_wolf_core | base mobilisation | mass urban + Kurdish + cosmopolitan + alevi trigger; international censure | net negative for AKP credibility | n/a | high |
| kilicdaroglu_kemal | partial | Background voice; CHP under Özel joins protests. | defensive, conciliatory | secular_urban_professional (residual) | mild positive | factional irrelevance | mild positive for opposition cohesion | n/a | medium |
| imamoglu_ekrem | true | The ballot must mean what it says — Istanbul stands with Van. | conciliatory, defiant | secular, cosmopolitan, kurdish, young | high cross-camp mobilisation | nationalist counter | toward CHP–DEM convergence | n/a | high |
| bahceli_devlet | true | Defend YSK process; protesters challenging the state. | combative, nationalist | nationalist_grey_wolf_core | base hold | n/a | toward MHP | n/a | medium |
| aksener_meral | partial | Defends ballot-principle in principle, but cautious on DEM specifically. | nationalist, defensive | moderate_nationalist_opposition (residual) | mild | mixed | none | n/a | medium |
| kurdish_movement_agent (DEM) | true | "Coup in Van"; mandate belongs to Van's voters; YSK must reverse; defend mandate through legal channels and visible protest. | defensive, mobilizing | kurdish_political_voter, cosmopolitan, alevi, secular, young | YSK 7-4 reversal Apr 3; Zeydan inaugurated | high nationalist_backlash_risk; subsequent kayyum wave (Hakkâri Jun 2024 onward — post-window note) | toward DEM legitimacy | strategy_state=hybrid; legal_pressure_state=critical; trustee_kayyum_salience=critical; mandate_contestation_state=mandate_revoked→protest_triggered→YSK_reversal→mandate_restored | high |
| hatimogullari_tulay | true | The provincial board decision is a coup against the ballot; YSK must uphold electoral law. | defensive, defiant | kurdish_political_voter, cosmopolitan, women | catalyses YSK reversal; mobilisation_strength surges | Erdoğan "provocateurs" label | toward DEM | n/a | high |
| bakirhan_tuncel | true | Joint co-leadership of YSK appeal. | technocratic, defensive | kurdish_political_voter | reinforces legal+protest channels | n/a | toward DEM | n/a | high |
| zeydan_abdullah | true | The mandate belongs to Van's voters; defend it through legal channels and visible protest. | defiant, mobilizing | kurdish_political_voter (Van), cosmopolitan | mass protest mobilisation; YSK reversal | nationalist backlash; future kayyum risk (Feb 2025 — post-window) | toward DEM legitimacy | n/a | high |
| sancar_mithat | true | Provincial board's reversal is a textbook violation of electoral law and a stress test of YSK independence. | technocratic, legalistic | cosmopolitan, secular, international | reinforces legal framing | n/a | toward DEM | n/a | high |
| bestas_meral_danis | true | Legal defence coordination. | technocratic | cosmopolitan, kurdish | reinforces legal framing | n/a | toward DEM | n/a | high |
| onder_sirri_sureyya | true | Institutional defender of the Van mandate; Deputy Speaker leverage. | hopeful, defiant | cosmopolitan, secular, kurdish | parliamentary amplification | nationalist counter | toward DEM | n/a | medium |
| turk_ahmet | true | Dialogue-faction commentary: defend the ballot while preserving peace-process horizon. | conciliatory, defiant | kurdish_political_voter (elder), international | factional balance | younger base reads as soft | toward DEM | n/a | medium |

---

## Output 5 — Kurdish Movement State Machine

State machine for `kurdish_movement_agent`. All numeric values are 0–1 source-grounded simulation calibration parameters (or categorical, where specified).

### Period 1 — `P1_HDP_2019_local_window`

```
period_id: P1_HDP_2019_local_window
start_date: 2019-01-01
end_date: 2019-03-31
current_party_label: HDP
active_leadership: [buldan_pervin, temelli_sezai]   # temelli context_only; not a broadcast agent
symbolic_leader: demirtas_selahattin
symbolic_leader_status: imprisoned (since 2016-11-04; ECtHR Chamber Nov 2018)
legal_pressure_state: high
closure_risk_level: 0.45
trustee_threat_level: 0.85   # 82/102 DBP municipalities under trustees
organizational_capacity: 0.70
voter_recognition: 0.85
strategic_voting_signal: 0.90   # explicit non-candidacy in 7 metros
opposition_alignment_signal: 0.45   # informal
independent_identity_signal: 0.75
boycott_signal: 0.05
nationalist_backlash_risk: 0.55
democratic_rights_salience: 0.85
kurdish_identity_salience: 0.90
peace_process_salience: 0.55
primary_strategy_state: hybrid   # pan-Kurdish east + strategic non-candidacy west
communication_mode: mobilizing
active_internal_personas: [buldan_pervin, demirtas_selahattin_invoked, turk_ahmet]
transition_trigger: end of March 2019 local elections
expected_voter_effect: secures Istanbul/Ankara CHP wins via Kurdish western tactical vote; consolidates Kurdish southeast base under HDP banner.
```

### Period 2 — `P2_HDP_kayyum_covid_ecthr`

```
period_id: P2_HDP_kayyum_covid_ecthr
start_date: 2019-04-01
end_date: 2020-12-31
current_party_label: HDP
active_leadership: [buldan_pervin, sancar_mithat (from 2020-02-23)]
symbolic_leader: demirtas_selahattin
symbolic_leader_status: imprisoned; ECtHR Grand Chamber ruling 2020-12-22 (defied)
legal_pressure_state: high
closure_risk_level: 0.50
trustee_threat_level: 0.95   # 48/65 HDP municipalities seized by Oct 2020
organizational_capacity: 0.45   # municipal platforms lost
voter_recognition: 0.85
strategic_voting_signal: 0.10   # no election
opposition_alignment_signal: 0.35   # informal CHP critique of kayyum
independent_identity_signal: 0.75
boycott_signal: 0.05
nationalist_backlash_risk: 0.50
democratic_rights_salience: 0.90   # ECtHR Grand Chamber
kurdish_identity_salience: 0.65   # COVID suppressed manifestations
peace_process_salience: 0.45
primary_strategy_state: strategic-silent-support
communication_mode: defensive
active_internal_personas: [buldan_pervin, sancar_mithat, bakirhan_tuncer, demirtas_selahattin_invoked, turk_ahmet]
transition_trigger: HDP closure indictment filed 2021-03-17
expected_voter_effect: preserves base but mobilisation suppressed by COVID + municipal-platform loss.
```

### Period 3 — `P3_HDP_closure_alliance`

```
period_id: P3_HDP_closure_alliance
start_date: 2021-03-17
end_date: 2022-12-31
current_party_label: HDP
active_leadership: [buldan_pervin, sancar_mithat]
symbolic_leader: demirtas_selahattin
symbolic_leader_status: imprisoned; remains most-recognised Kurdish figure
legal_pressure_state: critical
closure_risk_level: 0.90
trustee_threat_level: 0.85
organizational_capacity: 0.55
voter_recognition: 0.80
strategic_voting_signal: 0.40   # soft signals toward Kılıçdaroğlu
opposition_alignment_signal: 0.55   # conditional
independent_identity_signal: 0.80
boycott_signal: 0.20   # PKK pressure from Kandil; HDP resisted
nationalist_backlash_risk: 0.75   # Semra Güzel episode
democratic_rights_salience: 0.90
kurdish_identity_salience: 0.85   # 11-article declaration
peace_process_salience: 0.65
primary_strategy_state: hybrid   # Labour and Freedom Alliance + independent identity
communication_mode: legalistic
active_internal_personas: [buldan_pervin, sancar_mithat, bakirhan_tuncer, bestas_meral_danis, turk_ahmet, demirtas_selahattin_invoked]
transition_trigger: AYM rejects HDP delay request 2023-01-26; treasury freeze 2023-01-05; YSP decision Mar 24
expected_voter_effect: institutional-continuity signal stabilises base under existential pressure; soft alliance prep with Nation Alliance.
```

### Period 4 — `P4_YSP_2023_elections`

```
period_id: P4_YSP_2023_elections
start_date: 2023-01-01
end_date: 2023-05-31
current_party_label: HDP (institutional shell) / YSP (electoral)
active_leadership: [buldan_pervin, sancar_mithat]
symbolic_leader: demirtas_selahattin
symbolic_leader_status: imprisoned; publicly endorses Kılıçdaroğlu R2; announces withdrawal from active politics
legal_pressure_state: critical
closure_risk_level: 0.95   # treasury freeze, verbal-defence refusal
trustee_threat_level: 0.80
organizational_capacity: 0.65
voter_recognition: 0.65   # YSP brand new
strategic_voting_signal: 1.00   # explicit Kılıçdaroğlu endorsement
opposition_alignment_signal: 0.90   # formal
independent_identity_signal: 0.50
boycott_signal: 0.05
nationalist_backlash_risk: 0.90   # AKP deepfake; Özdağ Protocol
democratic_rights_salience: 0.90
kurdish_identity_salience: 0.65
peace_process_salience: 0.60
primary_strategy_state: full-alliance
communication_mode: mobilizing
active_internal_personas: [buldan_pervin, sancar_mithat, bestas_meral_danis, kilicgun_ucar_cigdem (transitional), onder_sirri_sureyya (rising), hatimogullari_tulay (background MP), demirtas_selahattin_invoked]
transition_trigger: HDP suspends Aug 27, 2023
expected_voter_effect: 8.82% YSP / 61 seats; 60-75% R1 for Kılıçdaroğlu in Kurdish provinces; -4 to -6% R2 Kurdish turnout drop after Özdağ Protocol.
```

### Period 5 — `P5_HDP_suspend_HEDEP`

```
period_id: P5_HDP_suspend_HEDEP
start_date: 2023-06-01
end_date: 2023-10-15
current_party_label: HDP (suspended Aug 27) → YSP → HEDEP (Oct 15)
active_leadership: [ozcan_sultan, kirkazak_cahit (HDP shell, from Aug 27); hatimogullari_tulay, bakirhan_tuncer (HEDEP, from Oct 15)]
symbolic_leader: demirtas_selahattin
symbolic_leader_status: imprisoned; reduced personal voice after May 2023 withdrawal statement
legal_pressure_state: high
closure_risk_level: 0.55   # HEDEP structurally separate
trustee_threat_level: 0.65
organizational_capacity: 0.55   # rebuild phase
voter_recognition: 0.55   # rebrand confusion
strategic_voting_signal: 0.05
opposition_alignment_signal: 0.40   # conditional; Third Way drift
independent_identity_signal: 0.85
boycott_signal: 0.05
nationalist_backlash_risk: 0.30   # post-election lull
democratic_rights_salience: 0.80
kurdish_identity_salience: 0.85   # Öcalan-interlocutor demand
peace_process_salience: 0.70   # rising
primary_strategy_state: independent-run (announced)
communication_mode: symbolic
active_internal_personas: [buldan_pervin (final HDP role), sancar_mithat (final HDP role), hatimogullari_tulay (rising), bakirhan_tuncer (rising), demirtas_selahattin_invoked]
transition_trigger: HEDEP→DEM brand change forced by Yargıtay; Dec 11, 2023
expected_voter_effect: brand-discontinuity managed; Third Way doctrine consolidated; pre-2024 base mobilisation primer.
```

### Period 6 — `P6_HEDEP_to_DEM_2024_campaign`

```
period_id: P6_HEDEP_to_DEM_2024_campaign
start_date: 2023-10-15
end_date: 2024-03-30
current_party_label: HEDEP (Oct 15) → DEM Party (Dec 11)
active_leadership: [hatimogullari_tulay, bakirhan_tuncer]
symbolic_leader: demirtas_selahattin
symbolic_leader_status: imprisoned; popularity exceeds DEM brand
legal_pressure_state: high
closure_risk_level: 0.45   # buffered
trustee_threat_level: 0.70   # anticipated post-election
organizational_capacity: 0.85
voter_recognition: 0.75   # DEM brand established by Mar 2024
strategic_voting_signal: 0.05   # explicitly NOT directing votes to CHP in western metros
opposition_alignment_signal: 0.10   # Third Way / no formal alignment
independent_identity_signal: 0.95
boycott_signal: 0.20   # internal debate; not official
nationalist_backlash_risk: 0.55   # AKP "vote-splitting" frame
democratic_rights_salience: 0.85
kurdish_identity_salience: 0.85
peace_process_salience: 0.60
primary_strategy_state: independent-run
communication_mode: mobilizing
active_internal_personas: [hatimogullari_tulay, bakirhan_tuncer, bestas_meral_danis (DEM Istanbul co-candidate), zeydan_abdullah (Van candidacy), onder_sirri_sureyya (TBMM Deputy Speaker), kisanak_gultan (symbolic Ankara candidacy Jan 2024), buldan_pervin (Imrali Delegation from Dec 2023), sancar_mithat (Imrali Delegation), turk_ahmet (dialogue-faction commentary), demirtas_selahattin_invoked, basak_demirtas_event_trigger (Jan-Feb 2024 candidacy debate)]
transition_trigger: March 31, 2024 local election; Van crisis Apr 2-3
expected_voter_effect: 78 municipalities incl. Diyarbakır, Van, Mardin metros; 10 provincial-capital recovery; nationalist counter mobilised.
```

### Period 7 — `P7_2024_post_local_Van_crisis` (optional, included as in source)

```
period_id: P7_2024_post_local_Van_crisis
start_date: 2024-04-01
end_date: 2024-04-30 (window closes; Van resolution complete by Apr 3)
current_party_label: DEM Party
active_leadership: [hatimogullari_tulay, bakirhan_tuncer]
symbolic_leader: demirtas_selahattin
symbolic_leader_status: imprisoned; May 16 Kobane verdict (42 years) — note: post-window event
legal_pressure_state: critical
closure_risk_level: 0.55   # HDP case formally pending; DEM buffered (CONTESTED)
trustee_threat_level: 0.90   # Hakkâri June 2024, multi-city Nov 2024, Van Feb 2025 — post-window cascade primed
organizational_capacity: 0.85
voter_recognition: 0.80
strategic_voting_signal: 0.05
opposition_alignment_signal: 0.45   # informal CHP convergence on Van protests
independent_identity_signal: 0.90
boycott_signal: 0.05
nationalist_backlash_risk: 0.55   # cross-pressures from Oct 2024 Bahçeli proposal — note: post-window
democratic_rights_salience: 0.90
kurdish_identity_salience: 0.90
peace_process_salience: 0.55
mandate_contestation_state: mandate_won→mandate_revoked→protest_triggered→YSK_reversal→mandate_restored
primary_strategy_state: hybrid   # celebrate 10 provincial wins + legal+protest defence + emerging Öcalan-dialogue track
communication_mode: defensive
active_internal_personas: [hatimogullari_tulay, bakirhan_tuncer, zeydan_abdullah (peak), sancar_mithat (legal commentary), bestas_meral_danis (legal defence), onder_sirri_sureyya (parliamentary defender), turk_ahmet (dialogue-faction commentary)]
transition_trigger: window closes; subsequent kayyum wave is out-of-window
expected_voter_effect: Van victory defended via YSK 7-4 reversal; movement reaches a legitimacy peak immediately followed by structural pressure return.
```

### Initial conditions and modeler notes

- **Demirtaş's imprisonment is an initial condition** (since 2016-11-04), not a 2019–2024 event. The simulation begins with `symbolic_leader_status = imprisoned`.
- **Two faction axes operate inside the movement from P5 onward**: `hatimogullari_tulay = weaken_AKP` vs `turk_ahmet = dialogue_first`. Expose `faction_weight` as a tunable parameter.
- **Co-chair pair collapsing** is supported: `(buldan_pervin, sancar_mithat)` in P2-P4 and `(hatimogullari_tulay, bakirhan_tuncer)` in P5-P7 can be collapsed to a single agent in low-resolution runs.
- **DEM's 2024 strategy is structurally different from HDP's 2019 strategy** — `strategic_voting_signal` drops from 0.90 (P1) to 0.05 (P6) and `independent_identity_signal` rises from 0.75 to 0.95.
- **Boycott_signal in P6** is set to 0.20 (soft, contested); sensitivity-test at 0.05 (none).

---

## Output 6 — JSON/YAML-Ready Config Objects

Four YAML files are written to the workspace and listed below.

### 6.1 `political_agents.yaml`

Contains every active broadcasting agent, the KurdishMovementAgent, and its internal personas. See standalone file.

### 6.2 `credibility_matrix.yaml`

Contains every (agent_id, voter_archetype) cell with credibility_score, likely_effect, and explanation. See standalone file.

### 6.3 `politician_event_responses.yaml`

Contains every (event_id, agent_id) cell with does_agent_broadcast, message_frame, emotional_tone, target_voter_groups, expected_positive_effect, expected_backlash, vote_shift_direction, movement_state_effect (where relevant), and confidence_level. See standalone file.

### 6.4 `movement_state_machine.yaml`

Contains the seven periods plus initial conditions and faction-axis configuration. See standalone file.

---

## Important calibration rules (for Claude Code consumption)

1. All 0–1 values are **source-grounded simulation calibration parameters**, not objective measurements. Treat them as tunable priors.
2. **No direct quotes anywhere**. Every `message_frame` is paraphrased.
3. **Sourced vs assumed** is preserved at the field level in the source profiles; in this consolidation, items that were `[INTERP]` or `[SIM-ASSUME]` in the source remain qualitatively flagged (lower `confidence_level`).
4. **Numeric bounds**: all values in [0,1] unless explicitly categorical or counted.
5. **No predictive accuracy claims** — this configuration is a representational scaffold, not a forecast.
6. **Voter-archetype generation is out of scope** for this configuration.
7. The configuration is **deterministic-first**: a single simulation run with these parameters should produce reproducible outputs. Stochasticity, where present (contested closure_risk, contested boycott_signal), is exposed as a tunable parameter band.
