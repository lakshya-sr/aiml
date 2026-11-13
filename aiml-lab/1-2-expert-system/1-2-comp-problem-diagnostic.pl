

% 1. SYMPTOM WEIGHTS

weight(no_power, power, 3).
weight(power_light_off, power, 2).
weight(battery_not_charging, power, 2).

weight(high_cpu_usage, performance, 2).
weight(high_memory_usage, performance, 2).
weight(computer_is_slow, performance, 1).
weight(system_freezes, performance, 2).

weight(fan_runs_fast, thermal, 2).
weight(computer_overheats, thermal, 3).
weight(computer_shuts_down, thermal, 2).

weight(no_display, display, 3).
weight(screen_flickers, display, 2).
weight(display_has_lines, display, 2).

weight(disk_error, storage, 3).
weight(strange_disk_noise, storage, 3).
weight(files_disappear, storage, 2).
weight(disk_is_full, storage, 1).

weight(no_internet, network, 3).
weight(wifi_not_detected, network, 2).
weight(wifi_disconnects, network, 2).
weight(cannot_connect_to_router, network, 2).

weight(unwanted_popups, security, 3).
weight(unknown_programs_running, security, 3).
weight(browser_redirects, security, 2).

weight(application_crashes, software, 2).
weight(error_message, software, 1).
weight(blue_screen, software, 2).


% 2. RECOMMENDATIONS

recommendation(power,
    'Check the power cable, adapter, and battery.').

recommendation(performance,
    'Close resource-heavy programs; check RAM/CPU usage.').

recommendation(thermal,
    'Clean the cooling system and improve ventilation.').

recommendation(display,
    'Check the display cable and graphics card.').

recommendation(storage,
    'Back up your data and check the disk for errors.').

recommendation(network,
    'Restart the router and check the network adapter/driver.').

recommendation(security,
    'Run an antivirus scan and remove suspicious software.').

recommendation(software,
    'Update, reinstall, or repair the affected application/OS.').


% 3. SCORING

category_score(Symptoms, Category, Score) :-
    findall(W,
        (member(S, Symptoms), weight(S, Category, W)),
        Ws),
    sum_list(Ws, Score).


% 4. GET ALL CATEGORIES

all_categories(Cats) :-
    setof(C, S^W^weight(S, C, W), Cats).


% 5. RANK CATEGORIES

rank(Symptoms, Ranked) :-
    all_categories(Cats),
    findall(Score-Cat,
        (member(Cat, Cats),
         category_score(Symptoms, Cat, Score)),
        Pairs),
    sort(0, @>=, Pairs, Ranked).


% 6. REPORT RESULTS

report(Symptoms) :-
    rank(Symptoms, Ranked),
    format('~nSymptom score by category:~n'),
    forall(
        member(Sc-Cat, Ranked),
        format(' ~w: ~w~n', [Cat, Sc])
    ),
    ( Ranked = [TopScore-TopCat|_],
      TopScore > 0
    -> recommendation(TopCat, Rec),
       format(
           '~nLikely cause: ~w (score ~w)~nRecommendation: ~w~n',
           [TopCat, TopScore, Rec]
       )
    ;  format(
           '~nNo matching issue found for the given symptoms.~n'
       )
    ).
