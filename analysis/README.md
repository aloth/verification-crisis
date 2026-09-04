# Reproducing the deposited statistics

This directory recomputes the summary table that ships with the Harvard Dataverse deposit, directly from the response file in the same deposit. It is an internal-consistency check: the numbers a reuser sees in the table are shown to follow from the data next to them.

It reads only openly licensed files. Both inputs come from [`doi:10.7910/DVN/BXO2QA`](https://doi.org/10.7910/DVN/BXO2QA) under CC0 1.0: the de-identified responses (54 observations, 41 variables) and `table_item_means_sd.tab`. Nothing here touches the restricted Zenodo deposit, and no identifying field is read, because none is present in the public file.

## Run it

```sh
./fetch_data.sh
python3 recompute_published_statistics.py
```

No dependencies beyond the Python standard library. Python 3.9 or later.

Expected output:

```
Responses: 54 rows, 41 columns
Table: 33 tabulated items

33/33 tabulated items reproduce exactly.
Every tabulated mean and SD recomputes from the response file.
```

## What it checks

For each of the 33 items in `table_item_means_sd.tab`, the script recomputes `n`, the mean and the standard deviation from the response file and compares all three at two decimal places. Any disagreement is printed and the script exits non-zero, so it works as a regression check rather than only as a demonstration.

## Two things worth knowing before you reuse this

**The deposited table uses the sample standard deviation (`ddof=1`).** The script follows that convention so its output lines up with the table. A recomputation using a population SD lands slightly lower, by roughly 0.01 to 0.02 per item at N=54.

**Columns are addressed by name, not by position.** The public deposit has 41 variables; the collection instrument has 58. Seventeen were removed before publication, so any position-based mapping written against the collection file silently reads the wrong column here. The table truncates long item labels, so the script matches on a label prefix and walks both files in the same column order.

## Scope

This covers the item-level descriptive statistics in that one table. Best-Worst Scaling counts, the ranking analysis and the qualitative coding are reported in the accompanying publications and are not recomputed here.
