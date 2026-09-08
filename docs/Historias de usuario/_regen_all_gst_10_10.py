# -*- coding: utf-8 -*-
"""Regenera TODAS las GST-FM-04 activas desde backlog definitivo (anti-hardcoding, 10/10)."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\jair.uribe\Datacenter\Malla-Turnos")
BD = ROOT / "docs" / "Backlog definitivo"
OUT = ROOT / "docs" / "Historias de usuario"
DATE = "05/09/2026"
AUTHOR = "Jair Uribe"

EPIC_META = {
    "00": ("Epica 00", "EP-00 — Integración del módulo a la plataforma GRH"),
    "01": ("Epica 01", "EP-01 — Parametrización de catálogos"),
    "02": ("Epica 02", "EP-02 — Construcción de la malla"),
    "03": ("Epica 03", "EP-03 — Validación, cobertura y rotación"),
    "04": ("Epica 04", "EP-04 — Publicación y ciclo de vida"),
    "05": ("Epica 05", "EP-05 — Novedades, cambios y auditoría"),
    "06": ("Epica 06", "EP-06 — Consulta operativa"),
    "07": ("Epica 07", "EP-07 — Vista del empleado"),
    "08": ("Epica 08", "EP-08 — Reportes y horas para nómina"),
    "09": ("Epica 09", "EP-09 — Intercambio de turnos"),
}

# Soften technical terms for client GST (order matters)
REPL = [
    (r"\bJWT\b", "contexto de sesión autenticado"),
    (r"companyId", "empresa del usuario autenticado"),
    (r"notification-service", "infraestructura de notificaciones de GRH"),
    (r"work_schedule", "jornada contractual"),
    (r"schedule_assignment", "asignación de jornada contractual"),
    (r"working-profile", "perfil de jornada"),
    (r"permisos\s+RBAC", "permisos"),
    (r"\bRBAC\b", "permisos"),
    (r"optimistic lock(?:ing)?", "control de versión al guardar", re.I),
    (r"\bETag\b", "versión de la celda"),
    (r"dry-run", "simulación"),
    (r"\bBFF\b", "capa de consulta del módulo"),
    (r"EmployeeFilterRequest", "filtros del listado de empleados"),
    (r"areaId", "área"),
    (r"permission_submodules", "permisos por sección de menú"),
    (r"SM_\*", "permisos de sección"),
    (r"timeline", "línea de tiempo de auditoría"),
    (r"invocar\s+la\s+API\b", "usar la función del sistema"),
    (r"la\s+API\b", "la función del sistema"),
    (r"\bAPI\b", "función del sistema"),
    (r"payloads?", "cargas de datos"),
    (r"N\+1", "consultas repetidas"),
    (r"use case", "caso de uso"),
    (r"Microservicios\s*/\s*GRH:[^\n]+", "capacidades existentes de la plataforma GRH"),
    (r"la\s+servicio\b", "el servicio"),
    (r"permisos\s+permisos\b", "permisos"),
]


def soft(text: str) -> str:
    if not text:
        return text
    out = text
    for item in REPL:
        if len(item) == 3:
            pat, repl, flags = item
            out = re.sub(pat, repl, out, flags=flags)
        else:
            pat, repl = item
            out = re.sub(pat, repl, out)
    # ban example frentes as product rules (only as frente names, not "sitio de asistencia")
    out = re.sub(
        r"Contact Center|Soporte(?: Técnico)?|Mesa de [Ss]ervicio|Laboratorio",
        "un frente operativo",
        out,
    )
    out = re.sub(
        r"\b(?:CC|SPT)\b",
        "el territorio configurado",
        out,
    )
    out = re.sub(r"\b42\s*h(oras)?\b", "el máximo de horas configurado", out, flags=re.I)
    out = re.sub(r"3 domingos", "el umbral de días configurado en la regla", out, flags=re.I)
    out = re.sub(r"estudio,\s*salud", "los tipos de restricción del catálogo", out, flags=re.I)
    out = re.sub(r"\bElemento\b", "un sitio del catálogo", out)
    return out


def slugify(title: str) -> str:
    s = title.lower()
    s = (
        s.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]


def infer_profiles(como: str, hid: str) -> list[tuple[str, str]]:
    c = como.lower()
    if "super-administrador" in c or "super administrador" in c or hid.endswith("HU01") or hid.endswith("HU71"):
        return [
            ("Super-administrador", "Ejecuta o valida esta capacidad de plataforma."),
            ("Administrador de empresa", "Consume el resultado en su empresa cuando aplica."),
            ("Usuario de la empresa", "No configura la plataforma; opera según permisos del módulo."),
        ]
    if "administrador de empresa" in c and "parametriz" not in c:
        return [
            ("Super-administrador", "No opera la configuración diaria de empresas cliente."),
            ("Administrador de empresa", "Ejecuta o autoriza esta historia en su empresa."),
            ("Usuario de la empresa", "Participa según el rol asignado."),
        ]
    if "empleado" in c or "funcionario" in c and "construcción" not in c:
        return [
            ("Super-administrador", "No participa."),
            ("Administrador de empresa", "Puede consultar según permiso."),
            ("Usuario de la empresa", "Empleado u operador con el permiso correspondiente."),
        ]
    return [
        ("Super-administrador", "No participa en la operación diaria de empresas cliente."),
        ("Administrador de empresa", "Puede ejecutarla si tiene el permiso de la sección."),
        ("Usuario de la empresa", "Coordinador, supervisora u otro rol con el permiso requerido."),
    ]


def infer_actors(como: str) -> list[tuple[str, str]]:
    return [
        ("Inicia", soft(como) if como else "Usuario autorizado de la empresa"),
        ("Participa", "Otros roles según la historia"),
        ("No participa", "Quienes no tienen permiso sobre la sección"),
    ]


def build_steps(h: dict) -> list[tuple[str, str]]:
    # Derive simple steps from CAs / cover
    steps = []
    title = soft(h["title"])
    steps.append(
        (
            f"El usuario entra a la función de {title.lower()}.",
            "Muestra la información de su empresa y frentes autorizados.",
        )
    )
    steps.append(
        (
            "Completa o confirma la acción descrita en la historia.",
            "Valida permisos, empresa y reglas aplicables.",
        )
    )
    steps.append(
        (
            "Guarda o confirma el resultado.",
            "Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.",
        )
    )
    if h["cas"]:
        name, d, c, e = h["cas"][0]
        steps.append((f"Cuando {soft(c)}.", f"Entonces {soft(e)}."))
    return steps[:5]


def build_gst(h: dict) -> str:
    hid = h["id"]
    m = re.match(r"MT-EP(\d+)-HU(\d+)", hid)
    ep, num = m.group(1), m.group(2)
    folder, epic_label = EPIC_META[ep]
    title = soft(h["title"])
    como = soft(h["como"]) or "usuario autorizado de la empresa"
    quiero = soft(h["quiero"]) or title.lower()
    para = soft(h["para"]) or "operar Malla de Turnos de forma parametrizable y aislada por empresa"

    # sanitize como: remove microservice names
    como = re.sub(r"/ equipo de plataforma", " o equipo de plataforma", como)

    actors = infer_actors(como)

    associated = []
    deps = h.get("deps") or ""
    for m2 in re.finditer(r"MT-EP\d+-HU\d+", deps):
        associated.append(m2.group(0))
    associated = associated[:5] or ["Ver dependencias en el backlog definitivo del módulo"]

    cubre = [soft(x) for x in h.get("cubren") or []]
    # Alcance section from backlog mixes Cubre/No cubre - filter
    cubre_lines = []
    no_cubre_lines = []
    # re-parse from original better - use reglas and cas primarily
    reglas = [soft(r) for r in (h.get("reglas") or [])]
    if not reglas:
        reglas = [
            "La funcionalidad es parametrizable por empresa y, cuando aplica, por frente.",
            "Solo opera sobre datos de la empresa del usuario autenticado.",
            "No hardcodea frentes, turnos, estados ni umbrales numéricos de negocio.",
        ]

    cas = h.get("cas") or []
    criteria = []
    for name, d, c, e in cas:
        criteria.append(f"{soft(name)}: dado que {soft(d)}, cuando {soft(c)}, entonces {soft(e)}.")
    if not criteria:
        criteria = [
            "La acción solo está disponible con el permiso correspondiente.",
            "Solo afecta datos de la empresa del usuario.",
            "El comportamiento variable depende de configuración, no de nombres fijos de frente o turno.",
        ]

    alternates = [
        "Si falta configuración previa requerida, el sistema indica qué falta y no continúa.",
        "Si el frente o la capacidad están deshabilitados, la acción no aparece o se informa.",
        "Si hay advertencias de reglas, el usuario puede confirmar solo cuando la configuración lo permita.",
    ]
    errors = [
        ("Datos incompletos o inválidos.", "No guarda; indica el problema."),
        ("Sin permiso o fuera de alcance de frente.", "Acceso no permitido."),
        ("Intento de operar datos de otra empresa.", "No visible / rechazado."),
        ("Fallo al guardar.", "Mensaje claro; no deja información inconsistente."),
    ]

    preconds = [
        "El módulo Malla de Turnos está habilitado para la empresa según su plan.",
        "El usuario tiene el permiso de la sección correspondiente.",
        "Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.",
    ]

    steps = build_steps(h)
    changelog = f"{title}."

    # Inputs - minimal
    if any(k in title.lower() for k in ["parametrizar", "configurar", "definir", "habilitar", "plantilla"]):
        inputs = """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Datos de configuración de esta historia | Malla de turnos | Formulario / listado |
