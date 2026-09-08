# -*- coding: utf-8 -*-
"""Genera HUs definitivas Malla de Turnos desde definición estructurada."""
from pathlib import Path

OUT = Path(__file__).resolve().parent


def hu(
    id_,
    title,
    priority,
    como,
    quiero,
    para,
    cubre,
    no_cubre,
    reglas,
    cas,
    deps_hu,
    deps_ms,
    tech=None,
):
    lines = [
        f"## {id_} — {title}",
        "",
        f"**Prioridad:** {priority}",
        "**Estado:** Definitiva",
        "",
        "### Historia",
        "",
        f"**Como:** {como}",
        "",
        f"**Quiero:** {quiero}",
        "",
        f"**Para:** {para}",
        "",
        "### Alcance",
        "",
        "**Cubre**",
        "",
    ]
    for x in cubre:
        lines.append(f"- {x}")
    lines += ["", "**No cubre**", ""]
    for x in no_cubre:
        lines.append(f"- {x}")
    lines += ["", "### Reglas de negocio", ""]
    for i, r in enumerate(reglas, 1):
        lines.append(f"{i}. {r}")
    lines += ["", "### Criterios de aceptación", ""]
    for i, (name, d, c, e) in enumerate(cas, 1):
        lines += [
            f"**CA{i:02d} — {name}**",
            "",
            f"Dado que {d}",
            "",
            f"Cuando {c}",
            "",
            f"Entonces {e}",
            "",
        ]
    lines += [
        "### Dependencias",
        "",
        f"- HUs: {deps_hu}",
        f"- Microservicios / GRH: {deps_ms}",
        "",
    ]
    if tech:
        lines += ["### Consideraciones técnicas", "", tech, ""]
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


ACTOR_PARAM = "Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)"
ACTOR_COORD = "Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)"
ACTOR_PUB = "Usuario de la empresa con permiso de publicación según configuración del frente"
ACTOR_EMP = "Usuario de la empresa vinculado a un funcionario (empleado)"
ACTOR_MESA = "Usuario de la empresa con permiso de consulta operativa"
ACTOR_SA = "Super-administrador de la plataforma GRH"
ACTOR_ADMIN = "Administrador de empresa"

HUS = []

