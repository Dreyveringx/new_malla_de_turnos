# -*- coding: utf-8 -*-
"""Genera PROPUESTA-BD-MALLA-TURNOS-GUIA-TABLAS.docx — explicación y prioridad de tablas."""
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx", "-q"])
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

OUT = Path(__file__).resolve().parent / "PROPUESTA-BD-MALLA-TURNOS-GUIA-TABLAS.docx"

doc = Document()
section = doc.sections[0]
section.top_margin = Cm(2)
section.bottom_margin = Cm(2)
section.left_margin = Cm(2.2)
section.right_margin = Cm(2.2)

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")


def set_cell_shading(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def add_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0x1A, 0x3A, 0x5C)
    return h


def p(text, bold=False, italic=False, size=11):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = "Calibri"
    return para


def bullet(text, bold_prefix=None):
    para = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        r = para.add_run(bold_prefix)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r2 = para.add_run(text)
        r2.font.name = "Calibri"
        r2.font.size = Pt(11)
    else:
        run = para.add_run(text)
        run.font.size = Pt(11)
        run.font.name = "Calibri"
    return para


# ---- Intro ----
t = doc.add_heading("Guia de tablas — Propuesta BD Malla de Turnos", 0)
for run in t.runs:
    run.font.color.rgb = RGBColor(0x1A, 0x3A, 0x5C)

p(
    "Modulo nuevo a integrar con GestionRRHH (ms_malla_turnos). "
    "Documento para decidir que tablas crear y cuales no, reutilizando lo que ya existe en GRH.",
    italic=True,
)
p("Base: sesion stakeholder 11-sep-2026 + plan BD del modulo.")
p("")

add_heading("1. Idea clave (leer primero)", 1)
p(
    "No todas las ~30 tablas del diagrama son obligatorias el dia 1. El modelo es completo para "
    "cubrir frentes, catalogos, grilla, swaps, novedades e importacion. Muchas filas son solo "
    "vinculos (N:M) o soporte. GRH ya tiene empresa, empleados, areas, cargos, usuarios, roles, "
    "festivos y notificaciones: esos NO se duplican."
)
p(
    "Regla de integracion: en ms_malla_turnos guardamos UUID logicos "
    "(company_id, employee_id, area_id, user_id, role_id). No hay FK cross-database hacia otros micros."
)

add_heading("Como leer la prioridad", 2)
for code, meaning in [
    ("OBLIGATORIA", "Nucleo del modulo. Sin ella no hay malla usable."),
    ("RECOMENDADA", "Necesaria para cumplir acuerdos de la sesion o un MVP realista."),
    ("OPCIONAL / FASE 2", "Se puede diferir si el frente no usa esa capacidad."),
    ("NO CREAR", "Ya vive en otro micro de GRH, o se elimino en la sesion."),
]:
    bullet(f" — {meaning}", bold_prefix=code)

add_heading("2. Resumen rapido", 1)
table = doc.add_table(rows=1, cols=3)
table.style = "Table Grid"
hdr = table.rows[0].cells
hdr[0].text = "Prioridad"
hdr[1].text = "Cantidad aprox."
hdr[2].text = "Que implica"
for c in hdr:
    set_cell_shading(c, "1A3A5C")
    for para in c.paragraphs:
        for run in para.runs:
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.bold = True

for a, b, c in [
    ("OBLIGATORIA", "aprox. 8-10", "Frente, turno, estados, malla, persona, celda, historial minimo"),
    ("RECOMENDADA", "aprox. 8-10", "Capacidades, vinculos area/turno, breaks, modalidad, reglas seed"),
    ("OPCIONAL / FASE 2", "aprox. 8-10", "Campanas, sitios, territorio, rotacion, swap, novedades, Excel"),
    ("NO CREAR", "varios", "Empleados, areas, auth, festivos, notificaciones, cobertura UI, cortes nomina"),
]:
    row = table.add_row().cells
    row[0].text = a
    row[1].text = b
    row[2].text = c

p("")
p(
    "Si el primer frente es tipo Mesa (semanal, sin campanas/territorio/sitio), se puede arrancar "
    "con un subconjunto pequeno y activar tablas cuando el frente pida esa capacidad.",
    italic=True,
)

add_heading("3. Explicacion tabla por tabla", 1)

