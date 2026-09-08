# -*- coding: utf-8 -*-
"""Genera docs/malla_turnos_propuesta.pdf — propuesta ejecutiva v1.0 (cliente / stakeholders)."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent / "malla_turnos_propuesta.pdf"
PAGE_W, PAGE_H = A4

BRAND = colors.HexColor("#1B3A4B")
ACCENT = colors.HexColor("#2E6B8A")
LIGHT = colors.HexColor("#F4F7F9")
MUTED = colors.HexColor("#5A6A72")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(0.6)
    canvas.line(1.8 * cm, 1.4 * cm, PAGE_W - 1.8 * cm, 1.4 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        1.8 * cm,
        0.85 * cm,
        "Plataforma GRH — Malla de Turnos",
    )
    canvas.drawRightString(PAGE_W - 1.8 * cm, 0.85 * cm, f"Página {doc.page}")
    canvas.restoreState()


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=BRAND,
            spaceAfter=6,
            alignment=TA_CENTER,
            leading=22,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=14,
            leading=13,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=BRAND,
            spaceBefore=12,
            spaceAfter=6,
            leading=15,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            textColor=ACCENT,
            spaceBefore=10,
            spaceAfter=3,
            leading=13,
        ),
        "epic_why": ParagraphStyle(
            "epic_why",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=MUTED,
            alignment=TA_JUSTIFY,
            leading=11.5,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#222"),
            alignment=TA_JUSTIFY,
            leading=12,
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=11.5,
            leftIndent=4,
        ),
        "hu_id": ParagraphStyle(
            "hu_id",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.8,
            leading=10,
            textColor=BRAND,
        ),
        "hu": ParagraphStyle(
            "hu",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.0,
            leading=10.2,
            textColor=colors.HexColor("#222"),
        ),
        "meta": ParagraphStyle(
            "meta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=MUTED,
            leading=10,
        ),
        "sprint_title": ParagraphStyle(
            "sprint_title",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=BRAND,
            spaceBefore=8,
            spaceAfter=2,
            leading=12,
        ),
    }


def meta_table(s):
    data = [
        [
            Paragraph("<b>Producto</b><br/>Plataforma GRH", s["meta"]),
            Paragraph(
                "<b>Principio</b><br/>Máxima parametrización por empresa y frente. Sin reglas fijas en el producto.",
                s["meta"],
            ),
        ],
        [
            Paragraph("<b>Módulo</b><br/>Malla de turnos", s["meta"]),
            Paragraph(
                "<b>Rotación</b><br/>Híbrida: manual / asistida / automática, con simulación",
                s["meta"],
            ),
        ],
        [
            Paragraph("<b>Versión</b><br/>1.0 — 07/09/2026", s["meta"]),
            Paragraph(
                "<b>Alcance de horas</b><br/>Entrega horas a nómina (no valores monetarios)",
                s["meta"],
            ),
        ],
    ]
    t = Table(data, colWidths=[8.5 * cm, 8.5 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, ACCENT),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D0D8DE")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def bullets(items, s):
    return ListFlowable(
        [ListItem(Paragraph(x, s["bullet"]), leftIndent=8, bulletColor=ACCENT) for x in items],
        bulletType="bullet",
        start="•",
        leftIndent=12,
        spaceBefore=2,
        spaceAfter=6,
    )


def hu_table(rows, s):
    """rows: (id, title, why)"""
    header = [
        Paragraph("<b>HU</b>", s["hu_id"]),
        Paragraph("<b>Historia</b>", s["hu_id"]),
        Paragraph("<b>Para qué (negocio)</b>", s["hu_id"]),
    ]
    data = [header]
    for hid, title, why in rows:
        data.append(
            [
                Paragraph(hid, s["hu_id"]),
                Paragraph(title, s["hu"]),
                Paragraph(why, s["hu"]),
            ]
        )
    t = Table(data, colWidths=[2.2 * cm, 6.5 * cm, 8.5 * cm])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), BRAND),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.4, ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.2, colors.HexColor("#D0D8DE")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    for i in range(1, len(data)):
        bg = LIGHT if i % 2 == 0 else colors.white
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t


# --- Contenido de negocio ---

EPICS = [
    {
        "title": "EP-00 — Integración del módulo a la plataforma GRH",
        "why": (
            "Para que Malla de Turnos exista como módulo de la plataforma: visible en el menú según el plan, "
            "con permisos, aislamiento por empresa y reutilización de maestros ya existentes en GRH."
        ),
        "hus": [
            ("HU01", "Completar módulo y submódulos en la plataforma", "Habilitar el acceso al módulo y sus secciones de menú según el plan de la empresa."),
            ("HU02", "Configurar permisos por sección de menú", "Definir quién puede crear, consultar, editar o eliminar en cada sección."),
            ("HU03", "Asignar alcance de frentes operativos a usuarios o roles", "Limitar la operación a los frentes que cada persona o rol puede gestionar."),
            ("HU04", "Aislar información por empresa", "Garantizar que cada empresa solo vea y opere su propia información."),
            ("HU05", "Reutilizar empleados, áreas, cargos y festivos de GRH", "Evitar duplicar maestros: la malla usa lo que ya existe en la plataforma."),
            ("HU06", "Distinguir jornada contractual de malla operativa", "Separar el horario contractual del armado operativo de turnos."),
            ("HU07", "Registrar eventos de notificación y línea de tiempo", "Dejar listos los avisos y la trazabilidad de cambios del módulo."),
            ("HU08", "Consumir listado de empleados con filtro por área o frente", "Seleccionar el personal correcto al armar o consultar la malla."),
        ],
    },
    {
        "title": "EP-01 — Parametrización de catálogos y reglas",
        "why": (
            "Para que cada empresa configure turnos, estados, sitios, reglas y capacidades de su frente "
            "sin depender de valores fijos del producto."
        ),
        "hus": [
            ("HU09", "Parametrizar frentes operativos", "Crear y mantener los frentes (operaciones) de la empresa."),
            ("HU10", "Configurar capacidades, armado y publicación del frente", "Definir cómo se arma y publica la malla en cada frente."),
            ("HU11", "Parametrizar plantillas de turno", "Disponer de turnos reutilizables con horario y color."),
            ("HU12", "Configurar horarios distintos por día en un turno", "Permitir que un mismo turno varíe según el día."),
            ("HU13", "Parametrizar break y almuerzo del turno", "Definir pausas asociadas a cada plantilla de turno."),
            ("HU14", "Parametrizar estados de celda con flags", "Modelar DES, permiso, actividad, etc., con su comportamiento."),
            ("HU15", "Parametrizar campañas o tareas de celda", "Etiquetar el trabajo del día (campaña/tarea) cuando aplique."),
            ("HU16", "Parametrizar territorio con niveles configurables", "Organizar cobertura territorial según la estructura de la empresa."),
            ("HU17", "Parametrizar modalidades de trabajo", "Registrar presencial, remoto u otras modalidades del catálogo."),
            ("HU18", "Parametrizar sitios de asistencia", "Definir dónde se presta el servicio cuando el frente lo usa."),
            ("HU19", "Parametrizar tipos y restricciones de persona", "Restringir asignación cuando una persona no puede operar."),
            ("HU20", "Usar festivos del calendario de empresa", "Respetar festivos ya definidos en GRH al armar y reportar."),
            ("HU21", "Parametrizar cortes de nómina", "Alinear reportes de horas a los periodos de corte de la empresa."),
            ("HU22", "Parametrizar tipos de hora y clasificación", "Clasificar horas (ordinaria, extra, etc.) según reglas de la empresa."),
            ("HU23", "Parametrizar reglas de compensatorio", "Configurar umbrales y criterios de compensatorio."),
            ("HU24", "Parametrizar reglas de cobertura", "Definir mínimos/máximos de cobertura por dimensión habilitada."),
            ("HU25", "Motor de reglas de validación parametrizable", "Centralizar validaciones con severidad info, advertencia o bloqueo."),
            ("HU26", "Configurar flags de atributos de celda del frente", "Activar solo los atributos que cada frente necesita en la grilla."),
            ("HU27", "Importación asistida desde Excel de operación", "Acelerar el alta de catálogos a partir de Excel existentes."),
        ],
    },
    {
        "title": "EP-02 — Construcción de la malla",
        "why": (
            "Para armar la programación operativa en grilla: personas, días, turnos/estados y atributos, "
            "con herramientas que reduzcan trabajo manual."
        ),
        "hus": [
            ("HU28", "Crear malla por periodo y frente", "Abrir una malla nueva para un frente y un periodo."),
            ("HU29", "Seleccionar grupo de funcionarios de la malla", "Definir quiénes aparecen como filas de la grilla."),
            ("HU30", "Asignar turno o estado a una celda", "Programar el día de cada persona con turno o estado."),
            ("HU31", "Asignar segundo turno o turno extra el mismo día", "Cubrir dobles turnos cuando la operación lo requiera."),
            ("HU32", "Asignar territorio a la celda", "Indicar el territorio de cobertura del día cuando aplique."),
            ("HU33", "Asignar modalidad y sitio a la celda", "Registrar cómo y dónde trabaja la persona ese día."),
            ("HU34", "Registrar observación en la celda", "Dejar notas operativas visibles en la celda."),
            ("HU35", "Visualizar grilla operativa", "Ver y navegar la malla completa de forma clara."),
            ("HU36", "Asignar campaña o tarea a la celda", "Asociar la celda a una campaña/tarea vigente."),
            ("HU37", "Cubrir recurso de otro frente o área el mismo día", "Prestar personal entre frentes/áreas cuando haga falta."),
            ("HU38", "Filtrar y buscar en la grilla", "Encontrar rápido personas o celdas por atributos habilitados."),
            ("HU39", "Control de concurrencia en edición de celdas", "Evitar que dos editores se pisen el mismo cambio."),
            ("HU40", "Carga parcial de grilla", "Mantener rendimiento con ventanas de fechas y paginación."),
            ("HU41", "Copiar semana o asignación masiva", "Reutilizar patrones ya armados y ahorrar tiempo."),
            ("HU42", "Fijar atributo de celda por periodo", "Bloquear un valor (sitio, turno, etc.) por un rango de días."),
        ],
    },
    {
        "title": "EP-03 — Validación, cobertura y rotación",
        "why": (
            "Para detectar conflictos a tiempo, medir cobertura y aplicar rotaciones "
            "(manual, asistida o automática) con simulación antes de confirmar."
        ),
        "hus": [
            ("HU43", "Visualizar indicadores de cobertura y contadores", "Ver si el día/periodo cumple la cobertura esperada."),
            ("HU44", "Visualizar equilibrio de turnos por persona", "Equilibrar cargas entre el equipo."),
            ("HU45", "Evaluar y mostrar conflictos de validación", "Avisar o bloquear incumplimientos de reglas."),
            ("HU46", "Definir patrón de rotación genérico", "Crear secuencias reutilizables de turnos/estados."),
            ("HU47", "Vincular patrón a grupo y periodo", "Aplicar el patrón al equipo correcto en el periodo."),
            ("HU48", "Simular patrón antes de aplicar", "Revisar el resultado sin afectar aún la malla real."),
            ("HU49", "Excluir personas o celdas de la rotación", "Sacar casos especiales del patrón automático."),
            ("HU50", "Aplicar resultado de rotación a la malla", "Confirmar la rotación simulada sobre la grilla."),
            ("HU51", "Construcción asistida de asignaciones", "Recibir sugerencias de armado y aceptarlas con control."),
            ("HU52", "Distribuir breaks y almuerzos", "Repartir pausas según plantillas y reglas del frente."),
            ("HU53", "Rotar sitios de asistencia", "Alternar sitios según la configuración del frente."),
            ("HU54", "Reequilibrar cargas tras una novedad", "Reordenar el equipo cuando aparece una novedad."),
            ("HU55", "Aplicar restricciones y motor al rotar o asignar", "Que toda asignación respete las reglas activas."),
            ("HU56", "Ajustar manualmente tras rotación o sugerencia", "Permitir el toque fino del coordinador."),
        ],
    },
    {
        "title": "EP-04 — Publicación y ciclo de vida",
        "why": (
            "Para gobernar cuándo la malla pasa de borrador a publicada, con revisión, rechazo "
            "y edición controlada después de publicar."
        ),
        "hus": [
            ("HU57", "Ciclo de vida de publicación de la malla", "Gestionar borrador, revisión, publicada y rechazada."),
            ("HU58", "Rechazar malla en revisión", "Devolver la malla con motivo cuando no está lista."),
            ("HU59", "Editar malla publicada", "Corregir la malla vigente cuando la configuración del frente lo permite."),
        ],
    },
    {
        "title": "EP-05 — Novedades, cambios y auditoría",
        "why": (
            "Para registrar novedades operativas, conservar historial confiable y avisar al empleado "
            "cuando un cambio le afecta, sin exigir su aceptación."
        ),
        "hus": [
            ("HU60", "Aplicar estado de novedad operativa a la celda", "Marcar vacaciones, incapacidad u otra novedad en la grilla."),
            ("HU61", "Definir ownership MVP de novedades", "Aclarar quién captura y responde por las novedades en el MVP."),
            ("HU62", "Historial inmutable de celda", "Conservar el rastro de cada cambio sin borrarlo."),
            ("HU63", "Notificar cambio relevante al empleado", "Informar al colaborador de cambios que le impactan."),
            ("HU64", "Consultar historial de cambios por funcionario", "Auditar qué cambió y cuándo para una persona."),
        ],
    },
    {
        "title": "EP-06 — Consulta operativa",
        "why": (
            "Para que supervisión y mesa respondan en el día a día: quién está en turno, "
            "quién está disponible y cómo va la cobertura."
        ),
        "hus": [
            ("HU65", "Buscar quién está en turno o disponible", "Ubicar personal usable en un momento dado."),
            ("HU66", "Consultar cobertura del día por dimensiones", "Ver cobertura del día según lo configurado en el frente."),
        ],
    },
    {
        "title": "EP-07 — Vista del empleado",
        "why": (
            "Para que cada colaborador consulte su programación y, según política del frente, "
            "la del grupo, además de su historial reciente."
        ),
        "hus": [
            ("HU67", "Ver programación del grupo", "Conocer turnos del equipo cuando la política lo permite."),
            ("HU68", "Ver mi programación", "Consultar la propia malla en día, semana o mes."),
            ("HU69", "Ver historial de mis turnos y cambios recientes", "Revisar cambios recientes que afectan al empleado."),
        ],
    },
    {
        "title": "EP-08 — Reportes y horas para nómina",
        "why": (
            "Para entregar horas clasificadas, exportar la malla y cruzar novedades de Talento Humano, "
            "sin liquidar dinero dentro del módulo."
        ),
        "hus": [
            ("HU70", "Calcular horas del periodo por tipos configurados", "Obtener horas ordinarias/extra/etc. según catálogo."),
            ("HU71", "Exportar malla a Excel o PDF", "Compartir o archivar la programación en formatos estándar."),
            ("HU72", "Reportar horas de novedad versus operativas", "Separar horas de novedad de las operativas."),
            ("HU73", "Exportar cobertura para terceros", "Entregar cobertura a áreas o proveedores externos."),
            ("HU74", "Parametrizar plantilla de importación de novedades TH", "Estandarizar el archivo que llega de Talento Humano."),
            ("HU75", "Cruzar programación con novedades TH importadas", "Contrastar la malla con novedades externas."),
            ("HU76", "Aplicar reglas de compensatorio en reporte", "Reflejar compensatorio según reglas parametrizadas."),
        ],
    },
    {
        "title": "EP-09 — Intercambio de turnos",
        "why": (
            "Para permitir, cuando el frente lo habilite, que los empleados soliciten intercambios "
            "con validación, aprobación, auditoría y notificación."
        ),
        "hus": [
            ("HU77", "Habilitar y configurar solicitudes de intercambio", "Encender o apagar el intercambio por frente."),
            ("HU78", "Solicitar intercambio de celda o turno", "Permitir al empleado pedir un canje de turno."),
            ("HU79", "Validar solicitud con motor de reglas", "Revisar que el intercambio no rompa reglas activas."),
            ("HU80", "Aprobar o rechazar solicitud de intercambio", "Dar control al rol autorizado sobre la solicitud."),
            ("HU81", "Aplicar intercambio, auditar y notificar", "Ejecutar el cambio, dejar rastro y avisar a las partes."),
        ],
    },
]

SPRINTS = [
    {
        "title": "Sprint 1 — Integración GRH y catálogos núcleo (EP-00 / EP-01 inicio)",
        "scope": "HU01 a HU18",
        "what": (
            "Habilitar el módulo en la plataforma (menú, permisos, alcance por frente, aislamiento por empresa "
            "y reuso de maestros GRH) y parametrizar el núcleo de catálogos: frentes, capacidades, turnos, "
            "horarios, pausas, estados, campañas, territorio, modalidades y sitios. "
            "La alta del módulo/submódulos desde Super Admin es una actividad corta dentro de este sprint."
        ),
        "deliverables": [
            "Módulo Malla de Turnos visible según plan, con permisos y alcance por frente.",
            "Aislamiento por empresa y consumo de empleados/áreas/cargos/festivos.",
            "Catálogo de frentes, plantillas de turno (con variantes y pausas), estados, campañas, territorio, modalidades y sitios.",
            "Base de notificaciones/trazabilidad lista para el resto del módulo.",
        ],
    },
    {
        "title": "Sprint 2 — Catálogos avanzados y motor de reglas (EP-01 cierre)",
        "scope": "HU19 a HU27",
        "what": (
            "Completar restricciones de persona, festivos, cortes, tipos de hora, compensatorio, cobertura, "
            "motor de validación, flags de atributos e importación asistida desde Excel."
        ),
        "deliverables": [
            "Reglas de negocio parametrizables (cobertura, compensatorio, validación).",
            "Tipos de hora y cortes alineados a nómina (solo horas).",
            "Importación asistida que acelera la carga inicial de catálogos.",
        ],
    },
    {
        "title": "Sprint 3 — Construcción de malla (núcleo EP-02)",
        "scope": "HU28 a HU35",
        "what": (
            "Crear mallas por periodo/frente, seleccionar el grupo, asignar turno/estado/extra/territorio/"
            "modalidad-sitio/nota y visualizar la grilla operativa."
        ),
        "deliverables": [
            "Creación de malla operativa por frente y periodo.",
            "Asignación básica de celdas (turno, estado, atributos principales).",
            "Grilla operativa usable para construir la programación.",
        ],
    },
    {
        "title": "Sprint 4 — Construcción avanzada (cierre EP-02)",
        "scope": "HU36 a HU42",
        "what": (
            "Campañas en celda, cobertura cruzada entre frentes, filtros, concurrencia, carga parcial, "
            "copia masiva y fijación de atributos por periodo."
        ),
        "deliverables": [
            "Herramientas de productividad (filtros, copia masiva, fijar atributos).",
            "Cobertura cruzada entre frentes/áreas.",
            "Edición concurrente segura y grilla performante.",
        ],
    },
    {
        "title": "Sprint 5 — Validación y rotación base (EP-03)",
        "scope": "HU43 a HU50",
        "what": (
            "Indicadores de cobertura y equilibrio, conflictos de validación, definición de patrones, "
            "vínculo a grupos, simulación, exclusiones y aplicación de rotación."
        ),
        "deliverables": [
            "Tablero de cobertura/equilibrio y alertas de validación.",
            "Patrones de rotación con simulación previa.",
            "Aplicación controlada del resultado a la malla.",
        ],
    },
    {
        "title": "Sprint 6 — Rotación avanzada y publicación (EP-03 / EP-04)",
        "scope": "HU51 a HU59",
        "what": (
            "Construcción asistida, distribución de pausas, rotación de sitios, reequilibrio, "
            "restricciones al asignar, ajuste manual y ciclo de publicación (revisión/rechazo/edición publicada)."
        ),
        "deliverables": [
            "Asistentes de armado y reequilibrio post-novedad.",
            "Ciclo de vida: borrador → revisión → publicada / rechazada.",
            "Edición post-publicación según política del frente.",
        ],
    },
    {
        "title": "Sprint 7 — Novedades, consulta y vista empleado (EP-05 / EP-06 / EP-07)",
        "scope": "HU60 a HU69",
        "what": (
            "Novedades operativas, ownership MVP, historial e notificaciones; consulta de quién está "
            "disponible; y vistas del empleado (grupo, propia e historial)."
        ),
        "deliverables": [
            "Gestión de novedades en celda con historial y avisos.",
            "Consulta operativa del día (turno/disponible/cobertura).",
            "Autoservicio del empleado para ver su programación.",
        ],
    },
    {
        "title": "Sprint 8 — Reportes y horas (EP-08)",
        "scope": "HU70 a HU76",
        "what": (
            "Cálculo de horas por tipo, exportes Excel/PDF, horas de novedad vs operativas, "
            "export de cobertura, plantilla e importación TH y compensatorio en reporte."
        ),
        "deliverables": [
            "Reportes de horas listos para alimentar nómina (sin liquidar pesos).",
            "Exportación de malla y cobertura.",
            "Cruce con novedades de Talento Humano según plantilla parametrizada.",
        ],
    },
    {
        "title": "Sprint 9 — Intercambio y estabilización (EP-09)",
        "scope": "HU77 a HU81",
        "what": (
            "Configurar el intercambio por frente, solicitar, validar con reglas, aprobar/rechazar, "
            "aplicar con auditoría y notificación; más estabilización para salida a piloto."
        ),
        "deliverables": [
            "Flujo completo de intercambio (configurable; puede nacer deshabilitado).",
            "Auditoría y notificación del canje aplicado.",
            "Módulo estabilizado para piloto con el alcance completo documentado.",
        ],
    },
]


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.6 * cm,
        bottomMargin=2.0 * cm,
        title="Propuesta Malla de Turnos v1.0 — GRH",
        author="GRH / Malla de Turnos",
    )
    story = []

    story.append(Paragraph("Épicas e Historias de Usuario", s["title"]))
    story.append(
        Paragraph(
            "Módulo Malla de Turnos — Plataforma GRH<br/>Versión 1.0",
            s["subtitle"],
        )
    )
    story.append(meta_table(s))
    story.append(Spacer(1, 8))

    # 1. Decisión
    story.append(Paragraph("1. Decisión de solución", s["h1"]))
    story.append(
        Paragraph(
            "La malla operativa <b>no</b> forma parte de la jornada contractual. Es un dominio propio del "
            "módulo Malla de Turnos que reutiliza empleados, áreas, cargos, calendario/festivos, "
            "autenticación, notificaciones y línea de tiempo de GRH; se parametriza por empresa y frente; "
            "estructura cada celda como persona × fecha × (turno o estado) × atributos opcionales; "
            "publica, audita y notifica sin exigir aceptación del empleado; y entrega <b>horas</b> a nómina, "
            "no valores a pagar.",
            s["body"],
        )
    )

    # 2. Épicas + HU
    story.append(Paragraph("2. Épicas e historias de usuario", s["h1"]))
    story.append(
        Paragraph(
            "A continuación se presenta cada épica con su propósito de negocio y las historias que la "
            "componen, con una explicación breve del valor que aportan. Toda la numeración sigue el "
            "orden de construcción del módulo (HU01 a HU81).",
            s["body"],
        )
    )

    for epic in EPICS:
        block = [
            Paragraph(epic["title"], s["h2"]),
            Paragraph(epic["why"], s["epic_why"]),
            hu_table(epic["hus"], s),
            Spacer(1, 4),
        ]
        story.append(KeepTogether(block))

    # 3. Orden de construcción
    story.append(Paragraph("3. Orden de construcción", s["h1"]))
    story.append(
        bullets(
            [
                "Todas las historias del listado forman parte del alcance del módulo.",
                "<b>Orden por dependencias:</b> EP-00 → EP-01 → EP-02 → EP-03 → EP-04 → EP-05 → EP-06 → EP-07 → EP-08 → EP-09.",
                "EP-09 (intercambio) puede iniciar deshabilitada por configuración del frente, pero la capacidad queda incluida.",
                "El orden indica secuencia de construcción; no implica dejar historias fuera del producto.",
            ],
            s,
        )
    )

    # 4. Sprints
    story.append(Paragraph("4. Plan de sprints", s["h1"]))
    story.append(
        Paragraph(
            "Plan orientativo de <b>9 sprints</b> (Sprint 1 a Sprint 9), de aproximadamente dos semanas cada uno. "
            "Sigue el orden de construcción HU01→HU81. Para cada sprint se indica el trabajo previsto y los "
            "entregables esperados ante negocio y dirección.",
            s["body"],
        )
    )

    for sp in SPRINTS:
        block = [
            Paragraph(sp["title"], s["sprint_title"]),
            Paragraph(f"<b>Alcance:</b> {sp['scope']}", s["meta"]),
            Paragraph(f"<b>Qué se hará:</b> {sp['what']}", s["body"]),
            Paragraph("<b>Entregables del sprint:</b>", s["body"]),
            bullets(sp["deliverables"], s),
        ]
        story.append(KeepTogether(block))

    # 5. Fuera de alcance
    story.append(Paragraph("5. Fuera de alcance (explícito)", s["h1"]))
    story.append(
        bullets(
            [
                "Liquidación de nómina en pesos (el módulo entrega horas, no dinero).",
                "Módulo completo de vacaciones/incapacidades de Talento Humano dentro de GRH (MVP = estado de celda + importación).",
                "Pantalla de indicadores de desempeño.",
                "Personal de fábrica (sesión propia).",
                "Reportería gráfica avanzada corporativa.",
            ],
            s,
        )
    )

    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Las historias de usuario se encuentran en el repositorio de SharePoint del proyecto "
            '(carpeta <b>Historias de usuario</b> — Malla de turnos): '
            '<link href="https://datacentercolombia.sharepoint.com/sites/GerenciaSolucionesTecnolgicas/Documentos%20compartidos/Forms/AllItems.aspx?id=%2Fsites%2FGerenciaSolucionesTecnolgicas%2FDocumentos%20compartidos%2FGeneral%2F02%2E%20OPERACI%C3%93N%2F02%2E02%20Proyectos%2FPRY%20%2D%20677705%20%2D%20Proyecto%20interno%20GRH%2F10%2E%20Hijos%2FPRY%20%2D%20Malla%20de%20turnos%2F03%2E%20Requerimientos%2F01%2E%20Historias%20de%20usuario&amp;viewid=d295584b%2D97d0%2D49ed%2Db5cd%2D70d640588ad9&amp;d=w3841597a4c304e20b2c1da0bb273a685&amp;csf=1&amp;ovuser=5c8b9f78%2D0560%2D43cc%2Dbb1a%2D7735b56cc8a3%2Cjair%2Euribe%40dcsas%2Ecom%2Eco&amp;TeamsCID=03a2de1f%2De814%2D4e64%2Dbb17%2D754399db2c4c&amp;OR=Teams%2DHL&amp;CT=1788623982200&amp;clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNjA4MTMxOTMwOCIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D&amp;CID=8e4738a2%2D308c%2Df000%2D0515%2D09a17655f4df&amp;cidOR=SPO&amp;FolderCTID=0x0120002643405752AFAC4DA7B0A8EFF135EF05">'
            "<u>Abrir en SharePoint</u></link>.",
            s["body"],
        )
    )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