# ========== EP-00 ==========
HUS.append(
    (
        "EP-00",
        "Integración con GRH",
        [
            hu(
                "MT-EP00-HU01",
                "Completar módulo y submódulos de Malla de Turnos en la plataforma",
                "MVP",
                ACTOR_SA,
                "completar el módulo Malla de Turnos (ya existente en catálogo) con sus submódulos, rutas de menú y asociación a planes",
                "que las empresas con el módulo en su plan vean las secciones en el menú sin crear un módulo duplicado",
                [
                    "Completar submódulos del módulo existente (Parametrización, Construcción, Consulta, Mi programación, Reportes)",
                    "Asociar el módulo a planes de servicio",
                    "Habilitar visibilidad en menú cuando el plan activo de la empresa lo incluye y hay permiso LEER",
                ],
                [
                    "Parametrizar frentes, turnos o mallas",
                    "Crear un segundo módulo con otro nombre o id",
                ],
                [
                    "El módulo de plataforma se identifica en el catálogo existente; no se crea un módulo paralelo.",
                    "Los submódulos son secciones de menú con permisos CREAR/LEER/ACTUALIZAR/ELIMINAR.",
                    "La empresa solo ve el módulo si su plan activo lo incluye.",
                    "Los nombres de frentes operativos no son ítems del menú de plataforma.",
                ],
                [
                    (
                        "Completar sin duplicar",
                        "existe el módulo Malla de Turnos en el catálogo de plataforma",
                        "el Super-administrador registra o completa los submódulos y los asocia a un plan",
                        "no se crea un segundo módulo y el plan queda asociado al módulo existente",
                    ),
                    (
                        "Visibilidad por plan",
                        "una empresa tiene plan activo con el módulo y un usuario con LEER en un submódulo",
                        "el usuario inicia sesión",
                        "ve las secciones habilitadas en el menú lateral",
                    ),
                    (
                        "Sin plan",
                        "una empresa no tiene el módulo en su plan",
                        "un usuario de esa empresa inicia sesión",
                        "no ve Malla de Turnos en el menú",
                    ),
                    (
                        "Permisos",
                        "solo el Super-administrador puede modificar el catálogo de módulos de plataforma",
                        "un administrador de empresa intenta crear un módulo de plataforma",
                        "la acción no está disponible",
                    ),
                ],
                "Ninguna previa de Malla",
                "company-admin (módulos, submódulos, plan_modulos); auth (permission_submodules); frontend menú",
                "Anclar al módulo id=13 en DEV si aplica. Checklist: company-admin + seeds permisos + rutas FE.",
            ),
            hu(
                "MT-EP00-HU02",
                "Configurar permisos RBAC por sección de menú",
                "MVP",
                ACTOR_ADMIN,
                "asignar a roles de mi empresa los permisos CREAR, LEER, ACTUALIZAR y ELIMINAR sobre las secciones de Malla de Turnos",
                "controlar quién parametriza, construye, publica, consulta o reporta sin inventar un sistema de seguridad paralelo",
                [
                    "Asignación de permisos por rol y submódulo usando el modelo de seguridad GRH",
                    "Validación de acceso en cada sección",
                ],
                [
                    "Alcance por frente operativo (ver HU70)",
                    "Roles hardcodeados tipo Contact Center",
                ],
                [
                    "Los únicos permisos de plataforma son CREAR, LEER, ACTUALIZAR y ELIMINAR por submódulo.",
                    "Los roles operativos (coordinador, supervisora, analista, etc.) son roles de la empresa, no enums del producto.",
                    "Sin LEER en la sección, el usuario no ve la opción de menú ni puede invocar la API correspondiente.",
                ],
                [
                    (
                        "Asignar permisos",
                        "existe un rol de empresa y submódulos de Malla",
                        "el administrador asigna LEER y ACTUALIZAR en Construcción",
                        "los usuarios con ese rol pueden abrir Construcción y modificar según ACTUALIZAR",
                    ),
                    (
                        "Denegación",
                        "un usuario no tiene LEER en Reportes",
                        "intenta acceder a Reportes",
                        "el sistema niega el acceso",
                    ),
                    (
                        "Multiempresa",
                        "dos empresas tienen roles con el mismo nombre",
                        "se consultan permisos",
                        "cada empresa solo ve y administra sus propios roles",
                    ),
                    (
                        "Sin inventar permisos",
                        "se configura seguridad",
                        "se listan permisos disponibles",
                        "solo aparecen CREAR/LEER/ACTUALIZAR/ELIMINAR (no permisos inventados de frente)",
                    ),
                ],
                "MT-EP00-HU01",
                "auth (roles, permission_submodules); company-admin submódulos",
                "Alcance por frente = HU70 (dominio Malla).",
            ),
            hu(
                "MT-EP00-HU70",
                "Asignar alcance de frentes operativos a usuarios o roles",
                "MVP",
                ACTOR_ADMIN + " o usuario con permiso de parametrización",
                "definir qué frentes operativos puede ver u operar cada usuario o rol dentro de Malla",
                "aislar operaciones por frente sin modificar el modelo RBAC de plataforma",
                [
                    "Matriz usuario/rol ↔ frentes autorizados",
                    "Filtrado de selectores y mallas según alcance",
                ],
                ["Permisos CREAR/LEER de menú (HU02)", "Crear frentes (HU64)"],
                [
                    "El alcance de frente es configuración del dominio Malla, no un permiso SM_* nuevo.",
                    "Un usuario solo opera frentes de su empresa y dentro de su alcance.",
                    "Si no tiene alcance asignado, no ve frentes (fail-closed) salvo rol con alcance total configurado explícitamente.",
                ],
                [
                    (
                        "Asignación",
                        "existen frentes A y B en la empresa",
                        "se autoriza al usuario solo el frente A",
                        "en selectores y listados solo aparece A",
                    ),
                    (
                        "Intento fuera de alcance",
                        "el usuario solo tiene frente A",
                        "intenta abrir una malla del frente B por identificador",
                        "el sistema rechaza por autorización",
                    ),
                    (
                        "Tenant",
                        "el frente pertenece a otra empresa",
                        "se intenta asignar alcance",
                        "no aparece ni se puede asignar",
                    ),
                    (
                        "Auditoría",
                        "se modifica el alcance de un usuario",
                        "se guarda el cambio",
                        "queda registro de quién cambió qué y cuándo",
                    ),
                ],
                "MT-EP00-HU02, MT-EP01-HU64",
                "Malla (nuevo); auth solo para identidad del usuario",
                None,
            ),
            hu(
                "MT-EP00-HU03",
                "Aislar información por empresa",
                "MVP",
                ACTOR_ADMIN + " / " + ACTOR_COORD,
                "que toda la información de Malla de Turnos pertenezca únicamente a mi empresa",
                "impedir fugas de datos entre tenants",
                [
                    "Aislamiento de catálogos, mallas, reglas, solicitudes, reportes e historial",
                    "companyId desde contexto autenticado",
                ],
                ["Lógica de negocio de turnos"],
                [
                    "El identificador de empresa proviene del contexto autenticado; no se confía en el valor enviado por el cliente como fuente de verdad.",
                    "Todas las consultas y escrituras están filtradas por empresa.",
                    "Catálogos, mallas, reglas, solicitudes de intercambio y exportaciones son tenant-scoped.",
                ],
                [
                    (
                        "Lectura aislada",
                        "la empresa A tiene frentes y mallas",
                        "un usuario de la empresa B lista frentes o mallas",
                        "no ve datos de A",
                    ),
                    (
                        "Escritura aislada",
                        "un usuario autenticado en empresa A",
                        "intenta crear un recurso indicando empresa B en el cuerpo",
                        "el sistema ignora ese valor y persiste solo bajo A, o rechaza la petición",
                    ),
                    (
                        "Empleados",
                        "se seleccionan funcionarios para una malla",
                        "se listan candidatos",
                        "solo aparecen empleados de la misma empresa",
                    ),
                    (
                        "Reportes",
                        "se exporta un reporte",
                        "se genera el archivo",
                        "solo incluye datos de la empresa del usuario",
                    ),
                ],
                "MT-EP00-HU01",
                "Todos los MS involucrados; JWT companyId",
                "Invariante de dominio: toda entidad operativa lleva company_id.",
            ),
            hu(
                "MT-EP00-HU04",
                "Reutilizar empleados, áreas, cargos y calendario de festivos de GRH",
                "MVP",
                ACTOR_COORD,
                "usar los funcionarios, áreas, cargos y festivos ya existentes en GRH al armar mallas",
                "no duplicar padrones ni calendarios",
                [
                    "Consumo de empleados, áreas, cargos y festivos del calendario de empresa",
                    "Referencia de solo lectura a jornada contractual cuando se consulte",
                ],
                [
                    "Crear empleados en Malla",
                    "Inventar sedes GRH (no existen): sitios = catálogo Malla HU13",
                    "Escribir jornada contractual desde Malla",
                ],
                [
                    "Malla no mantiene un padrón paralelo de empleados.",
                    "Áreas y cargos se leen de parametrización GRH.",
                    "Festivos se leen del calendario de empresa.",
                    "Sitios de asistencia son catálogo propio de Malla.",
                ],
                [
                    (
                        "Empleados",
                        "existen empleados activos en la empresa",
                        "el coordinador arma el grupo de la malla",
                        "selecciona desde el padrón GRH de su empresa",
                    ),
                    (
                        "Áreas y cargos",
                        "se filtra por área o cargo",
                        "se aplican filtros",
                        "los valores vienen de maestros GRH",
                    ),
                    (
                        "Festivos",
                        "el calendario de empresa tiene un festivo",
                        "se consulta el día en malla",
                        "el sistema reconoce el festivo sin catálogo paralelo de festivos en Malla",
                    ),
                    (
                        "Sin sedes GRH",
                        "se necesita un sitio de asistencia",
                        "el usuario busca sedes en GRH",
                        "usa el catálogo de sitios de Malla (HU13), no un maestro inexistente de sedes",
                    ),
                ],
                "MT-EP00-HU03, MT-EP00-HU72, MT-EP01-HU13, MT-EP01-HU15",
                "employee; parametrization (areas, positions, company-calendars); Malla para sitios",
                "Si employee no filtra por área: HU72.",
            ),
            hu(
                "MT-EP00-HU05",
                "Distinguir jornada contractual de malla operativa",
                "MVP",
                ACTOR_COORD,
                "consultar la jornada contractual como referencia sin modificarla al programar la malla",
                "separar condición laboral de la programación operativa diaria",
                [
                    "Lectura de jornada contractual como referencia",
                    "Programación operativa independiente (persona × fecha × turno/estado × atributos)",
                ],
                [
                    "Actualizar work_schedule / schedule_assignment desde Malla",
                    "Tratar la malla como fuente de jornada contractual",
                ],
                [
                    "La jornada contractual define condiciones laborales; la malla define la operación por fecha.",
                    "Guardar una celda no altera la jornada contractual.",
                    "Las diferencias entre jornada y malla pueden advertirse si existe una regla configurada; no se corrigen escribiendo la jornada.",
                ],
                [
                    (
                        "No escritura",
                        "un funcionario tiene jornada contractual definida",
                        "se le asigna un turno en malla distinto al habitual",
                        "la jornada contractual permanece igual",
                    ),
                    (
                        "Referencia",
                        "el coordinador consulta la ficha del funcionario en contexto de malla",
                        "abre la referencia de jornada",
                        "ve la jornada contractual en modo lectura",
                    ),
                    (
                        "Independencia",
                        "no hay jornada contractual cargada",
                        "se crea una celda operativa",
                        "la malla permite programar según reglas del frente (sin bloquear por ausencia de jornada, salvo regla explícita)",
                    ),
                    (
                        "Permisos",
                        "el usuario solo tiene permisos de Malla",
                        "intenta editar jornada contractual desde Malla",
                        "no existe esa acción",
                    ),
                ],
                "MT-EP00-HU04",
                "parametrization (work-schedules, schedule-assignments, working-profile) solo lectura",
                None,
            ),
            hu(
                "MT-EP00-HU71",
                "Registrar event types de notificación y timeline para Malla",
                "MVP",
                ACTOR_SA + " / equipo de plataforma",
                "registrar los tipos de evento de notificación y de timeline que usará Malla",
                "reutilizar notification-service y auditoría GRH sin mailers ni logs paralelos",
                [
                    "Alta de event types: publicación, cambio de celda, novedad, intercambio (aprobación/rechazo/aplicación)",
                    "Despacho vía infraestructura existente (correo + popup según config del evento)",
                ],
                ["Motor de plantillas de correo propio de Malla", "Auditoría paralela completa"],
                [
                    "Malla no envía correo directo; despacha eventos al servicio de notificaciones.",
                    "Los hechos de alto nivel van a timeline; el detalle de celda vive en historial de dominio (HU48).",
                    "Los despachos deben ser idempotentes por clave de evento de negocio.",
                ],
                [
                    (
                        "Registro",
                        "se despliegan los event types de Malla",
                        "se consultan en el catálogo de notificaciones",
                        "existen los códigos definidos para publicación, cambio, novedad e intercambio",
                    ),
                    (
                        "Publicación",
                        "se publica una malla",
                        "el flujo termina OK",
                        "se despacha el evento de publicación a los destinatarios configurados",
                    ),
                    (
                        "Timeline",
                        "ocurre un cambio relevante de celda o publicación",
                        "se consulta timeline",
                        "existe el hecho de negocio correspondiente",
                    ),
                    (
                        "Idempotencia",
                        "el mismo evento se reintenta con la misma clave",
                        "se procesa el reintento",
                        "no se duplica la notificación al destinatario",
                    ),
                ],
                "MT-EP00-HU01; usada por HU49, HU43, HU80",
                "notification-service; audit/timeline; parametrization catálogo timeline si aplica",
                None,
            ),
            hu(
                "MT-EP00-HU72",
                "Consumir listado de empleados con filtro por área o vínculo a frente",
                "MVP",
                ACTOR_COORD,
                "listar funcionarios aplicables al frente filtrando por área, cargo y estado sin traer toda la empresa de golpe",
                "armar grupos de malla de forma usable y tenant-safe",
                [
                    "Listado paginado de empleados de la empresa",
                    "Filtros por área, cargo, estado y texto",
                    "Resolución de empleados del frente vía vínculo frente↔área (HU65) o selección manual",
                ],
                ["Alta de empleados", "Filtros por frentes hardcodeados"],
                [
                    "Toda consulta de empleados usa la empresa del contexto autenticado.",
                    "Si el servicio de empleados no expone filtro por área, Malla debe paginar y filtrar de forma explícita documentada, o solicitar la extensión del API.",
                    "No se cachea padrón completo de otra empresa.",
                ],
                [
                    (
                        "Paginación",
                        "la empresa tiene cientos de empleados",
                        "se abre el selector de grupo",
                        "se cargan páginas o resultados filtrados, no un volcado único no paginado obligatorio",
                    ),
                    (
                        "Filtro área",
                        "el frente está vinculado a una o más áreas",
                        "se listan candidatos",
                        "se priorizan o filtran empleados de esas áreas según configuración",
                    ),
                    (
                        "Tenant",
                        "existen empleados en otra empresa",
                        "se lista",
                        "no aparecen",
                    ),
                    (
                        "Estado",
                        "hay empleados inactivos",
                        "se aplica filtro de activos",
                        "solo se ofrecen los que cumplen el filtro",
                    ),
                ],
                "MT-EP00-HU04, MT-EP01-HU65",
                "employee-service (extender filtro areaId si falta); Malla BFF/use case",
                "Dependencia técnica: hoy el listado employee puede no filtrar por areaId.",
            ),
        ],
    )
)

