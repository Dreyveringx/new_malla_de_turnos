# -*- coding: utf-8 -*-
"""Genera GST-FM-04 markdown para HUs nuevas del backlog definitivo."""
from pathlib import Path

ROOT = Path(r"C:\Users\jair.uribe\Datacenter\Malla-Turnos\docs\Historias de usuario")
DATE = "05/09/2026"
AUTHOR = "Jair Uribe"


def doc(
    epic_folder,
    epic_label,
    hu_id,
    slug,
    title,
    como,
    quiero,
    para,
    profiles,
    actors,
    associated,
    preconds,
    steps,
    result,
    alternates,
    errors,
    prototype,
    criteria,
    rules,
    inputs,
    note=None,
):
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
        f"| {DATE} | 1.0 | Creación de la historia de {title[0].lower() + title[1:] if title else 'usuario'}. | {AUTHOR} |",
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
        f"| Id. Requerimiento | {hu_id} |",
        f"| Id asociado | REQ-MT-{hu_id.split('-HU')[-1]} / {epic_label.split('—')[0].strip()} |",
        "",
        "### Descripción de historia de usuario",
        "",
        f"Como {como}, quiero {quiero}, para {para}.",
        "",
        "---",
        "",
        "## Perfiles de usuario en GRH (contexto)",
        "",
        "| Perfil | Rol en esta historia |",
        "| ------ | -------------------- |",
    ]
    for p, r in profiles:
        lines.append(f"| {p} | {r} |")
    lines += [
        "",
        "---",
        "",
        "## Actores",
        "",
        "| Tipo | Actor |",
        "| ---- | ----- |",
    ]
    for t, a in actors:
        lines.append(f"| {t} | {a} |")
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
    for i, (actor, system) in enumerate(steps, 1):
        lines.append(f"| {i} | {actor} | {system} |")
    lines += [
        "",
        f"Resultado esperado: {result}",
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
        prototype,
        "",
        "---",
        "",
        "## Criterios de aceptación",
        "",
    ]
    for i, c in enumerate(criteria, 1):
        lines.append(f"{i}. {c}")
    lines += [
        "",
        "---",
        "",
        "## Reglas de negocio",
        "",
        "| Id | Regla |",
        "| -- | ----- |",
    ]
    for i, r in enumerate(rules, 1):
        lines.append(f"| RN-{i:02d} | {r} |")
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
    if note:
        lines.insert(-2, note)
        lines.insert(-2, "")

    path = ROOT / epic_folder / f"GST-FM-04-{hu_id}-{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print("OK", path.relative_to(ROOT))
    return path


def annex(epic_folder, hu_id, slug, body):
    path = ROOT / epic_folder / f"GST-FM-04-{hu_id}-anexo-tecnico.md"
    text = f"""# Anexo técnico — {hu_id}

Audiencia: desarrollo / arquitectura. No presentar al cliente.

{body}

---
*Generado {DATE} con backlog definitivo v2.0.*
"""
    path.write_text(text, encoding="utf-8")
    print("OK anexo", path.name)


