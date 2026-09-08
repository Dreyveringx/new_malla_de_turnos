# -*- coding: utf-8 -*-
"""Renumeración LÓGICA: HU01..HU81 siguen el orden de construcción (EP-00→EP-09)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\jair.uribe\Datacenter\Malla-Turnos")
BD = ROOT / "docs" / "Backlog definitivo"
HU_DIR = ROOT / "docs" / "Historias de usuario"

# Orden lógico actual (IDs vigentes antes de este script) = propuesta §3
LOGICAL_OLD = [
    # EP-00
    1, 2, 65, 3, 4, 5, 66, 67,
    # EP-01
    61, 62, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 63, 20, 79,
    # EP-02
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 75, 76, 80, 81,
    # EP-03
    32, 33, 34, 64, 35, 68, 69, 36, 37, 38, 39, 40, 41, 42,
    # EP-04
    43, 44, 45,
    # EP-05
    46, 77, 47, 48, 49,
    # EP-06
    50, 51,
    # EP-07
    52, 53, 54,
    # EP-08
    55, 56, 57, 58, 78, 59, 60,
    # EP-09
    70, 71, 72, 73, 74,
]

assert len(LOGICAL_OLD) == 81, len(LOGICAL_OLD)
assert len(set(LOGICAL_OLD)) == 81
MAPPING = {old: i for i, old in enumerate(LOGICAL_OLD, 1)}


def protect_absorbed(text: str) -> str:
    text = re.sub(r"\bex-HU46\b", "EXHU46HIST", text)
    text = re.sub(r"\bex-HU50\b", "EXHU50HIST", text)
    text = re.sub(r"\bex-HU54\b", "EXHU54HIST", text)
    # bare historical in absorb tables already "ex-HU"
    return text


def restore_absorbed(text: str) -> str:
    # After remap, point absorb targets to NEW logical ids
    # ex-HU46 → capacidades(HU10) + publicación(HU57)
    # ex-HU50 → estados(HU14) + horas(HU70)
    # ex-HU54 → estados(HU14) + consulta(HU65)
    text = text.replace("EXHU46HIST", "ex-HU46")
    text = text.replace("EXHU50HIST", "ex-HU50")
    text = text.replace("EXHU54HIST", "ex-HU54")
    return text


def apply_map(text: str) -> str:
    text = protect_absorbed(text)
    for old in sorted(MAPPING.keys(), reverse=True):
        new = MAPPING[old]
        if old == new:
            continue
        text = re.sub(rf"\bHU{old:02d}\b", f"HU__TMP_{old}__", text)
        text = re.sub(rf"\bHU{old}\b", f"HU__TMP_{old}__", text)
    for old in sorted(MAPPING.keys(), reverse=True):
        new = MAPPING[old]
        if old == new:
            continue
        text = text.replace(f"HU__TMP_{old}__", f"HU{new:02d}")
    text = restore_absorbed(text)
    # Fix absorb target lines to logical new ids (stable)
    text = re.sub(r"ex-HU46\s*\|\s*HU\d+\s*\+\s*HU\d+", "ex-HU46 | HU10 + HU57", text)
    text = re.sub(r"ex-HU50\s*\|\s*HU\d+\s*\+\s*HU\d+", "ex-HU50 | HU14 + HU70", text)
    text = re.sub(r"ex-HU54\s*\|\s*HU\d+\s*\+\s*HU\d+", "ex-HU54 | HU14 + HU65", text)
    text = text.replace("A → HU62 + HU43", "A → HU10 + HU57")
    text = text.replace("A → HU09 + HU55", "A → HU14 + HU70")
    text = text.replace("A → HU09 + HU50", "A → HU14 + HU65")
    text = text.replace("absorben ex-HU50 y ex-HU54", "absorben ex-HU50 y ex-HU54")
    text = re.sub(
        r"Constructor/publicador en config del frente \(HU\d+\) \+ publicación \(HU\d+\)",
        "Constructor/publicador en config del frente (HU10) + publicación (HU57)",
        text,
    )
    return text


def rewrite_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    final = apply_map(raw)
    if final != raw:
        path.write_text(final, encoding="utf-8")
        return True
    return False


def rename_path(path: Path):
    if "_Obsoletas" in str(path):
        return None
    m = re.search(r"HU(\d+)", path.name)
    if not m:
        return None
    old = int(m.group(1))
    new = MAPPING.get(old, old)
    if new == old:
        return None
    return path


def two_phase_rename(paths: list[Path]) -> int:
    mid = []
    for p in paths:
        m = re.search(r"HU(\d+)", p.name)
        if not m:
            continue
        old = int(m.group(1))
        new = MAPPING.get(old, old)
        if new == old:
            continue
        tmp = p.with_name(re.sub(rf"HU{old:02d}\b", f"HUTMP{old:02d}", p.name))
        if "HUTMP" not in tmp.name:
            tmp = p.with_name(re.sub(rf"HU{old}\b", f"HUTMP{old}", p.name))
        if tmp.exists() and tmp.resolve() != p.resolve():
            tmp.unlink()
        p.rename(tmp)
        final = tmp.with_name(re.sub(rf"HUTMP{old:02d}\b", f"HU{new:02d}", tmp.name))
        if not re.search(rf"HU{new:02d}", final.name):
            final = tmp.with_name(re.sub(rf"HUTMP{old}\b", f"HU{new:02d}", tmp.name))
        mid.append((tmp, final))
    for tmp, final in mid:
        if final.exists() and final.resolve() != tmp.resolve():
            final.unlink()
        tmp.rename(final)
    return len(mid)


def update_parsed():
    path = BD / "_parsed_hus.json"
    hus = json.loads(path.read_text(encoding="utf-8"))
    for h in hus:
        m = re.search(r"MT-EP(\d+)-HU(\d+)", h["id"])
        ep, old = m.group(1), int(m.group(2))
        h["id"] = f"MT-EP{ep}-HU{MAPPING.get(old, old):02d}"
        for key in ("deps", "como", "quiero", "para", "title"):
            if isinstance(h.get(key), str):
                h[key] = apply_map(h[key])
        for key in ("cubren", "reglas"):
            if isinstance(h.get(key), list):
                h[key] = [apply_map(x) for x in h[key]]
        if h.get("cas"):
            h["cas"] = [[apply_map(x) if isinstance(x, str) else x for x in row] for row in h["cas"]]
    # reorder json by new id
    hus.sort(key=lambda h: int(re.search(r"HU(\d+)", h["id"]).group(1)))
    path.write_text(json.dumps(hus, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    (BD / "_renumber_logical_map.json").write_text(
        json.dumps({str(k): v for k, v in MAPPING.items()}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    to_rename = [p for p in HU_DIR.rglob("GST-FM-04*") if p.is_file() and rename_path(p)]
    n = two_phase_rename(to_rename)
    print(f"Renamed: {n}")

    targets = []
    targets += list(BD.glob("*.md"))
    targets += list((ROOT / "docs").glob("AUDITORIA*.md"))
    targets += [ROOT / "Propuesta-HU-Malla-Turnos.md", ROOT / "docs" / "_gen_propuesta_pdf.py"]
    targets += list(HU_DIR.rglob("*.md"))
    changed = 0
    for p in targets:
        if not p.exists() or p.name.startswith("_"):
            continue
        if rewrite_file(p):
            changed += 1
    print(f"Rewrote: {changed}")
    update_parsed()

    legend = [
        "# Renumeración lógica HU01…HU81 (05/09/2026)",
        "",
        "Los números siguen el **orden de construcción** (EP-00 → EP-09), no el orden histórico.",
        "",
        "| Antes | Después |",
        "| ----- | -------- |",
    ]
    for o in LOGICAL_OLD:
        n = MAPPING[o]
        if o != n:
            legend.append(f"| HU{o:02d} | HU{n:02d} |")
    legend += [
        "",
        "## Secuencia final (lectura de punta a punta)",
        "",
        "| Nuevo | Épica | Antes |",
        "| ----- | ----- | ----- |",
    ]
    # epic from parsed after update
    hus = json.loads((BD / "_parsed_hus.json").read_text(encoding="utf-8"))
    for h in hus:
        m = re.search(r"MT-EP(\d+)-HU(\d+)", h["id"])
        legend.append(f"| HU{int(m.group(2)):02d} | EP-{m.group(1)} | (ver mapa) | {h['title'][:50]} |")

    # fix legend table - I messed columns. rewrite simpler
    legend = [
        "# Renumeración lógica HU01…HU81 (05/09/2026)",
        "",
        "Los números siguen el **orden de construcción** (EP-00 → EP-09).",
        "",
        "| Nuevo | Épica | Título |",
        "| ----- | ----- | ------ |",
    ]
    for h in hus:
        m = re.search(r"MT-EP(\d+)-HU(\d+)", h["id"])
        legend.append(f"| HU{int(m.group(2)):02d} | EP-{m.group(1)} | {h['title']} |")
    legend += [
        "",
        "## Absorbidas (histórico)",
        "",
        "| Histórico | Absorbitas en |",
        "| --------- | ------------- |",
        "| ex-HU46 | HU10 + HU57 |",
        "| ex-HU50 | HU14 + HU70 |",
        "| ex-HU54 | HU14 + HU65 |",
        "",
    ]
    (BD / "RENUMERACION-LOGICA-ORDEN.md").write_text("\n".join(legend), encoding="utf-8")

    ids = [int(re.search(r"HU(\d+)", h["id"]).group(1)) for h in hus]
    assert ids == list(range(1, 82)), ids
    # verify epic blocks contiguous
    print("VERIFY OK logical HU01..HU81")
    for h in hus[:12]:
        print(h["id"], h["title"][:55])


if __name__ == "__main__":
    main()