# Continue adding EP-01 etc. in next chunks via append before write
# For maintainability, write EP-00 now and more files in subsequent script sections.

def write_epic(code, name, hus, path):
    idx = ["# " + code + " — " + name, "", "## Índice", ""]
    for h in hus:
        # extract id/title from first line of hu block
        first = h.split("\n", 1)[0]
        idx.append("- " + first.replace("## ", ""))
    idx += ["", "---", ""]
    Path(path).write_text("\n".join(idx) + "\n".join(hus), encoding="utf-8")
    print("Wrote", path, "HUs:", len(hus))


# EP-01
ep01 = []

def add(lst, *a, **k):
    lst.append(hu(*a, **k))

add(
    ep01,
    "MT-EP01-HU64",
    "Parametrizar frentes operativos de la empresa",
    "MVP",
    ACTOR_PARAM,
    "registrar frentes operativos con código, nombre, descripción y estado pertenecientes a mi empresa",
    "configurar operaciones distintas sin depender de una lista fija de nombres de negocio",
    [
        "CRUD de frentes por empresa",
        "Código único por empresa",
        "Activar/inactivar",
    ],
    [
        "Enum de producto Contact Center/Sitio/Mesa/Lab",
        "Ítems de menú de plataforma por frente",
    ],
    [
        "El frente es un catálogo tenant-scoped, no un enum de aplicación.",
        "Un frente inactivo no se ofrece para nuevas mallas.",
        "Los nombres de operaciones actuales son solo datos de configuración o seeds de ejemplo.",
    ],
    [
        (
            "Alta",
            "el usuario tiene permiso de parametrización",
            "crea un frente con código único en su empresa",
            "el frente queda disponible solo para esa empresa",
        ),
        (
            "Unicidad",
            "ya existe el código en la empresa",
            "intenta crear otro con el mismo código",
            "el sistema rechaza por duplicado",
        ),
        (
            "Sin defaults de producto",
            "una empresa nueva sin seeds",
            "abre el catálogo de frentes",
            "no asume frentes predefinidos de otras operaciones",
        ),
        (
            "Multiempresa",
            "empresa A tiene frentes",
            "usuario de empresa B lista frentes",
            "no ve los de A",
        ),
        (
            "Inactivo",
            "un frente está inactivo",
            "se crea una malla",
            "ese frente no aparece en el selector",
        ),
    ],
    "MT-EP00-HU02, MT-EP00-HU03",
    "Malla (nuevo dominio)",
    None,
)

add(
    ep01,
    "MT-EP01-HU65",
    "Configurar capacidades, estrategia de armado y publicación del frente",
    "MVP",
    ACTOR_PARAM,
    "definir para cada frente el periodo de planificación por defecto, la estrategia de armado, la separación constructor/publicador, la editabilidad post-publicación y las capacidades disponibles",
    "que el mismo producto se adapte a cada operación sin redesplegar código",
    [
        "Periodo por defecto (valores configurables: semanal, quincenal, mensual u otros definidos en catálogo de periodos)",
        "Estrategia de armado: ninguna, manual, asistida, automática",
        "Flags de publicación y roles lógicos constructor/publicador",
        "Vínculo opcional a una o más áreas GRH",
        "Habilitación de solicitudes de intercambio (default deshabilitado)",
    ],
    ["Implementar el algoritmo de rotación (EP-03)", "Hardcodear periodos por nombre de frente"],
    [
        "Si una capacidad está deshabilitada, la UI y las API no exigen ni persisten ese atributo en celdas nuevas.",
        "Si la estrategia es manual, las acciones de rotación automática permanecen deshabilitadas.",
        "Si constructor/publicador está separado, quien solo construye no publica; envía a revisión según flujo HU43.",
        "Publicar con advertencias solo si el flag del frente lo permite.",
        "El vínculo a áreas GRH es opcional; el frente sigue siendo entidad propia.",
    ],
    [
        (
            "Capacidad off",
            "el frente tiene deshabilitado territorio",
            "se edita una celda",
            "no se solicita ni muestra territorio",
        ),
        (
            "Estrategia",
            "estrategia = manual",
            "el usuario abre rotación automática",
            "la acción no está disponible e indica que la configuración del frente no la habilita",
        ),
        (
            "Constructor",
            "separación constructor/publicador activa",
            "el constructor intenta publicar",
            "solo puede enviar a revisión o se le niega publicar según config",
        ),
        (
            "Intercambio off",
            "solicitudes deshabilitadas en el frente",
            "un empleado abre su programación",
            "no ve la acción de solicitar intercambio",
        ),
        (
            "Auditoría config",
            "se cambia la estrategia de armado",
            "se guarda",
            "queda trazabilidad de antes/después, usuario y fecha",
        ),
        (
            "Tenant",
            "se edita config de un frente",
            "persiste",
            "solo afecta a la empresa dueña del frente",
        ),
    ],
    "MT-EP01-HU64, MT-EP00-HU70",
    "Malla; parametrization áreas (vínculo opcional)",
    None,
)

