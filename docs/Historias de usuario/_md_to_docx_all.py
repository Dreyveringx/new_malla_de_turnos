# -*- coding: utf-8 -*-
"""Genera GST-FM-04 .docx desde markdown usando la plantilla oficial (sin cambiar formato)."""
from __future__ import annotations

import re
import shutil
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
DOCS = ROOT.parent
TEMPLATE = DOCS / "GST-FM-04  FORMATO HISTORIA DE USUARIO.docx"


def set_cell_text(cell, text: str) -> None:
    """Reemplaza el texto de una celda preservando el estilo del primer párrafo."""
    text = text or ""
    lines = text.split("\n")
    # Clear existing paragraphs except keep one
    paragraphs = cell.paragraphs
    if not paragraphs:
        cell.add_paragraph(text)
        return
    # Use first paragraph style as base
    first = paragraphs[0]
    # Remove extra paragraphs from end
    for p in paragraphs[1:]:
        p._element.getparent().remove(p._element)
    # Clear runs in first
    for r in list(first.runs):
        r._element.getparent().remove(r._element)
    if not lines:
        first.add_run("")
        return
    first.add_run(lines[0])
    for line in lines[1:]:
        np = cell.add_paragraph()
        # copy pPr if possible
        if first._p.pPr is not None:
            np._p.get_or_add_pPr()
        np.add_run(line)


def set_merged_row_text(row, text: str, start_col: int = 0) -> None:
    """Escribe el mismo texto en celdas consecutivas del merge (evita basura visual)."""
    # Unique cell objects in order
    seen = []
    ids = set()
    for c in row.cells[start_col:]:
        cid = id(c._tc)
        if cid in ids:
            continue
        ids.add(cid)
        seen.append(c)
    if not seen:
        return
    set_cell_text(seen[0], text)
    # For other unique cells in merge, mirror (python-docx often shares tc for true merges;
    # if not shared, keep label cells alone when start_col>0)
    for c in seen[1:]:
        # Only mirror if cell was empty-ish or same merge visually for content rows
        if start_col == 0:
            set_cell_text(c, text)


