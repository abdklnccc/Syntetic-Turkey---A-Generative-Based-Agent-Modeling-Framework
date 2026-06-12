# Synthetic Turkey — LLM Voter Agent Simulation
## Historically Grounded Event Tick Timeline: June 2018 – May 28, 2023

> **Simulation Purpose:** This document provides a Game Master-ready event tick timeline for an academic LLM-based agent simulation of the 2023 Turkish presidential election. Each tick is a stimulus event that voter agents evaluate and respond to, updating belief states, emotional states, and vote intentions. Values are calibration hints for LLM agents — not deterministic rules.

***

# Output 1 — Full Event Tick Timeline (Narrative Form)

## Tick Reference Table

| tick_id | Date | Category | Title |
|---------|------|----------|-------|
| T001 | 2018-06-24 | election | 2018 Presidential & Parliamentary Elections — Erdoğan Wins First Round[^1] |
| T002 | 2018-08-10 | economy | Turkish Lira Currency Crisis — US-Turkey Brunson Sanctions[^2] |
| T003 | 2018-11-20 | Kurdish_politics | ECHR Orders Demirtaş Release — Turkey Refuses[^3] |
| T004 | 2019-03-31 | election | March 2019 Local Elections — AKP Loses Ankara and Istanbul[^4] |
| T005 | 2019-05-06 | legal_institutional | YSK Annuls Istanbul Election — Rerun / İmamoğlu Wins Landslide[^5] |
| T006 | 2019-08-18 | gender_violence | Emine Bulut Femicide — '#ÖlmekİstemiyorUM' Goes Viral[^6] |
| T007 | 2020-03-15 | other | COVID-19 Pandemic — Partial Lockdowns, Economic Shock[^7] |
| T008 | 2021-03-20 | gender_violence | Turkey Withdraws from Istanbul Convention[^8] |
| T009 | 2021-03-17 | Kurdish_politics | HDP Closure Case Filed — Party Under Existential Legal Threat[^9] |
| T010 | 2021-09-23 | economy | Lira Free-Fall — 60% Devaluation in 2021[^10] |
| T011 | 2021-12-21 | economy | Parliament Rejects Pension Hike — Pensioner Anger[^11] |
| T012 | 2022-08-01 | economy | Inflation Peaks at 80-85% — Worst Cost-of-Living Crisis in 24 Years[^12] |
| T013 | 2022-12-14 | legal_institutional | İmamoğlu Sentenced — Opposition Rallies[^13] |
| T014 | 2022-12-20 | economy | Erdoğan Announces Mandatory Retirement Elimination — 2M Workers[^14] |
| T015 | 2023-01-05 | Kurdish_politics | Constitutional Court Freezes HDP Treasury Aid[^15] |
| T016 | 2023-02-06 | disaster | EQ-A: Earthquake Day — 7.8 + 7.7 Double Strike[^16] |
| T017 | 2023-02-07 | disaster | EQ-B: AFAD Response Chaos — Rescue Teams Delayed[^17] |
| T018 | 2023-02-08 | social_media | EQ-C: Twitter/TikTok Banned During Earthquake Rescue[^18] |
| T019 | 2023-02-08 | disaster | EQ-D: Erdoğan Admits Problems — Visits Disaster Zone[^17] |
| T020 | 2023-02-11 | corruption | EQ-E: Contractors Arrested — Construction Amnesty Scandal[^19] |
| T021 | 2023-02-12 | opposition_alliance | EQ-F: Opposition Mayors' Aid Response[^14] |
| T022 | 2023-02-15 | disaster | EQ-G: National Mourning — Reconstruction Promises[^20] |
| T023 | 2023-03-03 | opposition_alliance | OPP-A: Akşener Leaves Table of Six[^21] |
| T024 | 2023-03-06 | opposition_alliance | OPP-B: Opposition Reunites — Kılıçdaroğlu Nominated[^22] |
| T025 | 2023-03-09 | Kurdish_politics | Constitutional Court Lifts HDP Treasury Aid Freeze[^23] |
| T026 | 2023-03-22 | economy | Erdoğan Announces Pension Increase to 7,500 Lira[^24] |
| T027 | 2023-04-28 | Kurdish_politics | HDP/YSP Formally Endorses Kılıçdaroğlu[^25] |
| T028 | 2023-05-08 | campaign | Erdoğan Raises Civil Servant Salaries 45%[^26] |
| T029 | 2023-05-11 | campaign | CAND-A: Muharrem İnce Withdraws[^27] |
| T030 | 2023-05-14 | election | ROUND1: First Round — Erdoğan 49.52%, Kılıçdaroğlu 44.88%, Oğan 5.17%[^28] |
| T031 | 2023-05-17 | campaign | RUN-A: Kılıçdaroğlu's Nationalist Turn — Anti-Refugee Rhetoric[^29] |
| T032 | 2023-05-22 | polling_shift | RUN-B: Sinan Oğan Endorses Erdoğan[^30] |
| T033 | 2023-05-24 | campaign | RUN-C: Kılıçdaroğlu Signs Özdağ Protocol — '13M Refugees' Pledge[^31] |
| T034 | 2023-05-26 | Kurdish_politics | RUN-D: Kurdish Voter Reluctance — HDP Maintains Support Despite Protocol[^32] |
| T035 | 2023-05-28 | election | FINAL: Presidential Runoff — Erdoğan Wins 52.18%[^33] |

***

## Detailed Tick Narratives

### T001 — 2018 Presidential & Parliamentary Elections (2018-06-24)

**Summary:** Erdoğan wins outright with 52.59% in the first round, activating the new executive presidential system created by the 2017 referendum. The People's Alliance (AKP-MHP) wins 344 of 600 parliamentary seats. HDP's Demirtaş runs from prison and earns 8.4%. The new system formally eliminates the prime ministerial office and concentrates executive power in the presidency.[^34][^1][^35]

**Why it matters for voter behavior:** This is the constitutional baseline of the simulation. Erdoğan now holds unprecedented executive authority. The AKP-MHP coalition has parliamentary majority. Opposition voters understand that defeating Erdoğan in 2023 requires a unified effort because parliament alone cannot check executive power.

**Affected voter archetypes:** Devout Anatolian Loyalist (vindicated); Secular Urban Professional (alarmed); Kurdish Political Voter (Demirtaş imprisoned, votes still cast for HDP from prison); Alevi-CHP Loyalist (defeated but mobilized); Nationalist Grey Wolf Core (rewarded via MHP alliance).

**Emotional impact:** Hope (+, loyalists) / Fear (+, opposition) / Anger (medium, opposition) / Sadness (medium, Kurdish voters)

**Likely vote effect:** Strongly helps Erdoğan's baseline, establishes AKP-MHP dominance as the simulation starting state.

**Confidence:** High

***

### T002 — Turkish Lira Currency Crisis / Brunson Sanctions (2018-08-10 to 2018-08-20)

**Summary:** The US doubles tariffs on Turkish steel and aluminum following Turkey's refusal to release American pastor Andrew Brunson. The lira collapses from ~4.5 to over 7 per dollar — a 40%+ devaluation in weeks. Inflation surges. Erdoğan frames the crisis as an external economic attack on Turkish sovereignty, rallying nationalist sentiment temporarily. The Central Bank raises interest rates in September, stabilizing the lira partially.[^36][^37][^38]

**Why it matters:** The 2018 currency shock is the first major economic injury of the simulation period. It begins eroding AKP's economic competence narrative and introduces the "economic anxiety" dimension that will dominate voter decision-making through 2023.

**Affected archetypes:** Conservative Economically Disillusioned (primary); Retired Protest Voter; Secular Urban Professional; Devout Anatolian Loyalist (temporary rally effect).

**Emotional impact:** High fear, high anger, low hope across most groups; moderate nationalist surge among loyalists.

**Confidence:** High

***

### T003 — ECHR Orders Demirtaş Release — Turkey Refuses (2018-11-20)

**Summary:** The European Court of Human Rights rules that Demirtaş's detention since November 2016 violates his rights and has the "ulterior purpose of stifling pluralism". Turkish courts refuse to comply. Demirtaş remains imprisoned, where he will continue to write political commentary and books from his cell throughout the simulation period.[^39][^3]

**Why it matters:** This tick is foundational for Kurdish voter disillusionment. Demirtaş's continued imprisonment despite a binding ECHR ruling signals that Turkey's institutions operate outside rule-of-law constraints when political stakes are high. It feeds the Kurdish rights salience dimension throughout the period.

**Affected archetypes:** Kurdish Political Voter (primary); Alevi-CHP Loyalist; Cosmopolitan Liberal Urban Professional.

**Confidence:** High

***

### T004 — March 2019 Local Elections: AKP Loses Ankara and Istanbul (2019-03-31)

**Summary:** CHP's Mansur Yavaş wins Ankara and Ekrem İmamoğlu narrowly wins Istanbul by ~13,000 votes. The AKP still wins 44% nationally but loses both of Turkey's two largest cities for the first time since 1994. The result is driven primarily by economic anxiety — the 2018 recession and currency crash. AKP contests Istanbul result.[^4][^40][^41]

**Why it matters:** The first concrete evidence that Erdoğan's coalition can be defeated. Opposition voters experience hope surge. Economic performance is confirmed as the dominant electoral variable. İmamoğlu and Yavaş become the faces of a viable opposition alternative.

