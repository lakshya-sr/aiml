
Name: Lakshya Shrivastav

PRN: 202401040338

Roll: 321


# Weighted-Scoring Computer Troubleshooting Expert System

## Overview

This system diagnoses computer problems from a list of observed symptoms
using a **weighted scoring model** instead of the traditional rule-chaining
approach (`IF symptom AND symptom THEN diagnosis`) used in the original
version. It is implemented in Prolog in about 65 lines and 26 facts.

## Methodology

1. **Weights** — Each symptom is linked to one or more problem categories
   (`power`, `performance`, `thermal`, `display`, `storage`, `network`,
   `security`, `software`) with a point value reflecting how strongly it
   indicates that category. For example, `computer_overheats` scores 3
   points toward `thermal`, while `computer_is_slow` scores only 1 point,
   split between `performance` and `thermal`.

2. **Scoring** — Given a list of symptoms, the system sums the points
   each symptom contributes to every category.

3. **Ranking** — All categories are sorted by total score, highest first.

4. **Decision** — The top-scoring category is reported as the likely
   cause, paired with its recommendation. If no symptoms match anything,
   the system reports no identifiable issue rather than guessing.

## Code

```prolog


weight(no_power,                power,       3).
weight(power_light_off,         power,       2).
weight(battery_not_charging,    power,       2).

weight(high_cpu_usage,          performance, 2).
weight(high_memory_usage,       performance, 2).
weight(computer_is_slow,        performance, 1).
weight(system_freezes,          performance, 2).

weight(fan_runs_fast,           thermal,     2).
weight(computer_overheats,      thermal,     3).
weight(computer_shuts_down,     thermal,     2).

weight(no_display,              display,     3).
weight(screen_flickers,         display,     2).
weight(display_has_lines,       display,     2).

weight(disk_error,              storage,     3).
weight(strange_disk_noise,      storage,     3).
weight(files_disappear,         storage,     2).
weight(disk_is_full,            storage,     1).

weight(no_internet,             network,     3).
weight(wifi_not_detected,       network,     2).
weight(wifi_disconnects,        network,     2).
weight(cannot_connect_to_router, network,    2).

weight(unwanted_popups,         security,    3).
weight(unknown_programs_running, security,   3).
weight(browser_redirects,       security,    2).

weight(application_crashes,     software,    2).
weight(error_message,           software,    1).
weight(blue_screen,             software,    2).


% ------------------------------------------------------------
% 2. RECOMMENDATIONS: one per category
% ------------------------------------------------------------

recommendation(power,       'Check the power cable, adapter, and battery.').
recommendation(performance, 'Close resource-heavy programs; check RAM/CPU usage.').
recommendation(thermal,     'Clean the cooling system and improve ventilation.').
recommendation(display,     'Check the display cable and graphics card.').
recommendation(storage,     'Back up your data and check the disk for errors.').
recommendation(network,     'Restart the router and check the network adapter/driver.').
recommendation(security,    'Run an antivirus scan and remove suspicious software.').
recommendation(software,    'Update, reinstall, or repair the affected application/OS.').



% Total score a list of symptoms gives to one category.
category_score(Symptoms, Category, Score) :-
    findall(W, (member(S, Symptoms), weight(S, Category, W)), Ws),
    sum_list(Ws, Score).

% Every category that appears in the weight table.
all_categories(Cats) :-
    setof(C, S^W^weight(S, C, W), Cats).

% Rank all categories by score, highest first.
rank(Symptoms, Ranked) :-
    all_categories(Cats),
    findall(Score-Cat, (member(Cat, Cats), category_score(Symptoms, Cat, Score)), Pairs),
    sort(0, @>=, Pairs, Ranked).



report(Symptoms) :-
    rank(Symptoms, Ranked),
    format('~nSymptom score by category:~n'),
    forall(member(Sc-Cat, Ranked), format('  ~w: ~w~n', [Cat, Sc])),
    ( Ranked = [TopScore-TopCat|_], TopScore > 0
    -> recommendation(TopCat, Rec),
       format('~nLikely cause: ~w (score ~w)~nRecommendation: ~w~n', [TopCat, TopScore, Rec])
    ;  format('~nNo matching issue found for the given symptoms.~n')
    ).
```
## Example

```prolog
?- report([high_cpu_usage, computer_is_slow, system_freezes]).

Symptom score by category:
  performance: 5
  thermal: 0
  storage: 0
  software: 0
  security: 0
  power: 0
  network: 0
  display: 0

Likely cause: performance (score 5)
Recommendation: Close resource-heavy programs; check RAM/CPU usage.
true.
```

Here, `computer_is_slow` slightly boosts `performance`, but `thermal`
still wins decisively because two strong, specific symptoms
(`fan_runs_fast`, `computer_overheats`) point directly at it.