add(
    ep01,
    "MT-EP01-HU06",
    "Parametrizar plantillas de turno",
    "MVP",
    ACTOR_PARAM,
    "registrar plantillas de turno con código, nombre, horarios, color, cruce de medianoche y aplicabilidad por frente",
    "reutilizar definiciones horarias al armar mallas sin quemar turnos en código",
    [
        "CRUD plantillas por empresa y aplicabilidad a frentes",
        "Duración calculada, color, nocturnidad, activo/inactivo",
    ],
    ["Asignar turnos a celdas (HU23)", "Listas fijas 1–12"],
    [
        "Las plantillas son catálogo tenant-scoped.",
        "Un turno inactivo no se ofrece en nuevas asignaciones.",
        "Los códigos de ejemplo de Excel son seeds, no enums.",
    ],
    [
        (
            "Alta",
            "existe al menos un frente",
            "crea plantilla con código único en el alcance definido",
            "queda disponible para asignar en frentes autorizados",
        ),
        (
            "Medianoche",
            "hora fin es menor que hora inicio y se marca cruce de medianoche",
            "se guarda",
            "la duración se calcula cruzando día",
        ),
        (
            "Inactivo",
            "plantilla inactiva",
            "se asigna celda nueva",
            "no aparece en el selector",
        ),
        (
            "Tenant",
            "otra empresa",
            "lista plantillas",
            "no ve las ajenas",
        ),
    ],
    "MT-EP01-HU64",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU07",
    "Configurar horarios distintos por día en un turno",
    "MVP",
    ACTOR_PARAM,
    "definir para una plantilla horarios diferentes según día de la semana u otros criterios de día configurables",
    "representar turnos que no tienen el mismo horario todos los días",
    ["Variantes de horario por día asociadas a la plantilla"],
    ["Reglas de cobertura"],
    [
        "Si no hay variante para un día, aplica el horario base de la plantilla.",
        "Las variantes pertenecen a la misma empresa que la plantilla.",
    ],
    [
        (
            "Variante",
            "existe una plantilla",
            "se define horario distinto para un día de la semana",
            "al asignar ese día se usa la variante",
        ),
        (
            "Default",
            "no hay variante para el día",
            "se asigna la plantilla",
            "usa horario base",
        ),
        (
            "Permisos",
            "usuario sin ACTUALIZAR en Parametrización",
            "intenta editar variantes",
            "se niega",
        ),
        (
            "Tenant",
            "plantilla de otra empresa",
            "intenta editar",
            "no accesible",
        ),
    ],
    "MT-EP01-HU06",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU08",
    "Parametrizar break y almuerzo del turno",
    "MVP",
    ACTOR_PARAM,
    "definir pausas (break, almuerzo u otros tipos de pausa del catálogo) asociadas a una plantilla",
    "que la operación programe pausas según configuración y no según reglas fijas por frente",
    ["Tipos de pausa configurables", "Horario o duración de pausa por plantilla"],
    ["Distribución automática en grilla (HU38)"],
    [
        "Las pausas son datos de plantilla; su obligatoriedad y efecto en cobertura lo definen reglas (HU66/HU19).",
        "No se asume que todos los frentes usan break y almuerzo.",
    ],
    [
        (
            "Alta pausa",
            "plantilla activa",
            "se agregan una o más pausas con tipo e intervalo",
            "quedan asociadas a la plantilla",
        ),
        (
            "Sin pausas",
            "frente/plantilla sin pausas",
            "se asigna el turno",
            "no se exigen pausas",
        ),
        (
            "Validación",
            "pausa fuera del horario del turno",
            "se guarda",
            "el sistema rechaza o advierte según regla configurada",
        ),
        (
            "Tenant",
            "otra empresa",
            "consulta pausas",
            "no ve datos ajenos",
        ),
    ],
    "MT-EP01-HU06",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU09",
    "Parametrizar estados de celda con flags de comportamiento",
    "MVP",
    ACTOR_PARAM,
    "registrar estados operativos de celda con código, nombre, color y flags que definen su comportamiento",
    "representar novedades y situaciones operativas sin HUs ni enums por cada estado de negocio",
    [
        "CRUD estados tenant-scoped",
        "Flags: cuenta horas ordinarias/extra/recargo/festivo; afecta cobertura; disponible para asignación de casos; requiere motivo; permite turno; permite ubicación; notifica empleado; requiere soporte; permite modificación",
    ],
    [
        "HUs separadas por vacaciones, incapacidad, actividad, etc.",
        "Cálculo monetario",
    ],
    [
        "Los estados son catálogo; vacaciones/incapacidad/actividad/descanso son ítems de datos, no tipos de sistema.",
        "El efecto en horas lo determinan los flags + motor de horas (HU58).",
        "Si un estado no es asignable a casos, la consulta operativa lo excluye de disponibilidad operativa según flag.",
        "HU50 y HU54 originales quedan absorbidas por estos flags.",
    ],
    [
        (
            "Alta estado",
            "usuario con permiso",
            "crea estado con flags",
            "queda disponible en celdas de la empresa (y frentes según aplicabilidad)",
        ),
        (
            "No suma horas",
            "estado con flag cuenta horas ordinarias = no",
            "se calcula el periodo",
            "esa celda no aporta horas ordinarias",
        ),
        (
            "Afecta cobertura",
            "estado con afecta cobertura = no",
            "se evalúa cobertura",
            "la persona no cuenta para el mínimo de esa dimensión",
        ),
        (
            "Motivo",
            "estado requiere motivo = sí",
            "se aplica a celda sin motivo",
            "el sistema bloquea o advierte según severidad configurada",
        ),
        (
            "Tenant",
            "estados de empresa A",
            "empresa B lista",
            "no los ve",
        ),
    ],
    "MT-EP01-HU64",
    "Malla",
    "Absorbe comportamiento de HU50 y HU54.",
)