| Empresa | Plataforma GRH | Contexto de sesión |
"""
    elif any(k in title.lower() for k in ["visualizar", "consultar", "ver ", "buscar", "reportar", "exportar", "calcular"]):
        inputs = """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Filtros de consulta (fechas, frente, persona) | Malla de turnos | Filtros / selectores |
"""
    else:
        inputs = """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Datos de la acción descrita en la historia | Malla de turnos | Formulario / grilla / modal |
"""

    lines = [
        "# GST-FM-04 — Malla de Turnos",
        "",
        "Nombre del proyecto: Malla de Turnos",
        f"Épica: {epic_label}",
        "Audiencia: Cliente, diseño, negocio y pruebas funcionales",
        "",
        "---",
        "",
        "## Control de cambios",
        "",
        "| Fecha | Versión | Descripción | Autor |",
        "| ----- | ------- | ----------- | ----- |",
        f"| {DATE} | 1.0 | {changelog} | {AUTHOR} |",
        "",
        "| Elaborado por | Fecha de elaboración | Fecha de entrega |",
        "| ------------- | -------------------- | ---------------- |",
        f"| {AUTHOR} | {DATE} | Pendiente validación con negocio |",
        "",
        "---",
        "",
        "## Información general",
        "",
        "| Campo | Valor |",
        "| ----- | ----- |",
        f"| Nombre historia de usuario | {title} |",
        f"| Id. Requerimiento | {hid} |",
        f"| Id asociado | REQ-MT-{num} / EP-{ep} |",
        "",
        "### Descripción de historia de usuario",
        "",
        f"Como {como}, quiero {quiero}, para {para}.",
        "",
        "---",
        "",
        "## Actores",
        "",
        "| Tipo | Actor |",
        "| ---- | ----- |",
    ]
    for a, b in actors:
        lines.append(f"| {a} | {b} |")
    lines += [
        "",
        "---",
        "",
        "## Historias de usuario asociadas",
        "",
        "| Ítem | Nombre |",
        "| ---- | ------ |",
    ]
    for i, name in enumerate(associated, 1):
        lines.append(f"| {i} | {name} |")
    lines += [
        "",
        "---",
        "",
        "## Flujo básico",
        "",
        "### Precondiciones",
        "",
    ]
    for i, p in enumerate(preconds, 1):
        lines.append(f"{i}. {p}")
    lines += [
        "",
        "### Pasos",
        "",
        "| # | Actor | Sistema |",
        "| - | ----- | ------- |",
    ]
    for i, (a, s) in enumerate(steps, 1):
        lines.append(f"| {i} | {a} | {s} |")
    lines += [
        "",
        f"Resultado esperado: {title} queda operativa, aislada por empresa y gobernada por configuración.",
        "",
        "---",
        "",
        "## Flujos alternos",
        "",
        "| Id | Descripción |",
        "| -- | ----------- |",
    ]
    for i, d in enumerate(alternates, 1):
        lines.append(f"| FA-{i:02d} | {d} |")
    lines += [
        "",
        "---",
        "",
        "## Errores",
        "",
        "| Id | Situación | Comportamiento esperado |",
        "| -- | --------- | ----------------------- |",
    ]
    for i, (sit, beh) in enumerate(errors, 1):
        lines.append(f"| E-{i:02d} | {sit} | {beh} |")
    lines += [
        "",
        "---",
        "",
        "## Prototipo de interfaz de usuario y/o reportes",
        "",
        f"Pantalla o flujo de «{title}» dentro del módulo Malla de Turnos.",
        "",
        "1. Acceso desde el menú o acción contextual correspondiente",
        "2. Solo datos de la empresa del usuario y frentes de su alcance",
        "3. Mensajes de validación y confirmación claros",
        "",
        "---",
        "",
        "## Criterios de aceptación",
        "",
    ]
    for i, c in enumerate(criteria, 1):
        lines.append(f"{i}. {c}")
    # Always add tenant + param criteria for 10/10
    lines.append(f"{len(criteria)+1}. Solo se muestran o modifican datos de la empresa del usuario autenticado.")
    lines.append(
        f"{len(criteria)+2}. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto."
    )
    lines += [
        "",
        "---",
        "",
        "## Reglas de negocio",
        "",
        "| Id | Regla |",
        "| -- | ----- |",
    ]
    for i, r in enumerate(reglas, 1):
        lines.append(f"| RN-{i:02d} | {r} |")
    # Ensure anti-hardcoding RN
    n = len(reglas)
    lines.append(
        f"| RN-{n+1:02d} | No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto. |"
    )
    lines.append(
        f"| RN-{n+2:02d} | La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla. |"
    )
    lines += [
        "",
        "---",
        "",
        "## Datos de entrada",
        "",
        inputs,
        "",
        "---",
        "",
        "*Documento para cliente y diseño.*",
        "",
    ]
    return "\n".join(lines), folder, hid, title


def main():
    hus = json.loads((BD / "_parsed_hus.json").read_text(encoding="utf-8"))
    # Keep anexos and obsoletas
    written = []
    for h in hus:
        content, folder, hid, title = build_gst(h)
        slug = slugify(title)
        dest_dir = OUT / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        # remove previous GST for same HU id (except anexo)
        for old in dest_dir.glob(f"GST-FM-04-{hid}-*.md"):
            if "anexo-tecnico" in old.name:
                continue
            old.unlink()
        path = dest_dir / f"GST-FM-04-{hid}-{slug}.md"
        path.write_text(content, encoding="utf-8")
        written.append(path.relative_to(OUT).as_posix())

    print(f"Wrote {len(written)} GST-FM-04 files")

    # Verify hardcoding
    banned = [
        r"Contact Center",
        r"\b42\s*h",
        r"3 domingos",
        r"estudio,\s*salud",
        r"\bElemento\b",
        r"Prioridad Fase",
        r"Fase 2",
        r"Fase 3",
        r"\bJWT\b",
        r"work_schedule",
        r"companyId",
        r"\bRBAC\b",
        r"permisos\s+permisos",
        r"la\s+servicio",
        r"\bAPI\b",
        r"microservicio",
    ]
    hits = []
    for p in OUT.rglob("GST-FM-04-MT-EP*-HU*.md"):
        if "anexo" in p.name or "_Obsoletas" in str(p):
            continue
        text = p.read_text(encoding="utf-8")
        for pat in banned:
            if re.search(pat, text, re.I):
                hits.append((p.name, pat, re.search(pat, text, re.I).group(0)))
    print("Banned hits:", len(hits))
    for h in hits[:40]:
        print(" ", h)

    Path(BD / "_gst_written.txt").write_text("\n".join(written), encoding="utf-8")


if __name__ == "__main__":
    main()