# (name, group, priority, for_what, reuses, can_skip, notes)
tables = [
    (
        "operational_front",
        "Catalogos / Configuracion",
        "OBLIGATORIA",
        "Define cada frente operativo (Contact Center, Mesa, etc.): periodo (semana/quincena/mes), "
        "si se puede editar publicado, si hay intercambio, modo de armado.",
        "company_id, created_by/updated_by apuntan a GRH (empresa / auth). No reutiliza una tabla "
        "existente de 'frente': es concepto nuevo del modulo.",
        "No. Es el corazon de la parametrizacion por frente.",
        "Acuerdos sesion: periodo quincena para CC; builder/publisher separados como opcion.",
    ),
    (
        "front_capability",
        "Catalogos / Configuracion",
        "RECOMENDADA",
        "Flags por frente: usa territorio, campanas, modalidad, sitio, multi-break, multi-zona. "
        "Evita pantallas/columnas que el frente no necesita.",
        "Ninguna tabla GRH equivalente.",
        "Se podria meter JSON en operational_front, pero la tabla facilita consultas y evolucion. Mejor mantenerla.",
        "Permite no crear/usar campanas o territorio si el flag esta apagado.",
    ),
    (
        "front_area_link",
        "Catalogos / Configuracion",
        "RECOMENDADA",
        "Vincula el frente con una o varias areas de organizacion ya existentes en GRH (parametrizacion).",
        "area_id → ms_parametrization (solo UUID).",
        "Solo si el producto no filtra personas por area al armar mallas. En la practica casi siempre se necesita.",
        "No duplica el catalogo de areas: solo el vinculo.",
    ),
    (
        "front_user_scope",
        "Catalogos / Configuracion",
        "RECOMENDADA",
        "Que usuarios pueden ver/gestionar cada frente (alcance).",
        "user_id → ms_auth.",
        "Si el alcance se resuelve solo con roles/permisos globales de GRH, se puede diferir. "
        "Util cuando un coordinador solo ve 'su' frente.",
        "Complementa RBAC de auth; no reemplaza roles del sistema.",
    ),
    (
        "front_role_scope",
        "Catalogos / Configuracion",
        "OPCIONAL / FASE 2",
        "Igual que user_scope pero por rol (todos los usuarios con ese rol ven el frente).",
        "role_id → ms_auth.",
        "Si, si al inicio se asigna alcance solo por usuario o por permiso generico.",
        "Alternativa a listar usuarios uno a uno.",
    ),
    (
        "catalog_code_sequence",
        "Catalogos / Configuracion",
        "RECOMENDADA",
        "Genera codigos auto-consecutivos (T001, EST01, etc.) por empresa y tipo de catalogo.",
        "No existe equivalente generico en GRH para este modulo.",
        "Si temporalmente (codigos manuales), pero la sesion pidio auto-consecutivo (#3).",
        "Sitios pueden seguir siendo manuales segun acuerdo.",
    ),
    (
        "shift_template",
        "Catalogos / Configuracion",
        "OBLIGATORIA",
        "Catalogo de turnos (manana, tarde, noche): horario, color, si cruza medianoche, multi-break.",
        "No hay catalogo de turnos reutilizable hoy en GRH para este uso. Es del modulo.",
        "No.",
        "Un turno = un horario; la zona no cambia el turno (acuerdo sesion).",
    ),
    (
        "shift_template_front",
        "Catalogos / Configuracion",
        "RECOMENDADA",
        "Que turnos estan habilitados para cada frente (catalogo unico de empresa, activacion por frente).",
        "Ninguna.",
        "Solo si todos los frentes comparten exactamente los mismos turnos siempre (poco realista).",
        "Evita duplicar el turno por frente.",
    ),
    (
        "shift_template_day_schedule",
        "Catalogos / Configuracion",
        "OPCIONAL / FASE 2",
        "Horario distinto por dia de la semana dentro de la misma plantilla (si aplica).",
        "Ninguna.",
        "Si, si al inicio todos los turnos tienen el mismo start/end todos los dias (ya estan en shift_template).",
        "Usar solo cuando haya turnos con variacion diaria.",
    ),
    (
        "shift_template_break",
        "Catalogos / Configuracion",
        "RECOMENDADA",
        "Breaks definidos en la plantilla del turno (uno o varios).",
        "Ninguna.",
        "Diferible si el MVP no modela breaks; la sesion pidio multi-break (#11).",
        "Las celdas pueden sobrescribir/aplicar breaks en schedule_cell_break.",
    ),
    (
        "cell_state",
        "Catalogos / Configuracion",
        "OBLIGATORIA",
        "Estados de celda: trabajo, descanso, vacaciones, incapacidad, etc. (catalogo configurable).",
        "No confundir con estados de empleado en GRH. Aqui es estado de la celda de la malla.",
        "No (aunque se puede seedear un set fijo al inicio).",
        "Codigos auto-consecutivos recomendados.",
    ),
    (
        "work_modality",
        "Catalogos / Configuracion",
        "RECOMENDADA (o REUTILIZAR)",
        "Catalogo global de modalidades (presencial, remoto, hibrido). Una sola lista por empresa.",
        "Si GRH ya tiene un catalogo de modalidad laboral usable via API, se puede REUTILIZAR y no crear "
        "esta tabla; solo guardar modality_id logico en la celda.",
        "Crear solo si no existe catalogo equivalente en parametrizacion/empleado. Sesion: modalidad GLOBAL (#2).",
        "Decision de producto: existe modalidad en GRH hoy? Si si → NO crear; si no → crear aqui.",
    ),
    (
        "attendance_site",
        "Catalogos / Configuracion",
        "OPCIONAL / FASE 2",
        "Sitios / sedes de asistencia (cuando el frente usa sitio).",
        "Si sedes ya existen en company-admin/parametrizacion, reutilizar UUID y no duplicar.",
        "Si, si front_capability.usa_sitio = false (p. ej. Mesa).",
        "Codigos pueden ser manuales.",
    ),
    (
        "attendance_site_front",
        "Catalogos / Configuracion",
        "OPCIONAL / FASE 2",
        "Habilita sitios por frente.",
        "Depende de attendance_site (o del catalogo GRH de sedes).",
        "Si, junto con sitios.",
        "",
    ),
    (
        "campaign",
        "Catalogos / Configuracion",
        "OPCIONAL / FASE 2",
        "Campanas operativas (Contact Center). Se asignan en la celda, no en el encabezado de la malla.",
        "Concepto nuevo del modulo (no es campana de seleccion de GRH).",
        "Si, si el frente no usa campanas (Mesa). Activar con usa_campanas.",
        "Acuerdo #17: sin campaign_id en cabecera de malla.",
    ),
    (
        "territory_level",
        "Catalogos / Configuracion",
        "OPCIONAL / FASE 2",
        "Niveles del arbol territorial (ej. Zona → SPT).",
        "No es el organigrama de areas GRH; es jerarquia operativa de cobertura.",
        "Si, si no hay multi-zona/territorio.",
        "Acuerdos #10/#14 multi-zona.",
    ),
    (
        "territory_node",
        "Catalogos / Configuracion",
        "OPCIONAL / FASE 2",
        "Nodos del territorio (zonas, SPT, etc.).",
        "No reutilizar areas GRH como si fueran zonas, salvo que negocio diga que son lo mismo (hoy no).",
        "Si, si no aplica territorio.",
        "",
    ),
    (
        "validation_rule",
        "Reglas internas y horas",
        "RECOMENDADA",
        "Reglas internas (seed/config): descansos, solapes, maximos, etc. Sin pantallas de cobertura/compensatorio.",
        "Ninguna en GRH.",
        "Se puede hardcodear reglas en codigo al inicio; la tabla permite tunear por empresa/frente sin redeploy.",
        "Sesion elimino UI de cobertura (#4) y compensatorio (#5); la logica puede vivir aqui o en codigo.",
    ),
    (
        "hour_classification_band",
        "Reglas internas y horas",
        "OPCIONAL / FASE 2",
        "Franjas para clasificar horas (diurna, nocturna, dominical, etc.) de cara a recargos.",
        "Festivos se leen de ms_parametrization (NO crear tabla de festivos ni cortes de nomina).",
        "Si al inicio si no se calcula recargo en el modulo; sesion #8 lo dejo como necesidad de franjas.",
        "Eliminado payroll_cutoff (#6).",
    ),
    (
        "rotation_pattern",
        "Reglas internas y horas",
        "OPCIONAL / FASE 2",
        "Patrones de rotacion para sugerir/asignar al cerrar o en modo asistido/automatico.",
        "Ninguna.",
        "Si, si el MVP es solo armado manual.",
        "Sesion #12: rotacion al cerrar periodo.",
    ),
    (
        "rotation_pattern_step",
        "Reglas internas y horas",
        "OPCIONAL / FASE 2",
        "Pasos del patron (dia N → turno/estado).",
        "Depende de rotation_pattern.",
        "Si, junto con el patron.",
        "",
    ),
    (
        "schedule_grid",
        "Operacion / Planificacion",
        "OBLIGATORIA",
        "La malla en si: frente + periodo (desde/hasta) + estado (borrador, publicada) + modo de armado.",
        "company_id, created_by → GRH. Sin campaign_id en cabecera.",
        "No.",
        "Periodo segun frente (semana / quincena / mes).",
    ),
    (
        "schedule_grid_person",
        "Operacion / Planificacion",
        "OBLIGATORIA",
        "Personas incluidas en esa malla (fila de la grilla).",
        "employee_id → ms_employee (datos de persona NO se copian; se consultan por API).",
        "No.",
        "Puede llevar modalidad/sitio por defecto de la persona en el periodo.",
    ),
    (
        "schedule_grid_person_territory",
        "Operacion / Planificacion",
        "OPCIONAL / FASE 2",
        "Multi-zona / SPT asignados a la persona dentro de la malla.",
        "territory_node del modulo.",
        "Si, si no hay multi-zona.",
        "Acuerdos #10/#14.",
    ),
    (
        "schedule_cell",
        "Operacion / Planificacion",
        "OBLIGATORIA",
        "Celda dia x persona: turno, estado, modalidad, sitio, campana, horas, notas.",
        "Referencias logicas a catalogos del modulo + modality/site si vienen de GRH.",
        "No.",
        "Es donde ocurre la operacion diaria.",
    ),
    (
        "schedule_cell_territory",
        "Operacion / Planificacion",
        "OPCIONAL / FASE 2",
        "Territorios asociados a una celda concreta (si aplica override por dia).",
        "territory_node.",
        "Si, si no hay territorio o solo se modela a nivel persona.",
        "",
    ),
    (
        "schedule_cell_break",
        "Operacion / Planificacion",
        "RECOMENDADA",
        "Breaks reales aplicados/registrados en la celda (incluyendo especiales).",
        "Puede nacer desde shift_template_break.",
        "Diferible si el MVP no gestiona breaks en grilla.",
        "Multi-break #11.",
    ),
    (
        "schedule_cell_history",
        "Operacion / Planificacion",
        "OBLIGATORIA (minimo)",
        "Auditoria de cambios en celdas (quien cambio que y cuando), sobre todo si published_editable = true.",
        "user_id → ms_auth. No reemplaza ms_audit global; es historial de negocio de la malla.",
        "No recomendable omitir si hay edicion post-publicacion. Se puede empezar con eventos minimos.",
        "Complementario a audit-service si mas adelante se integra.",
    ),
    (
        "shift_swap_request",
        "Intercambio, novedades e importacion",
        "OPCIONAL / FASE 2",
        "Solicitudes de intercambio entre personas. Sin tope mensual (#16).",
        "employee_id / user_id → GRH. Notificacion via ms_notification.",
        "Si, si swap_enabled = false en el frente al inicio.",
        "Activar cuando el frente habilite intercambio.",
    ),
    (
        "schedule_novelty",
        "Intercambio, novedades e importacion",
        "OPCIONAL / FASE 2",
        "Novedades (ausencias, cambios) vinculadas a la malla (#18).",
        "Evaluar si GRH ya tiene novedades de nomina/asistencia; si si, integrar por ID y no duplicar el dominio.",
        "Si al inicio; o solo un vinculo liviano a un sistema externo de novedades.",
        "Decision importante de reuso: la novedad es del modulo o de otro sistema?",
    ),
    (
        "excel_import_batch",
        "Intercambio, novedades e importacion",
        "OPCIONAL / FASE 2",
        "Cabecera de carga masiva Excel (quien, cuando, estado del lote).",
        "Ninguna.",
        "Si, si el armado es solo UI; la sesion mantuvo plantilla Excel (#20).",
        "Util para Contact Center / volumenes altos.",
    ),
    (
        "excel_import_row",
        "Intercambio, novedades e importacion",
        "OPCIONAL / FASE 2",
        "Detalle por fila del Excel (errores de validacion, mapeo).",
        "Depende del batch.",
        "Si, junto con importacion.",
        "",
    ),
]