add(
    ep01,
    "MT-EP01-HU10",
    "Parametrizar campañas o tareas de celda",
    "MVP",
    ACTOR_PARAM,
    "registrar campañas o tareas con código, nombre, color, vigencia y aplicabilidad a frentes",
    "etiquetar celdas sin hardcodear nombres de campaña",
    ["CRUD campañas/tareas", "Vigencia y activo"],
    ["Asignación en celda (HU29)"],
    [
        "Solo aplica si el frente tiene la capacidad habilitada (HU65/HU20).",
        "Ejemplos de operación son seeds.",
    ],
    [
        (
            "Alta",
            "capacidad campañas habilitada en un frente",
            "crea campaña vigente",
            "aparece al asignar celdas de ese frente",
        ),
        (
            "Vigencia",
            "campaña fuera de vigencia",
            "se asigna celda",
            "no se ofrece",
        ),
        (
            "Capacidad off",
            "frente sin campañas",
            "se edita celda",
            "no pide campaña",
        ),
        (
            "Tenant",
            "otra empresa",
            "lista",
            "no ve campañas ajenas",
        ),
    ],
    "MT-EP01-HU65",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU11",
    "Parametrizar territorio con niveles configurables",
    "MVP",
    ACTOR_PARAM,
    "definir la estructura territorial del frente con N niveles nombrados por configuración",
    "soportar jerarquías distintas sin fijar Regional/Zona/SPT en código",
    [
        "Definición de niveles por frente o empresa",
        "Árbol de nodos territoriales",
        "Activo/inactivo",
    ],
    ["Hardcodear 3 niveles con nombres fijos"],
    [
        "Los nombres de nivel son configuración, no enums de producto.",
        "Solo visible si el frente habilita territorio.",
    ],
    [
        (
            "Niveles",
            "el frente habilita territorio con K niveles nombrados",
            "se crean nodos",
            "la UI respeta esa jerarquía",
        ),
        (
            "Sin territorio",
            "capacidad deshabilitada",
            "se opera la malla",
            "no se exige territorio",
        ),
        (
            "Tenant",
            "nodos de otra empresa",
            "lista",
            "no visibles",
        ),
        (
            "Inactivo",
            "nodo inactivo",
            "asigna celda",
            "no se ofrece",
        ),
    ],
    "MT-EP01-HU65",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU12",
    "Parametrizar modalidades de trabajo",
    "MVP",
    ACTOR_PARAM,
    "registrar modalidades (presencial, virtual u otras) con flag que indique si requieren sitio",
    "extender modalidades sin enums fijos",
    ["CRUD modalidades", "Flag requiereSitio"],
    ["if (virtual) en código"],
    [
        "Presencial/virtual/híbrido son ejemplos de datos, no tipos de sistema.",
        "La obligatoriedad de sitio la define el flag + capacidad del frente.",
    ],
    [
        (
            "Alta",
            "permiso de parametrización",
            "crea modalidad con requiereSitio",
            "al asignar, si requiereSitio y capacidad sitio on, exige sitio",
        ),
        (
            "Nueva modalidad",
            "se necesita una modalidad nueva",
            "se crea en catálogo",
            "no requiere despliegue de código",
        ),
        (
            "Tenant",
            "otra empresa",
            "lista",
            "aislada",
        ),
        (
            "Capacidad off",
            "frente sin modalidad",
            "edita celda",
            "no pide modalidad",
        ),
    ],
    "MT-EP01-HU65",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU13",
    "Parametrizar sitios de asistencia",
    "MVP",
    ACTOR_PARAM,
    "registrar sitios de asistencia de la empresa aplicables a frentes",
    "ubicar la operación sin inventar maestro de sedes en GRH ni especializar un sitio por nombre",
    ["CRUD sitios", "Aplicabilidad a frentes", "Activo"],
    ["Tratar un nombre de sitio como caso especial de producto"],
    [
        "Sitios son catálogo Malla; GRH no provee sedes hoy.",
        "Cualquier nombre operativo es un ítem de catálogo.",
    ],
    [
        (
            "Alta",
            "capacidad sitio habilitada",
            "crea sitio",
            "disponible en celdas del frente",
        ),
        (
            "Inactivo",
            "sitio inactivo",
            "asigna",
            "no aparece",
        ),
        (
            "Tenant",
            "otra empresa",
            "lista",
            "no ve sitios ajenos",
        ),
        (
            "Sin hardcoding",
            "se documentan ejemplos",
            "se implementa",
            "ningún sitio aparece como condición en código",
        ),
    ],
    "MT-EP01-HU65",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU14",
    "Parametrizar tipos y restricciones de persona",
    "MVP",
    ACTOR_PARAM,
    "definir tipos de restricción y registrar restricciones por persona con alcance, vigencia y efecto",
    "respetar limitaciones individuales sin categorías quemadas",
    [
        "Catálogo de tipos de restricción",
        "Restricción: persona, vigencia, días/franjas, turnos/sitios/modalidades permitidos o no, efecto bloquear/advertir",
    ],
    ["Tipos estudio/salud como enums"],
    [
        "Los tipos son catálogo tenant-scoped.",
        "El motor de asignación/rotación consume restricciones (HU41).",
        "Efecto bloquear impide guardar; advertir permite con confirmación según severidad.",
    ],
    [
        (
            "Tipo",
            "parametrizador",
            "crea un tipo de restricción",
            "queda disponible para usar en restricciones",
        ),
        (
            "Restricción",
            "persona con restricción vigente que bloquea un turno",
            "se intenta asignar ese turno",
            "se aplica el efecto configurado",
        ),
        (
            "Vigencia",
            "restricción vencida",
            "se asigna",
            "no aplica",
        ),
        (
            "Tenant",
            "persona de otra empresa",
            "alta restricción",
            "imposible",
        ),
    ],
    "MT-EP00-HU04, MT-EP01-HU66",
    "Malla; employee (identidad)",
    None,
)

add(
    ep01,
    "MT-EP01-HU15",
    "Usar festivos del calendario de empresa",
    "MVP",
    ACTOR_COORD,
    "considerar los festivos definidos en el calendario GRH de la empresa al programar y calcular horas",
    "no duplicar calendarios",
    ["Lectura de festivos company calendar", "Uso en reglas de hora festiva si están configuradas"],
    ["CRUD de festivos dentro de Malla"],
    [
        "Fuente de verdad de festivos = calendario de empresa GRH.",
        "Malla no mantiene un calendario paralelo de festivos.",
    ],
    [
        (
            "Lectura",
            "hay festivo en calendario empresa",
            "se visualiza el día en malla",
            "se identifica como festivo",
        ),
        (
            "Horas",
            "existen reglas de tipo hora festiva",
            "se calcula el día festivo",
            "se clasifica según reglas HU17/HU58",
        ),
        (
            "Tenant",
            "festivos de otra empresa",
            "consulta",
            "no aplican",
        ),
        (
            "Sin calendario",
            "empresa sin festivos cargados",
            "opera malla",
            "no inventa festivos",
        ),
    ],
    "MT-EP00-HU04, MT-EP01-HU17",
    "parametrization company-calendars / holidays",
    None,
)

