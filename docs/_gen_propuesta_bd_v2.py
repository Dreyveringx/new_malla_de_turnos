# -*- coding: utf-8 -*-
"""
Propuesta BD Malla de Turnos v2 — post revision stakeholder (sep-2026).
Genera:
  - PROPUESTA-BD-MALLA-TURNOS-COLUMNAS.csv
  - PROPUESTA-BD-MALLA-TURNOS.xlsx  (hojas por BD + decisiones)
  - PROPUESTA-BD-MALLA-TURNOS.dbml
  - PROPUESTA-BD-MALLA-TURNOS-DECISIONES.md
"""
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl", "-q"])
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment

OUT = Path(__file__).resolve().parent
rows = []  # Base_datos, Grupo, Tabla, Columna, Tipo_dato, Descripcion


def add(db, grupo, table, col, typ, desc):
    rows.append((db, grupo, table, col, typ, desc))


DB_PARAM = "ms_parametrization"
DB_MALLA = "ms_malla_turnos"
DB_AUDIT = "ms_audit (reutilizar)"
DB_NONE = "NO CREAR"

G_PARAM = "Catalogos transversales (nuevos o reuso)"
G_MALLA_CFG = "Configuracion de frente / vinculos"
G_MALLA_OP = "Operacion / Planificacion"
G_MALLA_EXT = "Intercambio, novedades e importacion"
G_REUSE = "Ya existe en GRH — solo UUID logico"
G_DROP = "Eliminado del diseno"

# =============================================================================
# ms_parametrization — catalogos transversales NUEVOS
# =============================================================================

T = "catalog_code_sequence"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Secuencia de codigos auto-consecutivos transversal a TODOS los catalogos GRH.")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant. NULL solo si el catalogo es global del sistema.")
add(DB_PARAM, G_PARAM, T, "catalog_type", "VARCHAR(60) NOT NULL", "Ej. shift_template | cell_state | work_modality | attendance_site | operational_label | territory | operational_front | eps | positions...")
add(DB_PARAM, G_PARAM, T, "prefix", "VARCHAR(10) NULL", "Prefijo opcional (T, EST, SIT).")
add(DB_PARAM, G_PARAM, T, "next_value", "INT NOT NULL DEFAULT 1", "Siguiente consecutivo.")
add(DB_PARAM, G_PARAM, T, "pad_length", "SMALLINT NOT NULL DEFAULT 3", "Relleno (001).")
add(DB_PARAM, G_PARAM, T, "UNIQUE", "(company_id, catalog_type)", "Una secuencia por empresa y tipo.")

T = "shift_template"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Plantilla de turno OPERATIVO (Manana A, Noche B). NO es work_schedule (jornada contractual).")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant.")
add(DB_PARAM, G_PARAM, T, "code", "VARCHAR(20) NOT NULL", "UNIQUE(company_id, code). Preferible via catalog_code_sequence.")
add(DB_PARAM, G_PARAM, T, "name", "VARCHAR(120) NOT NULL", "Nombre visible.")
add(DB_PARAM, G_PARAM, T, "start_time", "TIME NOT NULL", "Hora inicio. Un turno = un horario (zona no lo cambia).")
add(DB_PARAM, G_PARAM, T, "end_time", "TIME NOT NULL", "Hora fin.")
add(DB_PARAM, G_PARAM, T, "crosses_midnight", "BOOLEAN NOT NULL DEFAULT FALSE", "Fin al dia siguiente.")
add(DB_PARAM, G_PARAM, T, "color_hex", "VARCHAR(7) NULL", "Color en grilla.")
add(DB_PARAM, G_PARAM, T, "net_hours", "NUMERIC(5,2) NULL", "Horas netas de referencia.")
add(DB_PARAM, G_PARAM, T, "multi_break_enabled", "BOOLEAN NOT NULL DEFAULT FALSE", "Permite varios breaks (#11).")
add(DB_PARAM, G_PARAM, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")
add(DB_PARAM, G_PARAM, T, "created_at", "TIMESTAMPTZ NOT NULL", "")
add(DB_PARAM, G_PARAM, T, "updated_at", "TIMESTAMPTZ NOT NULL", "")
add(
    DB_PARAM,
    G_PARAM,
    T,
    "NOTE_REUSO",
    "NO reutilizar work_schedule",
    "work_schedule / work_schedule_day / work_schedule_shift = jornada contractual por dia de semana (horas base, CPM, schedule_assignment). "
    "shift_template = catalogo de turnos para celdas de malla (codigo, color, habilitacion por frente). Dominios distintos → se deja esta tabla en parametrization.",
)

T = "break_type"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Tipos de pausa transversales (almuerzo, break, lactancia...). Reutilizable por malla y otros modulos.")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant.")
add(DB_PARAM, G_PARAM, T, "code", "VARCHAR(20) NOT NULL", "UNIQUE(company_id, code).")
add(DB_PARAM, G_PARAM, T, "name", "VARCHAR(80) NOT NULL", "Etiqueta.")
add(DB_PARAM, G_PARAM, T, "default_minutes", "INT NULL", "Duracion sugerida.")
add(DB_PARAM, G_PARAM, T, "paid_default", "BOOLEAN NOT NULL DEFAULT FALSE", "Si la pausa es remunerada por defecto.")
add(DB_PARAM, G_PARAM, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")

T = "shift_template_break"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Breaks definidos en una plantilla de turno (1..N).")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant.")
add(DB_PARAM, G_PARAM, T, "shift_template_id", "UUID NOT NULL", "FK -> shift_template.id")
add(DB_PARAM, G_PARAM, T, "break_type_id", "UUID NOT NULL", "FK -> break_type.id")
add(DB_PARAM, G_PARAM, T, "duration_minutes", "INT NOT NULL", "Minutos de esta instancia.")
add(DB_PARAM, G_PARAM, T, "paid", "BOOLEAN NOT NULL DEFAULT FALSE", "Override del default del tipo.")
add(DB_PARAM, G_PARAM, T, "sort_order", "SMALLINT NOT NULL DEFAULT 0", "")