def add_table_section(item):
    name, group, priority, for_what, reuses, can_skip, notes = item
    add_heading(name, 2)
    meta = doc.add_paragraph()
    r1 = meta.add_run("Grupo: ")
    r1.bold = True
    meta.add_run(f"{group}    ")
    r2 = meta.add_run("Prioridad: ")
    r2.bold = True
    r3 = meta.add_run(priority)
    r3.bold = True
    if priority.startswith("OBLIGATORIA"):
        r3.font.color.rgb = RGBColor(0xB0, 0x00, 0x20)
    elif priority.startswith("RECOMENDADA"):
        r3.font.color.rgb = RGBColor(0xC6, 0x5D, 0x00)
    elif priority.startswith("OPCIONAL"):
        r3.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)
    else:
        r3.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p("Para que sirve", bold=True)
    p(for_what)
    p("Que reutiliza de GRH / que no duplicar", bold=True)
    p(reuses)
    p("Se puede no crear o diferir?", bold=True)
    p(can_skip)
    if notes:
        p("Nota de sesion / diseno", bold=True)
        p(notes)


for item in tables:
    add_table_section(item)

add_heading("4. Lo que NO se crea en ms_malla_turnos", 1)
p("Estos conceptos se consumen de otros micros o se eliminaron en la sesion:")