add(
    ep01,
    "MT-EP01-HU16",
    "Parametrizar cortes de nómina",
    "MVP",
    ACTOR_PARAM,
    "definir la frecuencia y fechas de corte usadas para agrupar horas a entregar",
    "alinear reportes de horas con el ciclo de la empresa sin liquidar dinero",
    ["Config de corte por empresa (y override por frente si se habilita)", "Periodos de corte"],
    ["Cálculo de pesos", "Integración contable"],
    [
        "Malla entrega horas por corte; no calcula valores monetarios.",
        "La frecuencia y días de corte son configuración.",
    ],
    [
        (
            "Config",
            "se define frecuencia y anclas de corte",
            "se consulta un periodo",
            "el sistema determina el rango de corte aplicable",
        ),
        (
            "Reporte",
            "existe malla en el rango",
            "se pide horas del corte",
            "agrupa según la config (HU58)",
        ),
        (
            "Tenant",
            "cortes de otra empresa",
            "consulta",
            "no visibles",
        ),
        (
            "Sin dinero",
            "se genera salida de corte",
            "se inspecciona",
            "no incluye campos de liquidación monetaria",
        ),
    ],
    "MT-EP01-HU17, MT-EP08-HU58",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU17",
    "Parametrizar tipos de hora y reglas de clasificación",
    "MVP",
    ACTOR_PARAM,
    "definir tipos de hora (ordinaria, extra, festiva, nocturna, recargo u otros) con condiciones, prioridad y aplicabilidad",
    "clasificar horas sin fórmulas quemadas por frente",
    ["Catálogo tipos de hora", "Reglas de clasificación con prioridad"],
    ["Cálculo de dinero"],
    [
        "ORD/EXT/FES etc. son códigos de catálogo/seeds, no enums rígidos de producto.",
        "La prioridad resuelve solapes de clasificación.",
    ],
    [
        (
            "Alta tipo",
            "parametrizador",
            "crea tipo de hora",
            "disponible para el motor HU58",
        ),
        (
            "Prioridad",
            "dos reglas aplican al mismo intervalo",
            "se clasifica",
            "gana la de mayor prioridad según config",
        ),
        (
            "Tenant",
            "otra empresa",
            "lista tipos",
            "aislados",
        ),
        (
            "Extensibilidad",
            "se necesita un tipo nuevo",
            "se crea en catálogo",
            "sin despliegue de lógica específica",
        ),
    ],
    "MT-EP01-HU16",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU18",
    "Parametrizar reglas de compensatorio",
    "MVP",
    ACTOR_PARAM,
    "definir reglas que, ante umbrales y tipos de día configurables, sugieran o apliquen estados/acciones de compensatorio",
    "representar políticas distintas sin fijar cantidades de domingos u otros días en código",
    [
        "Reglas: ventana temporal, tipo de día, umbral, acción (sugerir estado, advertir, bloquear), severidad",
    ],
    ["Regla fija de tres domingos"],
    [
        "Cualquier umbral numérico es parámetro de la regla.",
        "La aplicación en reporte consume estas reglas (HU63).",
    ],
    [
        (
            "Alta regla",
            "se configura umbral N sobre tipo de día D en ventana V",
            "se evalúa",
            "si se cumple, aplica la acción configurada",
        ),
        (
            "Inactiva",
            "regla inactiva",
            "evaluación",
            "no se considera",
        ),
        (
            "Por frente",
            "dos frentes con umbrales distintos",
            "se evalúa cada uno",
            "usa su propia regla",
        ),
        (
            "Tenant",
            "otra empresa",
            "no ve reglas ajenas",
            "aislamiento OK",
        ),
    ],
    "MT-EP01-HU66, MT-EP01-HU09",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU19",
    "Parametrizar reglas de cobertura",
    "MVP",
    ACTOR_PARAM,
    "definir cobertura mínima y máxima por dimensiones configurables con severidad",
    "controlar dotación sin reglas del tipo mínimo fijo por región en código",
    [
        "Dimensiones: fecha, franja, turno, territorio, sitio, modalidad, campaña, frente (según capacidades)",
        "min/max + severidad info/advertencia/bloqueo + vigencia",
    ],
    ["mínimo N técnicos hardcodeado"],
    [
        "La evaluación usa solo dimensiones habilitadas en el frente.",
        "Personas con estado que no afecta cobertura no cuentan.",
    ],
    [
        (
            "Alta",
            "se crea regla min=X en dimensión configurada",
            "la malla queda por debajo",
            "se emite hallazgo con la severidad definida",
        ),
        (
            "Máximo",
            "se supera max",
            "evaluación",
            "aplica severidad de la regla",
        ),
        (
            "Dimensión off",
            "frente sin territorio",
            "no se exigen reglas de territorio",
            "no aparecen",
        ),
        (
            "Tenant",
            "reglas ajenas",
            "no visibles",
            "OK",
        ),
    ],
    "MT-EP01-HU66, MT-EP01-HU09, MT-EP01-HU65",
    "Malla",
    None,
)

add(
    ep01,
    "MT-EP01-HU66",
    "Motor de reglas de validación parametrizable",
    "MVP",
    ACTOR_PARAM,
    "administrar reglas de validación con código, alcance, parámetros, prioridad, severidad y estado, y evaluarlas al asignar o publicar",
    "centralizar solape, horas, cobertura, descanso, repetición, restricciones, anticipación e intercambio sin constantes en código",
    [
        "CRUD reglas por empresa/frente",
        "Severidades: informativa, advertencia, bloqueo",
        "Evaluación en asignación, publicación, rotación e intercambio",
    ],
    ["UI completa de conflictos (HU34)", "DSL visual avanzado (futuro)"],
    [
        "Invariante de dominio: solape horario real de la misma persona en el mismo instante es siempre bloqueo.",
        "Horas máximas/mínimas, cobertura, repetición, celda vacía, anticipación, etc. son reglas parametrizables.",
        "Regla inactiva no se evalúa.",
        "Parámetros numéricos viven en la regla, nunca en el título de una HU ni en constantes de negocio en código.",
    ],
    [
        (
            "Horas máximas",
            "regla max_hours_period = N para el frente",
            "la malla supera N",
            "se genera hallazgo con la severidad de la regla",
        ),
        (
            "Solape",
            "dos asignaciones se solapan en el tiempo para la misma persona",
            "se intenta guardar",
            "se bloquea",
        ),
        (
            "Inactiva",
            "regla inactiva",
            "validación",
            "no aparece",
        ),
        (
            "Alcance frente",
            "regla solo del frente A",
            "se valida malla del frente B",
            "no aplica",
        ),
        (
            "Tenant",
            "reglas empresa A",
            "empresa B",
            "aisladas",
        ),
    ],
    "MT-EP01-HU65; consumida por HU34, HU41, HU43, HU78",
    "Malla (domain service)",
    "No dispersar if/else de negocio fuera del motor.",
)

add(
    ep01,
    "MT-EP01-HU20",
    "Configurar flags de atributos de celda del frente",
    "MVP",
    ACTOR_PARAM,
    "activar o desactivar qué atributos puede tener una celda en el frente (territorio, campaña, modalidad, sitio, nota, doble turno, etc.)",
    "mostrar en grilla solo lo que la operación necesita",
    ["Flags de atributos de celda por frente"],
    ["Estrategia de armado (HU65)", "Crear los catálogos base"],
    [
        "HU65 define estrategia/publicación/vínculos; HU20 detalla atributos de celda visibles/editables.",
        "Atributo off ⇒ no se captura en UI ni se exige en API de celda.",
    ],
    [
        (
            "Flag off",
            "doble turno deshabilitado",
            "se edita celda",
            "no permite segundo turno",
        ),
        (
            "Flag on",
            "nota habilitada",
            "se edita celda",
            "permite observación",
        ),
        (
            "Consistencia",
            "se deshabilita campaña con celdas ya etiquetadas",
            "se consulta histórico",
            "se conserva dato histórico; nuevas celdas no piden campaña",
        ),
        (
            "Tenant",
            "config ajena",
            "no visible",
            "OK",
        ),
    ],
    "MT-EP01-HU65",
    "Malla",
    "HU46 absorbida: constructor/publicador está en HU65 + flujo HU43.",
)

add(
    ep01,
    "MT-EP01-HU85",
    "Importación asistida desde Excel de operación",
    "Fase 3",
    ACTOR_PARAM,
    "cargar un Excel de operación para sugerir catálogos (turnos, estados, sitios, campañas) sin convertir el Excel en modelo de datos",
    "acelerar el onboarding de un frente descubriendo columnas y valores",
    ["Mapeo asistido columna→catálogo", "Sugerencias de alta", "Confirmación humana"],
    ["Persistir filas Excel como tablas espejo", "Reemplazar la grilla por Excel"],
    [
        "El Excel es fuente de descubrimiento, no esquema de BD.",
        "Nada se crea sin confirmación del usuario autorizado.",
    ],
    [
        (
            "Sugerencia",
            "Excel con columnas de turnos",
            "se procesa",
            "sugiere plantillas candidatas",
        ),
        (
            "Confirmación",
            "hay sugerencias",
            "usuario confirma un subconjunto",
            "solo ese subconjunto se crea en catálogos",
        ),
        (
            "Tenant",
            "import",
            "persiste",
            "bajo la empresa del usuario",
        ),
        (
            "No espejo",
            "import termina",
            "se inspecciona modelo",
            "no existe tabla que replique el Excel crudo como fuente operativa",
        ),
    ],
    "MT-EP01-HU06..HU14",
    "Malla",
    None,
)

