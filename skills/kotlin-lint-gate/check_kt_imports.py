#!/usr/bin/env python3
"""Okamzity lint editovanych .kt souboru - chyta tridu chyb, ktera 1.-2. 9. 2026
stala dva placene macOS runy (v1.0.197 + v1.0.198): anotace/symboly bez importu
a importy bez pouziti. Bezi za zlomek sekundy, bez gradle.

Pouziti: check_kt_imports.py <soubor.kt> [<soubor.kt> ...]
Exit 0 = cisto, exit 1 = nalezy (vypsane na stdout, jeden na radek).
"""
import re
import sys

# jmena dostupna bez importu v KAZDEM source setu (kotlin.* default importy);
# kotlin.jvm.* sem NEPATRI - na native/common vyzaduje import (pad v1.0.197)
DEFAULT_OK = {
    "OptIn", "Suppress", "Deprecated", "DslMarker", "PublishedApi", "JvmField",
    "Throws", "SinceKotlin", "RequiresOptIn", "ExperimentalStdlibApi",
}

def check(path: str) -> list[str]:
    problems: list[str] = []
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        return [f"{path}: necitelny ({e})"]

    imports: dict[str, str] = {}  # simple name / alias -> full import
    for m in re.finditer(r"^import\s+([\w.]+)(?:\.\*)?(?:\s+as\s+(\w+))?", text, re.M):
        full, alias = m.group(1), m.group(2)
        name = alias or full.rsplit(".", 1)[-1]
        if name != "*":
            imports[name] = full

    body = re.sub(r"^import\s+[^\n]+", "", text, flags=re.M)
    body_no_pkg = re.sub(r"^package\s+[^\n]+", "", body, flags=re.M)

    # 1) anotace na urovni souboru bez importu (@file:X, @file:OptIn(Y::class))
    for m in re.finditer(r"@file:(\w+)(\(([^)]*)\))?", text):
        ann, args = m.group(1), m.group(3) or ""
        names = [ann] + re.findall(r"(\w+)::class", args)
        for n in names:
            if n in DEFAULT_OK or n in imports:
                continue
            if re.search(r"@file:[\w.]*\b" + re.escape(n) + r"\b", text) and "." in m.group(0)[6:].split("(")[0]:
                continue  # plne kvalifikovana anotace
            problems.append(f"{path}: @file anotace '{n}' bez importu")

    # 2) nepouzite importy (jmeno se v tele souboru nevyskytuje)
    for name, full in imports.items():
        if not re.search(r"\b" + re.escape(name) + r"\b", body_no_pkg):
            problems.append(f"{path}: nepouzity import {full}" + (f" (as {name})" if name != full.rsplit(".", 1)[-1] else ""))

    return problems


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    out: list[str] = []
    for p in sys.argv[1:]:
        if p.endswith(".kt"):
            out += check(p)
    for line in out:
        print(line)
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
