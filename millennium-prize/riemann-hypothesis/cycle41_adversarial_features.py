#!/usr/bin/env python3
"""Adversarial arithmetic classification of the Cycle 40 negative H bands.

Arithmetic covariates are integer-valued.  The labels come from the certified
Arb signs in cycle40-data/local-unit-kappa.csv; floating point is used only by
the statistical classifiers, never to construct an arithmetic feature.
"""

import argparse
import csv
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


FEATURE_NAMES = (
    "mu", "mertens", "abs_mertens", "mertens_d1", "mertens_back4",
    "mertens_forward4", "mertens_back8", "mertens_forward8",
    "is_prime", "omega", "bigomega", "is_squarefree", "is_prime_power",
    "prime_power_exponent", "prime_gap", "distance_prev_prime",
    "distance_next_prime", "squarefree_run_left", "squarefree_run_right",
    "squarefree_count_5", "squarefree_count_9", "prime_power_count_9",
    "psi_bit_mass_d1", "psi_bit_mass_back4", "psi_bit_mass_forward4",
    "psi_bit_curvature4",
)


def arithmetic_tables(limit):
    """Build exact integer arithmetic tables through limit."""
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for p in range(2, int(limit ** 0.5) + 1):
        if spf[p] == p:
            for multiple in range(p * p, limit + 1, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p

    mu = [0] * (limit + 1)
    omega = [0] * (limit + 1)
    bigomega = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        q = n
        distinct = 0
        total = 0
        square = False
        while q > 1:
            p = spf[q]
            exponent = 0
            while q % p == 0:
                q //= p
                exponent += 1
            distinct += 1
            total += exponent
            square |= exponent > 1
        omega[n] = distinct
        bigomega[n] = total
        mu[n] = 0 if square else (-1 if distinct % 2 else 1)

    primes = [n for n in range(2, limit + 1) if spf[n] == n]
    is_prime = [0] * (limit + 1)
    for p in primes:
        is_prime[p] = 1

    pp_exponent = [0] * (limit + 1)
    pp_base = [0] * (limit + 1)
    psi_bit_jump = [0] * (limit + 1)
    for p in primes:
        value = p
        exponent = 1
        while value <= limit:
            pp_exponent[value] = exponent
            pp_base[value] = p
            # An exact integer proxy for the log(p) mass in Lambda(value).
            psi_bit_jump[value] = p.bit_length()
            if value > limit // p:
                break
            value *= p
            exponent += 1

    mertens = [0] * (limit + 1)
    psi_bit_mass = [0] * (limit + 1)
    for n in range(1, limit + 1):
        mertens[n] = mertens[n - 1] + mu[n]
        psi_bit_mass[n] = psi_bit_mass[n - 1] + psi_bit_jump[n]
    return {
        "spf": spf,
        "mu": mu,
        "omega": omega,
        "bigomega": bigomega,
        "is_prime": is_prime,
        "pp_exponent": pp_exponent,
        "pp_base": pp_base,
        "psi_bit_jump": psi_bit_jump,
        "psi_bit_mass": psi_bit_mass,
        "mertens": mertens,
        "primes": primes,
    }


def interval_sum(prefix, left, right):
    left = max(1, left)
    right = min(len(prefix) - 1, right)
    return prefix[right] - prefix[left - 1] if left <= right else 0


def feature_rows(start, stop, radius=12):
    """Return (n, integer feature dict) for start <= n <= stop."""
    tables = arithmetic_tables(stop + radius + 2)
    mu = tables["mu"]
    mertens = tables["mertens"]
    is_prime = tables["is_prime"]
    pp_exp = tables["pp_exponent"]
    psi = tables["psi_bit_mass"]

    squarefree_prefix = [0] * len(mu)
    pp_prefix = [0] * len(mu)
    for n in range(1, len(mu)):
        squarefree_prefix[n] = squarefree_prefix[n - 1] + int(mu[n] != 0)
        pp_prefix[n] = pp_prefix[n - 1] + int(pp_exp[n] != 0)

    previous_prime = [0] * len(mu)
    latest = 0
    for n in range(len(mu)):
        if is_prime[n]:
            latest = n
        previous_prime[n] = latest
    next_prime = [0] * len(mu)
    latest = 0
    for n in range(len(mu) - 1, -1, -1):
        if is_prime[n]:
            latest = n
        next_prime[n] = latest

    rows = []
    for n in range(start, stop + 1):
        left_run = 0
        while n - left_run >= 1 and mu[n - left_run] != 0:
            left_run += 1
        right_run = 0
        while n + right_run < len(mu) and mu[n + right_run] != 0:
            right_run += 1
        prev_p = previous_prime[n]
        next_p = next_prime[n]
        prior_strict = previous_prime[n - 1]
        next_strict = next_prime[n + 1]
        enclosing_left = prior_strict if is_prime[n] else prev_p
        enclosing_right = next_strict if is_prime[n] else next_p
        values = {
            "mu": mu[n],
            "mertens": mertens[n],
            "abs_mertens": abs(mertens[n]),
            "mertens_d1": mu[n],
            "mertens_back4": interval_sum(mertens, n - 3, n),
            "mertens_forward4": interval_sum(mertens, n, n + 3),
            "mertens_back8": interval_sum(mertens, n - 7, n),
            "mertens_forward8": interval_sum(mertens, n, n + 7),
            "is_prime": is_prime[n],
            "omega": tables["omega"][n],
            "bigomega": tables["bigomega"][n],
            "is_squarefree": int(mu[n] != 0),
            "is_prime_power": int(pp_exp[n] != 0),
            "prime_power_exponent": pp_exp[n],
            "prime_gap": enclosing_right - enclosing_left,
            "distance_prev_prime": n - prev_p,
            "distance_next_prime": next_p - n,
            "squarefree_run_left": left_run,
            "squarefree_run_right": right_run,
            "squarefree_count_5": interval_sum(squarefree_prefix, n - 2, n + 2),
            "squarefree_count_9": interval_sum(squarefree_prefix, n - 4, n + 4),
            "prime_power_count_9": interval_sum(pp_prefix, n - 4, n + 4),
            "psi_bit_mass_d1": tables["psi_bit_jump"][n],
            "psi_bit_mass_back4": interval_sum(psi, n - 3, n),
            "psi_bit_mass_forward4": interval_sum(psi, n, n + 3),
            "psi_bit_curvature4": (
                interval_sum(psi, n, n + 3) - interval_sum(psi, n - 3, n)
            ),
        }
        rows.append((n, values))
    return rows


def load_labels(path):
    labels = {}
    with path.open(newline="", encoding="ascii") as handle:
        for row in csv.DictReader(handle):
            labels[int(row["n"])] = int(row["half_surplus"].lstrip().startswith("[-"))
    return labels


def runs(indices):
    result = []
    for n in sorted(indices):
        if not result or n != result[-1][-1] + 1:
            result.append([n])
        else:
            result[-1].append(n)
    return [(run[0], run[-1]) for run in result]


def confusion(y_true, y_pred):
    counts = Counter(zip(y_true, y_pred))
    return {
        "tp": counts[(1, 1)], "fp": counts[(0, 1)],
        "tn": counts[(0, 0)], "fn": counts[(1, 0)],
    }


def threshold_audit(X, y, names):
    """Find the best iff threshold for every scalar feature and expose errors."""
    audits = []
    for column, name in enumerate(names):
        values = sorted(set(int(row[column]) for row in X))
        candidates = [values[0] - 1] + values
        best = None
        for direction in ("<=", ">"):
            for threshold in candidates:
                pred = [int(v[column] <= threshold) if direction == "<="
                        else int(v[column] > threshold) for v in X]
                cm = confusion(y, pred)
                # Raw accuracy rewards the vacuous all-positive classifier in
                # this 12-versus-2034 data set.  Rank by balanced error first.
                fn_rate = cm["fn"] / (cm["tp"] + cm["fn"])
                fp_rate = cm["fp"] / (cm["tn"] + cm["fp"])
                balanced_error = (fn_rate + fp_rate) / 2
                errors = cm["fp"] + cm["fn"]
                score = (balanced_error, cm["fn"], cm["fp"], threshold)
                if best is None or score < best[0]:
                    bad = [i for i, (actual, guess) in enumerate(zip(y, pred))
                           if actual != guess]
                    best = (score, direction, threshold, cm, bad)
        audits.append({
            "feature": name,
            "direction": best[1],
            "threshold": best[2],
            "confusion": best[3],
            "balanced_accuracy": 1 - best[0][0],
            "error_count": best[3]["fp"] + best[3]["fn"],
            "counterexample_rows": best[4][:12],
        })
    return sorted(audits, key=lambda item: (-item["balanced_accuracy"], item["feature"]))


def necessary_screen(X, y, names, max_literals=3):
    """Find a short conjunction containing every observed negative cell."""
    positives = [i for i, label in enumerate(y) if label]
    literals = []
    for column, name in enumerate(names):
        low = min(X[i][column] for i in positives)
        high = max(X[i][column] for i in positives)
        literals.extend([
            (f"{name} >= {low}", lambda row, c=column, t=low: row[c] >= t),
            (f"{name} <= {high}", lambda row, c=column, t=high: row[c] <= t),
        ])
    best = None
    for size in range(1, max_literals + 1):
        for selected in combinations(literals, size):
            pred = [int(all(test(row) for _, test in selected)) for row in X]
            cm = confusion(y, pred)
            if cm["fn"]:
                continue
            score = (cm["fp"], size, tuple(text for text, _ in selected))
            if best is None or score < best[0]:
                best = (score, pred, cm)
    return {
        "condition": " and ".join(best[0][2]),
        "confusion": best[2],
        "false_positive_rows": [i for i, (label, pred) in enumerate(zip(y, best[1]))
                                if not label and pred][:30],
        "status": "finite necessary screen only; sufficiency is falsified by false positives",
    }


def classify(X, y, ns, seed):
    from sklearn.ensemble import ExtraTreesClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score, balanced_accuracy_score, roc_auc_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier, export_text

    # Contiguous 32-cell groups prevent adjacent members of a band leaking
    # between train and test.  This is deliberately harsher than random CV.
    groups = [(n - ns[0]) // 32 for n in ns]
    models = {
        "logistic": lambda: make_pipeline(
            StandardScaler(), LogisticRegression(
                class_weight="balanced", max_iter=5000, random_state=seed
            )
        ),
        "extra_trees": lambda: ExtraTreesClassifier(
            n_estimators=400, max_depth=4, min_samples_leaf=8,
            class_weight="balanced", random_state=seed, n_jobs=1,
        ),
    }
    results = {}
    for model_name, factory in models.items():
        probabilities = [None] * len(y)
        for group in sorted(set(groups)):
            train = [i for i, value in enumerate(groups) if value != group]
            test = [i for i, value in enumerate(groups) if value == group]
            if not any(y[i] for i in train):
                continue
            model = factory()
            model.fit([X[i] for i in train], [y[i] for i in train])
            scores = model.predict_proba([X[i] for i in test])[:, 1]
            for i, score in zip(test, scores):
                probabilities[i] = float(score)
        valid = [i for i, score in enumerate(probabilities) if score is not None]
        truth = [y[i] for i in valid]
        score = [probabilities[i] for i in valid]
        prediction = [int(value >= 0.5) for value in score]
        results[model_name] = {
            "blocked_cv_average_precision": average_precision_score(truth, score),
            "blocked_cv_roc_auc": roc_auc_score(truth, score),
            "blocked_cv_balanced_accuracy_at_half": balanced_accuracy_score(truth, prediction),
            "confusion_at_half": confusion(truth, prediction),
        }

    tree = DecisionTreeClassifier(
        max_depth=3, min_samples_leaf=4, class_weight="balanced", random_state=seed
    )
    tree.fit(X, y)
    tree_prediction = tree.predict(X).astype(int).tolist()
    tree_text = export_text(tree, feature_names=list(FEATURE_NAMES), decimals=1)

    # True leave-one-negative-band-out recall: each complete observed band is
    # unseen during fitting.  This directly attacks interpolation explanations.
    band_results = []
    for left, right in runs(ns[i] for i, value in enumerate(y) if value):
        held = [i for i, n in enumerate(ns) if left <= n <= right]
        train = [i for i in range(len(y)) if i not in held]
        model = models["extra_trees"]()
        model.fit([X[i] for i in train], [y[i] for i in train])
        held_scores = model.predict_proba([X[i] for i in held])[:, 1]
        band_results.append({
            "band": [left, right],
            "scores": [float(value) for value in held_scores],
            "recalled_at_half": int(sum(value >= 0.5 for value in held_scores)),
            "size": len(held),
        })
    return results, tree_text, confusion(y, tree_prediction), band_results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", type=Path,
                        default=Path("cycle40-data/local-unit-kappa.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("cycle41-data"))
    parser.add_argument("--seed", type=int, default=41041)
    args = parser.parse_args()

    labels = load_labels(args.labels)
    ns = sorted(labels)
    rows = feature_rows(min(ns), max(ns))
    X = [[values[name] for name in FEATURE_NAMES] for _, values in rows]
    y = [labels[n] for n, _ in rows]
    audits = threshold_audit(X, y, FEATURE_NAMES)
    screen = necessary_screen(X, y, FEATURE_NAMES)
    statistics, tree_text, tree_cm, band_results = classify(X, y, ns, args.seed)

    for audit in audits:
        audit["counterexample_indices"] = [ns[i] for i in audit.pop("counterexample_rows")]
    screen["false_positive_indices"] = [
        ns[i] for i in screen.pop("false_positive_rows")
    ]
    audit_by_name = {item["feature"]: item for item in audits}
    hypothesis_audit = {
        "prime_gaps": audit_by_name["prime_gap"],
        "Mertens_jumps": audit_by_name["mertens_d1"],
        "psi_prime_power_jumps": audit_by_name["psi_bit_mass_d1"],
        "squarefree_runs": max(
            (audit_by_name["squarefree_run_left"], audit_by_name["squarefree_run_right"]),
            key=lambda item: item["balanced_accuracy"],
        ),
    }
    summary = {
        "scope": "finite adversarial diagnostic; no deterministic law or RH claim",
        "range": [min(ns), max(ns)],
        "sample_count": len(ns),
        "negative_count": sum(y),
        "negative_bands": [list(band) for band in runs(n for n in ns if labels[n])],
        "integer_features": list(FEATURE_NAMES),
        "blocked_classification": statistics,
        "leave_one_negative_band_out": band_results,
        "simple_hypothesis_audit": hypothesis_audit,
        "best_single_thresholds": audits[:10],
        "candidate_deterministic_necessary_screen": screen,
        "candidate_depth3_tree": tree_text,
        "candidate_depth3_training_confusion": tree_cm,
        "warning": "The candidate tree is post-selected in-sample and is not a theorem.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "summary.json").open("w", encoding="ascii") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")
    with (args.output_dir / "integer-features.csv").open(
        "w", newline="", encoding="ascii"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=("n", "H_negative") + FEATURE_NAMES,
                                lineterminator="\n")
        writer.writeheader()
        for (n, values), label in zip(rows, y):
            writer.writerow({"n": n, "H_negative": label, **values})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