# ========== EP-02 ==========
ep02 = []
add(
    ep02,
    "MT-EP02-HU21",
    "Crear malla por periodo y frente",
    "MVP",
    ACTOR_COORD,
    "crear una malla asociada a un frente, con rango de fechas según el periodo configurado, en estado borrador",
    "iniciar la programación operativa del periodo",
    ["Alta de malla", "Estado inicial borrador", "Validación de frente y alcance"],
    ["Asignación de celdas", "Publicación"],
    [
        "La malla pertenece a la empresa del usuario y a un frente de su alcance.",
        "El periodo por defecto proviene de la config del frente; el usuario puede ajustar dentro de lo permitido.",
    ],
    [
        (
            "Alta",
            "frente activo y alcance OK",
            "crea malla con fechas",
            "queda en borrador",
        ),
        (
            "Sin alcance",
            "frente fuera de alcance",
            "intenta crear",
            "rechazo",
        ),
        (
            "Tenant",
            "frente de otra empresa",
            "crear",
            "imposible",
        ),
        (
            "Duplicidad",
            "ya existe malla solapada si la regla del frente lo prohíbe",
            "crea",
            "aplica severidad de la regla",
        ),
    ],
    "MT-EP01-HU65, MT-EP00-HU70",
    "Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU22",
    "Seleccionar grupo de funcionarios de la malla",
    "MVP",
    ACTOR_COORD,
    "definir el conjunto de funcionarios que participan en la malla",
    "delimitar el universo de filas de la grilla",
    ["Alta/baja de miembros", "Filtros HU72"],
    ["Asignar turnos"],
    [
        "Solo empleados de la misma empresa.",
        "Respetar filtros y paginación.",
    ],
    [
        (
            "Agregar",
            "malla borrador",
            "agrega funcionarios",
            "aparecen como filas",
        ),
        (
            "Quitar",
            "miembro sin celdas críticas o con política permitida",
            "se quita",
            "deja de listarse; historial de celdas previas se conserva",
        ),
        (
            "Tenant",
            "empleado otra empresa",
            "agregar",
            "imposible",
        ),
        (
            "Permisos",
            "sin ACTUALIZAR",
            "modifica grupo",
            "niega",
        ),
    ],
    "MT-EP02-HU21, MT-EP00-HU72",
    "employee; Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU23",
    "Asignar turno o estado a una celda",
    "MVP",
    ACTOR_COORD,
    "asignar a una persona y fecha un turno y/o estado operativo según catálogos y reglas",
    "construir la programación celda a celda",
    ["Upsert de celda", "Validación motor reglas", "Origen manual"],
    ["Publicación"],
    [
        "Celda = persona × fecha (+ turnos/estado + atributos habilitados).",
        "Se evalúa el motor de reglas al guardar.",
        "No se modifica jornada contractual.",
    ],
    [
        (
            "Asignar turno",
            "malla editable",
            "asigna plantilla activa",
            "celda queda con turno y origen manual",
        ),
        (
            "Estado",
            "asigna estado del catálogo",
            "guarda",
            "aplica flags del estado",
        ),
        (
            "Bloqueo regla",
            "violación con severidad bloqueo",
            "guarda",
            "rechaza y muestra motivo",
        ),
        (
            "Advertencia",
            "severidad advertencia",
            "guarda con confirmación si aplica",
            "persiste y registra hallazgo",
        ),
        (
            "Tenant/alcance",
            "malla fuera de empresa o frente",
            "edita",
            "niega",
        ),
    ],
    "MT-EP01-HU06, MT-EP01-HU09, MT-EP01-HU66, MT-EP02-HU81",
    "Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU24",
    "Asignar segundo turno o turno extra el mismo día",
    "MVP",
    ACTOR_COORD,
    "agregar un segundo turno el mismo día cuando la capacidad del frente lo permite",
    "cubrir jornadas partidas o extras operativas",
    ["Multi-turno por celda/día según flag"],
    ["Si capacidad doble turno off"],
    [
        "Solo si HU20 habilita doble turno.",
        "Solape real sigue siendo bloqueo.",
        "Marca de extra si el catálogo/regla lo define.",
    ],
    [
        (
            "Alta segundo",
            "capacidad on y sin solape",
            "agrega segundo turno",
            "ambos quedan registrados",
        ),
        (
            "Solape",
            "horarios se cruzan",
            "guarda",
            "bloquea",
        ),
        (
            "Capacidad off",
            "flag off",
            "intenta segundo turno",
            "no disponible",
        ),
        (
            "Reglas horas",
            "supera max_hours_period",
            "guarda",
            "aplica severidad regla",
        ),
    ],
    "MT-EP02-HU23, MT-EP01-HU20, MT-EP01-HU66",
    "Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU25",
    "Asignar territorio a la celda",
    "MVP",
    ACTOR_COORD,
    "asignar nodo territorial a la celda cuando el frente tiene la capacidad habilitada",
    "ubicar operativamente a la persona ese día",
    ["Set territorio"],
    ["Frentes sin territorio"],
    ["Solo nodos activos del árbol del frente/empresa."],
    [
        (
            "Asignar",
            "capacidad on",
            "elige nodo",
            "queda en celda",
        ),
        (
            "Off",
            "capacidad off",
            "edita",
            "campo ausente",
        ),
        (
            "Nodo inválido",
            "nodo de otro frente/empresa",
            "asigna",
            "rechaza",
        ),
        (
            "Cobertura",
            "existen reglas por territorio",
            "guarda",
            "revalúa cobertura",
        ),
    ],
    "MT-EP01-HU11, MT-EP02-HU23",
    "Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU26",
    "Asignar modalidad y sitio a la celda",
    "MVP",
    ACTOR_COORD,
    "definir modalidad y sitio de asistencia en la celda según flags y catálogos",
    "reflejar dónde y cómo asiste la persona",
    ["Set modalidad/sitio"],
    [],
    [
        "Si modalidad requiere sitio y capacidad sitio on, el sitio es obligatorio según severidad configurada.",
    ],
    [
        (
            "OK",
            "capacidades on",
            "asigna modalidad y sitio válidos",
            "persiste",
        ),
        (
            "Requiere sitio",
            "modalidad con requiereSitio y sin sitio",
            "guarda",
            "bloquea o advierte según regla",
        ),
        (
            "Off",
            "capacidades off",
            "edita",
            "campos ausentes",
        ),
        (
            "Tenant",
            "sitio ajeno",
            "asigna",
            "rechaza",
        ),
    ],
    "MT-EP01-HU12, MT-EP01-HU13, MT-EP02-HU23",
    "Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU27",
    "Registrar observación en la celda",
    "MVP",
    ACTOR_COORD,
    "agregar una nota u observación a la celda cuando la capacidad está habilitada",
    "dejar contexto operativo sin abusos de campos",
    ["Texto de observación", "Límite de longitud configurable"],
    [],
    ["Si el estado requiere motivo, el motivo puede mapearse a este campo o a campo motivo dedicado según diseño."],
    [
        (
            "Alta",
            "capacidad nota on",
            "guarda texto",
            "visible en celda e historial si cambia",
        ),
        (
            "Off",
            "capacidad off",
            "intenta",
            "no disponible",
        ),
        (
            "Límite",
            "excede longitud",
            "guarda",
            "rechaza",
        ),
        (
            "Permisos",
            "solo LEER",
            "edita nota",
            "niega",
        ),
    ],
    "MT-EP01-HU20, MT-EP02-HU23",
    "Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU28",
    "Visualizar grilla operativa",
    "MVP",
    ACTOR_COORD,
    "ver la grilla personas × fechas con turnos, estados, colores, leyenda, atributos habilitados y hallazgos",
    "operar la malla de forma visual",
    ["Render grilla", "Leyenda", "Indicadores de conflicto"],
    ["Export (HU59)", "Carga total sin ventana (prohibido: ver HU82)"],
    [
        "La grilla consume ventana temporal y página de personas (HU82).",
        "Colores vienen de catálogos, no de constantes de frente.",
    ],
    [
        (
            "Vista",
            "malla con celdas",
            "abre grilla",
            "ve filas/columnas de la ventana cargada",
        ),
        (
            "Leyenda",
            "existen turnos/estados con color",
            "abre leyenda",
            "lista códigos y colores del frente",
        ),
        (
            "Conflictos",
            "hay hallazgos",
            "visualiza",
            "se destacan celdas/reglas",
        ),
        (
            "Permisos",
            "sin LEER construcción",
            "abre",
            "niega",
        ),
    ],
    "MT-EP02-HU23, MT-EP02-HU82, MT-EP03-HU34",
    "Malla FE",
    None,
)

