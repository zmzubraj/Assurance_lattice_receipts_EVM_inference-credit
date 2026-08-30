#!/usr/bin/env python3
"""Generate editable tables and a vector TikZ figure from canonical ALR outputs."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "04-data/development/alr-pilot-v1-run-001"
TABLES = ROOT / "06-visuals/tables"
FIGURES = ROOT / "06-visuals/figures"


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def latex_escape(value: str) -> str:
    replacements = {"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#"}
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def main() -> int:
    base = list(csv.DictReader((RUN / "base-results.csv").open(encoding="utf-8")))
    mutations = list(csv.DictReader((RUN / "mutation-results.csv").open(encoding="utf-8")))
    primary = list(csv.DictReader((ROOT / "05-analysis/results/primary-results.csv").open(encoding="utf-8")))

    t2 = [
        {"method": "ALR candidate", "baseline_type": "proposed development artifact", "metric": "cross-runtime conformance", "estimate": "736/736", "uncertainty": "development-only; independent verification pending", "sample_size": 736, "source_artifact": "05-analysis/results/primary-results.csv"},
        {"method": "LATTICE", "baseline_type": "strongest governance predecessor", "metric": "feature-overlap disposition", "estimate": "close/defeating", "uncertainty": "independent full-text reconciliation pending", "sample_size": 1, "source_artifact": "01-novelty/novelty-matrix.csv"},
        {"method": "Tool Receipts / NabaOS", "baseline_type": "receipt predecessor", "metric": "feature-overlap disposition", "estimate": "close/defeating", "uncertainty": "settlement materiality unresolved", "sample_size": 1, "source_artifact": "01-novelty/novelty-matrix.csv"},
        {"method": "opML", "baseline_type": "optimistic ML verification predecessor", "metric": "primitive-novelty disposition", "estimate": "defeats primitive claim", "uncertainty": "composition obviousness unresolved", "sample_size": 1, "source_artifact": "01-novelty/novelty-matrix.csv"},
        {"method": "EigenAI", "baseline_type": "deterministic inference predecessor", "metric": "feature-overlap disposition", "estimate": "close", "uncertainty": "lifecycle difference unresolved", "sample_size": 1, "source_artifact": "01-novelty/novelty-matrix.csv"},
    ]
    write_csv(TABLES / "t2-proposed-vs-baselines.csv", list(t2[0]), t2)

    t3 = [
        {"condition_id": "BASE", "dataset_or_cohort": "complete synthetic assurance-state matrix", "population_or_setting": "local Python and Solidity development execution", "sample_size": 729, "inclusion": "all 3^6 tuples", "exclusion": "none", "provenance": "04-data/development/alr-pilot-v1-run-001/base-results.csv"},
        {"condition_id": "MUTATION", "dataset_or_cohort": "prespecified single-fault binding mutations", "population_or_setting": "all-PASS receipt with one failed binding", "sample_size": 7, "inclusion": "all seven named families", "exclusion": "compound mutations", "provenance": "04-data/development/alr-pilot-v1-run-001/mutation-results.csv"},
        {"condition_id": "REPLAY", "dataset_or_cohort": "same-owner deterministic replay", "population_or_setting": "same machine and toolchain", "sample_size": 3, "inclusion": "base CSV; mutation CSV; Python summary", "exclusion": "timing-bearing logs", "provenance": "05-analysis/reproducibility-report.md"},
    ]
    write_csv(TABLES / "t3-data-or-conditions.csv", list(t3[0]), t3)

    dimensions = ["execution", "semantic", "authority", "provenance", "freshness", "origin_scope"]
    t5 = []
    for dimension in dimensions:
        affected = [row for row in base if row[dimension] != "PASS"]
        activations = sum(row["observed_eligible"] == "true" for row in affected)
        t5.append({"component": dimension, "condition": f"{dimension} is FAIL or UNKNOWN", "metric": "unsafe activations", "estimate": f"{activations}/{len(affected)}", "uncertainty": "complete finite subset; no sampling interval", "interpretation": "fails closed within frozen model"})
    t5.append({"component": "exact bindings", "condition": "one binding fails while all dimensions PASS", "metric": "unsafe activations", "estimate": f"{sum(row['observed_eligible']=='true' for row in mutations)}/{len(mutations)}", "uncertainty": "seven named single-fault families only", "interpretation": "fails closed for prespecified mutations"})
    write_csv(TABLES / "t5-ablation-or-mechanism.csv", list(t5[0]), t5)

    t7 = [
        {"factor": "functional conformance", "setting": "same-owner local development", "measure": "shared-vector agreement", "estimate": "736/736", "uncertainty": "synthetic local scope", "threshold": "736/736", "decision": "PASS_DEVELOPMENT", "failure_mode": "independent verification absent"},
        {"factor": "gas boundedness", "setting": "Foundry test harness", "measure": "test-call gas", "estimate": "5491690 base; 39023 mutations", "uncertainty": "not transaction or production gas", "threshold": "NOT_FROZEN", "decision": "NOT_ASSESSABLE", "failure_mode": "no fair baseline"},
        {"factor": "external reproducibility", "setting": "independent machine/operator", "measure": "reproduction status", "estimate": "not performed", "uncertainty": "same-owner replay only", "threshold": "independent signed replay", "decision": "BLOCKED", "failure_mode": "external reviewer pending"},
        {"factor": "real-world validity", "setting": "production or field", "measure": "field evidence", "estimate": "absent", "uncertainty": "out of MPP scope", "threshold": "N/A only after claim narrowing", "decision": "NO_CLAIM", "failure_mode": "cannot generalize beyond local model"},
    ]
    write_csv(TABLES / "t7-real-world-feasibility.csv", list(t7[0]), t7)
    write_csv(TABLES / "t4-primary-results.csv", list(primary[0]), primary)

    reason_groups = Counter()
    for row in base:
        reason = row["observed_reason"]
        group = "Eligible" if reason == "ELIGIBLE" else reason.rsplit("_", 1)[0].replace("_", " ").title()
        reason_groups[group] += 1
    order = ["Execution", "Semantic", "Authority", "Provenance", "Freshness", "Origin Scope", "Eligible"]
    figure_rows = [{"first_reason_group": name, "state_count": reason_groups[name]} for name in order]
    write_csv(FIGURES / "reason-distribution-data.csv", ["first_reason_group", "state_count"], figure_rows)

    max_count = max(row["state_count"] for row in figure_rows)
    bar_width = 0.72
    pieces = [r"\begin{tikzpicture}[x=1.15cm,y=0.011cm]", r"\draw[->] (-0.55,0) -- (6.75,0) node[right,font=\scriptsize]{First decision group};", r"\draw[->] (-0.55,0) -- (-0.55,535) node[above,font=\scriptsize]{States};"]
    for tick in [0, 100, 200, 300, 400, 500]:
        pieces.append(rf"\draw[gray!35] (-0.6,{tick}) -- (6.55,{tick});")
        pieces.append(rf"\node[anchor=east,font=\tiny] at (-0.62,{tick}) {{{tick}}};")
    for index, row in enumerate(figure_rows):
        value = row["state_count"]
        fill = "blue!62" if row["first_reason_group"] != "Eligible" else "orange!75"
        left = f"{index-bar_width/2:.2f}"
        right = f"{index+bar_width/2:.2f}"
        pieces.append(rf"\filldraw[fill={fill},draw=black] ({left},0) rectangle ({right},{value});")
        pieces.append(rf"\node[font=\tiny,anchor=south] at ({index},{value+5}) {{{value}}};")
        label = latex_escape(row["first_reason_group"])
        pieces.append(rf"\node[font=\tiny,rotate=40,anchor=east] at ({index},-8) {{{label}}};")
    pieces.append(r"\end{tikzpicture}")
    (FIGURES / "reason-distribution-content.tex").write_text("\n".join(pieces) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