# ========== EP-00 ==========
doc(
    "Epica 00",
    "EP-00 — Integración del módulo a la plataforma GRH",
    "MT-EP00-HU70",
    "Asignar-alcance-frentes-usuarios-roles",
    "Asignar alcance de frentes operativos a usuarios o roles",
    "administrador de empresa o usuario con permiso de parametrización",
    "definir qué frentes operativos puede ver u operar cada usuario o rol dentro de Malla de Turnos",
    "aislar la operación por frente sin inventar un sistema de permisos distinto al de la plataforma",
    [
        ("Super-administrador", "No asigna alcances de frentes de empresas cliente."),
        ("Administrador de empresa", "Puede asignar alcances en su empresa."),
        ("Usuario de la empresa", "Recibe el alcance; opera solo los frentes autorizados."),
    ],
    [
        ("Inicia", "Administrador de empresa o usuario con permiso de parametrización"),
        ("Participa", "Usuarios o roles que reciben el alcance"),
        ("No participa", "Super-administrador de la plataforma GRH"),
    ],
    [
        "MT-EP00-HU02 — Configurar permisos por sección de menú",
        "MT-EP01-HU64 — Parametrizar frentes operativos",
        "MT-EP00-HU03 — Aislar información por empresa",
    ],
    [
        "El módulo está habilitado para la empresa (MT-EP00-HU01).",
        "Existen permisos de menú configurados (MT-EP00-HU02).",
        "Existe al menos un frente operativo en la empresa (MT-EP01-HU64).",
    ],
    [
        ("El administrador abre Parametrización → Alcance por frente.", "Muestra usuarios o roles de la empresa y frentes disponibles."),
        ("Selecciona un usuario o rol.", "Lista los frentes de la empresa."),
        ("Marca los frentes autorizados y guarda.", "Persiste el alcance solo para esa empresa."),
        ("El usuario inicia sesión y abre Malla de Turnos.", "Solo ve frentes de su alcance en selectores y listados."),
        ("Intenta abrir una malla de un frente no autorizado.", "El sistema niega el acceso."),
    ],
    "Cada usuario opera únicamente los frentes autorizados de su empresa.",
    [
        "Rol con alcance total explícito: ve todos los frentes activos de la empresa.",
        "Usuario sin alcance asignado: no ve frentes (comportamiento restrictivo).",
        "Frente inactivo: no aparece para nuevas operaciones aunque estuviera en el alcance.",
        "Cambio de alcance: queda registro de quién modificó y cuándo.",
    ],
    [
        ("Usuario sin permiso de parametrización intenta asignar alcance.", "Acceso no permitido."),
        ("Intenta asignar un frente de otra empresa.", "El frente no aparece; no se puede asignar."),
        ("Error al guardar.", "Mensaje claro; no deja alcance a medias."),
    ],
    """Referencia: pantalla de alcance usuario/rol ↔ frentes.

1. Listado de usuarios o roles de la empresa
2. Casillas o selector múltiple de frentes
3. Indicación de alcance vacío (sin frentes)
""",
    [
        "Un usuario solo ve y opera frentes de su empresa incluidos en su alcance.",
        "Intentar acceder a un frente fuera de alcance es rechazado.",
        "Los frentes de otra empresa nunca aparecen.",
        "Sin alcance asignado, no se ofrecen frentes (salvo rol con alcance total explícito).",
        "Los cambios de alcance quedan auditados (quién, cuándo, antes/después).",
        "Esta historia no reemplaza los permisos CREAR/LEER/ACTUALIZAR/ELIMINAR de menú (HU02).",
    ],
    [
        "El alcance por frente es configuración de Malla de Turnos, no un permiso nuevo de menú de plataforma.",
        "El alcance siempre está limitado a la empresa del usuario.",
        "Fail-closed: sin asignación, no hay frentes visibles.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Usuario o rol | Malla de turnos | Formulario / listado |
| Frentes autorizados | Malla de turnos | Selector múltiple |
""",
)

doc(
    "Epica 00",
    "EP-00 — Integración del módulo a la plataforma GRH",
    "MT-EP00-HU71",
    "Registrar-event-types-notificacion-timeline",
    "Registrar tipos de evento de notificación y timeline para Malla",
    "super-administrador o equipo de plataforma",
    "dejar registrados los tipos de aviso y de línea de tiempo que usará Malla de Turnos",
    "que publicación, cambios e intercambios usen la infraestructura de avisos y auditoría de GRH sin correos ni bitácoras paralelas",
    [
        ("Super-administrador", "Registra o valida los tipos de evento en la plataforma."),
        ("Administrador de empresa", "No registra tipos; consume los avisos en su empresa."),
        ("Usuario de la empresa", "Recibe avisos según el evento (publicación, cambio, intercambio)."),
    ],
    [
        ("Inicia", "Super-administrador / equipo de plataforma"),
        ("Participa", "Usuarios que reciben avisos en historias posteriores"),
        ("No participa", "Coordinadores en el armado diario de esta historia"),
    ],
    [
        "MT-EP00-HU01 — Completar módulo y submódulos",
        "MT-EP05-HU49 — Notificar cambio al empleado",
        "MT-EP04-HU43 — Publicar malla",
        "MT-EP09-HU80 — Aplicar intercambio y notificar",
    ],
    [
        "El módulo Malla de Turnos está en el catálogo de plataforma.",
        "La plataforma ya dispone de infraestructura de notificaciones y de línea de tiempo.",
    ],
    [
        ("El equipo registra los tipos de evento de Malla (publicación, cambio de celda, novedad, intercambio).", "Quedan disponibles en el catálogo de eventos de la plataforma."),
        ("Se publica una malla en una empresa habilitada.", "Se dispara el aviso de publicación a los destinatarios configurados."),
        ("Se confirma un cambio relevante de celda.", "Queda el hecho en la línea de tiempo y el historial de celda (HU48)."),
        ("Se reintenta el mismo aviso por un fallo temporal.", "No se duplica el aviso al destinatario."),
    ],
    "Malla reutiliza avisos y timeline de GRH con tipos de evento propios.",
    [
        "Un frente no usa notificaciones de cierto evento: la configuración del frente o del evento lo desactiva.",
        "Intercambio deshabilitado: los tipos de intercambio existen pero no se disparan hasta habilitar EP-09.",
    ],
    [
        ("Falta un tipo de evento obligatorio al desplegar.", "La verificación de plataforma lo detecta; no se da por cerrado el alta."),
        ("Fallo del canal de correo.", "Se registra el fallo; el reintento no duplica si ya se entregó el aviso."),
    ],
    """No hay pantalla de usuario final en esta historia.

1. Catálogo de tipos de evento de plataforma (administración)
2. Efecto visible: campana y/o correo en historias de publicación, cambio e intercambio
""",
    [
        "Existen tipos de evento para publicación, cambio de celda, novedad e intercambio.",
        "Al publicar una malla se dispara el aviso configurado.",
        "Los hechos relevantes quedan en la línea de tiempo de la plataforma.",
        "Un reintento del mismo aviso no duplica la entrega al destinatario.",
        "Malla no envía correo por fuera de la infraestructura de notificaciones de GRH.",
    ],
    [
        "Los avisos de Malla pasan por el servicio de notificaciones de la plataforma.",
        "El detalle de celda vive en el historial de dominio (HU48); la línea de tiempo guarda hechos de alto nivel.",
        "Cada aviso de negocio tiene una clave que evita duplicados.",
    ],
    "Esta historia no captura datos de formularios de usuario final. Define tipos de evento de plataforma.",
)

doc(
    "Epica 00",
    "EP-00 — Integración del módulo a la plataforma GRH",
    "MT-EP00-HU72",
    "Listar-empleados-filtro-paginacion-frente",
    "Listar empleados con filtro y paginación para armar mallas",
    "usuario de la empresa con permiso de construcción de malla",
    "buscar y seleccionar funcionarios de mi empresa filtrando por área, cargo o estado, sin cargar toda la nómina de una vez",
    "armar el grupo de la malla de forma usable y segura entre empresas",
    [
        ("Super-administrador", "No arma mallas de empresas cliente."),
        ("Administrador de empresa", "Puede construir si tiene permiso."),
        ("Usuario de la empresa", "Coordinador o supervisora con permiso de construcción."),
    ],
    [
        ("Inicia", "Usuario con permiso de construcción"),
        ("Participa", "Funcionarios candidatos del padrón de la empresa"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP00-HU04 — Reutilizar maestros GRH",
        "MT-EP01-HU65 — Vincular frente a áreas",
        "MT-EP02-HU22 — Seleccionar funcionarios de la malla",
    ],
    [
        "Existen empleados activos en la empresa.",
        "El usuario tiene alcance al frente (HU70).",
        "El frente puede estar vinculado a una o más áreas (HU65).",
    ],
    [
        ("El usuario abre el selector de funcionarios de la malla.", "Muestra una página de resultados, no un listado completo obligatorio."),
        ("Aplica filtros de área, cargo, estado o texto.", "Actualiza resultados de su empresa."),
        ("Si el frente tiene áreas vinculadas, prioriza o filtra esos empleados.", "Muestra candidatos alineados al frente según configuración."),
        ("Selecciona funcionarios y confirma.", "Quedan en el grupo de la malla (HU22)."),
    ],
    "El selector de empleados es paginado, filtrable y limitado a la empresa del usuario.",
    [
        "Sin vínculo a área: el usuario filtra manualmente.",
        "Empleados inactivos: se ocultan si el filtro de activos está aplicado.",
        "Búsqueda por nombre o documento según campos disponibles del padrón.",
    ],
    [
        ("Intenta ver empleados de otra empresa.", "No aparecen."),
        ("El servicio de empleados no responde.", "Mensaje de error; no deja la malla inconsistente."),
        ("Página vacía por filtros muy restrictivos.", "Estado vacío claro con opción de limpiar filtros."),
    ],
    """Referencia: selector de funcionarios en construcción de malla.

1. Buscador y filtros (área, cargo, estado)
2. Listado paginado
3. Selección múltiple
""",
    [
        "Solo se listan empleados de la empresa del usuario.",
        "Los resultados se presentan por páginas o de forma acotada.",
        "Los filtros de área/cargo/estado funcionan sobre el padrón GRH.",
        "Si el frente tiene áreas vinculadas, el listado las respeta según configuración.",
        "No se crea un padrón paralelo de empleados en Malla.",
    ],
    [
        "Malla reutiliza el padrón de empleados de GRH.",
        "No se permite mezclar empresas en el selector.",
        "La paginación es obligatoria cuando el volumen de empleados es alto.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Texto de búsqueda | Gestor de Hojas de Vida / empleados | Buscador |
| Área | Parametrización (organización) | Filtro |
| Cargo | Parametrización (organización) | Filtro |
| Estado del empleado | Gestor de Hojas de Vida / empleados | Filtro |
""",
)

annex(
    "Epica 00",
    "MT-EP00-HU70",
    "alcance",
    """## Implementación

- Tabla/dominio Malla: user_id o role_id × front_id × company_id.
- No crear permission_submodules nuevos por frente.
- Enforcement en use cases de malla/catálogos: filtrar por alcance + companyId JWT.

## Dependencias

- auth: identidad usuario/roles
- Malla: frentes (HU64)
""",
)

annex(
    "Epica 00",
    "MT-EP00-HU71",
    "events",
    """## Event types sugeridos (códigos orientativos)

- MALLA_PUBLICADA
- MALLA_CELDA_CAMBIADA
- MALLA_NOVEDAD_APLICADA
- MALLA_INTERCAMBIO_SOLICITADA
- MALLA_INTERCAMBIO_RESUELTA

## Integración

- notification-service: dispatch EMAIL+POPUP
- audit timeline: hechos de alto nivel
- Historial de celda (HU48) = detalle de dominio append-only
- Idempotencia por business event key
""",
)

annex(
    "Epica 00",
    "MT-EP00-HU72",
    "empleados",
    """## Gap conocido

- Employee list puede no filtrar por areaId hoy.
- Opciones: extender EmployeeFilterRequest o filtrar/paginar en BFF/use case Malla.

## Regla

- companyId siempre desde JWT; nunca del body como fuente de verdad.
""",
)

# ========== EP-01 ==========
doc(
    "Epica 01",
    "EP-01 — Parametrización de catálogos",
    "MT-EP01-HU64",
    "Parametrizar-frentes-operativos",
    "Parametrizar frentes operativos de la empresa",
    "usuario con permiso de parametrización en Malla de Turnos",
    "registrar frentes operativos con código, nombre, descripción y estado de mi empresa",
    "configurar distintas operaciones sin depender de una lista fija de nombres de negocio",
    [
        ("Super-administrador", "No parametriza frentes de empresas cliente."),
        ("Administrador de empresa", "Puede crear frentes si tiene permiso."),
        ("Usuario de la empresa", "Coordinador o supervisora con permiso de parametrización."),
    ],
    [
        ("Inicia", "Usuario con permiso de parametrización"),
        ("Participa", "—"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP00-HU02 — Permisos por sección",
        "MT-EP01-HU65 — Configurar capacidades del frente",
        "MT-EP00-HU70 — Alcance de frentes",
    ],
    [
        "Módulo habilitado y permiso de parametrización.",
        "La empresa no asume frentes predefinidos del producto.",
    ],
    [
        ("Entra a Parametrización → Frentes operativos.", "Lista frentes de su empresa."),
        ("Crea un frente con código, nombre y descripción.", "Valida código único en la empresa."),
        ("Activa o inactiva el frente.", "Inactivo no aparece para nuevas mallas."),
        ("Otro usuario de otra empresa lista frentes.", "No ve los de esta empresa."),
    ],
    "La empresa tiene un catálogo propio de frentes, sin enums de producto.",
    [
        "Empresa nueva sin datos: listado vacío; no se inventan frentes de ejemplo como obligatorios.",
        "Código duplicado: no guarda.",
        "Editar nombre: no cambia el código si ya está en uso, salvo política de edición definida.",
    ],
    [
        ("Código vacío o duplicado.", "No guarda; indica el problema."),
        ("Usuario sin permiso.", "Acceso no permitido."),
        ("Intento de ver frentes de otra empresa.", "No visibles."),
    ],
    """Referencia: catálogo de frentes.

1. Listado código / nombre / estado
2. Formulario de alta y edición
3. Activar / inactivar
""",
    [
        "Cada frente pertenece a una sola empresa.",
        "El código es único dentro de la empresa.",
        "Un frente inactivo no se ofrece para nuevas mallas.",
        "El sistema no asume nombres fijos de operación (Contact Center, Sitio, Mesa, Laboratorio u otros).",
        "Una empresa no ve frentes de otra.",
    ],
    [
        "El frente es un catálogo parametrizable, no un tipo fijo del producto.",
        "Los nombres de operaciones actuales son solo datos o ejemplos de configuración.",
        "Sin frentes activos no se pueden crear mallas.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Código | Malla de turnos | Formulario |
| Nombre | Malla de turnos | Formulario |
| Descripción | Malla de turnos | Formulario |
| Estado (activo/inactivo) | Malla de turnos | Formulario |
""",
)

doc(
    "Epica 01",
    "EP-01 — Parametrización de catálogos",
    "MT-EP01-HU65",
    "Configurar-capacidades-estrategia-publicacion-frente",
    "Configurar capacidades, estrategia de armado y publicación del frente",
    "usuario con permiso de parametrización",
    "definir para cada frente el periodo por defecto, la estrategia de armado, si se separa quien construye de quien publica, si la malla publicada se puede editar y qué capacidades usa",
    "que el mismo módulo se adapte a cada operación sin cambiar el producto por frente",
    [
        ("Super-administrador", "No configura frentes de empresas cliente."),
        ("Administrador de empresa", "Puede configurar si tiene permiso."),
        ("Usuario de la empresa", "Usuario con permiso de parametrización."),
    ],
    [
        ("Inicia", "Usuario con permiso de parametrización"),
        ("Participa", "—"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP01-HU64 — Frentes operativos",
        "MT-EP01-HU20 — Flags de atributos de celda",
        "MT-EP04-HU43 — Ciclo de publicación",
        "MT-EP09-HU76 — Configurar intercambio",
    ],
    [
        "Existe al menos un frente (HU64).",
        "Permiso de parametrización.",
    ],
    [
        ("Abre la configuración del frente.", "Muestra periodo, estrategia, publicación y capacidades."),
        ("Define periodo por defecto y estrategia (ninguna, manual, asistida, automática).", "Guarda la configuración del frente."),
        ("Activa o desactiva separación constructor/publicador y edición post-publicación.", "El ciclo de publicación (HU43) respeta esos valores."),
        ("Vincula opcionalmente una o más áreas de la organización.", "Sirve de guía para el selector de empleados (HU72)."),
        ("Habilita o deshabilita solicitudes de intercambio (por defecto deshabilitado).", "La vista del empleado respeta el valor."),
        ("Desactiva una capacidad (por ejemplo territorio).", "La grilla y formularios no piden ese dato."),
    ],
    "Cada frente tiene su perfil de comportamiento sin hardcoding por nombre de operación.",
    [
        "Estrategia manual: acciones de rotación automática no disponibles.",
        "Publicar con advertencias: solo si el frente lo permite.",
        "Cambio de configuración: queda trazabilidad de quién cambió qué.",
    ],
    [
        ("Guarda sin periodo o estrategia.", "Indica campos obligatorios."),
        ("Usuario sin permiso.", "Acceso no permitido."),
        ("Frente de otra empresa.", "No accesible."),
    ],
    """Referencia: ficha de configuración del frente.

1. Periodo por defecto
2. Estrategia de armado
3. Opciones de publicación
4. Capacidades / interruptores
5. Vínculo opcional a áreas
""",
    [
        "Si una capacidad está apagada, no se exige ni se muestra en celdas nuevas.",
        "La estrategia del frente determina qué acciones de armado/rotación están disponibles.",
        "Si constructor y publicador están separados, quien solo construye no publica.",
        "Las solicitudes de intercambio nacen deshabilitadas salvo que se activen.",
        "Los cambios de configuración quedan auditados.",
        "La configuración es por empresa y frente.",
    ],
    [
        "Periodo, estrategia y publicación son configuración, no código por frente.",
        "El vínculo a áreas de GRH es opcional; el frente sigue siendo entidad propia.",
        "HU46 (constructor/publicador) queda cubierta por esta configuración + HU43.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Periodo por defecto | Malla de turnos | Selector |
| Estrategia de armado | Malla de turnos | Selector |
| Separar constructor/publicador | Malla de turnos | Interruptor |
| Edición post-publicación | Malla de turnos | Interruptor |
| Publicar con advertencias | Malla de turnos | Interruptor |
| Solicitudes de intercambio | Malla de turnos | Interruptor |
| Áreas vinculadas | Parametrización (organización) | Selector múltiple |
| Capacidades del frente | Malla de turnos | Interruptores |
""",
)

doc(
    "Epica 01",
    "EP-01 — Parametrización de catálogos",
    "MT-EP01-HU66",
    "Motor-reglas-validacion-parametrizable",
    "Administrar motor de reglas de validación parametrizable",
    "usuario con permiso de parametrización",
    "definir reglas de validación con alcance, parámetros, prioridad, severidad y estado",
    "validar solapes, horas, cobertura, descansos, restricciones e intercambios sin dejar reglas fijas en el producto",
    [
        ("Super-administrador", "No define reglas de empresas cliente."),
        ("Administrador de empresa", "Puede administrar reglas si tiene permiso."),
        ("Usuario de la empresa", "Parametrizador; coordinadores ven el efecto en grilla (HU34)."),
    ],
    [
        ("Inicia", "Usuario con permiso de parametrización"),
        ("Participa", "Usuarios de construcción al guardar o publicar"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP01-HU65 — Configuración del frente",
        "MT-EP01-HU19 — Reglas de cobertura",
        "MT-EP03-HU34 — Panel de conflictos",
        "MT-EP09-HU78 — Validar solicitud de intercambio",
    ],
    [
        "Existe al menos un frente.",
        "Permiso de parametrización.",
    ],
    [
        ("Abre Parametrización → Reglas de validación.", "Lista reglas de la empresa/frente."),
        ("Crea una regla con código, alcance, parámetros y severidad (informativa, advertencia, bloqueo).", "Guarda la regla activa o inactiva."),
        ("Un coordinador guarda una celda que incumple la regla.", "Aplica la severidad configurada."),
        ("Desactiva la regla.", "Deja de evaluarse."),
    ],
    "Las validaciones de negocio variables viven como reglas configurables; el solape real sigue siendo bloqueo.",
    [
        "Regla solo de un frente: no aplica a otros.",
        "Dos reglas del mismo tipo: gana la prioridad configurada.",
        "Solape horario real de la misma persona: siempre bloqueo.",
    ],
    [
        ("Parámetros incompletos.", "No guarda."),
        ("Severidad inválida.", "No guarda."),
        ("Usuario sin permiso.", "Acceso no permitido."),
    ],
    """Referencia: catálogo de reglas + mensajes en grilla (HU34).

1. Listado de reglas
2. Formulario código / alcance / parámetros / severidad
3. Activar / inactivar
""",
    [
        "Las reglas parametrizables incluyen horas máximas/mínimas, cobertura, repetición, restricciones, anticipación y similares.",
        "El solape horario real de una misma persona en el mismo instante se bloquea siempre.",
        "Una regla inactiva no se evalúa.",
        "Los umbrales numéricos viven en la regla, no como constantes del producto.",
        "Las reglas son por empresa y, si aplica, por frente.",
        "El panel de conflictos (HU34) muestra el nombre de la regla y sus parámetros.",
    ],
    [
        "Severidades: informativa, advertencia, bloqueo.",
        "No se dispersan if/else de negocio por nombre de frente o turno en pantallas.",
        "HU34 deja de citar umbrales fijos (por ejemplo 42 horas) como regla del sistema.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Código | Malla de turnos | Formulario |
| Nombre | Malla de turnos | Formulario |
| Frente o alcance | Malla de turnos | Selector |
| Parámetros | Malla de turnos | Formulario |
| Severidad | Malla de turnos | Selector |
| Prioridad | Malla de turnos | Numérico |
| Estado | Malla de turnos | Interruptor |
""",
)

doc(
    "Epica 01",
    "EP-01 — Parametrización de catálogos",
    "MT-EP01-HU85",
    "Importacion-asistida-excel-operacion",
    "Importación asistida desde Excel de operación",
    "usuario con permiso de parametrización",
    "cargar un Excel de operación para sugerir catálogos (turnos, estados, sitios, campañas) y confirmar qué se crea",
    "acelerar el alta de un frente sin convertir el Excel en la base de datos del módulo",
    [
        ("Super-administrador", "No importa Excel de empresas cliente."),
        ("Administrador de empresa", "Puede importar si tiene permiso."),
        ("Usuario de la empresa", "Parametrizador."),
    ],
    [
        ("Inicia", "Usuario con permiso de parametrización"),
        ("Participa", "—"),
        ("No participa", "Empleado operativo"),
    ],
    [
        "MT-EP01-HU06 — Plantillas de turno",
        "MT-EP01-HU09 — Estados",
        "MT-EP01-HU13 — Sitios",
        "MT-EP01-HU10 — Campañas",
    ],
    [
        "Permiso de parametrización.",
        "Existe un frente destino (HU64).",
        "Prioridad Fase 3.",
    ],
    [
        ("Carga el archivo Excel.", "Analiza columnas y valores distintos."),
        ("Muestra sugerencias de catálogos a crear.", "El usuario revisa el mapeo."),
        ("Confirma un subconjunto.", "Solo ese subconjunto se crea en los catálogos."),
        ("Cancela.", "No se crea nada."),
    ],
    "El Excel sirve para descubrir configuración; la fuente operativa sigue siendo la malla y sus catálogos.",
    [
        "Columna no reconocida: se marca para mapeo manual.",
        "Valor ya existente en catálogo: se sugiere reutilizar, no duplicar.",
    ],
    [
        ("Archivo inválido o vacío.", "No procesa; mensaje claro."),
        ("Confirmación parcial con error en un ítem.", "Crea solo los válidos y reporta fallidos."),
        ("Usuario sin permiso.", "Acceso no permitido."),
    ],
    """Referencia: asistente de importación.

1. Carga de archivo
2. Vista de sugerencias
3. Confirmación por ítem
""",
    [
        "Nada se crea en catálogos sin confirmación del usuario autorizado.",
        "No se persiste el Excel como modelo operativo de la malla.",
        "Los datos creados pertenecen a la empresa del usuario.",
        "Se prioriza reutilizar catálogos existentes antes de duplicar.",
    ],
    [
        "El Excel es fuente de descubrimiento, no esquema de base de datos.",
        "Prioridad Fase 3.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Archivo Excel | Malla de turnos | Carga de archivo |
| Mapeo columna → catálogo | Malla de turnos | Asistente |
| Confirmación de altas | Malla de turnos | Casillas / confirmación |
""",
)

# ========== EP-02 ==========
doc(
    "Epica 02",
    "EP-02 — Construcción de la malla",
    "MT-EP02-HU81",
    "Control-concurrencia-edicion-celdas",
    "Controlar concurrencia en la edición de celdas",
    "usuario con permiso de construcción de malla",
    "que dos personas no sobrescriban en silencio la misma celda al editar al mismo tiempo",
    "proteger la integridad de la programación operativa",
    [
        ("Super-administrador", "No edita mallas de empresas cliente."),
        ("Administrador de empresa", "Puede editar si tiene permiso."),
        ("Usuario de la empresa", "Coordinadores que editan la grilla."),
    ],
    [
        ("Inicia", "Usuario que guarda una celda"),
        ("Participa", "Otro usuario que editó la misma celda"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP02-HU23 — Asignar turno o estado",
        "MT-EP05-HU48 — Historial inmutable",
    ],
    [
        "Existe una malla editable.",
        "Dos usuarios pueden tener permiso de edición sobre el mismo frente.",
    ],
    [
        ("Usuario A abre una celda y Usuario B abre la misma celda.", "Ambos ven el valor actual."),
        ("Usuario A guarda su cambio.", "La celda se actualiza y queda una versión nueva."),
        ("Usuario B intenta guardar con la versión anterior.", "El sistema rechaza por conflicto y pide recargar."),
        ("Usuario B recarga, revisa y vuelve a guardar si corresponde.", "Se aplica su cambio sobre la versión actual."),
    ],
    "No hay sobrescritura silenciosa entre ediciones concurrentes de la misma celda.",
    [
        "Conflicto en malla publicada: mismas reglas de versión; además aplican políticas de HU45.",
        "Usuario solo lectura: no llega a guardar.",
    ],
    [
        ("Versión obsoleta al guardar.", "Mensaje de conflicto; no pisa el cambio previo."),
        ("Fallo de red al guardar.", "No confirma éxito; el usuario puede reintentar."),
    ],
    """Referencia: mensaje de conflicto en celda/grilla.

1. Aviso de que otro usuario modificó la celda
2. Acción para recargar el valor actual
""",
    [
        "Guardar con versión desactualizada no sobrescribe el valor vigente.",
        "El usuario recibe un mensaje de conflicto comprensible.",
        "Tras un guardado exitoso, el historial de celda registra el cambio (HU48).",
        "Sin permiso de actualización no se puede guardar.",
    ],
    [
        "El control es por celda (bloqueo optimista / versión).",
        "No se exige bloquear toda la malla para editar una celda.",
    ],
    "Esta historia no agrega campos de negocio nuevos. El control ocurre al guardar la celda.",
)

doc(
    "Epica 02",
    "EP-02 — Construcción de la malla",
    "MT-EP02-HU82",
    "Carga-parcial-grilla-ventana-paginacion",
    "Cargar la grilla por ventana de fechas y páginas de personas",
    "usuario con permiso de construcción o consulta de malla",
    "ver solo el tramo de fechas y la página de personas que necesito",
    "operar mallas grandes sin esperar a cargar toda la programación de una vez",
    [
        ("Super-administrador", "No opera mallas de empresas cliente."),
        ("Administrador de empresa", "Puede consultar/construir según permiso."),
        ("Usuario de la empresa", "Coordinador, supervisora o analista con permiso."),
    ],
    [
        ("Inicia", "Usuario que abre la grilla"),
        ("Participa", "—"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP02-HU28 — Visualizar grilla",
        "MT-EP02-HU22 — Grupo de funcionarios",
        "MT-EP02-HU31 — Filtros de grilla",
    ],
    [
        "Existe una malla con varias personas y varios días.",
        "Permiso de lectura sobre la malla.",
    ],
    [
        ("Abre la malla.", "Carga una ventana de fechas y una página de personas por defecto."),
        ("Cambia el rango de fechas visible.", "Solicita solo esos días."),
        ("Pasa a la siguiente página de personas.", "Carga el siguiente bloque de filas."),
        ("Edita una celda de la ventana cargada.", "Guarda sin exigir recargar toda la malla."),
    ],
    "La grilla trabaja por ventanas y páginas; no obliga a traer toda la malla para operar.",
    [
        "Indicadores globales de cobertura pueden pedirse aparte (HU32).",
        "Filtros (HU31) se aplican sobre la consulta paginada.",
    ],
    [
        ("Rango de fechas inválido.", "No carga; pide corregir."),
        ("Timeout o error de carga.", "Mensaje claro; mantiene lo ya visible si aplica."),
    ],
    """Referencia: grilla con selector de fechas y paginación de filas.

1. Rango de fechas
2. Paginación o desplazamiento virtual de personas
3. Contador de personas totales vs visibles
""",
    [
        "Al abrir una malla grande no se exige descargar todas las personas y todos los días de una vez.",
        "El usuario puede pedir otra ventana de fechas u otra página de personas.",
        "Editar una celda de la ventana no requiere recargar la malla completa.",
        "Solo se muestran datos de la empresa y frentes del alcance del usuario.",
    ],
    [
        "La carga parcial es requisito de usabilidad y rendimiento.",
        "Los totales o indicadores pueden calcularse como consultas agregadas aparte.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Fecha desde / hasta | Malla de turnos | Selector de rango |
| Página de personas | Malla de turnos | Paginación |
""",
)

# ========== EP-03 ==========
doc(
    "Epica 03",
    "EP-03 — Cobertura y rotación híbrida",
    "MT-EP03-HU67",
    "Definir-patron-rotacion-generico",
    "Definir patrón de rotación genérico",
    "usuario con permiso de parametrización",
    "crear patrones como una secuencia ordenada de turnos o estados con duración de cada paso y un ciclo",
    "representar cualquier rotación (incluidos ejemplos de negocio) sin tipos fijos de patrón en el producto",
    [
        ("Super-administrador", "No define patrones de empresas cliente."),
        ("Administrador de empresa", "Puede crear patrones si tiene permiso."),
        ("Usuario de la empresa", "Parametrizador o coordinador con permiso."),
    ],
    [
        ("Inicia", "Usuario con permiso de parametrización"),
        ("Participa", "—"),
        ("No participa", "Empleado sin permiso de parametrización"),
    ],
    [
        "MT-EP01-HU06 — Plantillas de turno",
        "MT-EP01-HU09 — Estados",
        "MT-EP03-HU35 — Vincular patrón a grupo/periodo",
        "MT-EP03-HU74 — Simular patrón",
    ],
    [
        "Existen plantillas de turno o estados a usar en la secuencia.",
        "Permiso de parametrización.",
        "Prioridad Fase 2.",
    ],
    [
        ("Abre Parametrización → Patrones de rotación.", "Lista patrones de la empresa."),
        ("Crea un patrón y define la secuencia ordenada (turno/estado + días de duración).", "Calcula la longitud del ciclo como suma de duraciones."),
        ("Define vigencia, prioridad y si debe respetar restricciones de persona.", "Guarda el patrón."),
        ("Inactiva el patrón.", "Deja de ofrecerse para nuevas aplicaciones."),
    ],
    "Los patrones son datos configurables; no existen tipos especiales de rotación en el producto.",
    [
        "Secuencia de un solo paso: válida (patrón constante).",
        "Incluir estado de descanso en la secuencia: permitido.",
        "Ejemplos de negocio (15/15, mañana→tarde, 2×1) se modelan como instancias, no como tipos del sistema.",
    ],
    [
        ("Secuencia vacía o duración cero.", "No guarda."),
        ("Turno inexistente o inactivo.", "No guarda."),
        ("Usuario sin permiso.", "Acceso no permitido."),
    ],
    """Referencia: editor de patrón.

1. Nombre y vigencia
2. Lista ordenada de pasos (turno/estado + duración)
3. Opciones de respeto a restricciones
""",
    [
        "Un patrón es una secuencia de pasos con duración; el ciclo es la suma de esas duraciones.",
        "No existen tipos fijos de patrón en el producto.",
        "El patrón pertenece a la empresa y puede aplicarse a frentes autorizados.",
        "Un patrón inactivo no se ofrece para vincular o aplicar.",
        "Los ejemplos de operación se cargan solo como datos de configuración si se desea.",
    ],
    [
        "La rotación automática/asistida consume este modelo genérico.",
        "Prioridad Fase 2; el modelo queda listo desde el diseño.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Nombre del patrón | Malla de turnos | Formulario |
| Pasos (orden, turno/estado, duración) | Malla de turnos | Editor de secuencia |
| Respetar restricciones | Malla de turnos | Interruptor |
| Estado | Malla de turnos | Interruptor |
""",
)

doc(
    "Epica 03",
    "EP-03 — Cobertura y rotación híbrida",
    "MT-EP03-HU74",
    "Simular-patron-rotacion-dry-run",
    "Simular patrón de rotación antes de aplicar",
    "usuario con permiso de construcción de malla",
    "ejecutar una simulación del patrón que muestre la propuesta y los conflictos sin modificar la malla",
    "revisar el impacto antes de escribir la programación",
    [
        ("Super-administrador", "No simula mallas de empresas cliente."),
        ("Administrador de empresa", "Puede simular si tiene permiso."),
        ("Usuario de la empresa", "Coordinador con permiso de construcción."),
    ],
    [
        ("Inicia", "Usuario con permiso de construcción"),
        ("Participa", "—"),
        ("No participa", "Empleado sin permiso de construcción"),
    ],
    [
        "MT-EP03-HU35 — Vincular patrón",
        "MT-EP03-HU75 — Exclusiones",
        "MT-EP03-HU36 — Aplicar rotación",
        "MT-EP01-HU66 — Motor de reglas",
    ],
    [
        "Existe un vínculo de patrón a grupo/periodo (HU35).",
        "La estrategia del frente permite asistida o automática.",
        "Prioridad Fase 2.",
    ],
    [
        ("Ejecuta Simular.", "Calcula la propuesta sin guardar celdas."),
        ("Revisa el diff propuesto y la lista de conflictos.", "Muestra hallazgos del motor de reglas."),
        ("Ajusta exclusiones o parámetros y vuelve a simular.", "Actualiza la propuesta."),
        ("Decide no aplicar.", "La malla permanece igual."),
    ],
    "La simulación nunca escribe la malla; la aplicación es una historia aparte (HU36).",
    [
        "Personas excluidas (HU75): no aparecen como cambiadas en la propuesta.",
        "Configuración exige dry-run antes de aplicar: HU36 no permite aplicar sin simulación vigente.",
    ],
    [
        ("No hay vínculo de patrón.", "No permite simular."),
        ("Estrategia del frente es solo manual.", "Acción no disponible."),
        ("Error de cálculo.", "Mensaje claro; no modifica malla."),
    ],
    """Referencia: pantalla de simulación.

1. Resumen de celdas propuestas
2. Lista de conflictos
3. Acciones: volver a simular / aplicar (HU36) / descartar
""",
    [
        "La simulación no modifica celdas de la malla.",
        "Muestra propuesta y conflictos detectados.",
        "Respeta exclusiones de personas o celdas.",
        "Se puede repetir la simulación antes de aplicar.",
        "Solo opera sobre mallas de la empresa y frente del usuario.",
    ],
    [
        "Dry-run obligatorio cuando la configuración del frente o de la operación lo exija.",
        "Prioridad Fase 2.",
    ],
    "Esta historia no captura catálogos nuevos. Opera sobre el vínculo de patrón y la malla existente.",
)

doc(
    "Epica 03",
    "EP-03 — Cobertura y rotación híbrida",
    "MT-EP03-HU75",
    "Excluir-personas-celdas-rotacion",
    "Excluir personas o celdas de la rotación",
    "usuario con permiso de construcción de malla",
    "marcar personas o días concretos para que la rotación asistida o automática no los modifique",
    "proteger excepciones operativas durante el armado",
    [
        ("Super-administrador", "No opera exclusiones de empresas cliente."),
        ("Administrador de empresa", "Puede excluir si tiene permiso."),
        ("Usuario de la empresa", "Coordinador con permiso de construcción."),
    ],
    [
        ("Inicia", "Usuario con permiso de construcción"),
        ("Participa", "—"),
        ("No participa", "Empleado sin permiso"),
    ],
    [
        "MT-EP03-HU35 — Vincular patrón",
        "MT-EP03-HU74 — Simular",
        "MT-EP03-HU36 — Aplicar",
    ],
    [
        "Existe un vínculo de patrón o una simulación en curso.",
        "Prioridad Fase 2.",
    ],
    [
        ("Marca una persona como excluida.", "Queda fuera de la propuesta."),
        ("Marca una celda o rango de días.", "Esas celdas conservan su valor al aplicar."),
        ("Quita una exclusión.", "La persona o celda vuelve a participar."),
        ("Simula de nuevo.", "La propuesta respeta las exclusiones vigentes."),
    ],
    "Las exclusiones son explícitas, auditables y limitadas a la empresa del usuario.",
    [
        "Excluir a alguien ya rotado: no deshace lo aplicado; solo afecta nuevas simulaciones/aplicaciones.",
        "Exclusión fuera del grupo de la malla: no aplica.",
    ],
    [
        ("Excluir persona de otra malla/empresa.", "No permitido."),
        ("Usuario sin permiso.", "Acceso no permitido."),
    ],
    """Referencia: marcas de exclusión en grilla o panel de rotación.

1. Excluir persona
2. Excluir celda / rango
3. Listado de exclusiones activas
""",
    [
        "Las personas o celdas excluidas no se modifican al simular o aplicar la rotación.",
        "Se puede quitar una exclusión y volver a simular.",
        "Las exclusiones pertenecen a la empresa y a la malla/vínculo correspondientes.",
        "Queda registro de quién marcó o quitó una exclusión.",
    ],
    [
        "Las exclusiones no borran historial previo.",
        "Prioridad Fase 2.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Persona excluida | Malla de turnos | Selección en grilla |
| Celda o rango excluido | Malla de turnos | Selección en grilla |
| Motivo de exclusión (opcional) | Malla de turnos | Texto |
""",
)

# ========== EP-05 ==========
doc(
    "Epica 05",
    "EP-05 — Novedades, cambios y auditoría",
    "MT-EP05-HU83",
    "Ownership-mvp-novedades-estado-celda",
    "Definir el ownership MVP de novedades operativas",
    "administrador de empresa o usuario con permiso de parametrización",
    "operar las novedades (vacaciones, incapacidades u otras) como estados de celda del catálogo, con importación opcional de archivo",
    "evitar asumir un módulo de Talento Humano que hoy no existe en GRH y dejar clara la fuente operativa",
    [
        ("Super-administrador", "No define ownership de novedades de empresas cliente."),
        ("Administrador de empresa", "Alinea el criterio MVP en su empresa."),
        ("Usuario de la empresa", "Aplica estados de novedad en celdas (HU47) y cruza archivos en Fase 2 (HU62)."),
    ],
    [
        ("Inicia", "Administrador de empresa / parametrizador"),
        ("Participa", "Coordinadores que aplican estados; TH externo vía archivo en Fase 2"),
        ("No participa", "Super-administrador en el día a día"),
    ],
    [
        "MT-EP01-HU09 — Estados con flags",
        "MT-EP05-HU47 — Aplicar novedad a celda",
        "MT-EP08-HU84 — Plantilla de importación TH",
        "MT-EP08-HU62 — Cruzar con novedades TH",
    ],
    [
        "Existe catálogo de estados (HU09).",
        "Se acepta el default MVP: estado de celda + import opcional.",
    ],
    [
        ("Se documenta y configura que la fuente operativa MVP es el estado de la celda.", "Las pantallas de novedad usan el catálogo de estados."),
        ("Se aplica una novedad en celda (HU47).", "El comportamiento de horas y cobertura lo definen los flags del estado."),
        ("En Fase 2 se importa un archivo TH (HU84/HU62).", "El cruce propone o aplica estados; no inventa un módulo TH dentro de GRH."),
        ("Se consulta si GRH tiene vacaciones/incapacidades nativas.", "El producto no asume ese módulo hoy."),
    ],
    "Queda explícito que el MVP de novedades vive en la malla (estado de celda) con importación opcional.",
    [
        "Futuro conector TH: no debe borrar el historial de celda.",
        "Estados concretos (vacaciones, incapacidad, etc.) son ítems del catálogo, no historias aparte.",
    ],
    [
        ("Intentar configurar un módulo TH inexistente como obligatorio.", "No se ofrece; se usa estado de celda + import."),
    ],
    """No es una pantalla larga de usuario final.

1. Criterio visible en parametrización / ayuda del módulo
2. Flujo operativo: cambio de estado en celda (HU47)
3. Flujo Fase 2: importación y cruce (HU84/HU62)
""",
    [
        "En MVP, la novedad operativa se registra como estado de celda del catálogo.",
        "No se afirma que GRH tenga un módulo completo de vacaciones/incapacidades.",
        "La importación de archivo es opcional y complementaria (Fase 2).",
        "Los efectos de horas y cobertura dependen de los flags del estado (HU09), no de HUs por cada novedad.",
        "El historial de celda se conserva ante importaciones o futuros conectores.",
    ],
    [
        "HU50 queda absorbida por flags de HU09 + cálculo HU58.",
        "Decisión de negocio D1 queda cerrada por defecto: estado + import.",
    ],
    "Esta historia define criterio de ownership. Los campos de captura viven en HU47 y HU84.",
)

# ========== EP-08 ==========
doc(
    "Epica 08",
    "EP-08 — Reportes y horas para nómina",
    "MT-EP08-HU84",
    "Parametrizar-plantilla-importacion-novedades-th",
    "Parametrizar plantilla de importación de novedades de Talento Humano",
    "usuario con permiso de parametrización o reportes",
    "definir cómo se mapean las columnas de un archivo de novedades a personas y estados de la malla",
    "cruzar información externa sin dejar un formato único quemado en el producto",
    [
        ("Super-administrador", "No define plantillas de empresas cliente."),
        ("Administrador de empresa", "Puede definir la plantilla de su empresa."),
        ("Usuario de la empresa", "Parametrizador o rol de reportes/TH según permisos."),
    ],
    [
        ("Inicia", "Usuario con permiso de parametrización o reportes"),
        ("Participa", "—"),
        ("No participa", "Empleado sin ese permiso"),
    ],
    [
        "MT-EP05-HU83 — Ownership MVP novedades",
        "MT-EP01-HU09 — Estados",
        "MT-EP08-HU62 — Cruzar programación con novedades TH",
    ],
    [
        "Existe catálogo de estados.",
        "Prioridad Fase 2.",
    ],
    [
        ("Abre Parametrización → Plantilla de importación de novedades.", "Muestra mapeo actual de la empresa."),
        ("Define columnas obligatorias y el mapeo a documento/persona, fechas y estado.", "Guarda la plantilla."),
        ("Agrega una columna nueva al mapeo.", "Queda disponible sin cambiar el producto."),
        ("Ejecuta una prueba con archivo de ejemplo.", "Valida formato antes del cruce (HU62)."),
    ],
    "Cada empresa puede tener su plantilla de importación parametrizable.",
    [
        "Varias plantillas por empresa: si se habilita, se elige cuál usar al importar.",
        "Estado destino inexistente: el mapeo no se puede activar hasta corregirlo.",
    ],
    [
        ("Faltan columnas obligatorias en la plantilla.", "No activa."),
        ("Archivo de prueba inválido.", "Reporta errores de formato."),
        ("Usuario sin permiso.", "Acceso no permitido."),
    ],
    """Referencia: editor de plantilla de importación.

1. Columnas del archivo
2. Campos destino (persona, fechas, estado)
3. Obligatorio / opcional
4. Prueba de archivo
""",
    [
        "La plantilla pertenece a la empresa del usuario.",
        "El mapeo define cómo interpretar el archivo en el cruce HU62.",
        "Se pueden agregar columnas al mapeo sin redesplegar reglas fijas de formato.",
        "Un archivo que no cumple la plantilla se rechaza con errores claros.",
        "No se asume un único formato nacional fijo en el producto.",
    ],
    [
        "Prioridad Fase 2.",
        "Complementa el ownership MVP de HU83.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Nombre de plantilla | Malla de turnos | Formulario |
| Columna archivo | Malla de turnos | Mapeo |
| Campo destino | Malla de turnos | Selector |
| Obligatorio | Malla de turnos | Interruptor |
""",
)

# ========== EP-09 ==========
EP09 = "EP-09 — Intercambio de turnos"

doc(
    "Epica 09",
    EP09,
    "MT-EP09-HU76",
    "Configurar-solicitudes-intercambio",
    "Habilitar y configurar solicitudes de intercambio por frente",
    "usuario con permiso de parametrización",
    "activar o desactivar el intercambio de turnos por frente y definir anticipación, quién solicita, quién aprueba y límites",
    "ofrecer la capacidad solo donde la operación la necesite",
    [
        ("Super-administrador", "No configura intercambios de empresas cliente."),
        ("Administrador de empresa", "Puede configurar si tiene permiso."),
        ("Usuario de la empresa", "Parametrizador."),
    ],
    [
        ("Inicia", "Usuario con permiso de parametrización"),
        ("Participa", "—"),
        ("No participa", "Empleado solicitante (usa HU77 cuando esté habilitado)"),
    ],
    [
        "MT-EP01-HU65 — Configuración del frente",
        "MT-EP00-HU02 — Permisos de menú",
        "MT-EP09-HU77 — Solicitar intercambio",
    ],
    [
        "Existe el frente (HU64/HU65).",
        "Prioridad Fase 2.",
        "Default: deshabilitado.",
    ],
    [
        ("Abre la configuración de intercambio del frente.", "Muestra interruptor y parámetros."),
        ("Deja el intercambio deshabilitado.", "El empleado no ve la acción de solicitar."),
        ("Lo habilita y define anticipación, aprobadores y límites.", "Queda activo solo para ese frente."),
        ("Guarda.", "Las historias HU77–HU80 respetan la configuración."),
    ],
    "El intercambio es opcional por frente y nace apagado.",
    [
        "Cambiar de on a off: no borra solicitudes históricas; impide nuevas.",
        "Anticipación en días u horas según parámetro.",
    ],
    [
        ("Parámetros incompletos al habilitar.", "No guarda."),
        ("Usuario sin permiso.", "Acceso no permitido."),
    ],
    """Referencia: sección Intercambio en configuración del frente.

1. Interruptor habilitar
2. Anticipación mínima
3. Quién solicita / quién aprueba
4. Límite de solicitudes
""",
    [
        "Por defecto el intercambio está deshabilitado.",
        "Con intercambio off, el empleado no ve la acción de solicitar.",
        "Anticipación, límites y aprobadores son parámetros configurables.",
        "La configuración no cruza empresas.",
        "Los cambios de configuración quedan auditados.",
    ],
    [
        "No se asume que todos los frentes usan intercambio.",
        "Prioridad Fase 2.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Habilitado | Malla de turnos | Interruptor |
| Anticipación mínima | Malla de turnos | Numérico |
| Quién puede solicitar | Malla de turnos | Selector |
| Quién puede aprobar | Malla de turnos | Selector |
| Límite de solicitudes | Malla de turnos | Numérico |
""",
)

doc(
    "Epica 09",
    EP09,
    "MT-EP09-HU77",
    "Solicitar-intercambio-celda-turno",
    "Solicitar intercambio de celda o turno",
    "usuario de la empresa vinculado a un funcionario (empleado)",
    "iniciar una solicitud de intercambio eligiendo mi celda y un compañero candidato con su celda",
    "resolver cambios de turno dentro de la plataforma cuando el frente lo permita",
    [
        ("Super-administrador", "No solicita intercambios de empresas cliente."),
        ("Administrador de empresa", "No es el flujo típico; puede tener vista de administración."),
        ("Usuario de la empresa", "Empleado con intercambio habilitado en su frente."),
    ],
    [
        ("Inicia", "Empleado solicitante"),
        ("Participa", "Empleado candidato"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP09-HU76 — Configurar intercambio",
        "MT-EP07-HU56 — Mi programación",
        "MT-EP09-HU78 — Validar solicitud",
    ],
    [
        "El frente tiene intercambio habilitado.",
        "El empleado ve su programación publicada.",
        "Prioridad Fase 2.",
    ],
    [
        ("Desde Mi programación elige una celda propia.", "Ofrece solicitar intercambio si está habilitado."),
        ("Selecciona un compañero y su celda candidata.", "Muestra resumen de la solicitud."),
        ("Confirma el envío.", "La solicitud queda pendiente; la malla aún no cambia."),
        ("Consulta el estado de su solicitud.", "Ve pendiente / aprobada / rechazada."),
    ],
    "El empleado puede solicitar intercambio sin modificar la malla hasta la aprobación y aplicación.",
    [
        "Candidato de otra empresa: no aparece.",
        "Límite de solicitudes superado: no envía.",
        "Intercambio off: la acción no existe.",
    ],
    [
        ("Celda no elegible (borrador o fuera de reglas).", "No permite solicitar."),
        ("Validación de bloqueo al crear (HU78).", "No crea la solicitud y muestra motivos."),
        ("Usuario sin vínculo a empleado.", "No puede solicitar."),
    ],
    """Referencia: flujo desde Mi programación.

1. Selección de mi celda
2. Búsqueda de compañero / celda
3. Confirmación
4. Estado de solicitudes
""",
    [
        "Solo se puede solicitar si el frente tiene intercambio habilitado.",
        "Solicitante y candidato pertenecen a la misma empresa.",
        "Crear la solicitud no modifica la malla.",
        "Se respetan límites y elegibilidad configurados.",
        "El empleado ve el estado de sus solicitudes.",
    ],
    [
        "Prioridad Fase 2.",
        "La malla solo cambia en HU80 tras aprobación.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Mi celda | Malla de turnos | Selector |
| Compañero candidato | Malla de turnos | Buscador |
| Celda del compañero | Malla de turnos | Selector |
| Motivo (si aplica) | Malla de turnos | Texto |
""",
)

doc(
    "Epica 09",
    EP09,
    "MT-EP09-HU78",
    "Validar-solicitud-intercambio-reglas",
    "Validar solicitud de intercambio con el motor de reglas",
    "sistema al crear o aprobar una solicitud; usuario ve el resultado",
    "validar anticipación, solape, cobertura, horas y restricciones al solicitar o aprobar un intercambio",
    "evitar intercambios que rompan la operación",
    [
        ("Super-administrador", "No valida solicitudes de empresas cliente."),
        ("Administrador de empresa", "Puede ver hallazgos si tiene permiso de aprobación."),
        ("Usuario de la empresa", "Solicitante y aprobador ven mensajes de validación."),
    ],
    [
        ("Inicia", "Sistema en creación o aprobación"),
        ("Participa", "Solicitante / aprobador"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP01-HU66 — Motor de reglas",
        "MT-EP09-HU76 — Configuración de intercambio",
        "MT-EP09-HU77 — Solicitar",
        "MT-EP09-HU79 — Aprobar/rechazar",
    ],
    [
        "Existen reglas y configuración de intercambio.",
        "Prioridad Fase 2.",
    ],
    [
        ("Se crea una solicitud.", "El motor evalúa reglas de anticipación, solape, cobertura, horas y restricciones."),
        ("Hay un bloqueo.", "No se crea o no se aprueba; se informan motivos."),
        ("Hay advertencias.", "La solicitud puede quedar pendiente con advertencias visibles al aprobador."),
        ("Entre la creación y la aprobación cambió la malla.", "Se revalida al aprobar."),
    ],
    "Toda solicitud pasa por el mismo motor de reglas del módulo.",
    [
        "Solape real: siempre bloqueo.",
        "Regla de anticipación del frente: parámetro de HU76.",
    ],
    [
        ("Bloqueo al crear.", "No crea solicitud."),
        ("Bloqueo al aprobar por cambio de malla.", "No aprueba; informa motivos."),
    ],
    """Referencia: mensajes de validación en solicitud y bandeja de aprobación.

1. Lista de hallazgos con severidad
2. Enlace a celdas involucradas
""",
    [
        "La creación y la aprobación revalidan con el motor de reglas.",
        "El solape horario real bloquea siempre.",
        "Las advertencias quedan visibles para el aprobador.",
        "Si la malla cambió, una solicitud antes válida puede fallar al aprobar.",
        "La validación no cruza empresas.",
    ],
    [
        "Reutiliza HU66; no inventa un motor aparte para intercambios.",
        "Prioridad Fase 2.",
    ],
    "Esta historia no captura catálogos nuevos. Evalúa reglas existentes sobre la solicitud.",
)

doc(
    "Epica 09",
    EP09,
    "MT-EP09-HU79",
    "Aprobar-rechazar-solicitud-intercambio",
    "Aprobar o rechazar solicitud de intercambio",
    "usuario de la empresa autorizado a aprobar según la configuración del frente",
    "revisar solicitudes pendientes y aprobarlas o rechazarlas con motivo",
    "gobernar el cambio de turnos con responsabilidad clara",
    [
        ("Super-administrador", "No aprueba intercambios de empresas cliente."),
        ("Administrador de empresa", "Puede aprobar si su rol está configurado."),
        ("Usuario de la empresa", "Aprobador configurado (coordinador/supervisora u otro)."),
    ],
    [
        ("Inicia", "Usuario aprobador"),
        ("Participa", "Solicitante y candidato (reciben aviso)"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP09-HU76 — Configurar intercambio",
        "MT-EP09-HU78 — Validar solicitud",
        "MT-EP09-HU80 — Aplicar intercambio",
        "MT-EP00-HU71 — Event types de notificación",
    ],
    [
        "Existen solicitudes pendientes.",
        "El usuario está habilitado como aprobador.",
        "Prioridad Fase 2.",
    ],
    [
        ("Abre la bandeja de solicitudes.", "Lista pendientes de su alcance."),
        ("Revisa detalle, advertencias y celdas involucradas.", "Muestra validaciones vigentes."),
        ("Aprueba una solicitud válida.", "Pasa a aprobada (lista para aplicar en HU80) o se aplica según diseño acordado."),
        ("Rechaza con motivo.", "La malla no cambia; se notifica a los involucrados."),
    ],
    "Solo usuarios configurados aprueban o rechazan; el rechazo no altera la malla.",
    [
        "Solicitud ya no válida: no se aprueba.",
        "Usuario no aprobador: no ve acción de aprobar.",
        "Varios niveles de aprobación: solo si la configuración del frente lo define (mínimo un nivel).",
    ],
    [
        ("Rechazo sin motivo cuando es obligatorio.", "No permite rechazar."),
        ("Aprobar sin permiso.", "Acceso no permitido."),
        ("Revalidación con bloqueo.", "No aprueba; muestra motivos."),
    ],
    """Referencia: bandeja de aprobación.

1. Listado pendiente / resuelta
2. Detalle de solicitud
3. Acciones aprobar / rechazar
""",
    [
        "Solo el aprobador configurado puede resolver la solicitud.",
        "Rechazar exige motivo cuando la configuración lo indica y no cambia la malla.",
        "Aprobar revalida reglas antes de continuar.",
        "Se notifica el resultado a los afectados.",
        "El alcance es por empresa y frente.",
    ],
    [
        "Quién aprueba lo define la configuración, no un nombre de rol quemado en el producto.",
        "Prioridad Fase 2.",
    ],
    """| Campo | Sistema | Interfaz |
| ----- | ------- | -------- |
| Decisión (aprobar/rechazar) | Malla de turnos | Acciones |
| Motivo de rechazo | Malla de turnos | Texto |
""",
)

doc(
    "Epica 09",
    EP09,
    "MT-EP09-HU80",
    "Aplicar-intercambio-auditar-notificar",
    "Aplicar intercambio aprobado, auditar y notificar",
    "sistema tras la aprobación; usuario aprobador confirma si el diseño lo requiere",
    "aplicar el intercambio sobre las celdas, dejar historial con origen intercambio y avisar a los afectados",
    "cerrar el ciclo de forma trazable y segura",
    [
        ("Super-administrador", "No aplica intercambios de empresas cliente."),
        ("Administrador de empresa", "Puede operar si es aprobador."),
        ("Usuario de la empresa", "Aprobador; empleados reciben aviso."),
    ],
    [
        ("Inicia", "Sistema / aprobador según diseño"),
        ("Participa", "Empleados involucrados"),
        ("No participa", "Super-administrador"),
    ],
    [
        "MT-EP09-HU79 — Aprobar/rechazar",
        "MT-EP05-HU48 — Historial de celda",
        "MT-EP00-HU71 — Notificaciones",
        "MT-EP02-HU81 — Concurrencia",
    ],
    [
        "Solicitud aprobada y vigente.",
        "Prioridad Fase 2.",
    ],
    [
        ("Se aplica el intercambio.", "Las dos celdas intercambian los atributos configurados de forma conjunta."),
        ("Se registra historial en ambas celdas con origen intercambio y referencia a la solicitud.", "Eventos inmutables (HU48)."),
        ("Se notifica a los empleados involucrados.", "Aviso informativo; sin aceptación adicional."),
        ("Si hay conflicto de versión en una celda.", "No aplica nada (todo o nada) y reporta el error."),
    ],
    "El intercambio aprobado queda aplicado, auditado y notificado sin aceptación extra del empleado.",
    [
        "Reintento de una solicitud ya aplicada: no vuelve a intercambiar.",
        "Malla ya no editable según políticas: no aplica.",
    ],
    [
        ("Conflicto de concurrencia.", "Rollback; malla intacta; mensaje claro."),
        ("Solicitud no aprobada.", "No aplica."),
        ("Fallo de notificación.", "El cambio puede quedar aplicado; el aviso se reintenta sin duplicar."),
    ],
    """Referencia: resultado en grilla + avisos.

1. Celdas actualizadas
2. Historial con origen intercambio
3. Campana / correo a involucrados
""",
    [
        "La aplicación es conjunta: ambas celdas o ninguna.",
        "El historial referencia la solicitud y el origen intercambio.",
        "Se notifica a los afectados sin pedir aceptación del turno.",
        "Un reintento de la misma solicitud aplicada no duplica el cambio.",
        "Respeta empresa, frente y control de concurrencia.",
    ],
    [
        "Origen del cambio = intercambio.",
        "Prioridad Fase 2.",
    ],
    "Esta historia no captura un formulario largo. Aplica el resultado de una solicitud ya aprobada.",
)

print("\nDone. New GST-FM-04 files created.")