add(
    ep02,
    "MT-EP02-HU29",
    "Asignar campaña o tarea a la celda",
    "MVP",
    ACTOR_COORD,
    "etiquetar la celda con campaña/tarea si la capacidad está activa",
    "reflejar la actividad operativa del día",
    ["Set campaña"],
    [],
    ["Solo campañas vigentes y del frente/empresa."],
    [
        (
            "OK",
            "capacidad on",
            "asigna campaña vigente",
            "persiste",
        ),
        (
            "Off",
            "capacidad off",
            "campo ausente",
            "OK",
        ),
        (
            "No vigente",
            "campaña vencida",
            "asigna",
            "rechaza",
        ),
        (
            "Tenant",
            "campaña ajena",
            "rechaza",
            "OK",
        ),
    ],
    "MT-EP01-HU10, MT-EP02-HU23",
    "Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU30",
    "Cubrir recurso de otro frente o área el mismo día",
    "Fase 2",
    ACTOR_COORD,
    "asignar a una persona en una malla distinta el mismo día cuando las reglas de solape y horas lo permitan",
    "soportar coberturas cruzadas sin hardcodear frentes",
    ["Asignación cruzada gobernada por reglas"],
    ["Permitir solape real"],
    [
        "La contabilización de horas en cruce sigue la configuración (cuenta en malla destino por defecto).",
        "Solape horario real siempre bloquea.",
    ],
    [
        (
            "Permitido",
            "sin solape y reglas OK",
            "asigna en segunda malla",
            "ambas celdas existen",
        ),
        (
            "Solape",
            "horarios cruzan",
            "bloquea",
            "OK",
        ),
        (
            "Horas",
            "supera tope",
            "aplica severidad",
            "OK",
        ),
        (
            "Tenant",
            "malla otra empresa",
            "imposible",
            "OK",
        ),
    ],
    "MT-EP02-HU23, MT-EP01-HU66",
    "Malla",
    "Default recomendado: cuenta horas donde se asigna + regla solape.",
)

add(
    ep02,
    "MT-EP02-HU31",
    "Filtrar y buscar en la grilla por atributos habilitados",
    "MVP",
    ACTOR_COORD,
    "filtrar la grilla por texto, turno, estado y atributos habilitados del frente",
    "encontrar rápido personas o situaciones",
    ["Filtros dinámicos según flags"],
    [],
    ["No mostrar filtros de capacidades deshabilitadas."],
    [
        (
            "Filtro estado",
            "hay varios estados",
            "filtra uno",
            "solo filas/celdas coincidentes en la ventana",
        ),
        (
            "Sin filtro fantasma",
            "territorio off",
            "abre filtros",
            "no aparece filtro territorio",
        ),
        (
            "Permisos",
            "LEER",
            "filtra",
            "permitido",
        ),
        (
            "Tenant",
            "datos",
            "filtro",
            "solo propia empresa",
        ),
    ],
    "MT-EP02-HU28, MT-EP01-HU20",
    "Malla",
    None,
)

add(
    ep02,
    "MT-EP02-HU81",
    "Control de concurrencia en edición de celdas",
    "MVP",
    ACTOR_COORD,
    "evitar que dos ediciones concurrentes sobrescriban en silencio la misma celda",
    "proteger integridad operativa",
    ["Versionado/optimistic locking por celda", "Conflicto visible al usuario"],
    ["Bloqueo pesimista de malla completa (no requerido)"],
    [
        "Cada celda tiene versión; escribir con versión obsoleta falla con conflicto.",
        "El usuario debe poder recargar y reintentar.",
    ],
    [
        (
            "Conflicto",
            "usuario A y B cargan misma celda",
            "A guarda y luego B guarda con versión vieja",
            "B recibe error de conflicto y no pisa a A",
        ),
        (
            "OK",
            "versión actual",
            "guarda",
            "incrementa versión",
        ),
        (
            "Historial",
            "guarda OK",
            "consulta historial",
            "incluye el cambio de A",
        ),
        (
            "Permisos",
            "sin ACTUALIZAR",
            "guarda",
            "niega antes del versionado",
        ),
    ],
    "MT-EP02-HU23, MT-EP05-HU48",
    "Malla",
    "Optimistic locking / ETag por celda.",
)

add(
    ep02,
    "MT-EP02-HU82",
    "Carga parcial de grilla por ventana temporal y paginación de personas",
    "MVP",
    ACTOR_COORD,
    "cargar solo la ventana de fechas y la página de personas necesarias",
    "operar mallas grandes sin payloads inmanejables",
    ["API de grilla con from/to + page/size", "Virtualización en UI"],
    ["Descargar 1000×31 siempre"],
    [
        "El backend no debe exigir devolver toda la malla para editar una ventana.",
        "Los contadores globales pueden ser proyecciones/agregados aparte.",
    ],
    [
        (
            "Ventana",
            "malla de un mes",
            "pide 7 días",
            "solo recibe esos días",
        ),
        (
            "Página",
            "200 personas",
            "pide página 1 size 50",
            "recibe 50 filas",
        ),
        (
            "Edición",
            "celda de la ventana",
            "guarda",
            "no requiere recargar toda la malla",
        ),
        (
            "Permisos/tenant",
            "consulta",
            "datos",
            "solo empresa y alcance",
        ),
    ],
    "MT-EP02-HU28",
    "Malla",
    "Requisito no funcional de performance.",
)

# Write EP-00 from HUS[0], EP-01, EP-02
write_epic("EP-00", "Integración con GRH", HUS[0][2], OUT / "EP-00-Integracion-GRH.md")
write_epic("EP-01", "Parametrización y catálogos", ep01, OUT / "EP-01-Parametrizacion.md")
write_epic("EP-02", "Construcción de malla", ep02, OUT / "EP-02-Construccion.md")
print("OK part1")
