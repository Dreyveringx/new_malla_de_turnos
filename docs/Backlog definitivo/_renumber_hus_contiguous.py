# -*- coding: utf-8 -*-
"""Renumera HUs activas a HU01..HU81 sin huecos (módulo de cero)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\jair.uribe\Datacenter\Malla-Turnos")
BD = ROOT / "docs" / "Backlog definitivo"
HU_DIR = ROOT / "docs" / "Historias de usuario"
MAP_PATH = BD / "_renumber_map.json"

MAPPING: dict[int, int] = {int(k): int(v) for k, v in json.loads(MAP_PATH.read_text(encoding="utf-8")).items()}


def hu_token(n: int) -> str:
    return f"HU{n:02d}"


def protect_absorbed(text: str) -> str:
    """Evita que menciones históricas de absorbidas choquen con IDs reutilizados."""
    text = re.sub(r"\bHU46\b", "EXHU46HIST", text)
    text = re.sub(r"\bHU50\b", "EXHU50HIST", text)
    text = re.sub(r"\bHU54\b", "EXHU54HIST", text)
    return text


def restore_absorbed(text: str) -> str:
    text = text.replace("EXHU46HIST", "ex-HU46")
    text = text.replace("EXHU50HIST", "ex-HU50")
    text = text.replace("EXHU54HIST", "ex-HU54")
    return text


def apply_map(text: str) -> str:
    text = protect_absorbed(text)
    # high → temp
    for old in sorted(MAPPING.keys(), reverse=True):
        new = MAPPING[old]
        if old == new:
            continue
        text = re.sub(rf"\bHU{old:02d}\b", f"HU__TMP_{old}__", text)
        text = re.sub(rf"\bHU{old}\b", f"HU__TMP_{old}__", text)
    # temp → final
    for old in sorted(MAPPING.keys(), reverse=True):
        new = MAPPING[old]
        if old == new:
            continue
        text = text.replace(f"HU__TMP_{old}__", hu_token(new))
    return restore_absorbed(text)


def rewrite_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    final = apply_map(raw)
    if final != raw:
        path.write_text(final, encoding="utf-8")
        return True
    return False


def rename_path(path: Path) -> Path | None:
    m = re.search(r"(HU)(\d+)", path.name)
    if not m:
        return None
    old = int(m.group(2))
    new = MAPPING.get(old, old)
    if new == old:
        return None
    # skip obsoletas: keep historical filenames
    if "_Obsoletas" in str(path):
        return None
    new_name = re.sub(rf"HU{old:02d}\b", f"HU{new:02d}", path.name)
    new_name = re.sub(rf"HU{old}\b", f"HU{new:02d}", new_name)
    if new_name == path.name:
        return None
    dest = path.with_name(new_name)
    return dest


def two_phase_rename(paths: list[Path]) -> int:
    # to temp
    mid = []
    for p in paths:
        dest = rename_path(p)
        if not dest:
            continue
        m = re.search(r"HU(\d+)", p.name)
        old = int(m.group(1))
        tmp = p.with_name(re.sub(rf"HU{old:02d}\b", f"HUTMP{old:02d}", p.name))
        tmp = tmp if "HUTMP" in tmp.name else p.with_name(re.sub(rf"HU{old}\b", f"HUTMP{old}", p.name))
        if tmp.exists() and tmp.resolve() != p.resolve():
            tmp.unlink()
        p.rename(tmp)
        final = tmp.with_name(re.sub(rf"HUTMP{old:02d}\b", f"HU{MAPPING[old]:02d}", tmp.name))
        final = final if re.search(rf"HU{MAPPING[old]:02d}", final.name) else tmp.with_name(
            re.sub(rf"HUTMP{old}\b", f"HU{MAPPING[old]:02d}", tmp.name)
        )
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
    path.write_text(json.dumps(hus, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    # 1) rename files first (md/docx) outside obsoletas
    to_rename = []
    for p in list(HU_DIR.rglob("GST-FM-04*")) + list(BD.glob("*.md")):
        if p.is_file() and rename_path(p):
            to_rename.append(p)
    n = two_phase_rename(to_rename)
    print(f"Renamed files: {n}")

    # 2) rewrite text contents once
    targets = []
    targets += list(BD.glob("*.md"))
    targets += list((ROOT / "docs").glob("AUDITORIA*.md"))
    targets += [ROOT / "Propuesta-HU-Malla-Turnos.md", ROOT / "docs" / "_gen_propuesta_pdf.py"]
    targets += list(HU_DIR.rglob("*.md"))
    changed = 0
    for p in targets:
        if not p.exists() or p.name.startswith("_renumber") or p.name.startswith("_regen") or p.name.startswith("_md_to"):
            continue
        if rewrite_file(p):
            changed += 1
    print(f"Rewrote texts: {changed}")

    update_parsed()

    legend = ["# Renumeración sin huecos (05/09/2026)", "", "Motivo: módulo de cero — numeración continua HU01…HU81.", "", "| Antes | Después |", "| ----- | -------- |"]
    for o in sorted(MAPPING):
        if MAPPING[o] != o:
            legend.append(f"| HU{o:02d} | HU{MAPPING[o]:02d} |")
    legend += [
        "",
        "## Absorbidas (histórico, ya no ocupan número)",
        "",
        "| Histórico | Absorbitas en (IDs nuevos) |",
        "| --------- | ------------------------- |",
        "| ex-HU46 Separar constructor/publicador | HU62 + HU43 |",
        "| ex-HU50 Dejar de sumar horas en novedad | HU09 + HU55 |",
        "| ex-HU54 Actividad no asignable a casos | HU09 + HU50 |",
        "",
        "Nota: HU01–HU45 no cambiaron. A partir de HU46 la secuencia se compactó.",
        "",
    ]
    (BD / "RENUMERACION-SIN-HUECOS.md").write_text("\n".join(legend), encoding="utf-8")

    hus = json.loads((BD / "_parsed_hus.json").read_text(encoding="utf-8"))
    ids = sorted(int(re.search(r"HU(\d+)", h["id"]).group(1)) for h in hus)
    assert ids == list(range(1, 82)), ids
    print("VERIFY OK: HU01..HU81")


if __name__ == "__main__":
    main()
