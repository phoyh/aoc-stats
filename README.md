This is the home of my personal times, ranks and scores on [Advent of Code](https://adventofcode.com/).

Note that only those dates are included on which I participated in a *"competitive"* manner (i.e., being available at 6am CET).

# Series Table
Rank by Quantile
```
Year | Best |  5% | 10% | 20% |  30% | Median |  75% |  90% | Worst
===================================================================
2021 |  128 | 137 | 142 | 351 |  544 |   1088 | 2110 | 2864 |  3617
2022 |   73 | 141 | 431 | 495 | 1042 |   1323 | 2177 | 4454 |  6540
2023 |   45 | 226 | 230 | 340 |  473 |    765 | 1655 | 2563 |  3932
```
Frequency by Rank
```
Year | 100 | 150 | 200 | 300 | 500 | 700 | 1000 | 1500 | 2000 | 3000 | 5000
===========================================================================
2021 |  0% | 10% | 13% | 16% | 26% | 36% |  40% |  66% |  73% |  90% | 100%
2022 |  3% |  6% |  9% |  9% | 21% | 21% |  25% |  53% |  71% |  81% |  93%
2023 |  4% |  4% |  4% | 16% | 32% | 44% |  58% |  74% |  80% |  90% | 100%
```

# Series Chart

```mermaid
flowchart TD 
style 2021 fill:#f84,stroke:#333,stroke-width:2px,color:#fff
style 2022 fill:#1d6,stroke:#333,stroke-width:2px,color:#fff
style 2023 fill:#77f,stroke:#333,stroke-width:2px,color:#fff
```

![Metrics](/cumulative-rank-frequency.svg)

# Overall
```mermaid
%%{init: {"themeVariables": {"pie1": "#e2e200", "pie2": "#0b510b", "pie3": "#f03a3a", "pie4": "#a81d1d", "pie5": "#999900", "pie6": "#0081d3", "pie7": "#004e8b", "pie8": "#287d28", "pie9": "#62d362", "pie10": "#80ff80", "pie11": "#45a845", "pie12": "#600000"}}}%%
pie
title Ranking within Top-k Segment
"25 * [1001, 1500]": 25
"15 * [301, 500]": 15
"13 * [2001, 3000]": 13
"12 * [3001, 5000]": 12
"11 * [1501, 2000]": 11
"9 * [501, 700]": 9
"9 * [701, 1000]": 9
"7 * [201, 300]": 7
"4 * [101, 150]": 4
"3 * [1, 100]": 3
"2 * [151, 200]": 2
"2 * [5001, 6540]": 2
```