T = "work_modality"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Modalidad laboral GLOBAL (presencial, remoto, hibrido). NO confundir con study_modalities.")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant.")
add(DB_PARAM, G_PARAM, T, "code", "VARCHAR(20) NOT NULL", "UNIQUE(company_id, code).")
add(DB_PARAM, G_PARAM, T, "name", "VARCHAR(80) NOT NULL", "")
add(DB_PARAM, G_PARAM, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")
add(
    DB_PARAM,
    G_PARAM,
    T,
    "NOTE_REUSO",
    "No existe hoy",
    "En GRH solo hay study_modalities (estudios academicos). No hay modalidad laboral → catalogo nuevo transversal.",
)

T = "attendance_site"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Sitio/sede de asistencia. Catalogo transversal. NO existe hoy en parametrization ni company-admin.")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant.")
add(DB_PARAM, G_PARAM, T, "code", "VARCHAR(20) NOT NULL", "Puede ser manual o via catalog_code_sequence.")
add(DB_PARAM, G_PARAM, T, "name", "VARCHAR(120) NOT NULL", "")
add(DB_PARAM, G_PARAM, T, "address", "TEXT NULL", "Direccion opcional.")
add(DB_PARAM, G_PARAM, T, "city_id", "UUID NULL", "UUID logico cities (parametrization).")
add(DB_PARAM, G_PARAM, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")
add(
    DB_PARAM,
    G_PARAM,
    T,
    "NOTE",
    "sin attendance_site_front",
    "Se quito el vinculo por frente: si el frente tiene capability usa_sitio, usa el catalogo de la empresa.",
)

T = "operational_label"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Etiquetas informativas (antes 'campaign'). Catalogo transversal reutilizable (tags/labels).")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant.")
add(DB_PARAM, G_PARAM, T, "code", "VARCHAR(20) NOT NULL", "UNIQUE(company_id, code).")
add(DB_PARAM, G_PARAM, T, "name", "VARCHAR(120) NOT NULL", "Ej. Campana X, Cliente Y, Proyecto Z.")
add(DB_PARAM, G_PARAM, T, "color_hex", "VARCHAR(7) NULL", "Color chip.")
add(DB_PARAM, G_PARAM, T, "category", "VARCHAR(40) NULL", "Opcional: campana | cliente | otro.")
add(DB_PARAM, G_PARAM, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")
add(
    DB_PARAM,
    G_PARAM,
    T,
    "NOTE",
    "renombra campaign",
    "En malla se referencia como label_id en la celda (informativo). No va en cabecera de malla (#17).",
)

T = "territory"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Arbol territorial unico (adyacencia). Un nodo puede tener parent_id → hijos → nietos.")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant.")
add(DB_PARAM, G_PARAM, T, "parent_id", "UUID NULL", "FK -> territory.id (NULL = raiz).")
add(DB_PARAM, G_PARAM, T, "code", "VARCHAR(20) NOT NULL", "UNIQUE(company_id, code).")
add(DB_PARAM, G_PARAM, T, "name", "VARCHAR(120) NOT NULL", "Ej. Zona Norte, SPT-12.")
add(DB_PARAM, G_PARAM, T, "level_label", "VARCHAR(40) NULL", "Etiqueta libre del nivel (Zona, SPT...). Sin tabla territory_level.")
add(DB_PARAM, G_PARAM, T, "sort_order", "INT NOT NULL DEFAULT 0", "")
add(DB_PARAM, G_PARAM, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")
add(
    DB_PARAM,
    G_PARAM,
    T,
    "NOTE_REUSO",
    "No reutilizar zone_types ni areas",
    "zone_types = tipificacion urbana/rural global. organizational_areas = organigrama. "
    "territory = cobertura operativa jerarquica de malla (multi-zona #10/#14).",
)

T = "hour_classification_band"
add(DB_PARAM, G_PARAM, T, "id", "UUID PK", "Franjas para clasificar horas (ordinaria, nocturna, dominical, festiva, extras). Transversal (malla, reportes, futuros calculos).")
add(DB_PARAM, G_PARAM, T, "company_id", "UUID NOT NULL", "Tenant.")
add(DB_PARAM, G_PARAM, T, "code", "VARCHAR(20) NOT NULL", "ORDI | NOCT | DOM | FEST | HEXA | HEXN. UNIQUE(company_id, code)")
add(DB_PARAM, G_PARAM, T, "name", "VARCHAR(120) NOT NULL", "Nombre reporteria.")
add(DB_PARAM, G_PARAM, T, "band_type", "VARCHAR(40) NOT NULL", "ordinaria | nocturna | dominical | festiva | extra_diurna | extra_nocturna")
add(DB_PARAM, G_PARAM, T, "start_time", "TIME NULL", "Inicio franja horaria.")
add(DB_PARAM, G_PARAM, T, "end_time", "TIME NULL", "Fin franja.")
add(DB_PARAM, G_PARAM, T, "crosses_midnight", "BOOLEAN NOT NULL DEFAULT FALSE", "")
add(DB_PARAM, G_PARAM, T, "applies_sunday", "BOOLEAN NOT NULL DEFAULT FALSE", "")
add(DB_PARAM, G_PARAM, T, "applies_holiday", "BOOLEAN NOT NULL DEFAULT FALSE", "Festivos: leer company_calendar / national_holidays (ya existen).")
add(DB_PARAM, G_PARAM, T, "priority", "INT NOT NULL DEFAULT 100", "Si dos franjas solapan, gana menor priority.")
add(DB_PARAM, G_PARAM, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")
add(
    DB_PARAM,
    G_PARAM,
    T,
    "NOTE",
    "recargos",
    "Si la persona tiene varios turnos/slots el mismo dia, cada celda (slot) se clasifica contra estas franjas + festivos. "
    "No calcula nomina: solo clasifica horas para reporteria/export. Cortes de nomina NO van aqui (#6).",
)

# cell_state → REUSO entity_status (filas de documentacion)
add(
    DB_PARAM,
    G_REUSE,
    "entity_status (REUSO)",
    "entity_type",
    "VARCHAR = 'malla_cell_state'",
    "YA EXISTE. Usar entity_status con entity_type='malla_cell_state' (o similar) para Trabajo, Descanso, VAC, INC... "
    "Tiene name, color, sort_order, is_active, is_final_status. NO crear cell_state aparte.",
)
add(
    DB_PARAM,
    G_REUSE,
    "entity_status (REUSO)",
    "como se usa",
    "UUID logico",
    "En schedule_cell.cell_state_id guardar entity_status.id. Filtrar por company_id + entity_type.",
)

# =============================================================================
# ms_malla_turnos — dominio
# =============================================================================

T = "operational_front"
add(DB_MALLA, G_MALLA_CFG, T, "id", "UUID PK", "Frente operativo (Contact Center, Mesa...).")
add(DB_MALLA, G_MALLA_CFG, T, "company_id", "UUID NOT NULL", "Tenant GRH (logico).")
add(DB_MALLA, G_MALLA_CFG, T, "code", "VARCHAR(20) NOT NULL", "UNIQUE(company_id, code). Via catalog_code_sequence (param).")
add(DB_MALLA, G_MALLA_CFG, T, "name", "VARCHAR(120) NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "description", "TEXT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "builder_profile_label", "VARCHAR(120) NULL", "Texto guia del perfil que arma.")
add(DB_MALLA, G_MALLA_CFG, T, "publisher_profile_label", "VARCHAR(120) NULL", "Texto guia del perfil que publica.")
add(DB_MALLA, G_MALLA_CFG, T, "separate_builder_publisher", "BOOLEAN NOT NULL DEFAULT FALSE", "")
add(DB_MALLA, G_MALLA_CFG, T, "build_mode", "VARCHAR(20) NOT NULL", "manual | asistido | automatico")
add(DB_MALLA, G_MALLA_CFG, T, "period_type", "VARCHAR(10) NOT NULL", "semana | quincena | mes")
add(DB_MALLA, G_MALLA_CFG, T, "published_editable", "BOOLEAN NOT NULL DEFAULT FALSE", "")
add(DB_MALLA, G_MALLA_CFG, T, "swap_enabled", "BOOLEAN NOT NULL DEFAULT FALSE", "Sin tope mensual (#16).")
add(DB_MALLA, G_MALLA_CFG, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")
add(DB_MALLA, G_MALLA_CFG, T, "created_at", "TIMESTAMPTZ NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "updated_at", "TIMESTAMPTZ NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "created_by", "UUID NULL", "user_id ms_auth.")
add(DB_MALLA, G_MALLA_CFG, T, "updated_by", "UUID NULL", "")

T = "front_capability"
add(DB_MALLA, G_MALLA_CFG, T, "id", "UUID PK", "Flags: usa_territorio | usa_labels | usa_modalidad | usa_sitio | usa_multi_break | usa_multi_zona")
add(DB_MALLA, G_MALLA_CFG, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "front_id", "UUID NOT NULL", "FK -> operational_front.id")
add(DB_MALLA, G_MALLA_CFG, T, "capability_code", "VARCHAR(40) NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "enabled", "BOOLEAN NOT NULL DEFAULT FALSE", "")
add(DB_MALLA, G_MALLA_CFG, T, "config_json", "JSONB NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "UNIQUE", "(company_id, front_id, capability_code)", "")

T = "front_area_link"
add(DB_MALLA, G_MALLA_CFG, T, "id", "UUID PK", "Frente ↔ areas GRH (organizational_areas).")
add(DB_MALLA, G_MALLA_CFG, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "front_id", "UUID NOT NULL", "FK -> operational_front.id")
add(DB_MALLA, G_MALLA_CFG, T, "area_id", "UUID NOT NULL", "UUID logico organizational_areas.")
add(DB_MALLA, G_MALLA_CFG, T, "UNIQUE", "(company_id, front_id, area_id)", "")

T = "front_user_scope"
add(DB_MALLA, G_MALLA_CFG, T, "id", "UUID PK", "Alcance por usuario (que frentes ve). Roles → RBAC ms_auth (sin front_role_scope).")
add(DB_MALLA, G_MALLA_CFG, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "front_id", "UUID NOT NULL", "FK -> operational_front.id")
add(DB_MALLA, G_MALLA_CFG, T, "user_id", "UUID NOT NULL", "UUID logico ms_auth.")
add(DB_MALLA, G_MALLA_CFG, T, "UNIQUE", "(company_id, front_id, user_id)", "")

T = "shift_template_front"
add(DB_MALLA, G_MALLA_CFG, T, "id", "UUID PK", "Habilita plantillas de turno (param) en un frente.")
add(DB_MALLA, G_MALLA_CFG, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "front_id", "UUID NOT NULL", "FK -> operational_front.id")
add(DB_MALLA, G_MALLA_CFG, T, "shift_template_id", "UUID NOT NULL", "UUID logico shift_template (param).")
add(DB_MALLA, G_MALLA_CFG, T, "UNIQUE", "(company_id, front_id, shift_template_id)", "")

T = "rotation_pattern"
add(DB_MALLA, G_MALLA_CFG, T, "id", "UUID PK", "Patron de rotacion por frente (#12).")
add(DB_MALLA, G_MALLA_CFG, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "front_id", "UUID NOT NULL", "FK -> operational_front.id")
add(DB_MALLA, G_MALLA_CFG, T, "code", "VARCHAR(20) NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "name", "VARCHAR(120) NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "cycle_length", "SMALLINT NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "auto_apply_on_period_close", "BOOLEAN NOT NULL DEFAULT TRUE", "")
add(DB_MALLA, G_MALLA_CFG, T, "active", "BOOLEAN NOT NULL DEFAULT TRUE", "")

T = "rotation_pattern_step"
add(DB_MALLA, G_MALLA_CFG, T, "id", "UUID PK", "Paso del patron.")
add(DB_MALLA, G_MALLA_CFG, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "pattern_id", "UUID NOT NULL", "FK -> rotation_pattern.id")
add(DB_MALLA, G_MALLA_CFG, T, "step_order", "SMALLINT NOT NULL", "")
add(DB_MALLA, G_MALLA_CFG, T, "shift_template_id", "UUID NULL", "UUID logico shift_template (param).")
add(DB_MALLA, G_MALLA_CFG, T, "cell_state_id", "UUID NULL", "UUID logico entity_status (param).")

T = "schedule_grid"
add(DB_MALLA, G_MALLA_OP, T, "id", "UUID PK", "Cabecera de malla.")
add(DB_MALLA, G_MALLA_OP, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "front_id", "UUID NOT NULL", "FK -> operational_front.id")
add(DB_MALLA, G_MALLA_OP, T, "name", "VARCHAR(160) NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "period_start", "DATE NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "period_end", "DATE NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "period_type", "VARCHAR(10) NOT NULL", "semana | quincena | mes")
add(DB_MALLA, G_MALLA_OP, T, "status", "VARCHAR(20) NOT NULL", "borrador | revision | publicada | cerrada | rechazada")
add(DB_MALLA, G_MALLA_OP, T, "build_mode", "VARCHAR(20) NOT NULL", "manual | asistido | automatico")
add(DB_MALLA, G_MALLA_OP, T, "owner_user_id", "UUID NULL", "ms_auth")
add(DB_MALLA, G_MALLA_OP, T, "publisher_user_id", "UUID NULL", "ms_auth")
add(DB_MALLA, G_MALLA_OP, T, "rejection_reason", "TEXT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "published_at", "TIMESTAMPTZ NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "closed_at", "TIMESTAMPTZ NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "version", "INT NOT NULL DEFAULT 1", "")
add(DB_MALLA, G_MALLA_OP, T, "created_at", "TIMESTAMPTZ NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "updated_at", "TIMESTAMPTZ NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "NOTE", "sin label en cabecera", "Etiquetas van en celda (#17).")

T = "schedule_grid_person"
add(DB_MALLA, G_MALLA_OP, T, "id", "UUID PK", "Persona en la malla.")
add(DB_MALLA, G_MALLA_OP, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "grid_id", "UUID NOT NULL", "FK -> schedule_grid.id")
add(DB_MALLA, G_MALLA_OP, T, "employee_id", "UUID NOT NULL", "UUID logico ms_employee.")
add(DB_MALLA, G_MALLA_OP, T, "sort_order", "INT NOT NULL DEFAULT 0", "")
add(DB_MALLA, G_MALLA_OP, T, "modality_id", "UUID NULL", "UUID logico work_modality (param).")
add(DB_MALLA, G_MALLA_OP, T, "site_id", "UUID NULL", "UUID logico attendance_site (param).")
add(DB_MALLA, G_MALLA_OP, T, "UNIQUE", "(grid_id, employee_id)", "")

T = "schedule_grid_person_territory"
add(DB_MALLA, G_MALLA_OP, T, "id", "UUID PK", "Multi-zona/SPT de la persona en el periodo.")
add(DB_MALLA, G_MALLA_OP, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "grid_person_id", "UUID NOT NULL", "FK -> schedule_grid_person.id")
add(DB_MALLA, G_MALLA_OP, T, "territory_id", "UUID NOT NULL", "UUID logico territory (param).")
add(DB_MALLA, G_MALLA_OP, T, "is_primary", "BOOLEAN NOT NULL DEFAULT FALSE", "")
add(DB_MALLA, G_MALLA_OP, T, "UNIQUE", "(grid_person_id, territory_id)", "")

T = "schedule_cell"
add(DB_MALLA, G_MALLA_OP, T, "id", "UUID PK", "Celda persona x dia (slot 0 = principal).")
add(DB_MALLA, G_MALLA_OP, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "grid_id", "UUID NOT NULL", "FK -> schedule_grid.id")
add(DB_MALLA, G_MALLA_OP, T, "employee_id", "UUID NOT NULL", "ms_employee")
add(DB_MALLA, G_MALLA_OP, T, "work_date", "DATE NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "slot", "SMALLINT NOT NULL DEFAULT 0", "1+ = turno extra mismo dia.")
add(DB_MALLA, G_MALLA_OP, T, "shift_template_id", "UUID NULL", "UUID logico shift_template (param).")
add(DB_MALLA, G_MALLA_OP, T, "cell_state_id", "UUID NULL", "UUID logico entity_status (param).")
add(DB_MALLA, G_MALLA_OP, T, "modality_id", "UUID NULL", "UUID logico work_modality (param).")
add(DB_MALLA, G_MALLA_OP, T, "site_id", "UUID NULL", "UUID logico attendance_site (param).")
add(DB_MALLA, G_MALLA_OP, T, "label_id", "UUID NULL", "UUID logico operational_label (param). Antes campaign_id.")
add(DB_MALLA, G_MALLA_OP, T, "note", "TEXT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "locked_attrs", "JSONB NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "origin", "VARCHAR(40) NULL", "manual | rotacion | intercambio | import | novedad")
add(DB_MALLA, G_MALLA_OP, T, "updated_at", "TIMESTAMPTZ NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "updated_by", "UUID NULL", "ms_auth")
add(DB_MALLA, G_MALLA_OP, T, "UNIQUE", "(grid_id, employee_id, work_date, slot)", "")

T = "schedule_cell_territory"
add(DB_MALLA, G_MALLA_OP, T, "id", "UUID PK", "Override de territorio en la celda.")
add(DB_MALLA, G_MALLA_OP, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "cell_id", "UUID NOT NULL", "FK -> schedule_cell.id")
add(DB_MALLA, G_MALLA_OP, T, "territory_id", "UUID NOT NULL", "UUID logico territory (param).")
add(DB_MALLA, G_MALLA_OP, T, "UNIQUE", "(cell_id, territory_id)", "")

T = "schedule_cell_break"
add(DB_MALLA, G_MALLA_OP, T, "id", "UUID PK", "Breaks reales de la celda (incluye especiales / repetidos #11).")
add(DB_MALLA, G_MALLA_OP, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "cell_id", "UUID NOT NULL", "FK -> schedule_cell.id")
add(DB_MALLA, G_MALLA_OP, T, "break_type_id", "UUID NULL", "UUID logico break_type (param).")
add(DB_MALLA, G_MALLA_OP, T, "template_break_id", "UUID NULL", "UUID logico shift_template_break (param).")
add(DB_MALLA, G_MALLA_OP, T, "label", "VARCHAR(80) NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "duration_minutes", "INT NOT NULL", "")
add(DB_MALLA, G_MALLA_OP, T, "paid", "BOOLEAN NOT NULL DEFAULT FALSE", "")
add(DB_MALLA, G_MALLA_OP, T, "sort_order", "SMALLINT NOT NULL DEFAULT 0", "")

T = "shift_swap_request"
add(DB_MALLA, G_MALLA_EXT, T, "id", "UUID PK", "Intercambio. Sin tope mensual (#16). Sin motor de reglas de cobertura/compensatorio.")
add(DB_MALLA, G_MALLA_EXT, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "front_id", "UUID NOT NULL", "FK -> operational_front.id")
add(DB_MALLA, G_MALLA_EXT, T, "grid_id", "UUID NOT NULL", "FK -> schedule_grid.id")
add(DB_MALLA, G_MALLA_EXT, T, "requester_employee_id", "UUID NOT NULL", "ms_employee")
add(DB_MALLA, G_MALLA_EXT, T, "counterpart_employee_id", "UUID NOT NULL", "ms_employee")
add(DB_MALLA, G_MALLA_EXT, T, "requester_cell_id", "UUID NOT NULL", "FK -> schedule_cell.id")
add(DB_MALLA, G_MALLA_EXT, T, "counterpart_cell_id", "UUID NOT NULL", "FK -> schedule_cell.id")
add(DB_MALLA, G_MALLA_EXT, T, "status", "VARCHAR(30) NOT NULL", "pendiente_aprobacion | aprobada | rechazada | aplicada | cancelada")
add(DB_MALLA, G_MALLA_EXT, T, "decision_reason", "TEXT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "decided_by", "UUID NULL", "ms_auth")
add(DB_MALLA, G_MALLA_EXT, T, "decided_at", "TIMESTAMPTZ NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "created_at", "TIMESTAMPTZ NOT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "updated_at", "TIMESTAMPTZ NOT NULL", "")

T = "schedule_novelty"
add(DB_MALLA, G_MALLA_EXT, T, "id", "UUID PK", "Novedad vinculada a malla (#18).")
add(DB_MALLA, G_MALLA_EXT, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "grid_id", "UUID NOT NULL", "FK -> schedule_grid.id")
add(DB_MALLA, G_MALLA_EXT, T, "cell_id", "UUID NULL", "FK -> schedule_cell.id")
add(DB_MALLA, G_MALLA_EXT, T, "employee_id", "UUID NOT NULL", "ms_employee")
add(DB_MALLA, G_MALLA_EXT, T, "work_date", "DATE NOT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "cell_state_id", "UUID NULL", "entity_status (param)")
add(DB_MALLA, G_MALLA_EXT, T, "description", "TEXT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "source", "VARCHAR(40) NOT NULL", "manual | th_import | sistema")
add(DB_MALLA, G_MALLA_EXT, T, "created_by", "UUID NULL", "ms_auth")
add(DB_MALLA, G_MALLA_EXT, T, "created_at", "TIMESTAMPTZ NOT NULL", "")

T = "excel_import_batch"
add(DB_MALLA, G_MALLA_EXT, T, "id", "UUID PK", "Import Excel (#20).")
add(DB_MALLA, G_MALLA_EXT, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "front_id", "UUID NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "import_type", "VARCHAR(40) NOT NULL", "catalogos | malla_borrador | novedades_th")
add(DB_MALLA, G_MALLA_EXT, T, "file_name", "VARCHAR(255) NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "status", "VARCHAR(20) NOT NULL", "cargado | descubierto | confirmado | aplicado | error")
add(DB_MALLA, G_MALLA_EXT, T, "summary_json", "JSONB NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "uploaded_by", "UUID NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "created_at", "TIMESTAMPTZ NOT NULL", "")

T = "excel_import_row"
add(DB_MALLA, G_MALLA_EXT, T, "id", "UUID PK", "Fila staging.")
add(DB_MALLA, G_MALLA_EXT, T, "company_id", "UUID NOT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "batch_id", "UUID NOT NULL", "FK -> excel_import_batch.id")
add(DB_MALLA, G_MALLA_EXT, T, "row_number", "INT NOT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "payload_json", "JSONB NOT NULL", "")
add(DB_MALLA, G_MALLA_EXT, T, "action", "VARCHAR(40) NULL", "crear | mapear | ignorar")
add(DB_MALLA, G_MALLA_EXT, T, "status", "VARCHAR(20) NOT NULL", "pendiente | aceptada | rechazada | aplicada")
add(DB_MALLA, G_MALLA_EXT, T, "message", "TEXT NULL", "")

# =============================================================================
# Auditoria / externos / eliminados
# =============================================================================

add(
    DB_AUDIT,
    G_REUSE,
    "audit_log / timeline",
    "como se usa",
    "API ms_audit",
    "NO crear schedule_cell_history en malla. Cada cambio de celda/publicacion/swap emite evento a ms_audit "
    "(affectedTable, operation, oldData, newData) y/o timeline_event. La UI de historial consulta audit.",
)

for concept, where, note in [
    ("company_id", "ms_company_admin / JWT", "Tenant."),
    ("employee_id", "ms_employee", "Persona por API."),
    ("area_id / cargo_id / positions", "ms_parametrization", "organizational_areas, positions."),
    ("user_id / roles / permisos", "ms_auth RBAC", "Sin front_role_scope."),
    ("festivos / calendario", "company_calendar + national_holidays", "Ya existen."),
    ("jornada contractual", "work_schedule + schedule_assignment", "NO usar como plantilla de malla."),
    ("notificaciones", "ms_notification", "Eventos de publicacion/cambios."),
]:
    add(DB_NONE if False else "EXTERNO GRH", G_REUSE, "EXTERNO", concept, where, note)

for name, reason in [
    ("front_role_scope", "Roles se manejan con RBAC ms_auth."),
    ("attendance_site_front", "Si usa_sitio, el frente usa el catalogo empresa; no hace falta N:M."),
    ("shift_template_day_schedule", "Un turno = un horario fijo. Variacion diaria ya la cubre work_schedule (contractual), no la plantilla operativa."),
    ("territory_level + territory_node", "Reemplazados por territory (arbol parent_id)."),
    ("campaign", "Renombrado a operational_label (etiquetas transversales)."),
    ("cell_state (tabla propia)", "Reutilizar entity_status con entity_type=malla_cell_state."),
    ("validation_rule", "Se eliminan reglas operativas / restricciones de asignacion / cobertura / compensatorio / normas del diseno."),
    ("coverage_rule / compensatory_rule / assignment_restriction / operational_norm", "Fuera del alcance de BD (sesion + revision)."),
    ("payroll_cutoff", "Eliminado sesion #6."),
    ("work_modality_front", "Modalidad global."),
    ("swap_monthly_limit", "Sin tope #16."),
    ("schedule_cell_history", "Pasa a ms_audit."),
    ("catalog_code_sequence en malla", "Se mueve a ms_parametrization (transversal)."),
]:
    add(DB_NONE, G_DROP, name, "—", "N/A", reason)

# =============================================================================
# Outputs
# =============================================================================

csv_path = OUT / "PROPUESTA-BD-MALLA-TURNOS-COLUMNAS.csv"
with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
    f.write("Base_datos;Grupo;Tabla;Columna;Tipo_dato;Descripcion\n")

    def esc(x):
        return '"' + str(x).replace('"', '""') + '"'

    for r in rows:
        f.write(";".join(esc(x) for x in r) + "\n")

wb = Workbook()

# --- Decisiones ---
ws_d = wb.active
ws_d.title = "Decisiones"
ws_d.append(["Tema", "Decision", "Detalle / como reutilizar"])
decisions = [
    (
        "front_role_scope",
        "QUITAR",
        "El alcance por rol ya lo cubre RBAC de ms_auth (permisos/submodulos). Solo se mantiene front_user_scope para excepciones por usuario.",
    ),
    (
        "catalog_code_sequence",
        "MOVER a ms_parametrization (transversal)",
        "Servicio/API de consecutivos por (company_id, catalog_type). Lo usan malla y cualquier catalogo GRH que hoy pide codigo manual.",
    ),
    (
        "shift_template vs calendario",
        "NO reutilizar work_schedule — CREAR en parametrization",
        "work_schedule/day/shift = jornada contractual semanal (horas base, CPM, schedule_assignment). "
        "shift_template = turnos operativos de malla (codigo, color, breaks, habilitacion por frente). Dominios distintos.",
    ),
    (
        "shift_template_day_schedule",
        "QUITAR",
        "Acuerdo: un turno = un horario. La variacion por dia de semana ya existe en work_schedule_day (contractual).",
    ),
    (
        "shift_template_break / break_type",
        "MOVER a ms_parametrization (transversal)",
        "break_type es catalogo reutilizable; shift_template_break asocia pausas a la plantilla.",
    ),
    (
        "cell_state",
        "REUTILIZAR entity_status",
        "Usar entity_status con entity_type='malla_cell_state'. schedule_cell.cell_state_id = entity_status.id.",
    ),
    (
        "work_modality",
        "CREAR en ms_parametrization (transversal)",
        "No existe modalidad laboral (solo study_modalities academicas).",
    ),
    (
        "attendance_site",
        "CREAR en ms_parametrization (transversal)",
        "No existe en parametrization ni company-admin. Catalogo de sedes/sitios reutilizable.",
    ),
    (
        "attendance_site_front",
        "QUITAR",
        "Con front_capability.usa_sitio basta para mostrar el catalogo empresa.",
    ),
    (
        "campaign",
        "RENOMBRAR → operational_label en parametrization",
        "Etiquetas informativas transversales. En celda: label_id. Sin cabecera de malla.",
    ),
    (
        "territory_level + territory_node",
        "REEMPLAZAR por territory (arbol)",
        "Una sola tabla con parent_id (hijos anidados). level_label texto libre. No usar zone_types ni organizational_areas.",
    ),
    (
        "hour_classification_band",
        "MOVER a ms_parametrization (transversal)",
        "Clasifica horas de cada celda/slot (varios turnos el mismo dia = varios slots). Usa festivos existentes. No es nomina ni cortes.",
    ),
    (
        "schedule_cell_history",
        "QUITAR de malla → ms_audit",
        "Emitir AuditLog/timeline en cada cambio. UI de historial consulta ms_audit.",
    ),
    (
        "validation_rule / cobertura / compensatorio / restricciones / normas",
        "QUITAR del diseno BD",
        "Fuera de alcance. Validaciones basicas en codigo/use case si hacen falta; sin tablas ni pantallas de reglas.",
    ),
]
for d in decisions:
    ws_d.append(list(d))
for cell in ws_d[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F4E79")
ws_d.column_dimensions["A"].width = 36
ws_d.column_dimensions["B"].width = 42
ws_d.column_dimensions["C"].width = 100

# --- Por BD ---
hdr_fill = {
    DB_PARAM: "2E7D32",
    DB_MALLA: "1F4E79",
    DB_AUDIT: "6A1B9A",
    DB_NONE: "B71C1C",
    "EXTERNO GRH": "455A64",
}


def write_sheet(title, predicate):
    ws = wb.create_sheet(title)
    ws.append(["Base_datos", "Grupo", "Tabla", "Columna", "Tipo_dato", "Descripcion"])
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E79")
    for r in rows:
        if predicate(r[0]):
            ws.append(list(r))
    for col, w in zip("ABCDEF", (22, 38, 28, 28, 42, 95)):
        ws.column_dimensions[col].width = w
    ws.auto_filter.ref = ws.dimensions
    ws.freeze_panes = "A2"
    return ws


write_sheet("01_ms_parametrization", lambda db: db == DB_PARAM)
write_sheet("02_ms_malla_turnos", lambda db: db == DB_MALLA)
write_sheet("03_Auditoria_y_Externos", lambda db: db in (DB_AUDIT, "EXTERNO GRH"))
write_sheet("04_Eliminados", lambda db: db == DB_NONE)
write_sheet("00_TODAS", lambda db: True)

# Resumen tablas
ws_r = wb.create_sheet("Resumen_tablas", 1)
ws_r.append(["Base_datos", "Tabla", "Accion", "Notas"])
for cell in ws_r[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F4E79")

resumen = [
    (DB_PARAM, "catalog_code_sequence", "NUEVA transversal", "Consecutivos para cualquier catalogo"),
    (DB_PARAM, "shift_template", "NUEVA transversal", "NO es work_schedule"),
    (DB_PARAM, "break_type", "NUEVA transversal", "Tipos de pausa"),
    (DB_PARAM, "shift_template_break", "NUEVA transversal", "Breaks de plantilla"),
    (DB_PARAM, "work_modality", "NUEVA transversal", "No confundir con study_modalities"),
    (DB_PARAM, "attendance_site", "NUEVA transversal", "No existia"),
    (DB_PARAM, "operational_label", "NUEVA transversal", "Antes campaign (etiquetas)"),
    (DB_PARAM, "territory", "NUEVA transversal", "Arbol parent_id; reemplaza level+node"),
    (DB_PARAM, "hour_classification_band", "NUEVA transversal", "Clasificacion horas/recargos reporteria"),
    (DB_PARAM, "entity_status", "REUSO existente", "entity_type=malla_cell_state"),
    (DB_MALLA, "operational_front", "NUEVA dominio", ""),
    (DB_MALLA, "front_capability", "NUEVA dominio", ""),
    (DB_MALLA, "front_area_link", "NUEVA dominio", "area_id logico"),
    (DB_MALLA, "front_user_scope", "NUEVA dominio", "Sin front_role_scope"),
    (DB_MALLA, "shift_template_front", "NUEVA dominio", "Vinculo frente↔turno param"),
    (DB_MALLA, "rotation_pattern", "NUEVA dominio", ""),
    (DB_MALLA, "rotation_pattern_step", "NUEVA dominio", ""),
    (DB_MALLA, "schedule_grid", "NUEVA dominio", ""),
    (DB_MALLA, "schedule_grid_person", "NUEVA dominio", ""),
    (DB_MALLA, "schedule_grid_person_territory", "NUEVA dominio", ""),
    (DB_MALLA, "schedule_cell", "NUEVA dominio", "label_id en vez de campaign_id"),
    (DB_MALLA, "schedule_cell_territory", "NUEVA dominio", ""),
    (DB_MALLA, "schedule_cell_break", "NUEVA dominio", ""),
    (DB_MALLA, "shift_swap_request", "NUEVA dominio", ""),
    (DB_MALLA, "schedule_novelty", "NUEVA dominio", ""),
    (DB_MALLA, "excel_import_batch", "NUEVA dominio", ""),
    (DB_MALLA, "excel_import_row", "NUEVA dominio", ""),
    (DB_AUDIT, "audit_log / timeline", "REUSO", "Reemplaza schedule_cell_history"),
]
for r in resumen:
    ws_r.append(list(r))
for col, w in zip("ABCD", (28, 34, 22, 55)):
    ws_r.column_dimensions[col].width = w

xlsx_path = OUT / "PROPUESTA-BD-MALLA-TURNOS-v2.xlsx"
try:
    wb.save(xlsx_path)
except PermissionError:
    xlsx_path = OUT / "PROPUESTA-BD-MALLA-TURNOS-ACTUALIZADO.xlsx"
    wb.save(xlsx_path)

# Also try overwrite classic name
classic = OUT / "PROPUESTA-BD-MALLA-TURNOS.xlsx"
try:
    wb.save(classic)
    xlsx_path = classic
except PermissionError:
    pass

# =============================================================================
# DBML
# =============================================================================
dbml = []
dbml.append("// Propuesta BD Malla de Turnos v2 — post revision")
dbml.append("// IDs entre BD = UUID logicos SIN FK cross-database")
dbml.append("// Pegar en https://dbdiagram.io")
dbml.append("")
dbml.append("Project malla_turnos_v2 {")
dbml.append("  database_type: 'PostgreSQL'")
dbml.append("  Note: 'Catalogos transversales en ms_parametrization. Dominio en ms_malla_turnos. Historial en ms_audit.'")
dbml.append("}")
dbml.append("")
dbml.append("// ========== ms_parametrization (catalogos transversales) ==========")
dbml.append("")
dbml.append("Table catalog_code_sequence {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null, note: 'Tenant']")
dbml.append("  catalog_type varchar(60) [not null]")
dbml.append("  prefix varchar(10)")
dbml.append("  next_value int [not null, default: 1]")
dbml.append("  pad_length smallint [not null, default: 3]")
dbml.append("  Indexes { (company_id, catalog_type) [unique] }")
dbml.append("  Note: 'ms_parametrization — transversal a todo GRH'")
dbml.append("}")
dbml.append("")
dbml.append("Table shift_template {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(120) [not null]")
dbml.append("  start_time time [not null]")
dbml.append("  end_time time [not null]")
dbml.append("  crosses_midnight boolean [not null, default: false]")
dbml.append("  color_hex varchar(7)")
dbml.append("  net_hours numeric(5,2)")
dbml.append("  multi_break_enabled boolean [not null, default: false]")
dbml.append("  active boolean [not null, default: true]")
dbml.append("  created_at timestamptz [not null]")
dbml.append("  updated_at timestamptz [not null]")
dbml.append("  Indexes { (company_id, code) [unique] }")
dbml.append("  Note: 'ms_parametrization. NO es work_schedule (jornada contractual)'")
dbml.append("}")
dbml.append("")
dbml.append("Table break_type {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(80) [not null]")
dbml.append("  default_minutes int")
dbml.append("  paid_default boolean [not null, default: false]")
dbml.append("  active boolean [not null, default: true]")
dbml.append("  Indexes { (company_id, code) [unique] }")
dbml.append("  Note: 'ms_parametrization — tipos de pausa transversales'")
dbml.append("}")
dbml.append("")
dbml.append("Table shift_template_break {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  shift_template_id uuid [not null, ref: > shift_template.id]")
dbml.append("  break_type_id uuid [not null, ref: > break_type.id]")
dbml.append("  duration_minutes int [not null]")
dbml.append("  paid boolean [not null, default: false]")
dbml.append("  sort_order smallint [not null, default: 0]")
dbml.append("  Note: 'ms_parametrization'")
dbml.append("}")
dbml.append("")
dbml.append("Table work_modality {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(80) [not null]")
dbml.append("  active boolean [not null, default: true]")
dbml.append("  Indexes { (company_id, code) [unique] }")
dbml.append("  Note: 'ms_parametrization. Distinto de study_modalities'")
dbml.append("}")
dbml.append("")
dbml.append("Table attendance_site {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(120) [not null]")
dbml.append("  address text")
dbml.append("  city_id uuid [note: 'cities logico']")
dbml.append("  active boolean [not null, default: true]")
dbml.append("  Indexes { (company_id, code) [unique] }")
dbml.append("  Note: 'ms_parametrization — no existia; sin site_front'")
dbml.append("}")
dbml.append("")
dbml.append("Table operational_label {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(120) [not null]")
dbml.append("  color_hex varchar(7)")
dbml.append("  category varchar(40) [note: 'campana|cliente|otro']")
dbml.append("  active boolean [not null, default: true]")
dbml.append("  Indexes { (company_id, code) [unique] }")
dbml.append("  Note: 'ms_parametrization — etiquetas (antes campaign)'")
dbml.append("}")
dbml.append("")
dbml.append("Table territory {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  parent_id uuid [ref: > territory.id, note: 'NULL=raiz']")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(120) [not null]")
dbml.append("  level_label varchar(40) [note: 'Zona, SPT...']")
dbml.append("  sort_order int [not null, default: 0]")
dbml.append("  active boolean [not null, default: true]")
dbml.append("  Indexes { (company_id, code) [unique] }")
dbml.append("  Note: 'ms_parametrization — arbol unico; reemplaza territory_level/node'")
dbml.append("}")
dbml.append("")
dbml.append("Table hour_classification_band {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(120) [not null]")
dbml.append("  band_type varchar(40) [not null]")
dbml.append("  start_time time")
dbml.append("  end_time time")
dbml.append("  crosses_midnight boolean [not null, default: false]")
dbml.append("  applies_sunday boolean [not null, default: false]")
dbml.append("  applies_holiday boolean [not null, default: false]")
dbml.append("  priority int [not null, default: 100]")
dbml.append("  active boolean [not null, default: true]")
dbml.append("  Indexes { (company_id, code) [unique] }")
dbml.append("  Note: 'ms_parametrization — clasifica horas; festivos ya en company_calendar'")
dbml.append("}")
dbml.append("")
dbml.append("Table entity_status {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  entity_type varchar(50) [not null, note: 'usar malla_cell_state']")
dbml.append("  name varchar(100) [not null]")
dbml.append("  description varchar(255)")
dbml.append("  sort_order int [not null]")
dbml.append("  color varchar(7)")
dbml.append("  is_active boolean [not null]")
dbml.append("  is_final_status boolean [not null]")
dbml.append("  is_default_status boolean [not null]")
dbml.append("  Note: 'YA EXISTE en ms_parametrization — REUSO para estados de celda'")
dbml.append("}")
dbml.append("")
dbml.append("// ========== ms_malla_turnos (dominio) ==========")
dbml.append("")
dbml.append("Table operational_front {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(120) [not null]")
dbml.append("  description text")
dbml.append("  builder_profile_label varchar(120)")
dbml.append("  publisher_profile_label varchar(120)")
dbml.append("  separate_builder_publisher boolean [not null, default: false]")
dbml.append("  build_mode varchar(20) [not null]")
dbml.append("  period_type varchar(10) [not null, note: 'semana|quincena|mes']")
dbml.append("  published_editable boolean [not null, default: false]")
dbml.append("  swap_enabled boolean [not null, default: false]")
dbml.append("  active boolean [not null, default: true]")
dbml.append("  created_at timestamptz [not null]")
dbml.append("  updated_at timestamptz [not null]")
dbml.append("  created_by uuid")
dbml.append("  updated_by uuid")
dbml.append("  Indexes { (company_id, code) [unique] }")
dbml.append("  Note: 'ms_malla_turnos'")
dbml.append("}")
dbml.append("")
dbml.append("Table front_capability {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  front_id uuid [not null, ref: > operational_front.id]")
dbml.append("  capability_code varchar(40) [not null]")
dbml.append("  enabled boolean [not null, default: false]")
dbml.append("  config_json jsonb")
dbml.append("  Indexes { (company_id, front_id, capability_code) [unique] }")
dbml.append("}")
dbml.append("")
dbml.append("Table front_area_link {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  front_id uuid [not null, ref: > operational_front.id]")
dbml.append("  area_id uuid [not null, note: 'organizational_areas logico']")
dbml.append("  Indexes { (company_id, front_id, area_id) [unique] }")
dbml.append("}")
dbml.append("")
dbml.append("Table front_user_scope {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  front_id uuid [not null, ref: > operational_front.id]")
dbml.append("  user_id uuid [not null, note: 'ms_auth']")
dbml.append("  Indexes { (company_id, front_id, user_id) [unique] }")
dbml.append("  Note: 'Sin front_role_scope — RBAC'")
dbml.append("}")
dbml.append("")
dbml.append("Table shift_template_front {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  front_id uuid [not null, ref: > operational_front.id]")
dbml.append("  shift_template_id uuid [not null, note: 'shift_template param logico']")
dbml.append("  Indexes { (company_id, front_id, shift_template_id) [unique] }")
dbml.append("}")
dbml.append("")
dbml.append("Table rotation_pattern {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  front_id uuid [not null, ref: > operational_front.id]")
dbml.append("  code varchar(20) [not null]")
dbml.append("  name varchar(120) [not null]")
dbml.append("  cycle_length smallint [not null]")
dbml.append("  auto_apply_on_period_close boolean [not null, default: true]")
dbml.append("  active boolean [not null, default: true]")
dbml.append("}")
dbml.append("")
dbml.append("Table rotation_pattern_step {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  pattern_id uuid [not null, ref: > rotation_pattern.id]")
dbml.append("  step_order smallint [not null]")
dbml.append("  shift_template_id uuid [note: 'param logico']")
dbml.append("  cell_state_id uuid [note: 'entity_status logico']")
dbml.append("}")
dbml.append("")
dbml.append("Table schedule_grid {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  front_id uuid [not null, ref: > operational_front.id]")
dbml.append("  name varchar(160)")
dbml.append("  period_start date [not null]")
dbml.append("  period_end date [not null]")
dbml.append("  period_type varchar(10) [not null]")
dbml.append("  status varchar(20) [not null]")
dbml.append("  build_mode varchar(20) [not null]")
dbml.append("  owner_user_id uuid")
dbml.append("  publisher_user_id uuid")
dbml.append("  rejection_reason text")
dbml.append("  published_at timestamptz")
dbml.append("  closed_at timestamptz")
dbml.append("  version int [not null, default: 1]")
dbml.append("  created_at timestamptz [not null]")
dbml.append("  updated_at timestamptz [not null]")
dbml.append("  Note: 'ms_malla_turnos — sin label en cabecera'")
dbml.append("}")
dbml.append("")
dbml.append("Table schedule_grid_person {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  grid_id uuid [not null, ref: > schedule_grid.id]")
dbml.append("  employee_id uuid [not null, note: 'ms_employee']")
dbml.append("  sort_order int [not null, default: 0]")
dbml.append("  modality_id uuid [note: 'work_modality param']")
dbml.append("  site_id uuid [note: 'attendance_site param']")
dbml.append("  Indexes { (grid_id, employee_id) [unique] }")
dbml.append("}")
dbml.append("")
dbml.append("Table schedule_grid_person_territory {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  grid_person_id uuid [not null, ref: > schedule_grid_person.id]")
dbml.append("  territory_id uuid [not null, note: 'territory param']")
dbml.append("  is_primary boolean [not null, default: false]")
dbml.append("  Indexes { (grid_person_id, territory_id) [unique] }")
dbml.append("}")
dbml.append("")
dbml.append("Table schedule_cell {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  grid_id uuid [not null, ref: > schedule_grid.id]")
dbml.append("  employee_id uuid [not null]")
dbml.append("  work_date date [not null]")
dbml.append("  slot smallint [not null, default: 0]")
dbml.append("  shift_template_id uuid [note: 'param']")
dbml.append("  cell_state_id uuid [note: 'entity_status']")
dbml.append("  modality_id uuid [note: 'work_modality']")
dbml.append("  site_id uuid [note: 'attendance_site']")
dbml.append("  label_id uuid [note: 'operational_label']")
dbml.append("  note text")
dbml.append("  locked_attrs jsonb")
dbml.append("  origin varchar(40)")
dbml.append("  updated_at timestamptz [not null]")
dbml.append("  updated_by uuid")
dbml.append("  Indexes { (grid_id, employee_id, work_date, slot) [unique] }")
dbml.append("}")
dbml.append("")
dbml.append("Table schedule_cell_territory {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  cell_id uuid [not null, ref: > schedule_cell.id]")
dbml.append("  territory_id uuid [not null, note: 'territory param']")
dbml.append("  Indexes { (cell_id, territory_id) [unique] }")
dbml.append("}")
dbml.append("")
dbml.append("Table schedule_cell_break {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  cell_id uuid [not null, ref: > schedule_cell.id]")
dbml.append("  break_type_id uuid [note: 'break_type param']")
dbml.append("  template_break_id uuid [note: 'shift_template_break param']")
dbml.append("  label varchar(80) [not null]")
dbml.append("  duration_minutes int [not null]")
dbml.append("  paid boolean [not null, default: false]")
dbml.append("  sort_order smallint [not null, default: 0]")
dbml.append("}")
dbml.append("")
dbml.append("Table shift_swap_request {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  front_id uuid [not null, ref: > operational_front.id]")
dbml.append("  grid_id uuid [not null, ref: > schedule_grid.id]")
dbml.append("  requester_employee_id uuid [not null]")
dbml.append("  counterpart_employee_id uuid [not null]")
dbml.append("  requester_cell_id uuid [not null, ref: > schedule_cell.id]")
dbml.append("  counterpart_cell_id uuid [not null, ref: > schedule_cell.id]")
dbml.append("  status varchar(30) [not null]")
dbml.append("  decision_reason text")
dbml.append("  decided_by uuid")
dbml.append("  decided_at timestamptz")
dbml.append("  created_at timestamptz [not null]")
dbml.append("  updated_at timestamptz [not null]")
dbml.append("}")
dbml.append("")
dbml.append("Table schedule_novelty {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  grid_id uuid [not null, ref: > schedule_grid.id]")
dbml.append("  cell_id uuid [ref: > schedule_cell.id]")
dbml.append("  employee_id uuid [not null]")
dbml.append("  work_date date [not null]")
dbml.append("  cell_state_id uuid [note: 'entity_status']")
dbml.append("  description text")
dbml.append("  source varchar(40) [not null]")
dbml.append("  created_by uuid")
dbml.append("  created_at timestamptz [not null]")
dbml.append("}")
dbml.append("")
dbml.append("Table excel_import_batch {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  front_id uuid")
dbml.append("  import_type varchar(40) [not null]")
dbml.append("  file_name varchar(255)")
dbml.append("  status varchar(20) [not null]")
dbml.append("  summary_json jsonb")
dbml.append("  uploaded_by uuid")
dbml.append("  created_at timestamptz [not null]")
dbml.append("}")
dbml.append("")
dbml.append("Table excel_import_row {")
dbml.append("  id uuid [pk]")
dbml.append("  company_id uuid [not null]")
dbml.append("  batch_id uuid [not null, ref: > excel_import_batch.id]")
dbml.append("  row_number int [not null]")
dbml.append("  payload_json jsonb [not null]")
dbml.append("  action varchar(40)")
dbml.append("  status varchar(20) [not null]")
dbml.append("  message text")
dbml.append("}")
dbml.append("")
dbml.append("TableGroup parametrization_transversal {")
dbml.append("  catalog_code_sequence")
dbml.append("  shift_template")
dbml.append("  break_type")
dbml.append("  shift_template_break")
dbml.append("  work_modality")
dbml.append("  attendance_site")
dbml.append("  operational_label")
dbml.append("  territory")
dbml.append("  hour_classification_band")
dbml.append("  entity_status")
dbml.append("}")
dbml.append("")
dbml.append("TableGroup malla_turnos_dominio {")
dbml.append("  operational_front")
dbml.append("  front_capability")
dbml.append("  front_area_link")
dbml.append("  front_user_scope")
dbml.append("  shift_template_front")
dbml.append("  rotation_pattern")
dbml.append("  rotation_pattern_step")
dbml.append("  schedule_grid")
dbml.append("  schedule_grid_person")
dbml.append("  schedule_grid_person_territory")
dbml.append("  schedule_cell")
dbml.append("  schedule_cell_territory")
dbml.append("  schedule_cell_break")
dbml.append("  shift_swap_request")
dbml.append("  schedule_novelty")
dbml.append("  excel_import_batch")
dbml.append("  excel_import_row")
dbml.append("}")

dbml_path = OUT / "PROPUESTA-BD-MALLA-TURNOS.dbml"
dbml_path.write_text("\n".join(dbml) + "\n", encoding="utf-8")

# Markdown decisiones
md = []
md.append("# Decisiones BD Malla de Turnos v2")
md.append("")
md.append("Revision post feedback: transversalidad, reuso GRH, quitar reglas de cobertura/compensatorio/restricciones/normas.")
md.append("")
md.append("## Que ya existe en GRH y como se reutiliza")
md.append("")
md.append("| Concepto | Donde esta | Como lo usa Malla |")
md.append("|---|---|---|")
md.append("| Empresa (tenant) | `ms_company_admin` / JWT | `company_id` UUID logico en todas las tablas |")
md.append("| Empleado | `ms_employee` | `employee_id` UUID; datos por API |")
md.append("| Areas / cargos | `organizational_areas`, `positions` | `front_area_link.area_id`; no duplicar |")
md.append("| Usuarios / roles / permisos | `ms_auth` RBAC | Permisos de modulo; **sin** `front_role_scope` |")
md.append("| Estados configurables | `entity_status` | `entity_type='malla_cell_state'` → estados de celda |")
md.append("| Festivos / calendario | `company_calendar`, `national_holidays` | Lectura API para clasificacion de horas |")
md.append("| Jornada contractual | `work_schedule`, `work_schedule_day`, `work_schedule_shift`, `schedule_assignment` | **No** reutilizar como plantilla de malla (otro dominio) |")
md.append("| Modalidad de estudio | `study_modalities` | **No** sirve para modalidad laboral |")
md.append("| Tipos de zona | `zone_types` | **No** es arbol operativo de cobertura |")
md.append("| Auditoria | `ms_audit` (`audit_log` / timeline) | Reemplaza `schedule_cell_history` |")
md.append("| Notificaciones | `ms_notification` | Eventos de publicacion/cambios |")
md.append("")
md.append("## Catalogos NUEVOS en `ms_parametrization` (transversales)")
md.append("")
md.append("- `catalog_code_sequence`")
md.append("- `shift_template` + `break_type` + `shift_template_break`")
md.append("- `work_modality`")
md.append("- `attendance_site`")
md.append("- `operational_label` (antes campaign)")
md.append("- `territory` (arbol `parent_id`)")
md.append("- `hour_classification_band`")
md.append("")
md.append("## Dominio en `ms_malla_turnos`")
md.append("")
md.append("Frente, capacidades, vinculos, rotacion, grilla, celdas, breaks de celda, swap, novedades, import Excel.")
md.append("")
md.append("## Eliminado")
md.append("")
md.append("`front_role_scope`, `attendance_site_front`, `shift_template_day_schedule`, `territory_level`, `territory_node`, `campaign` (→ label), `cell_state` (→ entity_status), `validation_rule` y toda cobertura/compensatorio/restricciones/normas, `schedule_cell_history` (→ audit), secuencia local de malla.")
md.append("")

(OUT / "PROPUESTA-BD-MALLA-TURNOS-DECISIONES.md").write_text("\n".join(md), encoding="utf-8")

print("OK CSV", csv_path)
print("OK XLSX", xlsx_path)
print("OK DBML", dbml_path)
print("Filas", len(rows))