def parse_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    def field(label: str) -> str:
        m = re.search(rf"\| {re.escape(label)} \| (.+?) \|", text)
        return m.group(1).strip() if m else ""

    title = field("Nombre historia de usuario")
    req = field("Id. Requerimiento")
    assoc_req = field("Id asociado")

    # description
    desc = ""
    m = re.search(
        r"### Descripción de historia de usuario\s*\n\n(.+?)(?:\n\n---|\n\n## )",
        text,
        re.S,
    )
    if m:
        desc = " ".join(m.group(1).split())

    # actors (lista con viñetas o tabla legacy)
    actors_lines = []
    in_actors = False
    for line in lines:
        if line.startswith("## Actores"):
            in_actors = True
            continue
        if in_actors and line.startswith("## "):
            break
        if not in_actors:
            continue
        m = re.match(r"^[-*]\s+(.+)$", line)
        if m:
            actors_lines.append(m.group(1).strip())
            continue
        if line.startswith("|") and "Tipo" not in line and "----" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                actors_lines.append(f"{parts[0]}: {parts[1]}")
    actors = "\n".join(actors_lines) if actors_lines else ""

    # associated
    associated = []
    in_as = False
    for line in lines:
        if line.startswith("## Historias de usuario asociadas"):
            in_as = True
            continue
        if in_as and line.startswith("## "):
            break
        if in_as and line.startswith("|") and "Ítem" not in line and "Item" not in line and "----" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2 and parts[0].isdigit():
                associated.append((parts[0], parts[1]))

    # preconditions + steps
    preconds = []
    in_pre = False
    for line in lines:
        if line.startswith("### Precondiciones"):
            in_pre = True
            continue
        if in_pre and (line.startswith("### ") or line.startswith("## ")):
            break
        if in_pre:
            m = re.match(r"^\d+\.\s+(.*)", line)
            if m:
                preconds.append(m.group(1))

    steps = []
    in_steps = False
    current_step = None
    for line in lines:
        if line.startswith("### Pasos"):
            in_steps = True
            continue
        if in_steps and line.startswith("## "):
            break
        if not in_steps:
            continue
        m = re.match(r"^(\d+)\.\s+(.*)", line)
        if m:
            if current_step:
                steps.append(current_step)
            current_step = [m.group(1), m.group(2).strip(), ""]
            continue
        m = re.match(r"^\s*[-*]\s+Sistema:\s*(.*)", line)
        if m and current_step:
            current_step[2] = m.group(1).strip()
            continue
        if line.startswith("|") and not line.startswith("| #") and "----" not in line and "Actor" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 3 and parts[0].isdigit():
                steps.append((parts[0], parts[1], parts[2]))
    if current_step:
        steps.append(tuple(current_step))

    result = ""
    m = re.search(r"Resultado esperado:\s*(.+)", text)
    if m:
        result = m.group(1).strip()

    flujo_parts = []
    if preconds:
        flujo_parts.append("Precondiciones:\n" + "\n".join(f"- {p}" for p in preconds))
    if steps:
        flujo_parts.append(
            "Pasos:\n"
            + "\n".join(
                f"{n}. {a}" + (f"\n   Sistema: {s}" if s else "")
                for n, a, s in steps
            )
        )
    if result:
        flujo_parts.append(f"Resultado esperado: {result}")
    flujo = "\n\n".join(flujo_parts)

    # alternates (lista o tabla)
    fas = []
    in_fa = False
    for line in lines:
        if line.startswith("## Flujos alternos"):
            in_fa = True
            continue
        if in_fa and line.startswith("## "):
            break
        if not in_fa:
            continue
        m = re.match(r"^[-*]\s+(FA-\d+)\s*:\s*(.+)$", line)
        if m:
            fas.append(f"{m.group(1)}. {m.group(2).strip()}")
            continue
        if line.startswith("|") and "Id" not in line and "----" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                fas.append(f"{parts[0]}. {parts[1]}")
    fa_text = (
        "Flujos Alternos\n"
        "(Describe desviaciones o excepciones del flujo básico)\n\n" + "\n\n".join(fas)
    )

    # errors (lista o tabla)
    errs = []
    in_e = False
    pending_err = None
    for line in lines:
        if line.startswith("## Errores"):
            in_e = True
            continue
        if in_e and line.startswith("## "):
            break
        if not in_e:
            continue
        m = re.match(r"^[-*]\s+(E-\d+)\s*:\s*(.+)$", line)
        if m:
            if pending_err:
                errs.append(pending_err)
            pending_err = f"{m.group(1)}. {m.group(2).strip()}"
            continue
        m = re.match(r"^\s*[-*]\s+Comportamiento esperado:\s*(.+)$", line)
        if m and pending_err:
            pending_err = f"{pending_err}: {m.group(1).strip()}"
            continue
        if line.startswith("|") and "Id" not in line and "----" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 3:
                errs.append(f"{parts[0]}. {parts[1]}: {parts[2]}")
    if pending_err:
        errs.append(pending_err)
    err_text = "\n".join(errs)

    # prototype
    proto = ""
    m = re.search(
        r"## Prototipo de interfaz de usuario y/o reportes\s*\n\n(.+?)(?:\n\n---|\n\n## )",
        text,
        re.S,
    )
    if m:
        proto = m.group(1).strip()

    # criteria
    crits = []
    in_c = False
    for line in lines:
        if line.startswith("## Criterios de aceptación"):
            in_c = True
            continue
        if in_c and line.startswith("## "):
            break
        if in_c:
            m = re.match(r"^\d+\.\s+(.*)", line)
            if m:
                crits.append(m.group(0))
    criteria = "\n".join(crits)

    # rules (lista o tabla)
    rules = []
    in_r = False
    for line in lines:
        if line.startswith("## Reglas de negocio"):
            in_r = True
            continue
        if in_r and line.startswith("## "):
            break
        if not in_r:
            continue
        m = re.match(r"^[-*]\s+(RN-\d+)\s*:\s*(.+)$", line)
        if m:
            rules.append(f"{m.group(1)}. {m.group(2).strip()}")
            continue
        if line.startswith("|") and "Id" not in line and "----" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                rules.append(f"{parts[0]}. {parts[1]}")
    rules_text = "\n".join(rules)

    # inputs — filas Campo|Longitud|Tipo|Obligatorio|Sistema|Interfaz|Descripción
    inputs_note = ""
    input_rows: list[list[str]] = []
    m = re.search(r"## Datos de entrada\s*\n\n(.+?)(?:\n\n---|\n\n\*|$)", text, re.S)
    if m:
        block = m.group(1).strip()
        for line in block.splitlines():
            if line.startswith("|") and "----" not in line:
                parts = [p.strip() for p in line.strip("|").split("|")]
                if not parts or parts[0] in {"Campo", "-----"}:
                    continue
                if len(parts) >= 7:
                    input_rows.append(parts[:7])
                else:
                    input_rows.append(parts)
            elif line and not line.startswith("|"):
                inputs_note = (inputs_note + " " + line).strip() if inputs_note else line
        if not input_rows and not inputs_note:
            inputs_note = block

    # changelog first row
    fecha, version, descripcion, autor = "05/09/2026", "1.0", title, "Jair Uribe"
    in_cc = False
    for line in lines:
        if line.startswith("## Control de cambios"):
            in_cc = True
            continue
        if in_cc and line.startswith("|") and "Fecha" not in line and "----" not in line and "Elaborado" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 4 and re.match(r"\d{2}/\d{2}/\d{4}", parts[0]):
                fecha, version, descripcion, autor = parts[0], parts[1], parts[2], parts[3]
                break

    elaborado = field("Elaborado por") or autor
    # from second meta table in md
    m = re.search(
        r"\| Elaborado por \| Fecha de elaboración \| Fecha de entrega \|\s*\n\|[^\n]+\|\s*\n\| ([^|]+) \| ([^|]+) \| ([^|]+) \|",
        text,
    )
    entrega = "Pendiente validación con negocio"
    if m:
        elaborado = m.group(1).strip()
        fecha = m.group(2).strip() or fecha
        entrega = m.group(3).strip()

    return {
        "title": title,
        "req": req,
        "assoc_req": assoc_req,
        "desc": desc,
        "actors": actors,
        "associated": associated,
        "flujo": flujo,
        "fa": fa_text,
        "errors": err_text,
        "proto": proto,
        "criteria": criteria,
        "rules": rules_text,
        "input_rows": input_rows,
        "inputs_note": inputs_note,
        "fecha": fecha,
        "version": version,
        "descripcion": descripcion,
        "autor": autor,
        "elaborado": elaborado,
        "entrega": entrega,
    }


