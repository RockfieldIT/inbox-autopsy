#!/usr/bin/env python3
"""verify.py — offline structural checker for Inbox Autopsy diagnoses.

A must in a markdown file is a request. A must in code is a constraint.
This checker enforces, without any API key or network access, what rules.md
requires in prose:

  FORMAT       all five sections present, in order, exactly once
  ONE-CAUSE    the DIAGNOSIS section names a single primary cause
               (no lists, no "several causes", bounded length)
  GROUNDING    every double-quoted evidence span in EVIDENCE CHAIN appears
               verbatim in the supplied source artifact (whitespace-normalized;
               "..." inside a quote splits it into parts that must each match)
  NO-RX        no prescription/fix language anywhere in the diagnosis
               (quoted material is exempt — users may say "we set up SPF");
               evidence acts (check/lookup/screenshot/verify) are allowed
  CONFIDENCE   a stated level: high, moderate, or provisional

Usage:
  python3 verify.py <diagnosis.md> <artifact.txt>   check one diagnosis
  python3 verify.py --selftest                      run positive + negative fixtures

Exit code 0 = pass, 1 = fail (or selftest mismatch). Each failure names its check.
"""
import re
import sys
from pathlib import Path

SECTIONS = ["DIAGNOSIS:", "EVIDENCE CHAIN:", "RULED OUT:",
            "CONTRIBUTING FACTORS:", "CONFIDENCE:"]

# Prescription language. Deliberately blunt: false positives are cheaper than
# a fix sneaking through. Scanned outside quoted spans only.
RX_PATTERNS = [
    r"\byou (should|need to|must|could|can) (add|set|create|publish|enable|configure|update|change|switch|migrate|remove|install|use)\b",
    r"\bto fix (this|it)\b", r"\bthe fix\b", r"\bnext steps?\b",
    r"\brecommend(ed)?\b", r"\btry this\b", r"\binstead,? (use|send|switch)\b",
    r"\b(add|publish|create) (a|an|the|your) (dmarc|spf|dkim|txt|cname|mx|dns)\b",
    r"\bset up (dkim|spf|dmarc|authentication|a custom)\b",
    r"\benable (dkim|custom|authentication)\b",
    r"\bswitch (to|from) (a|an|another|different)\b",
    r"\bhere'?s (how|what) (to|you)\b", r"\bstep[- ]by[- ]step\b",
    r"\brewrite\b", r"\bwe suggest\b",
]

# Evidence acts are permitted; if a sentence contains one of these verbs and
# matched only the weaker patterns, it is not a violation on its own.
EVIDENCE_ACT = r"\b(check|look ?up|screenshot|verify|confirm|overturn|show me|paste|run a .{0,20}lookup)\b"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def strip_quotes(text: str) -> str:
    """Remove double-quoted spans so quoted user/header material isn't scanned."""
    return re.sub(r'"[^"]*"', '""', text)


def split_sections(text: str):
    idx = {}
    for s in SECTIONS:
        positions = [m.start() for m in re.finditer(re.escape(s), text)]
        idx[s] = positions
    return idx


def check(diag_path: str, artifact_path: str, quiet=False):
    failures = []
    text = Path(diag_path).read_text(encoding="utf-8")
    artifact = norm(Path(artifact_path).read_text(encoding="utf-8"))

    # FORMAT
    idx = split_sections(text)
    for s in SECTIONS:
        if len(idx[s]) == 0:
            failures.append(("FORMAT", f"missing section {s!r}"))
        elif len(idx[s]) > 1:
            failures.append(("FORMAT", f"section {s!r} appears {len(idx[s])} times"))
    if not failures:
        order = [idx[s][0] for s in SECTIONS]
        if order != sorted(order):
            failures.append(("FORMAT", "sections out of order"))

    def section(name):
        if not idx.get(name):
            return ""
        start = idx[name][0] + len(name)
        later = [idx[s][0] for s in SECTIONS if idx.get(s) and idx[s][0] > idx[name][0]]
        end = min(later) if later else len(text)
        return text[start:end]

    # ONE-CAUSE
    diag = section("DIAGNOSIS:")
    if diag:
        if re.search(r"^\s*(\d+[\.\)]|[-*•])\s+", diag, re.M):
            failures.append(("ONE-CAUSE", "DIAGNOSIS contains a list; one primary cause only"))
        if re.search(r"\b(several|multiple|three|four|a number of) (possible |likely |candidate )?causes\b", diag, re.I):
            failures.append(("ONE-CAUSE", "DIAGNOSIS hedges across multiple causes"))
        sentences = [x for x in re.split(r"(?<=[.!?])\s+", diag.strip()) if x.strip()]
        if len(sentences) > 4:
            failures.append(("ONE-CAUSE", f"DIAGNOSIS is {len(sentences)} sentences; state one cause, tightly (max 4)"))

    # GROUNDING
    chain = section("EVIDENCE CHAIN:")
    quotes = re.findall(r'"([^"]+)"', chain)
    for q in quotes:
        parts = [p for p in q.split("...") if p.strip()]
        for p in parts:
            if norm(p) not in artifact:
                failures.append(("GROUNDING", f"quoted evidence not found in artifact: \"{p.strip()[:70]}\""))

    # NO-RX
    scannable = strip_quotes(text)
    for pat in RX_PATTERNS:
        for m in re.finditer(pat, scannable, re.I):
            line_start = scannable.rfind("\n", 0, m.start()) + 1
            line_end = scannable.find("\n", m.end())
            line = scannable[line_start:line_end if line_end != -1 else None]
            if re.search(EVIDENCE_ACT, line, re.I) and pat not in RX_PATTERNS[:1]:
                continue  # evidence act, permitted
            failures.append(("NO-RX", f"prescription language: {m.group(0)!r}"))

    # CONFIDENCE
    conf = section("CONFIDENCE:")
    if conf and not re.search(r"\b(high|moderate|provisional)\b", conf, re.I):
        failures.append(("CONFIDENCE", "no stated level (high|moderate|provisional)"))

    if not quiet:
        if failures:
            print(f"FAIL {diag_path}")
            for chk, msg in failures:
                print(f"  [{chk}] {msg}")
        else:
            print(f"PASS {diag_path} (format, one-cause, grounding on "
                  f"{len(quotes)} quotes, no-rx, confidence)")
    return failures


def selftest():
    here = Path(__file__).parent / "fixtures"
    plan = [
        ("good-output.md",        "good-artifact.txt", None),
        ("bad-three-causes.md",   "good-artifact.txt", "ONE-CAUSE"),
        ("bad-prescription.md",   "good-artifact.txt", "NO-RX"),
        ("bad-fabricated-quote.md","good-artifact.txt", "GROUNDING"),
        ("bad-missing-sections.md","good-artifact.txt", "FORMAT"),
    ]
    ok = True
    for diag, art, expected in plan:
        failures = check(str(here / diag), str(here / art), quiet=True)
        kinds = {f[0] for f in failures}
        if expected is None:
            passed = not failures
            verdict = "clean pass" if passed else f"unexpected failures {kinds}"
        else:
            passed = expected in kinds
            verdict = f"fails on [{expected}] as designed" if passed else \
                      f"expected [{expected}], got {kinds or 'clean pass'}"
        print(f"{'OK  ' if passed else 'BAD '} {diag}: {verdict}")
        ok &= passed
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    sys.exit(1 if check(sys.argv[1], sys.argv[2]) else 0)