**Affected archetypes:** Conservative Economically Disillusioned (primary movers); Secular Urban Professional; Alevi-CHP Loyalist; Young Urban Protest Voter.

**Emotional impact:** Hope surge (opposition); Anger (AKP bloc, at result); Moderate political fatigue (long campaign).

**Confidence:** High

***

### T005 — YSK Annuls Istanbul Election → Rerun → İmamoğlu Wins Landslide (2019-05-06 to 2019-06-23)

**Summary:** Turkey's Supreme Electoral Council annuls the Istanbul March result on technical grounds — unsigned documents and non-civil-servant ballot box officials. The rerun is held June 23. İmamoğlu wins with 54% vs 45%, a margin of ~775,000 votes — a massive repudiation of the annulment. The backfire effect makes İmamoğlu the most popular opposition figure in Turkey.[^5][^42][^43]

**Why it matters:** This is arguably the single most damaging institutional self-inflicted wound of Erdoğan's era. The annulment was perceived as electoral manipulation, and the landslide punished it severely. İmamoğlu's "fools" comment targeting YSK will become the basis for a future criminal conviction (T013).

**Affected archetypes:** Secular Urban Professional (galvanized); Young Urban Protest Voter (inspired); Moderate Nationalist Opposition (softened toward opposition); Conservative Economically Disillusioned (many switch); Alevi-CHP Loyalist (energized).

**Likely vote effect:** Strongly hurts Erdoğan, strongly helps Kılıçdaroğlu coalition by establishing İmamoğlu as opposition symbol.

**Confidence:** High

***

### T006 — Emine Bulut Femicide: '#ÖlmekİstemiyorUM' (2019-08-18 to 2019-09-01)

**Summary:** Emine Bulut, 38, is stabbed to death in front of her 10-year-old daughter in Kırıkkale by her ex-husband on August 18. Her dying words "I don't want to die" are captured on video, go viral days later, and trigger nationwide women's protests. The hashtag #ÖlmekİstemiyorUM trends nationally. Turkish feminist groups link the murder to the government's policies on divorce restrictions and family mediation.[^44][^45][^6]

**Why it matters:** Femicide has been a mounting political issue in Turkey, with hundreds of women killed annually. This event crystallizes public anger and becomes a major mobilization catalyst for women voters. It accumulates toward the Istanbul Convention withdrawal (T008) as a related grievance.

**Affected archetypes:** Secular Urban Professional (female); Young Urban Protest Voter (female); Cosmopolitan Liberal Urban Professional; Alevi-CHP Loyalist (female). Devout Anatolian Loyalist women: mixed — some quietly concerned, others deferential to government framing.

**Emotional impact:** Very high anger and sadness; high fear among women voters.

**Confidence:** High

***

### T007 — COVID-19 Pandemic (2020-03-15 to 2020-06-30)

**Summary:** Turkey confirms its first COVID-19 case on March 11, 2020. Erdoğan imposes partial lockdowns while prioritizing economic continuity — refusing a full economic standstill. GDP contracts 9.9% in Q2 2020. Government welfare support is limited relative to peers. A brief rally-around-the-flag effect partially boosts government approval. The pandemic accelerates pre-existing economic fragilities.[^7][^46][^47]

**Why it matters:** COVID creates a period of forced political quietism — no major protests, reduced opposition activities. However, economic pain accumulates, and the government's weak social protection record creates resentment among low-income and retired groups that will feed through to 2021-2022.

**Affected archetypes:** Retired Protest Voter (exposed by weak pension/support system); Conservative Economically Disillusioned; Young Urban Protest Voter (locked down, economic anxiety).