def fill_template(md_path: Path, out_path: Path) -> None:
    data = parse_md(md_path)
    shutil.copy2(TEMPLATE, out_path)
    doc = Document(str(out_path))

    # Table 0 — proyecto
    set_cell_text(doc.tables[0].rows[0].cells[0], "Nombre del Proyecto: Malla de Turnos")

    # Table 1 — control cambios
    t1 = doc.tables[1]
    set_cell_text(t1.rows[2].cells[0], data["fecha"])
    set_cell_text(t1.rows[2].cells[1], data["version"])
    set_cell_text(t1.rows[2].cells[2], data["descripcion"])
    set_cell_text(t1.rows[2].cells[3], data["autor"])

    # Table 2 — elaborado
    t2 = doc.tables[2]
    set_cell_text(t2.rows[0].cells[2], data["fecha"])
    set_cell_text(t2.rows[1].cells[0], data["elaborado"])
    set_cell_text(t2.rows[1].cells[2], data["entrega"])

    # Table 3 — cuerpo
    t3 = doc.tables[3]
    # R1 nombre + ids
    set_cell_text(t3.rows[1].cells[2], data["title"])
    set_cell_text(t3.rows[1].cells[4], f"Id. Requerimiento: {data['req']}")
    set_cell_text(t3.rows[1].cells[5], f"Id asociado: {data['assoc_req']}")

    # R2 descripción (content from col 2)
    set_cell_text(t3.rows[2].cells[2], data["desc"])

    # R3 actores
    set_cell_text(t3.rows[3].cells[2], data["actors"])

    # R6-R8 associated (keep empty if fewer)
    for i in range(3):
        row = t3.rows[6 + i]
        if i < len(data["associated"]):
            item, name = data["associated"][i]
            set_cell_text(row.cells[0], item)
            set_cell_text(row.cells[1], name)
            set_cell_text(row.cells[3], "Pendiente")
            set_cell_text(row.cells[6], "Listado de épicas — Malla de Turnos")
        else:
            set_cell_text(row.cells[0], "")
            set_cell_text(row.cells[1], "")
            set_cell_text(row.cells[3], "")
            set_cell_text(row.cells[6], "")

    # R10 flujo
    set_merged_row_text(t3.rows[10], data["flujo"], 0)

    # R11 FA
    set_merged_row_text(t3.rows[11], data["fa"], 0)

    # R12 errors
    set_merged_row_text(t3.rows[12], data["errors"], 0)

    # R14 prototype content
    set_merged_row_text(t3.rows[14], data["proto"], 0)

    # R15 criteria (label stays in C0/C1; content C2)
    set_cell_text(t3.rows[15].cells[2], data["criteria"])

    # R16 rules
    set_cell_text(t3.rows[16].cells[2], data["rules"])

    # Table 4 datos — tabla anidada 7 columnas (formato oficial)
    outer = doc.tables[4].rows[1].cells[0]
    nested = outer.tables[0] if outer.tables else None
    if nested is not None:
        # Limpiar nota previa en párrafos del contenedor (dejar vacíos)
        for p in outer.paragraphs:
            for r in list(p.runs):
                r._element.getparent().remove(r._element)

        rows_needed = max(len(data["input_rows"]), 1 if data["inputs_note"] else 0)
        # La plantilla trae 1 header + 4 filas vacías
        while len(nested.rows) - 1 < rows_needed:
            tbl = nested._tbl
            last = nested.rows[-1]._tr
            tbl.append(deepcopy(last))

        # Vaciar filas de datos existentes
        for ri in range(1, len(nested.rows)):
            for ci in range(7):
                set_cell_text(nested.rows[ri].cells[ci], "")

        if data["input_rows"]:
            for i, parts in enumerate(data["input_rows"]):
                row = nested.rows[i + 1]
                for ci in range(7):
                    set_cell_text(row.cells[ci], parts[ci] if ci < len(parts) else "")
        elif data["inputs_note"]:
            set_cell_text(nested.rows[1].cells[0], data["inputs_note"])
            set_cell_text(nested.rows[1].cells[6], "No aplica captura de formulario")
    else:
        fallback = data["inputs_note"]
        if data["input_rows"]:
            fallback = "\n".join(" | ".join(r) for r in data["input_rows"])
        set_cell_text(outer, fallback or "")

    core = doc.core_properties
    core.author = data["autor"]
    core.title = f"{data['req']} — {data['title']}"
    core.subject = "GST-FM-04 Malla de Turnos"

    doc.save(str(out_path))