t2 = doc.add_table(rows=1, cols=3)
t2.style = "Table Grid"
h = t2.rows[0].cells
h[0].text = "Concepto"
h[1].text = "Donde vive"
h[2].text = "Implicacion"
for c in h:
    set_cell_shading(c, "1A3A5C")
    for para in c.paragraphs:
        for run in para.runs:
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.bold = True

for a, b, c in [
    ("company_id (empresa)", "ms_company_admin / JWT", "Tenant en todas las tablas; nunca tabla local de empresas."),
    ("employee_id (persona)", "ms_employee", "Nombre, documento, cargo, etc. por API. Solo UUID en malla."),
    ("area_id / cargo_id", "ms_parametrization", "Organizacion ya existe; solo vinculos."),
    ("user_id / role_id", "ms_auth", "Permisos, alcance, auditoria de quien cambio."),
    ("Festivos / calendario", "ms_parametrization", "Lectura API. No tabla local de cortes de nomina (#6)."),
    ("Notificaciones", "ms_notification", "Publicacion y cambios (#13); el modulo emite eventos."),
    ("coverage_rule (UI)", "Eliminado sesion #4", "Sin pantalla de cobertura por franjas."),
    ("compensatory_rule (UI)", "Eliminado sesion #5", "Sin pantalla de compensatorio."),
    ("payroll_cutoff", "Eliminado sesion #6", "Sin calendario de cortes de nomina en el modulo."),
    ("work_modality_front", "Eliminado sesion #2", "Modalidad es global, no por frente."),
    ("swap_monthly_limit", "Eliminado sesion #16", "Solicitudes de intercambio sin tope mensual."),
]:
    row = t2.add_row().cells
    row[0].text = a
    row[1].text = b
    row[2].text = c