**Confidence:** Medium (pandemic's precise voter impact is diffuse)

***

### T008 — Turkey Withdraws from Istanbul Convention (2021-03-20 to 2021-07-01)

**Summary:** Erdoğan signs a presidential decree withdrawing Turkey from the Istanbul Convention on violence against women in March 2021. The decree — made without parliamentary debate — cites concerns about sexual orientation provisions being "incompatible with family values". Formal exit takes effect July 1. Thousands of women protest in Istanbul, Ankara, and other cities across the withdrawal process. International condemnation from UN, EU, and Amnesty International follows.[^48][^49][^8][^50]

**Why it matters:** The decision activates women voters across ideological boundaries. It signals that Erdoğan's government is actively retreating from women's rights frameworks. Combined with the Emine Bulut case (T006), it creates a sustained women's mobilization narrative. Even some conservative women voters feel unsafe.

**Affected archetypes:** Secular Urban Professional (very strong negative); Young Urban Protest Voter; Cosmopolitan Liberal Urban Professional; Alevi-CHP Loyalist; Devout Anatolian Loyalist (mixed — some approve on religious grounds).

**Likely vote effect:** Significantly hurts Erdoğan among women voters; helps any opposition alternative that pledges to reinstate the convention.

**Confidence:** High

***

### T009 — HDP Closure Case Filed (2021-03-17)

**Summary:** Chief Public Prosecutor Bekir Şahin files a closure case against the HDP at the Constitutional Court, citing alleged organic ties to the PKK. The indictment covers dozens of politicians and seeks a ban on party members from politics for five years. The case will hang over HDP for the entire pre-election period, affecting candidate recruitment, fundraising, and alliance-building.[^23][^51][^9]

**Why it matters:** The closure case forces HDP into an existential survival mode. It shapes the decision to run parliamentary candidates under the surrogate Green Left Party (YSP), to endorse Kılıçdaroğlu instead of running their own presidential candidate, and to accept constitutional court rules even when they view them as biased. Kurdish voters see this as continued state persecution.

**Affected archetypes:** Kurdish Political Voter (primary); Alevi-CHP Loyalist; Cosmopolitan Liberal Urban Professional.

**Confidence:** High

***

### T010 — Lira Free-Fall: 60% Devaluation in 2021 (2021-09-23 to 2021-12-31)

**Summary:** After dismissing three central bank governors in one year, Erdoğan enforces an unorthodox low-interest-rate policy in the face of high inflation, citing his belief that "high interest rates cause inflation". The lira loses 44-60% of its value through 2021, hitting 18.5 to the dollar by December — the lowest level since AKP took power. Inflation surges past 20% then accelerates. Citizens scramble to hold dollars, gold, or cryptocurrency as protection.[^52][^10]

**Why it matters:** This is the most structurally significant economic event of the simulation. The lira collapse destroys savings, raises import costs, and triggers the inflation spiral that peaks at 80%+ in 2022 (T012). It is the direct cause of "Conservative Economically Disillusioned" archetype formation — previously loyal AKP voters who cannot ignore the economic pain.

**Affected archetypes:** All archetypes feel this — primary impact on Conservative Economically Disillusioned, Retired Protest Voter, and Pious Disillusioned Islamist.

**Confidence:** High

***

### T011 — Parliament Rejects Pension Hike (2021-12-21)

**Summary:** The AKP-controlled parliament votes down an opposition proposal to raise the lowest pensions to minimum wage level. At the time, 70% of retirees earn below minimum wage. The minimum wage itself is raised 50% in January 2022 — but pensions are excluded, deepening the inequality gap.[^11]

**Why it matters:** Pensioners are a large and historically AKP-leaning bloc. This rejection directly signals to retired voters that the government's economic priorities exclude them. It plants the seed of AKP defection among retired voters — particularly those who voted loyally for decades. The issue persists until Erdoğan offers pre-election pension increases in 2023 (T026).

**Affected archetypes:** Retired Protest Voter (primary); Conservative Economically Disillusioned; Devout Anatolian Loyalist (pension-age segment).

**Confidence:** High

***

### T012 — Inflation Peaks at 80-85% (2022-06-01 to 2022-10-31)

**Summary:** Official CPI inflation peaks at 83-85% in August-October 2022, with independent ENAG estimates suggesting 170%+ due to methodological concerns. Food prices spike 90%+, energy costs surge, and rent becomes unaffordable in major cities. The minimum wage is raised three times during 2022, but real purchasing power continues falling. The government's FX-protected deposit scheme (KKM) stabilizes the exchange rate at enormous fiscal cost.[^12][^53][^52]

**Why it matters:** This is the apex of economic anxiety in the simulation. Virtually no voter archetype is unaffected. Even devout AKP loyalists cannot dismiss kitchen-table costs. This is the primary driver of opposition poll leads through late 2022 — which Erdoğan partially offsets through pre-election transfers (T014, T026, T028).

**Affected archetypes:** All archetypes. Most intense for Conservative Economically Disillusioned, Retired Protest Voter, Young Urban Protest Voter, and Pious Disillusioned Islamist.

**Confidence:** High

***

### T013 — İmamoğlu Sentenced to 2.5 Years (2022-12-14)

**Summary:** An Istanbul court sentences Mayor Ekrem İmamoğlu to 2 years and 7 months for calling YSK members "fools" after the 2019 Istanbul annulment — a statement widely regarded as a political response to an illegitimate ruling. The verdict is not yet final (subject to appeal), so İmamoğlu remains in office. But if upheld, he would face a political ban and cannot run for president.[^13][^54][^55]

**Why it matters:** This verdict directly shapes the 2023 presidential race. Opposition voters believe it is designed to eliminate İmamoğlu as a candidate. It triggers CHP internal debate on candidacy. Ironically, it elevates İmamoğlu's profile and national popularity — his campus visits produce mass student mobilization. İmamoğlu's "I will not bow" posture becomes an opposition symbol.[^54]

**Affected archetypes:** Secular Urban Professional (galvanized); Young Urban Protest Voter (mobilized — İmamoğlu campus tours draw huge crowds); Alevi-CHP Loyalist; Moderate Nationalist Opposition (some sympathy).

**Likely vote effect:** Short-term: strongly motivates opposition base. Medium-term: shapes opposition candidacy debate.

**Confidence:** High

***

### T014 — Mandatory Retirement Elimination + Minimum Wage Hike (2022-12-20)

**Summary:** Erdoğan announces removal of the retirement age threshold, enabling over 2 million workers to retire immediately. A 55% minimum wage hike (to 8,500 lira) is also announced — the third such increase in 2022. Both measures are widely characterized as pre-election economic engineering, intended to rebuild the loyalty of working-class and retired voters eroded by inflation.[^24][^14]

**Why it matters:** Government-initiated economic transfers do generate electoral returns in Turkey. Some previously disillusioned voters respond positively to direct material benefit. However, the transfers come against a backdrop of 80%+ inflation, reducing their real value. The policy also increases fiscal pressure and long-term debt.

**Affected archetypes:** Retired Protest Voter (primary target — partially mollified); Devout Anatolian Loyalist; Conservative Economically Disillusioned (partially responsive).

**Confidence:** Medium (effect on vote intention is real but partial)

***

### T015 — Constitutional Court Freezes HDP Treasury Aid (2023-01-05)

**Summary:** The Constitutional Court, on the public prosecutor's request within the ongoing closure case, freezes HDP's ~539 million lira ($28.7M) in state election funding just months before elections. The decision is made by an 8-7 majority — HDP argues this is constitutionally insufficient for such a measure. The BBC and opposition parties call it politically motivated.[^51][^15]

**Why it matters:** Kurdish voters interpret this as a direct attempt to kripple HDP's electoral capacity. It accelerates HDP's transition to the YSP surrogate strategy and deepens the institutional trust deficit. Abstention risk rises among HDP base voters who may feel participating in a "rigged" system is pointless.[^51]

**Confidence:** High

***

## Output 2 — Special Multi-Day Event Windows

### A. February 2023 Earthquake Sub-Ticks (T016–T022)

The earthquake produced the most intense and multi-dimensional political shock of the simulation period. Seven dedicated sub-ticks are provided:

#### T016 — EQ-A: Earthquake Day (2023-02-06)
At 04:17 local time, a 7.8 Mw earthquake strikes Pazarcık, Kahramanmaraş. A second 7.7 shock follows at 13:24. Both are among the deadliest in Turkish history. Ten provinces affected. Death toll begins rising. Citizens are in shock — not yet in political mode.[^56][^16]

*Voter groups:* Earthquake Zone Loyalist; Devout Anatolian Loyalist; Kurdish Political Voter in affected southeastern provinces.

*Government approval:* Initial shock — attribution not yet assigned. Fear and sadness dominate. No vote effect yet.

*Institutional trust:* Neutral — waiting for government response.

*Turnout effect:* Neutral — too early. Will become highly negative as trauma accumulates.

***

#### T017 — EQ-B: AFAD Response Chaos (2023-02-07 to 2023-02-09)
Death toll surpasses 17,000 within 72 hours. AFAD declares Level-4 emergency but rescue teams face road damage, winter storms, and coordination failures. Survivors' voices are heard under rubble without help arriving. Social media documents the gap between declared emergency operations and reality on the ground.[^17][^57][^56]

*Voter groups:* All — earthquake zone voters most acutely.

*Government approval:* Strong negative — visible operational failure.

*Institutional trust:* Strong negative — AFAD seen as overwhelmed.

*Turnout effect:* Negative — earthquake zone voters experiencing trauma, displacement.

***

#### T018 — EQ-C: Twitter/TikTok Banned During Rescue (2023-02-08)
BTK restricts Twitter and TikTok for ~9 hours as citizens use Twitter to share survivor GPS coordinates and coordinate rescue. The ban is lifted after massive backlash. The transport minister later defends it with no coherent justification. Police begin tracking "provocative" social media users — 925 identified, 134 detained by late February.[^58][^18][^59][^60]

*Voter groups:* All groups — especially Young Urban Protest Voter; Secular Urban Professional.

*Government approval:* Severe negative — even loyalists express anger.

*Institutional trust:* Severe negative — censorship during a rescue emergency.

*Democratic rights salience:* Very high — media freedom and state power over communication.

*Possible vote effect:* Strongly hurts Erdoğan even among wavering loyalists.

***

#### T019 — EQ-D: Erdoğan Admits Problems / Visits Disaster Zone (2023-02-08 to 2023-02-10)
Erdoğan visits Kahramanmaraş and unusually admits "problems" in the initial response. He promises no one will be left homeless. State of emergency declared in 10 provinces. Some survivors confront officials. Erdoğan's religious framing ("this is fate/God's will") is accepted by some but criticized by secular voices.[^17]

*Voter groups:* Earthquake Zone Loyalist; Devout Anatolian Loyalist.

*Government approval:* Marginal recovery among loyal segment — others remain furious.

*Notes for simulation:* "God's will" framing provides partial cover for devout loyalists. Earthquake zone loyalists who lost family are less accepting of any framing.

***

#### T020 — EQ-E: Construction Amnesty / Contractor Arrests (2023-02-11 to 2023-03-20)
113 arrest warrants issued within 5 days. By March, 298 arrested (contractors, building inspectors, owners). Evidence mounts that government-issued "construction amnesties" — which allowed developers to bypass safety codes for fees — directly enabled the catastrophic building collapses in earthquake-prone zones. Construction sector ties to AKP political economy become widely debated.[^19][^61][^62][^63]

*Voter groups:* All — this is corruption salience's defining moment. Earthquake Zone Loyalist most acutely; Conservative Economically Disillusioned; Pious Disillusioned Islamist.

*Government approval:* Severe negative — policy-linked deaths.

*Corruption salience:* Maximum. The amnesties were formal government policy, approved by parliament.

*Possible vote effect:* Strongly hurts Erdoğan; potentially activates conservative-religious voters who see corruption as a moral failure.

***

#### T021 — EQ-F: Opposition Mayors' Aid Response (2023-02-12 to 2023-02-20)
CHP-run Istanbul and Ankara municipalities send aid trucks, search teams, and volunteers. İmamoğlu and Yavaş are physically present in disaster zones. A narrative battle emerges over who is actually helping. Some media report that government-allied checkpoints initially slowed CHP aid. Opposition municipalities' responsiveness is widely shared on social media.[^14]

*Voter groups:* Earthquake Zone Loyalist; Devout Anatolian Loyalist (for some, CHP competence is noticed for first time); Pious Disillusioned Islamist.

*Government approval:* Marginal loss — opposition gains governance credibility.

*Opposition trust:* Strong positive — empirical demonstration of governance ability.

*Notes for simulation:* This tick can shift some earthquake zone AKP loyalists toward Kılıçdaroğlu — particularly if they personally received opposition aid before government aid.

***

#### T022 — EQ-G: National Mourning / Reconstruction Promises (2023-02-15 to 2023-02-28)
Final Turkish death toll confirmed at 53,537. Estimated 1.5 million displaced. Erdoğan promises 200,000 new homes within one year and rapid reconstruction. A political debate emerges on whether to delay elections — opposition opposes delay. The earthquake zone remains politically traumatized and partially displaced for the rest of the simulation period.[^20][^16]

*Voter groups:* Earthquake Zone Loyalist (reduced turnout probability due to displacement); Kurdish Political Voter in Hatay and Adıyaman; Devout Anatolian Loyalist.

*Turnout effect:* Significantly negative for earthquake zone voters (displacement, trauma, polling stations may be damaged/relocated).

*Government approval:* Mixed — reconstruction promises are viewed against the amnesty scandal.

*Religious identity salience:* Elevated — national mourning and theological framing of disaster.

***

### B. March 2023 Opposition Candidate Crisis (T023–T024)

#### T023 — OPP-A: Akşener Leaves Table of Six (2023-03-03 to 2023-03-05)
On February 3's meeting of the Table of Six, İYİ Party leader Meral Akşener walks out, refusing to accept Kılıçdaroğlu's candidacy and demanding İmamoğlu or Yavaş — both polling significantly ahead of Kılıçdaroğlu against Erdoğan. The coalition fractures publicly. Erdoğan's camp is energized. Some İYİ members resign in protest of Akşener's decision.[^21][^64]

*Political actors damaged:* Nation Alliance, İYİ Party, Kılıçdaroğlu.

*Political actors helped:* Erdoğan, AKP. Sinan Oğan (protest voter destination if coalition collapses).

*Voter groups:* Moderate Nationalist Opposition (primary — Akşener's base); Secular Urban Professional (alarmed).

*Opposition trust:* Sharp negative — just months before elections.

***

#### T024 — OPP-B: Opposition Reunites (2023-03-06)
After 72 hours of intense negotiations described in the press as Turkey's most dramatic political deal, Akşener returns to the table. The deal names Kılıçdaroğlu as presidential candidate and commits to naming İmamoğlu and Yavaş as future vice-presidents. HDP signals it will endorse Kılıçdaroğlu without running its own candidate.[^22][^65][^66][^67]

*Political actors helped:* Kılıçdaroğlu, Nation Alliance, HDP (indirectly).

*Political actors damaged:* Erdoğan (loses the gift of opposition chaos).

*Voter groups:* All opposition-leaning groups — hope restored. Kurdish voters: encouraged by HDP's implied support. Moderate nationalists: reassured by İmamoğlu/Yavaş VP formula.

*Note:* This is the opposition's best coalition moment of the simulation. Subsequent events (T033, T034) partially unravel it.

***

### C. May 2023 Final Campaign, First Round, and Runoff Period (T029–T035)

#### T029 — Muharrem İnce Withdraws (2023-05-11)
İnce cites a deepfake video campaign depicting sexual misconduct and blames FETÖ for the smear. He withdraws 3 days before the election. His name remains on the ballot (overseas votes already counted). His 2% polling share was expected to mostly go to Kılıçdaroğlu in any case, but the withdrawal consolidates the anti-Erdoğan vote more cleanly.[^68][^27]

*Political actors helped:* Kılıçdaroğlu (marginally — vote consolidation).

*Note:* İnce's entire candidacy was viewed by some as a vote-splitting scheme. His withdrawal restores some of that suspicion as reversed cooperation.

***

#### T030 — First Round: Erdoğan 49.52%, Kılıçdaroğlu 44.88%, Oğan 5.17% (2023-05-14)
Erdoğan falls just short of the 50% threshold. No candidate wins outright — a historic first for Turkey. Turnout is 88.84%. Sinan Oğan's 5.17% is significantly higher than polls predicted. Parliamentary result: AKP-MHP retain majority. HDP/YSP wins ~8.8% in parliament. Nation Alliance underperforms legislatively.[^28][^69]

*Key analytical implication:* Oğan's voters are now kingmakers. Both candidates must court approximately 2.8 million nationalist voters who chose neither major alliance in the first round. This shapes the entire two-week runoff campaign.

***

#### T031 — Kılıçdaroğlu's Nationalist Turn (2023-05-17 to 2023-05-20)
Kılıçdaroğlu releases anti-refugee video, claiming "10 million irregular migrants" entered under Erdoğan. He pledges to return Syrians within two years. This is a dramatic shift from his "Turkey's Gandhi" moderate image. The move is intended to court Oğan voters.[^29][^70]

*Political actors helped:* Moderate nationalists within Kılıçdaroğlu's potential coalition.

*Political actors damaged:* Kılıçdaroğlu (credibility as liberal/democratic candidate); HDP/YSP (deeply uncomfortable).

*Kurdish voter risk:* High. The claim of "10 million migrants" (vs. UNHCR's 3.9 million) is inflated and signals anti-Kurdish conflation.[^29]

***

#### T032 — Oğan Endorses Erdoğan (2023-05-22)
Sinan Oğan endorses Erdoğan at a nationally televised press conference, citing anti-terrorism and anti-PKK stance as his conditions. He says nationalists are now "key players" in Turkish politics. The endorsement sends approximately 3 million first-round Oğan voters a signal to back Erdoğan in the runoff.[^30][^71][^72]

*Political actors helped:* Erdoğan — major numerical boost.

*Political actors damaged:* Kılıçdaroğlu — loses the larger block of nationalist swing voters.

*Note:* Not all Oğan voters follow the endorsement — some were protest voters who dislike both alliances. But the signal effect is significant.

***

#### T033 — Kılıçdaroğlu Signs Özdağ Protocol (2023-05-24)
Kılıçdaroğlu signs a 7-article protocol with Victory Party leader Ümit Özdağ pledging to expel all refugees (described as "13 million") within one year. Özdağ endorses Kılıçdaroğlu. HDP officially maintains support but expresses deep discomfort. Kurdish voters in Diyarbakır begin publicly expressing anger in BBC Turkish interviews.[^73][^31][^74]

*Political actors helped:* Özdağ; far-right nationalist Kılıçdaroğlu voters.

*Political actors damaged:* Kılıçdaroğlu (HDP credibility cost); HDP/YSP (forced to choose between their values and tactical support); Kurdish voters (feel abandoned).

*Key tension:* Kılıçdaroğlu needed both Kurdish and far-right nationalist votes — a mathematically impossible coalition when both groups define each other as the enemy.

***

#### T034 — Kurdish Voter Reluctance / Runoff Abstention Risk (2023-05-26)
HDP/YSP formally reaffirms Kılıçdaroğlu support but Kurdish grassroots anger is visible. BBC Turkish interviews in Diyarbakır document voters declaring they will abstain. The HDP base faces a dilemma: vote for Kılıçdaroğlu (who has just pledged refugee deportation and "fight against terrorism") or abstain and potentially re-elect Erdoğan.[^32][^74]

*Key simulation variable:* Kurdish turnout differential between first round and runoff. If Kurdish voter turnout drops significantly in the runoff, it directly explains Erdoğan's victory margin.

***

#### T035 — Runoff: Erdoğan Wins 52.18% (2023-05-28)
Erdoğan wins 52.18% to Kılıçdaroğlu's 47.82%. The margin is larger than the first round gap suggested. Evidence suggests Oğan voters largely backed Erdoğan, and Kurdish turnout in key southeastern provinces declined relative to round one. Kılıçdaroğlu concedes. Erdoğan secures his third presidential term.[^33][^75][^32]

***

# Output 3 — Candidate-Specific Interpretation by Actor

## Recep Tayyip Erdoğan / AKP / People's Alliance

| Period | Status | Key Events |
|--------|--------|------------|
| 2018 | Strong start | Wins executive presidency outright; parliament majority secured |
| 2018-2020 | Weakening | Lira crisis, Brunson sanctions, 2019 local election defeats; COVID partial stabilization |
| 2021-2022 | Severe damage | Istanbul Convention withdrawal; HDP closure case; lira collapse; 80% inflation; İmamoğlu sentence creates opposition martyr |
| Feb 2023 | Earthquake crisis | Response failures, Twitter ban, construction amnesty scandal cause maximum approval damage |
| March-May 2023 | Recovery | Pre-election transfers (pensions, salaries); benefits from opposition candidate crisis; Oğan endorsement; nationalist runoff framing |
| May 28 | Victory | 52.18% — coalition of devout loyalists, nationalists (including Oğan endorsement flow), and conservative economically disillusioned who ultimately stayed |

**Who benefits from which events:** T001 (election win), T002 (nationalist framing of foreign attack), T007 (partial COVID rally), T014 (retirement policy), T023 (opposition crisis), T026 (pension increase), T028 (salary raise), T032 (Oğan endorsement).

**Who is damaged:** T002-T004 (economic decline + local losses), T005 (Istanbul rerun disaster), T008 (Istanbul Convention protests), T012 (inflation peak), T013 (İmamoğlu sentence backfires), T016-T022 (earthquake response failures, Twitter ban, construction amnesty).

***

## Kemal Kılıçdaroğlu / CHP / Nation Alliance

| Period | Status | Key Events |
|--------|--------|------------|
| 2018-2019 | Stable opposition | AKP losses help CHP; İmamoğlu and Yavaş victories expand CHP credibility |
| 2020-2022 | Building coalition | Table of Six formed; economic anxiety grows opposition base; İmamoğlu sentence mobilizes base |
| Feb 2023 | Earthquake narrative gain | CHP municipalities praised for aid response; government narrative weakened |
| March 2023 | Candidate crisis + recovery | Akşener walkout causes temporary damage; nomination formula with İmamoğlu/Yavaş VP deal restores coalition |
| April 2023 | HDP endorsement | Kurdish votes added; nationalist problem created |
| May 2023 | Runoff dilemma | Nationalist turn + Özdağ protocol wins some nationalists but risks Kurdish turnout suppression; net loss |
| May 28 | Defeat | 47.82% — insufficient Kurdish turnout in runoff, Oğan voters mostly went to Erdoğan |

**Key strategic mistake (simulation assumption, not confirmed causation):** The decision to sign the Özdağ protocol — which alienated Kurdish voters who were essential to his vote total — without gaining enough additional nationalist votes to compensate.

***

## Sinan Oğan / ATA Alliance

| Period | Status |
|--------|--------|
| Pre-election | Unknown quantity; polls suggest 1-3% |
| First round | Overperforms: 5.17% — becomes kingmaker |
| May 14-22 | Maximum leverage period — both candidates court him |
| May 22 | Endorses Erdoğan — nationalist anti-PKK stance is condition |

**Beneficiaries of Oğan's candidacy:** Erdoğan (first round — Oğan takes fewer votes from Erdoğan than from Kılıçdaroğlu; second round — endorsement).

**Voter groups:** Nationalist Grey Wolf Core; Moderate Nationalist Opposition; protest voters in ATA Alliance.

***

## Muharrem İnce / Homeland Party (Memleket)

| Period | Status |
|--------|--------|
| March 2023 | Announces candidacy — seen by some as spoiler for Kılıçdaroğlu |
| April 2023 | Polls at ~8% but declining rapidly |
| May 11 | Withdraws citing deepfake smear campaign |
| May 14 | 0.44% — some voters already switched; name on ballot |

**Who benefits from İnce's candidacy:** Erdoğan (vote splitting effect in first round if İnce had stayed). **Who benefits from İnce's withdrawal:** Kılıçdaroğlu (consolidates anti-Erdoğan vote, though most İnce voters had already defected).

***

## HDP/YSP / DEM Movement

| Period | Key Event |
|--------|-----------|
| 2021 | Closure case filed — party under existential threat |
| Jan 2023 | Treasury aid frozen |
| March 2023 | Treasury aid restored; begins open support for Kılıçdaroğlu |
| April 2023 | Formally endorses Kılıçdaroğlu in presidential race |
| May 2023 | Özdağ protocol creates internal tensions — maintains support despite reservations |
| May 28 | Kurdish voter turnout depressed in runoff — partially explains Erdoğan victory |

***

## İYİ Party (Meral Akşener)

Akşener's walkout (T023) and return (T024) nearly destroyed the opposition coalition. Her demand for İmamoğlu or Yavaş was read as a data-driven argument (both led Erdoğan in polls) but was overridden by CHP bloc's preference for Kılıçdaroğlu. Her return was conditioned on the VP formula. The İYİ Party ultimately supported Kılıçdaroğlu but moderate nationalists within her base had complex reactions — some followed Akşener back, others migrated toward Oğan.

***

# Output 4 — Voter Archetype Impact Matrix

> Scale: strong_positive | mild_positive | neutral | mild_negative | strong_negative | mixed

## Archetype Definitions

1. **Devout Anatolian Loyalist** — Conservative, rural/small-town, long-term AKP voter; identity linked to religious-national synthesis
2. **Secular Urban Professional** — CHP-leaning, educated, urban; democratic rights, EU norms, rule-of-law primary concerns
3. **Conservative Economically Disillusioned** — Former AKP voter turned swing; economic pain primary driver, conservative values remain
4. **Alevi-CHP Loyalist** — Minority identity + CHP historical alliance; fears both Islamist governance and Kurdish nationalism accusations
5. **Kurdish Political Voter** — HDP/YSP-aligned; rights-based, suspicious of both AKP and CHP; Demirtaş's imprisonment is defining grievance
6. **Nationalist Grey Wolf Core** — Hard MHP voter; ethnic Turk nationalism; PKK threat is the organizing fear
7. **Moderate Nationalist Opposition** — Former İYİ Party / soft MHP voter; economic concerns + national unity; can switch to opposition if economic pain is sufficient
8. **Pious Disillusioned Islamist** — Voted AKP historically on religious grounds; feels AKP has become corrupt and failed the Islamic promise; may vote Yeniden Refah or stay home
9. **Young Urban Protest Voter** — <30, urban; primary issues: economic opportunity, democratic rights, women's rights, climate; high protest potential, high abstention risk
10. **Earthquake Zone Loyalist** — Formerly reliable AKP voter in southeast Anatolia; the earthquake changed their calculation fundamentally
11. **Retired Protest Voter** — Pension-dependent; once AKP, now angry about pension-wage gap; primary issue: retirement income dignity
12. **Cosmopolitan Liberal Urban Professional** — Secular, internationally oriented; EU integration, press freedom, LGBTQ+ rights primary concerns

***

### Major Tick Impact Matrix (Selected Key Ticks)

| Archetype | T002 (Lira Crisis) | T005 (İstanbul Rerun Win) | T008 (Istanbul Convention) | T010 (2021 Lira Collapse) | T012 (80% Inflation) |
|-----------|-------------------|--------------------------|---------------------------|--------------------------|---------------------|
| Devout Anatolian Loyalist | mild_negative ("external attack" frames it) | mild_negative | mild_positive (family values) | mild_negative | strong_negative |
| Secular Urban Professional | mild_negative | strong_positive | strong_negative (gov) | strong_negative | strong_negative |
| Conservative Economically Disillusioned | strong_negative | mild_positive | neutral | strong_negative | strong_negative |
| Alevi-CHP Loyalist | mild_negative | strong_positive | strong_negative (gov) | strong_negative | strong_negative |
| Kurdish Political Voter | mild_negative | neutral | mild_negative (gov) | strong_negative | strong_negative |
| Nationalist Grey Wolf Core | mixed | mild_negative | mild_positive | mild_negative | strong_negative |
| Moderate Nationalist Opposition | strong_negative | mild_positive | mild_negative (gov) | strong_negative | strong_negative |
| Pious Disillusioned Islamist | strong_negative | neutral | mild_positive | strong_negative | strong_negative |
| Young Urban Protest Voter | strong_negative | strong_positive | strong_negative (gov) | strong_negative | strong_negative |
| Earthquake Zone Loyalist | mild_negative | neutral | neutral | mild_negative | strong_negative |
| Retired Protest Voter | strong_negative | neutral | neutral | strong_negative | strong_negative |
| Cosmopolitan Liberal | strong_negative | strong_positive | strong_negative (gov) | strong_negative | strong_negative |

***

| Archetype | T016-T022 (Earthquake) | T023 (Akşener Leaves) | T024 (Opposition Reunites) | T032 (Oğan → Erdoğan) | T033 (Özdağ Protocol) |
|-----------|----------------------|----------------------|--------------------------|----------------------|----------------------|
| Devout Anatolian Loyalist | mixed (faith + anger at gov) | mild_positive (opp chaos) | mild_negative | mild_positive | neutral |
| Secular Urban Professional | strong_negative (gov failures) | strong_negative | strong_positive | mild_negative | mild_negative |
| Conservative Economically Disillusioned | strong_negative (corruption) | strong_negative | mild_positive | mild_positive | neutral |
| Alevi-CHP Loyalist | strong_negative (gov) | strong_negative | strong_positive | mild_negative | mild_negative |
| Kurdish Political Voter | strong_negative (gov failures in Kurdish zones) | mild_negative | strong_positive | strong_negative | strong_negative |
| Nationalist Grey Wolf Core | mild_negative | mild_positive | neutral | strong_positive | mild_positive |
| Moderate Nationalist Opposition | strong_negative (gov) | strong_negative | mild_positive | mild_positive | mild_positive |
| Pious Disillusioned Islamist | strong_negative (construction corruption) | mixed | mild_positive | neutral | neutral |
| Young Urban Protest Voter | strong_negative (Twitter ban) | strong_negative | strong_positive | mild_negative | mild_negative |
| Earthquake Zone Loyalist | strong_negative (family loss + corruption) | mild_negative | mild_positive | mild_negative | neutral |
| Retired Protest Voter | mild_negative | mild_negative | mild_positive | neutral | neutral |
| Cosmopolitan Liberal | strong_negative (all dimensions) | strong_negative | strong_positive | strong_negative | strong_negative |

***

# Output 5 — Simulation Tick JSON

The complete JSON payload (35 ticks) is delivered as a separate downloadable file. The schema follows the specification exactly:

```json
{
  "tick_id": "T016",
  "date": "2023-02-06",
  "date_range": null,
  "title": "EQ-A: Kahramanmaraş Earthquake Day — 7.8 and 7.7 Magnitude Double Strike",
  "category": "disaster",
  "summary": "At 04:17 local time, a 7.8 magnitude earthquake strikes Pazarcık...",
  "date_fence": "Only information available up to 2023-02-06 23:59 should be visible to agents.",
  "affected_dimensions": {
    "government_approval": -0.1,
    "opposition_trust": 0.0,
    "institutional_trust": -0.2,
    "economic_anxiety": 0.3,
    "nationalist_salience": 0.1,
    "kurdish_rights_salience": 0.1,
    "religious_identity_salience": 0.2,
    "corruption_salience": 0.1,
    "turnout_probability": 0.0
  },
  "emotional_impact": {
    "anger": 0.3,
    "fear": 1.0,
    "hope": 0.0,
    "sadness": 1.0,
    "political_fatigue": 0.0
  },
  "candidate_effect_hint": {
    "Erdogan": -0.1,
    "Kilicdaroglu": 0.0,
    "Sinan_Ogan": 0.0,
    "Muharrem_Ince": 0.0,
    "Undecided_Abstain": 0.0
  },
  "affected_archetypes": ["Earthquake Zone Loyalist", "Devout Anatolian Loyalist", "Kurdish Political Voter"],
  "notes_for_llm_agents": "The earthquake has just struck...",
  "sources": ["https://en.wikipedia.org/wiki/2023_Turkey–Syria_earthquakes", "..."]
}
```

The complete machine-readable JSON file (all 35 ticks) is available as a downloadable artifact accompanying this report.

***

# Output 6 — Recommended MVP Timeline Configurations

## Tradeoff Framework

| Factor | Minimal MVP | Medium MVP | Detailed MVP |
|--------|-------------|------------|--------------|
| Tick Count | 12-15 | 25-35 | 50-80 |
| Voter Agents | 50 | 50 | 50 |
| LLM Calls (agents only) | 600-750 | 1,250-1,750 | 2,500-4,000 |
| + Game Master broadcasts | +60-90 | +125-175 | +250-400 |
| + Agent-to-agent interactions | optional | optional | optional |
| **Total calls (base estimate)** | **660-840** | **1,375-1,925** | **2,750-4,400** |
| Cost (@ $0.01/call estimate) | $6.60-8.40 | $13.75-19.25 | $27.50-44.00 |
| Prompt fatigue risk | Low | Medium | High |
| Historical realism | Sparse | Good | Very High |
| Thesis evaluation value | Baseline proof | Core evaluation | Full simulation |

***

## Version 1: Minimal MVP (12 Ticks)

**Recommended ticks:** T001, T002, T005, T008, T010, T012, T013, T016 (combined EQ window), T020, T024, T030, T035

**Rationale:** Covers the five structural dimensions — economic shock, democratic erosion, women's mobilization, earthquake, and election outcome. Can demonstrate the simulation methodology without full historical density. Good for initial validation that agents respond realistically.

**Tradeoff:** Missing Kurdish politics thread (T009, T015, T025, T027, T034), opposition candidate crisis (T023), and runoff dynamics (T031-T033). Results will show coarser voter behavior patterns.

**Use for:** First proof-of-concept; LLM calibration; committee demonstration.

***

## Version 2: Medium MVP (25-35 Ticks)

**Recommended ticks:** All 35 ticks defined in this document.

**Rationale:** The 35-tick set provided is specifically calibrated as a Medium MVP. It covers all major thematic threads — economic shocks, earthquake sub-ticks (7 dedicated), opposition crisis, Kurdish politics, runoff dynamics, candidate effects. The multi-day earthquake windows ensure voters process the earthquake's distinct phases rather than a single compressed event.

**Tradeoff:** Still missing some thematic events — e.g., Gezi protests legacy (pre-2018), Syrian refugee crisis early phase (2015-2017 context ticks), Kavala trial (ongoing human rights case), Afrin military operation (2018 nationalism), Boğaziçi University protests (2021, youth mobilization), individual corruption scandals, detailed polling data ticks showing opinion shifts. These can be added in the Detailed MVP.

**Use for:** Core thesis simulation; most publication-ready configuration; balances LLM cost against historical density.

***

## Version 3: Detailed MVP (50-80 Ticks)

**Additional ticks to add beyond the 35 provided:**

| Suggested Addition | Date | Category | Rationale |
|-------------------|------|----------|-----------|
| Afrin military operation | Jan-Mar 2018 | security_nationalism | Pre-election nationalist surge; Kurdish voter fear |
| Kavala arrest/conviction | Oct 2017 / Apr 2022 | legal_institutional | Democratic erosion; civil society |
| Boğaziçi protests | Jan-Mar 2021 | social_media | Youth mobilization; LGBTQ+ rights |
| PKK urban conflict aftermath | 2015-2018 background | security_nationalism | Why 2018 Kurdish voter context matters |
| Inflation ENAG vs TurkStat debate | 2022 | economy | Institutional trust / statistics manipulation perception |
| HDP co-chair Demirtaş prison writings | 2020-2022 | Kurdish_politics | Cultural/symbolic mobilization |
| Yeniden Refah Party founded | Nov 2018 | religion_culture | AKP Islamic base fracture beginning |
| AKP vote share trends / polling | 2020-2023 | polling_shift | Signal to agents of broader sentiment trajectory |
| Earthquake zone voter displacement logistics | March 2023 | disaster | Operational turnout impact |
| Kılıçdaroğlu campaign platform rollout | April 2023 | campaign | Policy promises: economy, democracy, judiciary |
| Erdoğan campaign rallies and nationalism | April-May 2023 | campaign | Counter-narrative framing |
| HDP trustee (kayyum) policy timeline | 2016-2023 | Kurdish_politics | Core Kurdish grievance — elected mayors removed |
| Sinan Oğan campaign and voter profile | March-May 2023 | campaign | Kingmaker origin story |
| Polling aggregate shifts pre-election | 2023 Q1-Q2 | polling_shift | Calibration reference for agents |
| Disinformation law passage (Oct 2022) | Oct 2022 | legal_institutional | Media freedom; enables Twitter ban framing |

**Tradeoff:** 50-80 ticks × 50 agents = 2,500-4,000 base LLM calls. At more complex prompts (each agent also reads a personal memory + broadcast summary), actual call count can reach 5,000-8,000. This increases both cost and risk of prompt fatigue — where agents give generic/repetitive responses rather than nuanced voter-specific ones.

**Recommendation:** Use Detailed MVP only if each agent has a rich persona with persistent memory and you use incremental update prompts rather than full-context prompts per tick.

***

## LLM Call Count Model

For Medium MVP (35 ticks, 50 agents):

- **Per tick:** 50 agent belief updates + 1 GM broadcast synthesis + 5-10 inter-agent debates (optional) = **~57-62 calls per tick**
- **Total:** 35 × 60 ≈ **2,100 calls**
- **If using GPT-4o (input+output ~2,000 tokens each):** ~4.2M tokens ≈ **$12-25 total depending on model pricing**
- **If using o3-mini or Claude Haiku:** significantly cheaper

**Prompt fatigue mitigation strategies:**
- Keep voter agent prompts to <800 tokens per tick
- Use persistent belief state deltas (not full history) per agent
- Only send the tick summary + 3-5 most relevant belief dimensions to each agent
- Limit inter-agent debate to high-salience ticks (T016, T024, T030, T035)

***

# Appendix: Calibration Notes for Academic Use

## Simulation Assumptions

> The following are explicitly marked as simulation design assumptions, not historical claims:

1. **Numeric belief dimension values** (e.g., `government_approval: -0.5`) are calibration hints derived from event severity and source evidence. They are not empirically measured polling values. They should be treated as agent initialization biases, not ground truth.

2. **Voter archetype archetypes** are idealized constructs. Real Turkish voters do not belong cleanly to one archetype. Each agent should be initialized with a primary archetype and 2-3 secondary trait weights.

3. **Candidate effect hints** indicate the direction of likely benefit, not vote probability. A value of `-0.7` for Erdoğan on a tick does not mean 70% of voters switch — it means the tick creates strong negative sentiment that *may* shift vote intention depending on agent-specific belief states.

4. **Date fence** values are critical: agents must not know about future events. The earthquake victims in T016 do not know about the contractor arrests (T020) or the opposition VP formula (T024). Temporal integrity is essential for realistic simulation.

5. **Kurdish voter abstention** in the runoff is an analytical hypothesis consistent with observed regional vote patterns and media reports. It is not confirmed by disaggregated official data.[^74][^32]

6. **Construction amnesty → earthquake deaths causal link** is analytically supported and had high public salience. The legal and causal evidence is acknowledged as probabilistic, not absolute.[^62][^19]

## Source Reliability Notes

- Official election results (YSK/Anadolu Agency): High reliability[^28][^34]
- AFAD official earthquake statistics: High reliability, slightly delayed[^56]
- Inflation data: Official TurkStat figures used; note ENAG independent estimates were significantly higher
- Voter archetype impact estimates: Derived from multiple journalistic, think tank, and academic sources — Carnegie Endowment, IFRI, Al Jazeera Studies, INSS, OSW[^53][^76][^67][^40][^4]
- Human rights assessments: Human Rights Watch, Bianet, ECHR records[^77][^11][^39]

---

## References

1. [Erdogan wins new term with executive powers](https://www.aljazeera.com/news/2018/6/25/erdogan-wins-re-election-in-historic-turkish-polls) - Erdogan becomes Turkey's first executive president after winning more than half the votes, election ...

2. [U.S. Threatens Further Sanctions Against Turkey Over Detained ...](https://www.npr.org/2018/08/17/639511112/u-s-threatens-further-sanctions-against-turkey-over-detained-pastor) - The US is threatening further sanctions against Turkey if it does not quickly release American pasto...

3. [Turkish court keeps Selahattin Demirtas in jail despite ECHR](https://web.archive.org/web/20190821043015/https:/www.aljazeera.com/news/2018/11/turkish-court-selahattin-demirtas-jail-echr-181130140610828.html) - Court rejects appeal to release pro-Kurdish politician despite a recent ruling by the European right...

4. [Turkish municipal elections: AKP victory tastes like defeat in major cities | Al Jazeera Centre for Studies](https://studies.aljazeera.net/en/positionpapers/2019/04/turkish-municipal-elections-akp-victory-tastes-defeat-major-cities-190404104930606.html) - The municipal elections in Turkey on 31 March 2019 were one of the most hotly contested polls in dec...

5. [Turkey's opposition wins rerun of Istanbul mayoral vote](https://www.aljazeera.com/news/2019/6/24/turkeys-opposition-wins-rerun-of-istanbul-mayoral-vote) - AK Party's candidate concedes defeat after initial results show CHP's Ekrem Imamoglu leading with 54...

6. [Last Words of Emine Bulut on Social Media: I Don't Want to Die](https://bianet.org/haber/last-words-of-emine-bulut-on-social-media-i-don-t-want-to-die-212129) - Days after she was stabbed to death by her ex-husband, the video featuring the last words of Emine B...

7. [Turkey and the Corona Crisis: The Instrumentalization of the ... - IEMed](https://www.iemed.org/publication/turkey-and-the-corona-crisis-the-instrumentalization-of-the-pandemic-for-domestic-and-foreign-policy/) - The Covid-19 pandemic has caught Turkey off guard. As the corona pandemic hit the country severely, ...

8. [Thousands protest Turkey's exit from domestic violence treaty](https://www.aljazeera.com/news/2021/3/27/thousands-protest-turkey-exit-domestic-violence-treaty) - Protesters rally for second consecutive weekend to demand reversal of decision to withdraw from Ista...

9. [Peoples' Democratic Party closure case (2021–present) - Wikipedia](https://en.wikipedia.org/wiki/Peoples'_Democratic_Party_closure_case_(2021%E2%80%93present)) - While the party's closure case was ongoing, HDP decided to transfer its political activities to the ...

10. [[PDF] The crisis of the Turkish lira: Toward economic collapse or a new ...](https://studies.aljazeera.net/sites/default/files/articles/documents/2021-12/The%20crisis%20of%20the%20Turkish%20lira%20Toward%20economic%20collapse%20or%20a%20new%20economic%20model_0.pdf)

11. [Parliament rejects bill to increase pensions to minimum wage level](https://bianet.org/haber/parliament-rejects-bill-to-increase-pensions-to-minimum-wage-level-255178) - The pensions of 70 percent of the retirees were below the minimum wage in 2020.

12. [The Falling Lira | Özgür Orhangazi - Phenomenal World](https://www.phenomenalworld.org/analysis/the-falling-lira/) - The tower came tumbling down in 2018, with a currency crisis followed by interest rate hikes and a r...

13. [The Conviction of Ekrem İmamoğlu and the Prospects for ...](https://www.cats-network.eu/publication/the-conviction-of-ekrem-i%CC%87mamoglu-and-the-prospects-for-democracy-in-turkey) - İmamoğlu's conviction suggests that the government is ready to completely abolish the competitive di...

14. [Turkey elections: Biggest test for Erdogan amid cost of living crisis](https://www.bbc.com/news/world-europe-64413620) - Istanbul's mayor on trial for corruption charges. Ekrem Imamoglu is seen as Turkish President Recep ...

15. [Turkey freezes pro-Kurdish party funds before vote - BBC](https://www.bbc.com/news/world-europe-64179858) - This latest court decision is seen by many in Turkey as a significant marker in favour of the HDP's ...

16. [2023 Turkey–Syria earthquakes - Wikipedia](https://en.wikipedia.org/wiki/2023_Turkey%E2%80%93Syria_earthquakes)

17. [Turkey leader acknowledges earthquake relief problems as death toll passes 12,000](https://japannews.yomiuri.co.jp/news-services/reuters/20230209-89925/) - KAHRAMANMARAS/ANTAKYA, Turkey, Feb 8 (Reuters) – President Tayyip Erdogan on Wednesday admitted ther...

18. [Twitter Was Blocked in Turkey, Internet-Monitoring Group ...](https://www.nytimes.com/2023/02/08/world/europe/turkey-earthquake-twitter-blocked.html) - Twitter was blocked on several networks inside Turkey, according to NetBlocks, a group that tracks i...

19. [Turkey earthquake: 113 arrest warrants connected to building ... - BBC](https://www.bbc.com/news/world-middle-east-64615349) - Officials in Turkey say 113 arrest warrants have been issued in connection with the construction of ...

20. [UNHCR Türkiye Emergency Response to Earthquake (13 February 2023) - Türkiye](https://reliefweb.int/report/turkiye/unhcr-turkiye-emergency-response-earthquake-13-february-2023) - Situation Report in English on Türkiye about Food and Nutrition, Health, Earthquake and more; publis...

21. [Turkish opposition bloc faces split over joint candidate](https://toronto.citynews.ca/2023/03/03/turkish-opposition-bloc-faces-split-over-joint-candidate/) - ISTANBUL (AP) — One of Turkey’s leading opposition politicians indicated Friday that her party is br...

22. [Turkey's opposition names Kilicdaroglu as presidential candidate](https://www.aljazeera.com/news/2023/3/6/turkeys-opposition-names-kilicdaroglu-as-presidential-candidate) - Turkish opposition leader Kemal Kilicdaroglu has been named as the main challenger to President Rece...

23. [Constitutional Court lifts blocking of Treasury aid to HDP - Bianet](https://bianet.org/haber/constitutional-court-lifts-blocking-of-treasury-aid-to-hdp-275440) - The Constitutional Court has today (March 9) lifted the blocking of the People's Democratic Party (H...

24. [Erdoğan raises pensions in run-up to elections amid falling popularity](https://turkishminute.com/2023/03/23/erdogan-raise-pensions-run-up-to-elections-amid-falling-popularity/) - Turkish President Recep Tayyip Erdoğan has announced a TL 2000 ($105) increase in pensions, bringing...

25. [Turkey's pro-Kurdish party backs Erdogan's rival for president](https://www.aljazeera.com/news/2023/4/28/turkeys-pro-kurdish-party-backs-erdogans-rival-for-president) - Party calls on Kurds and other supporters to vote for main opposition alliance's presidential candid...

26. [Turkey raises public worker salaries by 45% days before elections](https://www.aljazeera.com/news/2023/5/9/turkey-raises-public-worker-salaries-by-45-days-before-elections) - President Erdogan makes announcement as he seeks re-election and economic turmoil hurts his chances.

27. [Days ahead of vote, Ince withdraws from Turkey presidential race](https://www.aljazeera.com/news/2023/5/11/days-ahead-of-vote-ince-withdraws-from-turkey-presidential-race) - Ince's withdrawal gives the opposition a possible boost as it seeks to unseat President Erdogan.

28. [Turkey election run-off results 2023 by the numbers - Al Jazeera](https://www.aljazeera.com/news/2023/5/28/follow-the-vote-turkey-election-run-off-results-2023) - Erdogan, who has dominated Turkish politics for 20 years, will now serve another five-year term.

29. [Kilicdaroglu turns to anti-migrant fears before Turkey run-off](https://www.aljazeera.com/news/2023/5/17/kilicdaroglu-turns-to-anti-migrant-fears-before-turkey-run-off) - Kilicdaroglu came second to Erdogan in Sunday's presidential election, and is seeking nationalist su...

30. [Ogan endorses Erdogan in Turkey's presidential run-off](https://www.aljazeera.com/news/2023/5/22/sinan-ogan-endorses-erdogan-in-turkey-election-run-off) - Third-placed candidate says he will support incumbent in Sunday's second round of voting.

31. [Kılıçdaroğlu secures far-right support for presidential runoff, vows to expel '13 million refugees' - Turkish Minute](https://www.turkishminute.com/2023/05/24/kilicdaroglu-secured-far-right-support-for-presidential-runoff-vows-to-expel-13-million-refugees/) - Ahead of a historic election runoff scheduled for May 28, Kemal Kılıçdaroğlu, the main opposition Re...

32. [Kilicdaroglu's dilemma of maintaining support of 'ultranationalists’ and Kurds](https://www.middleeasteye.net/news/turkey-elections-kilicdaroglu-dilemma-keeping-support-ultranationalists-kurds) - Kurds reluctant to vote for opposition leader as he courts far-right party ahead of election run-off

33. [Turkey's Recep Tayyip Erdogan secures victory in runoff election](https://www.npr.org/2023/05/28/1178660299/erdogan-has-claimed-victory-in-turkeys-presidential-runoff-election) - Turkish President Recep Tayyip Erdogan has secured a victory in a historic runoff election, the toug...

34. [Turkey announces final results of June 24 general elections](http://www.xinhuanet.com/english/2018-07/04/c_137301742.htm)

35. [Erdogan declared winner of Turkey presidential vote – DW – 06/25/2018](https://www.dw.com/en/turkeys-erdogan-claims-victory-in-presidential-and-parliamentary-elections/a-44375907) - Turkey's president, Recep Tayyip Erdogan, has won another term, securing an outright majority accord...

36. [US threatens new Turkey sanctions over Christian pastor | Euronews](https://www.euronews.com/business/2018/08/17/us-threatens-new-turkey-sanctions-over-christian-pastor) - President Trump tweeted on Friday (August 17) that the US "will pay nothing" for Andrew Brunson's re...

37. [Turkish Lira Falls Against the Dollar As Trump ... - Business Insider](https://www.businessinsider.com/trump-usa-sanctions-against-turkey-2018-8) - US Treasury Secretary Steven Mnuchin threatened further sanctions against Turkey if it fails to rele...

38. [Turkey, US lift sanctions on officials after pastor's release - Al Jazeera](https://www.aljazeera.com/news/2018/11/2/turkey-us-lift-sanctions-on-officials-after-pastors-release) - Turkey, US lift sanctions on officials after pastor's release. US pastor Andrew Brunson was freed in...

39. [Turkey: Opposition Politicians Detained for Four Years](https://www.hrw.org/news/2020/11/19/turkey-opposition-politicians-detained-four-years) - The Turkish government should immediately release from detention Selahattin Demirtaş, former co-lead...

40. [Turkey's Local Elections: A Blow to the AKP - INSS](https://www.inss.org.il/publication/turkeys-local-elections-blow-akp/) - The results of the local elections held in Turkey on March 31, 2019 dealt a substantive political bl...

41. [A Turning Point for Turkey’s Opposition?](https://carnegieendowment.org/sada/2019/04/a-turning-point-for-turkeys-opposition?lang=en) - The AKP’s losses in key major cities in Turkey’s local elections provide opposition parties the oppo...

42. [Opposition candidate wins Istanbul election rerun - DW.com](https://www.dw.com/en/istanbul-election-rerun-opposition-candidate-wins-key-mayoral-race/a-49321179) - Opposition candidate Ekrem Imamoglu has taken the lead in a high-stakes rerun of Istanbul's mayoral ...

43. [Supreme Election Council Rejects Applications of CHP and İYİ Party](https://bianet.org/haber/supreme-election-council-rejects-applications-of-chp-and-iyi-party-208448) - After the Council annulled the Metropolitan Mayoral elections in İstanbul, where CHP's candidate Ekr...

44. [Kadınlar Emine Bulut cinayetini protesto ediyor: #Ölmekİstemiyorum](https://www.evrensel.net/haber/385419/kadinlar-emine-bulut-cinayetini-protesto-ediyor-olmekistemiyorum) - Eski eşi tarafından öldürülen Emine Bulut için Türkiye'nin pek çok yerinde kadınlar sokağa çıkarak e...

45. [Emine Bulut cinayeti - Vikipedi](https://tr.wikipedia.org/wiki/Emine_Bulut_cinayeti) - Ne olur, ölme!" şeklindeki feryatları duyuldu. Günler sonra cinayet görüntüsünün ve Emine Bulut ile ...

46. [Turkey’s Economy Amid the COVID-19 Pandemic: Measures and Their Impact](https://books.openedition.org/ifeagd/3827) - The COVID-19 pandemic hit Turkey’s economy hard after two years of turbulence and aggravated economi...

47. [Viral year 2020: Turkish economy stands up to COVID challenges](https://aa.com.tr/en/economy/viral-year-2020-turkish-economy-stands-up-to-covid-challenges/2081059)

48. [Women rally in Istanbul before rights treaty formal exit – DW – 06/19/2021](https://www.dw.com/en/turkey-women-rally-ahead-of-rights-treaty-official-exit/a-57969132) - Protesters have called on President Recep Tayyip Erdogan to reverse Turkey's withdrawal from the Ist...

49. [Turkey's rights treaty pullout sparks more protests – DW – 07/01/2021](https://www.dw.com/en/turkeys-istanbul-convention-exit-sparks-more-protests/a-58129917) - Turkey has formally withdrawn from the international accord on violence against women. President Rec...

50. [Protests over Turkey's withdrawal from women's treaty](https://www.euronews.com/2021/03/21/protests-over-turkey-s-withdrawal-from-women-s-treaty) - Thousands of protesters took to the streets of Istanbul after Turkey pulled out of an international ...

51. [Turkey's Constitutional Court suspends payment of treasury funds to ...](https://www.hdp.org.tr/en/turkey-s-constitutional-court-suspends-payment-of-treasury-funds-to-the-hdp/17044) - The Constitutional Court temporarily blocked the treasury funds that were due to be paid to the HDP....

52. [Current account deficit and foreign-currency debt](https://wikipedia.nucleos.com/viewer/wikipedia_en_all_maxi_2025-08/Turkish_economic_crisis_(2018%E2%80%93current))

53. [Turbulent stabilisation: Turkey's economy under Şimşek's supervision](https://www.osw.waw.pl/en/publikacje/analyses/2025-07-09/turbulent-stabilisation-turkeys-economy-under-simseks-supervision) - The second stabilisation attempt occurred in the run-up to the May 2023 elections, when inflation fe...

54. [How does the Imamoğlu sentencing affect politics? - SETA](https://www.setav.org/en/how-does-the-imamoglu-sentencing-affect-politics) - Since either court could disagree with the verdict, Imamoğlu's prison sentence and ban from politics...

55. [Istanbul Mayor Imamoğlu receives prison sentence for insulting YSK](https://www.dailysabah.com/politics/elections/istanbul-mayor-imamoglu-receives-prison-sentence-for-insulting-ysk) - Istanbul Metropolitan Municipality Mayor Ekrem Imamoğlu was sentenced to two years and seven months ...

56. [UNHCR Türkiye Emergency Response to Earthquake (9 February 2023)](https://reliefweb.int/report/turkiye/unhcr-turkiye-emergency-response-earthquake-9-february-2023) - Situation Report in English on Türkiye about Protection and Human Rights, Shelter and Non-Food Items...

57. [Disaster management following the great Kahramanmaraş ...](https://nhess.copernicus.org/articles/25/2031/2025/) - Abstract. Türkiye experienced devastating earthquakes in Kahramanmaraş on 6 February 2023, making it...

58. [Turkish police chase down social media users who shared ...](https://nordicmonitor.com/2023/02/turkish-police-chase-up-social-media-users-who-shared-critical-messages-after-massive-earthquakes/) - Levent Kenez /Stockholm

59. [Twitter restricted in Turkey two days after quake, says ...](https://www.reuters.com/business/media-telecom/twitter-restricted-turkey-netblocks-2023-02-08/) - "Real-time network data show Twitter has been restricted in Turkey; the filtering is applied on majo...

60. ['We cut the internet during the earthquake, because...'](https://bianet.org/haber/we-cut-the-internet-during-the-earthquake-because-276948) - Two days after the devastating earthquakes, authorities restricted the bandwidth of Twitter for near...

61. [Arrests over Turkey quakes increase to 298 - Bianet](https://bianet.org/haber/arrests-over-turkey-quakes-increase-to-298-276012) - There are a total of 1325 suspects. Prosecutors issued arrest warrants against 305 suspects and dete...

62. [Turkey earthquake: Nearlly 200 arrested for alleged poor building ...](https://edition.cnn.com/2023/02/26/europe/turkey-earthquake-arrests-intl) - Nearly 200 people have been arrested for alleged poor building construction following the catastroph...

63. [Contractors arrested in Turkey as poor construction is partly blamed ...](https://www.lemonde.fr/en/turkey/article/2023/02/12/contractors-arrested-in-turkey-as-poor-construction-is-blamed-for-increasing-devastation_6015396_219.html) - Turkish officials detained or issued arrest warrants for some 130 people allegedly involved in the c...

64. [To write history or to be history: İYİ Parti seems to have chosen the latter](https://bianet.org/haber/to-write-history-or-to-be-history-iyi-parti-seems-to-have-chosen-the-latter-275249) - İYİ Party broke the ranks of the opposition alliance and left the table when only a short time was l...

65. [Turkey's opposition picks Kemal Kilicdaroglu to take on Erdogan in ...](https://www.lemonde.fr/en/elections/article/2023/03/07/turkey-s-opposition-picks-candidate-to-take-on-erdogan-in-may-election_6018420_84.html) - A six-party alliance on Monday nominated the main opposition party leader as its common candidate to...

66. [Turkiye’s Opposition Is Gambling: 72 Critical Hours Decided the Name of Erdogan’s Rival](https://www.alestiklal.net/en/article/turkiyes-opposition-is-gambling-72-critical-hours-decided-the-name-of-erdogans-rival)

67. [The Kurdish Vote and the Turkish Election](https://carnegieendowment.org/sada/2023/04/the-kurdish-vote-and-the-turkish-election?lang=en) - The pro-Kurdish HDP has come out of the shadows to support Kemal Kilicdaroglu’s candidacy.

68. [Turkish opposition candidate Muharrem Ince drops out of election race](https://www.dailysabah.com/politics/turkish-opposition-candidate-muharrem-ince-drops-out-of-election-race/news) - In a shocking move just days ahead of the Turkish elections, Muharrem Ince, a contender against Pres...

69. [What's a run-off? All to know about Turkey election results](https://www.aljazeera.com/news/2023/5/15/whats-a-runoff-everything-to-know-about-turkey-election-results) - This is the first time Erdogan faces a second-round run-off vote as a presidential candidate.

70. ['Syrians will go!' As Turkey's election runoff nears, refugees face new threats](https://www.latimes.com/world-nation/story/2023-05-26/syrian-refugees-face-new-threats-turkey-presidential-election) - The election battle between Turkey's president and his main challenger is increasingly focused on on...

71. [Ogan endorses Erdogan in Turkish election runoff](https://www.middleeasteye.net/news/turkey-elections-ogan-endorse-erdogan-presidential-run-off) - Third-placed ultra-nationalist candidate announces support for the president in a televised statemen...

72. [Turkey election: Third-place finisher endorses Erdogan – DW – 05/22/2023](https://www.dw.com/en/turkey-election-third-place-finisher-endorses-erdogan/a-65701274) - Ultra-nationalist Sinan Ogan has thrown his support behind the incumbent in the runoff vote. He had ...

73. [Turkey election: Anti-migration leader backs Erdogan rival – DW – 05/24/2023](https://www.dw.com/en/turkey-election-anti-migration-party-backs-erdogan-rival/a-65718474) - Opposition candidate Kemal Kilicdaroglu and President Recep Tayyip Erdogan have each racked up high-...

74. [HDP, pseudo-left back anti-refugee, anti-Kurdish candidate Kılıçdaroğlu in Turkish elections](https://www.wsws.org/en/articles/2023/05/26/byfs-m26.html) - The Kurdish-nationalist HDP is backing Kılıçdaroğlu’s right-wing campaign even after he pledged to a...

75. [Turkish Supreme Election Council officially declares Erdogan ...](https://www.aa.com.tr/en/politics/turkish-supreme-election-council-officially-declares-erdogan-winner-of-presidential-runoff/2911800) - Final results of elections show Recep Tayyip Erdogan received 52.18% of votes, while opposition lead...

76. [Political Coalitions in Turkey in the Run-Up to the 2023 Elections | Ifri](https://www.ifri.org/en/studies/political-coalitions-turkey-run-2023-elections) - The electoral campaign is polarized around two major coalitions: the People's Alliance, led by the p...

77. [Selahattin Demirtaş](https://humanrightscommission.house.gov/DFP/Countries/Turkey/Selahattin-Demirtas) - Status: Imprisoned Country: Turkey Advocate: Rep. Jamie Raskin (D-MD)