def iter_hu_mds():
    for md in sorted(ROOT.rglob("PRY - HU*.md")):
        if "_Obsoletas" in str(md):
            continue
        if "anexo-tecnico" in md.name.lower() or "anexo tecnico" in md.name.lower():
            continue
        yield md


def main():
    if not TEMPLATE.exists():
        raise SystemExit(f"Plantilla no encontrada: {TEMPLATE}")

    written = 0
    for md in iter_hu_mds():
        out = md.with_suffix(".docx")
        fill_template(md, out)
        written += 1

        # remove other docx with same HU number but different stem
        m = re.search(r"HU(\d+)", md.name.upper())
        if m:
            num = int(m.group(1))
            for old in md.parent.glob("PRY - HU*.docx"):
                om = re.search(r"HU(\d+)", old.name.upper())
                if om and int(om.group(1)) == num and old.resolve() != out.resolve():
                    try:
                        old.unlink()
                    except OSError:
                        pass

    # orphans
    stems = {p.stem for p in iter_hu_mds()}
    removed = 0
    for d in list(ROOT.rglob("PRY - HU*.docx")):
        if "_Obsoletas" in str(d):
            continue
        if d.stem not in stems:
            d.unlink()
            removed += 1

    # size sanity
    sample = next(ROOT.joinpath("Epica 00").glob("PRY - HU01*.docx"))
    print(f"Wrote {written} docx from official template")
    print(f"Sample size {sample.stat().st_size} bytes (template {TEMPLATE.stat().st_size})")
    print(f"Orphans removed: {removed}")


if __name__ == "__main__":
    main()