add_heading("5. Subconjunto sugerido para un MVP (Mesa o primer frente simple)", 1)
p("Si el objetivo es validar armado y publicacion sin Contact Center completo:")

p("Crear si o si", bold=True)
for name in [
    "operational_front",
    "front_capability (aunque sea con flags en false)",
    "front_area_link",
    "shift_template + shift_template_front",
    "cell_state",
    "schedule_grid + schedule_grid_person + schedule_cell",
    "schedule_cell_history (minimo)",
    "catalog_code_sequence (o codigos manuales temporales)",
]:
    bullet(name)

p("Diferir hasta que el frente lo pida", bold=True)
for name in [
    "campaign, attendance_site*, territory_*",
    "schedule_grid_person_territory, schedule_cell_territory",
    "shift_template_day_schedule",
    "rotation_pattern*",
    "shift_swap_request",
    "schedule_novelty (o integrar novedad GRH existente)",
    "excel_import_*",
    "hour_classification_band (si no hay calculo de recargo aun)",
    "front_role_scope",
]:
    bullet(name)

p("Decidir con el equipo GRH antes de crear", bold=True)
for name in [
    "work_modality — ya existe catalogo en parametrizacion/empleado?",
    "attendance_site — ya existen sedes/sitios en company-admin?",
    "schedule_novelty — el dominio de novedades ya esta en otro modulo?",
]:
    bullet(name)

add_heading("6. Como usar este documento con el Excel y dbdiagram", 1)
bullet("detalle columna a columna (tipo y descripcion).", bold_prefix="Excel / CSV: ")
bullet("diagrama visual de relaciones internas del modulo.", bold_prefix="dbdiagram (.dbml): ")
bullet("decide que tablas entran al MVP y cuales se aplazan o se reutilizan.", bold_prefix="Esta guia: ")

p("")
p("Archivos hermanos en docs/:", italic=True)
bullet("PROPUESTA-BD-MALLA-TURNOS.xlsx")
bullet("PROPUESTA-BD-MALLA-TURNOS-COLUMNAS.csv")
bullet("PROPUESTA-BD-MALLA-TURNOS.dbml")

doc.save(OUT)
print("OK", OUT)
print("bytes", OUT.stat().st_size)
