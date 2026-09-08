# -*- coding: utf-8 -*-
from pathlib import Path

OUT = Path(__file__).resolve().parent

def hu(id_, title, priority, como, quiero, para, cubre, no_cubre, reglas, cas, deps_hu, deps_ms, tech=None):
    lines = [
        f"## {id_} — {title}", "",
        f"**Prioridad:** {priority}", "**Estado:** Definitiva", "",
        "### Historia", "",
        f"**Como:** {como}", "", f"**Quiero:** {quiero}", "", f"**Para:** {para}", "",
        "### Alcance", "", "**Cubre**", "",
    ]
    for x in cubre: lines.append(f"- {x}")
    lines += ["", "**No cubre**", ""]
    for x in (no_cubre or ["—"]): lines.append(f"- {x}")
    lines += ["", "### Reglas de negocio", ""]
    for i, r in enumerate(reglas, 1): lines.append(f"{i}. {r}")
    lines += ["", "### Criterios de aceptación", ""]
    for i, (name, d, c, e) in enumerate(cas, 1):
        lines += [f"**CA{i:02d} — {name}**", "", f"Dado que {d}", "", f"Cuando {c}", "", f"Entonces {e}", ""]
    lines += ["### Dependencias", "", f"- HUs: {deps_hu}", f"- Microservicios / GRH: {deps_ms}", ""]
    if tech: lines += ["### Consideraciones técnicas", "", tech, ""]
    lines += ["---", ""]
    return "\n".join(lines)

def add(lst, *a, **k): lst.append(hu(*a, **k))

def write_epic(code, name, hus, path):
    idx = [f"# {code} — {name}", "", "## Índice", ""]
    for h in hus:
        idx.append("- " + h.split("\n", 1)[0].replace("## ", ""))
    idx += ["", "---", ""]
    path.write_text("\n".join(idx) + "\n".join(hus), encoding="utf-8")
    print("Wrote", path.name, len(hus))

AP = "Usuario de la empresa con permiso de parametrización"
AC = "Usuario de la empresa con permiso de construcción de malla"
APUB = "Usuario de la empresa con permiso de publicación según configuración del frente"
AE = "Usuario de la empresa vinculado a un funcionario"
AM = "Usuario de la empresa con permiso de consulta operativa"
AR = "Usuario de la empresa con permiso de reportes"

ep03 = []
add(ep03, "MT-EP03-HU32", "Visualizar indicadores de cobertura y contadores", "MVP", AC,
    "ver indicadores de cobertura y contadores calculados según las reglas y plantillas del frente",
    "detectar faltantes o excesos sin fórmulas fijas por operación",
    ["Contadores por dimensiones habilitadas", "Actualización al cambiar celdas de la ventana"],
    ["Definir reglas de cobertura (HU19)"],
    ["Los contadores se derivan de reglas HU19 y turnos/estados del catálogo, no de fórmulas Excel de un frente.",
     "Personas con estado que no afecta cobertura no cuentan."],
    [("Vista", "existen reglas de cobertura", "abre indicadores", "muestra min/max/actual por dimensión configurada"),
     ("Recalc", "cambia una celda relevante", "guarda", "actualiza indicadores afectados"),
     ("Capacidad", "dimensión no habilitada", "abre indicadores", "no muestra esa dimensión"),
     ("Tenant", "consulta", "datos", "solo su empresa")],
    "MT-EP01-HU19, MT-EP02-HU28", "Malla", None)

add(ep03, "MT-EP03-HU33", "Visualizar equilibrio de turnos por persona", "Fase 2", AC,
    "ver distribución de plantillas/estados por persona en el periodo según métricas configurables",
    "apoyar decisiones de equidad sin umbrales quemados",
    ["Métricas de distribución configurables"],
    ["Forzar equilibrio automático"],
    ["Los umbrales de desequilibrio son reglas parametrizables (advertencia/bloqueo).",
     "No existe una métrica única hardcodeada por frente."],
    [("Vista", "malla con asignaciones", "abre equilibrio", "lista métricas por persona"),
     ("Regla", "se supera umbral configurado", "evalúa", "marca hallazgo con severidad"),
     ("Permisos", "LEER", "consulta", "permitido"),
     ("Tenant", "datos", "aislados", "OK")],
    "MT-EP01-HU66, MT-EP02-HU28", "Malla", None)

add(ep03, "MT-EP03-HU34", "Evaluar y mostrar conflictos de validación en grilla", "MVP", AC,
    "ejecutar el motor de reglas y mostrar hallazgos en la grilla y un panel de conflictos",
    "corregir problemas antes de publicar",
    ["Listado de hallazgos", "Navegación a celda", "Filtro por severidad"],
    ["Administrar reglas (HU66)", "Usar constantes numéricas de negocio en UI"],
    ["Los mensajes muestran el nombre de la regla y sus parámetros, no constantes de producto.",
     "Bloqueos impiden publicar si la config de publicación exige cero bloqueos."],
    [("Eval", "hay violaciones", "ejecuta validación", "lista hallazgos con severidad"),
     ("Navegar", "selecciona un hallazgo", "hace clic", "enfoca la celda"),
     ("Filtro", "filtra solo bloqueos", "aplica", "oculta info/advertencias"),
     ("Sin hardcode", "regla max_hours_period=N", "muestra mensaje", "incluye N desde la regla"),
     ("Tenant", "validación", "solo malla propia", "OK")],
    "MT-EP01-HU66, MT-EP02-HU28", "Malla", None)

add(ep03, "MT-EP03-HU67", "Definir patrón de rotación genérico", "Fase 2", AP,
    "crear patrones como secuencia ordenada de elementos (turno/estado), cada uno con duración, formando un ciclo",
    "representar cualquier rotación (incluidos ejemplos 15/15 o 2×1) sin tipos enum de patrón",
    ["CRUD patrón", "Secuencia + duraciones + ciclo", "Fecha inicio de anclaje", "Respeto opcional de restricciones"],
    ["Enums FIFTEEN_FIFTEEN / TWO_ONE", "Aplicar a malla (HU36)"],
    ["Un patrón es solo datos: secuencia, duraciones, ciclo, prioridad, vigencia.",
     "No existen tipos de patrón de producto.",
     "Ejemplos de negocio son seeds o instancias."],
    [("Alta", "define secuencia de plantillas con duraciones", "guarda", "patrón reutilizable en la empresa"),
     ("Ciclo", "secuencia completa", "se consulta longitud de ciclo", "es la suma de duraciones"),
     ("Sin enum", "lista tipos de patrón del sistema", "consulta", "no hay tipos especiales; solo patrones creados"),
     ("Tenant", "patrón ajeno", "invisible", "OK"),
     ("Inactivo", "patrón inactivo", "aplicar", "no ofrecido")],
    "MT-EP01-HU06, MT-EP01-HU09", "Malla", None)

add(ep03, "MT-EP03-HU35", "Vincular patrón de rotación a grupo y periodo", "Fase 2", AC,
    "asociar un patrón a una malla o subconjunto de personas y un rango de fechas",
    "preparar la simulación/aplicación controlada",
    ["Vínculo patrón↔malla/grupo/fechas"],
    ["Aplicar sin simular"],
    ["Solo si la estrategia del frente es asistida o automática.",
     "El vínculo no modifica celdas hasta aplicar (HU36) tras simulación (HU74)."],
    [("Vínculo", "patrón activo y estrategia permite", "asocia a grupo/fechas", "queda listo para simular"),
     ("Estrategia manual", "frente manual", "intenta vincular auto", "acción no disponible"),
     ("Alcance", "personas fuera de malla", "asocia", "rechaza"),
     ("Tenant", "patrón otra empresa", "rechaza", "OK")],
    "MT-EP03-HU67, MT-EP01-HU65, MT-EP02-HU22", "Malla", None)

add(ep03, "MT-EP03-HU74", "Simular patrón de rotación antes de aplicar", "Fase 2", AC,
    "ejecutar un dry-run del patrón que muestre asignaciones propuestas y conflictos sin alterar la malla",
    "revisar el impacto antes de escribir",
    ["Resultado simulado", "Lista de conflictos", "Diff propuesto"],
    ["Persistir simulación como malla real sin confirmación"],
    ["La simulación no escribe celdas.",
     "Debe mostrar qué sería automático y qué queda excluido (HU75)."],
    [("Dry-run", "vínculo válido", "simula", "muestra propuesta sin cambiar malla"),
     ("Conflictos", "hay violaciones", "simula", "lista conflictos detectados"),
     ("Exclusiones", "personas excluidas", "simula", "no propone cambios para ellas"),
     ("Reintentar", "ajusta parámetros", "vuelve a simular", "actualiza propuesta"),
     ("Permisos", "sin ACTUALIZAR", "simula si LEER+política lo permite o niega escritura posterior", "según permisos")],
    "MT-EP03-HU35, MT-EP03-HU75, MT-EP01-HU66", "Malla", None)

add(ep03, "MT-EP03-HU75", "Excluir personas o celdas de la rotación", "Fase 2", AC,
    "marcar personas o celdas concretas para que la rotación asistida/automática no las modifique",
    "proteger excepciones operativas",
    ["Exclusiones por persona, rango o celda"],
    [],
    ["Las exclusiones son tenant-scoped y auditables.",
     "Celdas excluidas conservan su valor actual al aplicar."],
    [("Excluir persona", "grupo vinculado", "marca exclusión", "simulación no la altera"),
     ("Excluir celda", "día específico", "excluye", "propuesta la omite"),
     ("Quitar exclusión", "había exclusión", "quita", "vuelve a participar"),
     ("Tenant", "exclusión", "propia empresa", "OK")],
    "MT-EP03-HU35", "Malla", None)

add(ep03, "MT-EP03-HU36", "Aplicar resultado de rotación a la malla", "Fase 2", AC,
    "aplicar la propuesta simulada aceptada, marcando origen automático y dejando historial",
    "materializar la rotación de forma trazable",
    ["Aplicación atómica o por lote con reporte", "Origen=automático", "Historial"],
    ["Aplicar sin simulación previa si la config exige dry-run"],
    ["Toda celda escrita por rotación registra origen automático.",
     "Ajustes posteriores manuales cambian origen a manual (HU42).",
     "Se revalidan reglas; bloqueos impiden aplicar esas celdas."],
    [("Aplicar", "simulación aceptada sin bloqueos críticos", "aplica", "celdas actualizadas con origen automático"),
     ("Parcial", "algunas celdas bloqueadas", "aplica", "omite bloqueadas y reporta"),
     ("Historial", "celda cambia", "consulta historial", "antes/después + origen automático"),
     ("Sin simulación", "config exige dry-run", "aplica directo", "rechaza"),
     ("Notificación", "si flags de estado/config lo requieren", "aplica", "despacha eventos HU71")],
    "MT-EP03-HU74, MT-EP05-HU48, MT-EP00-HU71", "Malla; notification", None)

add(ep03, "MT-EP03-HU37", "Construcción asistida de asignaciones", "Fase 2", AC,
    "obtener sugerencias de asignación según la estrategia asistida del frente y aceptarlas o modificarlas",
    "acelerar el armado sin perder control humano",
    ["Sugerencias de turnos/cobertura/descansos/sitios según config", "Aceptar/rechazar por celda o lote"],
    ["Estrategia automática plena sin revisión"],
    ["Solo si estrategia=asistida (o automática con paso de revisión).",
     "Sugerir ≠ aplicar; aplicar genera origen asistido/automático."],
    [("Sugerir", "estrategia asistida", "solicita sugerencias", "recibe propuesta"),
     ("Aceptar", "selecciona subconjunto", "acepta", "escribe celdas elegidas"),
     ("Modificar", "ajusta una sugerencia", "guarda", "origen manual o asistido según diseño"),
     ("Estrategia", "manual", "sugerir", "no disponible")],
    "MT-EP01-HU65, MT-EP01-HU66, MT-EP03-HU67", "Malla", None)

add(ep03, "MT-EP03-HU38", "Distribuir breaks y almuerzos según plantillas y reglas", "Fase 2", AC,
    "proponer o aplicar distribución de pausas cuando el frente y las plantillas lo definen",
    "evitar solapes de pausas que rompan cobertura si hay reglas",
    ["Distribución asistida de pausas"],
    ["Pausas hardcodeadas por frente"],
    ["Depende de HU08 y reglas de cobertura en franja de pausa."],
    [("Distribuir", "plantillas con pausas y capacidad on", "ejecuta", "propone horarios de pausa"),
     ("Conflicto cobertura", "regla de cobertura en pausa", "evalúa", "hallazgo con severidad"),
     ("Off", "sin pausas en plantillas", "acción", "no aplica"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU08, MT-EP01-HU19, MT-EP03-HU37", "Malla", None)

add(ep03, "MT-EP03-HU39", "Rotar sitios de asistencia según configuración", "Fase 2", AC,
    "aplicar un patrón o política de rotación de sitios cuando la capacidad está habilitada",
    "alternar ubicaciones sin reglas fijas por nombre de sitio",
    ["Rotación de sitios parametrizable"],
    [],
    ["Sitios son catálogo; la secuencia es configuración."],
    [("Aplicar", "capacidad sitio on y patrón de sitios", "simula/aplica", "asigna sitios según secuencia"),
     ("Exclusión", "persona excluida", "aplica", "no cambia sitio"),
     ("Off", "capacidad off", "acción ausente", "OK"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU13, MT-EP03-HU67, MT-EP03-HU74", "Malla", None)

add(ep03, "MT-EP03-HU40", "Reequilibrar cargas tras una novedad", "Fase 2", AC,
    "obtener sugerencias de reasignación cuando una novedad deja huecos de cobertura",
    "recuperar cobertura sin rearmar toda la malla a ciegas",
    ["Sugerencias post-novedad"],
    ["Borrar historial de la novedad"],
    ["Se dispara tras HU47 según estrategia del frente.",
     "No hardcodea tipos de novedad."],
    [("Hueco", "estado no afecta cobertura deja min incumplido", "solicita reequilibrio", "sugiere candidatos"),
     ("Aceptar", "elige sugerencia", "aplica", "historial con origen asistido"),
     ("Estrategia", "manual sin asistida", "reequilibrio auto", "no disponible o solo aviso"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP05-HU47, MT-EP03-HU37, MT-EP01-HU19", "Malla", None)

add(ep03, "MT-EP03-HU41", "Aplicar restricciones y motor de reglas al rotar o asignar", "MVP", AC,
    "que toda asignación manual, asistida o automática pase por restricciones de persona y reglas del frente",
    "impedir propuestas inválidas",
    ["Integración restricciones HU14 + motor HU66 en todos los flujos de escritura"],
    [],
    ["Bloqueo de restricción impide propuesta/guardado.",
     "Advertencia requiere confirmación cuando la UI lo permita."],
    [("Bloqueo", "restricción vigente incompatible", "asigna o simula", "no propone/guarda ese turno"),
     ("Rotación", "patrón caería en turno prohibido", "simula", "marca conflicto o excluye"),
     ("Manual", "mismo control", "guarda celda", "idéntica evaluación"),
     ("Tenant", "restricción ajena", "no aplica", "OK")],
    "MT-EP01-HU14, MT-EP01-HU66, MT-EP02-HU23, MT-EP03-HU74", "Malla", None)

add(ep03, "MT-EP03-HU42", "Ajustar manualmente tras rotación o sugerencia", "MVP", AC,
    "modificar celdas después de una aplicación automática/asistida, dejando trazabilidad de origen manual",
    "permitir excepciones humanas controladas",
    ["Edición post-aplicación", "Cambio de origen a manual", "Historial"],
    [],
    ["El ajuste manual revalida reglas.",
     "Si la malla está publicada, aplican políticas HU45."],
    [("Ajuste", "celda origen automático", "cambia turno", "origen pasa a manual y hay historial"),
     ("Regla", "ajuste inválido", "guarda", "aplica severidad"),
     ("Publicada", "editabilidad off", "intenta", "niega o exige flujo HU45"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP03-HU36, MT-EP02-HU23, MT-EP05-HU48, MT-EP04-HU45", "Malla", None)

ep04 = []
add(ep04, "MT-EP04-HU43", "Ciclo de vida de publicación de la malla", "MVP", APUB,
    "mover la malla entre borrador, en revisión, publicada y rechazada según la configuración del frente",
    "controlar cuándo la programación es oficial",
    ["Transiciones de estado", "Validación previa", "Publicar con advertencias si el flag lo permite", "Notificación de publicación"],
    ["Versionado completo de malla (no requerido)", "Aceptación del empleado"],
    ["Estados: Borrador, En revisión (si aplica), Publicada, Rechazada.",
     "Si constructor/publicador está separado (HU65), el constructor solo envía a revisión.",
     "No se publica con bloqueos; advertencias requieren confirmación solo si el frente lo permite.",
     "HU46 absorbida aquí + HU65."],
    [("Publicar", "borrador sin bloqueos y usuario publicador", "publica", "estado=Publicada y se notifica según HU71"),
     ("Revisión", "separación activa", "constructor envía", "pasa a En revisión"),
     ("Advertencias", "flag permite y hay advertencias", "confirma", "publica registrando aceptación de advertencias"),
     ("Bloqueos", "hay bloqueos", "publica", "rechaza"),
     ("Permisos", "no publicador", "publica", "niega"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU65, MT-EP03-HU34, MT-EP00-HU71, MT-EP05-HU49", "Malla; notification", None)

add(ep04, "MT-EP04-HU44", "Rechazar malla en revisión", "MVP", APUB,
    "rechazar una malla en revisión con motivo y devolverla a borrador",
    "permitir correcciones antes de publicar",
    ["Rechazo con motivo", "Vuelta a borrador", "Notificación al constructor si aplica"],
    [],
    ["Solo desde En revisión.", "Motivo obligatorio."],
    [("Rechazo", "malla en revisión", "rechaza con motivo", "queda borrador y motivo visible"),
     ("Sin motivo", "rechaza vacío", "valida", "bloquea"),
     ("Estado inválido", "ya publicada", "rechaza", "niega"),
     ("Permisos", "no autorizado", "niega", "OK")],
    "MT-EP04-HU43", "Malla; notification", None)

add(ep04, "MT-EP04-HU45", "Editar malla publicada", "MVP", AC,
    "modificar celdas de una malla publicada cuando la configuración lo permite, con motivo e historial",
    "atender cambios reales sin perder trazabilidad",
    ["Edición post-publicación gobernada", "Motivo según config", "Historial + notificación"],
    ["Crear nueva versión completa de malla"],
    ["Si editabilidad post-publicación = no, solo novedades vía flujo permitido o nada.",
     "Cada cambio deja historial inmutable.",
     "Estado puede marcarse como modificada después de publicar a nivel de celda/malla según diseño."],
    [("Edición permitida", "flag on", "cambia celda con motivo", "persiste, historial y notifica si corresponde"),
     ("Flag off", "no editable", "intenta", "niega"),
     ("Motivo", "config exige motivo", "guarda sin motivo", "bloquea"),
     ("Concurrencia", "versión vieja", "guarda", "conflicto HU81"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU65, MT-EP05-HU48, MT-EP05-HU49, MT-EP02-HU81", "Malla; notification", None)

ep05 = []
add(ep05, "MT-EP05-HU47", "Aplicar estado de novedad operativa a la celda", "MVP", AC,
    "cambiar el estado de una celda a un estado de novedad del catálogo (vacaciones, incapacidad u otros ítems)",
    "reflejar la disponibilidad real sin inventar un módulo TH inexistente",
    ["Cambio de estado a ítems del catálogo HU09", "Motivo/soporte según flags", "Recálculo cobertura/horas"],
    ["Módulo completo de vacaciones GRH", "HUs por cada tipo de novedad"],
    ["Ownership MVP: la novedad operativa vive como estado de celda (HU83).",
     "No existen estados especiales en código; solo flags.",
     "HU50 absorbida: si el estado no cuenta horas, HU58 no las suma."],
    [("Aplicar", "estado novedad del catálogo", "asigna a celda", "flags determinan cobertura/horas/notificación"),
     ("Motivo", "requiere motivo", "sin motivo", "bloquea/advierte"),
     ("Publicada", "políticas HU45", "aplica", "historial + posible notificación"),
     ("Sin hardcode", "cualquier código de estado", "mismo flujo", "OK"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU09, MT-EP05-HU83, MT-EP04-HU45, MT-EP05-HU48", "Malla", None)

add(ep05, "MT-EP05-HU83", "Definir ownership MVP de novedades", "MVP", AP,
    "operar novedades como estado de celda con importación opcional, dejando explícito que no hay módulo TH en GRH hoy",
    "evitar dobles fuentes de verdad no gobernadas",
    ["Política MVP documentada e implementada", "Importación opcional (HU84/HU62)", "Extensibilidad a conector futuro"],
    ["Afirmar que GRH ya tiene vacaciones/incapacidades"],
    ["Fuente operativa MVP = estado de celda.",
     "Archivo TH es complemento de cruce, no reemplaza el catálogo de estados.",
     "Futuro conector TH no debe romper historial de celda."],
    [("MVP", "se aplica novedad", "persiste", "como estado de celda"),
     ("Import", "existe archivo", "importa", "propone/aplica estados según mapeo"),
     ("Sin módulo TH", "documentación/producto", "consulta capacidades GRH", "no asume módulo TH"),
     ("Tenant", "import", "empresa del usuario", "OK")],
    "MT-EP01-HU09, MT-EP08-HU84", "Malla", "Decisión D1 cerrada por defecto: estado + import.")

add(ep05, "MT-EP05-HU48", "Historial inmutable de celda", "MVP", AC,
    "registrar de forma append-only cada cambio de celda con antes, después, usuario, fecha, motivo y origen",
    "auditar la operación sin versionar toda la malla",
    ["Historial por celda", "Orígenes: manual, automático, asistido, novedad, intercambio, import"],
    ["Borrado de historial", "Duplicar timeline GRH con el mismo detalle"],
    ["El historial de dominio es la fuente del detalle de celda.",
     "Timeline GRH guarda hechos de alto nivel (HU71).",
     "Inmutable: no update/delete de eventos de historial."],
    [("Registro", "cambia celda", "guarda OK", "existe evento con antes/después/usuario/origen"),
     ("Inmutable", "intenta borrar historial", "acción", "no existe o se niega"),
     ("Origen intercambio", "cambio por HU80", "historial", "referencia solicitud"),
     ("Consulta", "usuario autorizado", "abre historial celda", "lista cronológica"),
     ("Tenant", "historial ajeno", "invisible", "OK")],
    "MT-EP02-HU23, MT-EP00-HU71", "Malla; audit timeline (alto nivel)", None)

add(ep05, "MT-EP05-HU49", "Notificar cambio relevante al empleado", "MVP", AE,
    "recibir notificación informativa cuando cambia su programación publicada según flags y event types",
    "enterarse del cambio sin tener que aceptar en la plataforma",
    ["Despacho notification-service", "Popup/email según event type", "Sin aceptación"],
    ["Workflow de aceptación del empleado", "Mailer propio"],
    ["Si el estado/config indica notifica=sí y la malla está en alcance de notificación, se despacha.",
     "Idempotencia por clave de evento."],
    [("Cambio", "celda publicada cambia y notifica=sí", "guarda", "empleado recibe notificación"),
     ("Sin aceptación", "recibe aviso", "abre app", "no se le pide aceptar el turno"),
     ("No notifica", "flag notifica=no", "cambia", "no despacha a empleado"),
     ("Falla canal", "email falla", "reintento idempotente", "no duplica popup si ya entregado según diseño del MS"),
     ("Tenant", "destinatario", "misma empresa", "OK")],
    "MT-EP00-HU71, MT-EP01-HU09, MT-EP04-HU45", "notification-service", None)

add(ep05, "MT-EP05-HU51", "Consultar historial de cambios por funcionario", "MVP", AC,
    "ver el historial de cambios de celdas de un funcionario en un rango de fechas",
    "investigar novedades y ajustes",
    ["Consulta por persona + rango", "Detalle de eventos HU48"],
    [],
    ["Respeta alcance de frente y permisos LEER."],
    [("Consulta", "persona de la empresa", "filtra fechas", "lista cambios"),
     ("Vacío", "sin cambios", "consulta", "estado vacío claro"),
     ("Permisos", "sin LEER", "niega", "OK"),
     ("Tenant", "persona otra empresa", "niega", "OK")],
    "MT-EP05-HU48", "Malla", None)

ep06 = []
add(ep06, "MT-EP06-HU52", "Buscar quién está en turno o disponible", "MVP", AM,
    "consultar qué personas están en turno o disponibles en una fecha/franja según filtros del frente",
    "atender operación en tiempo real",
    ["Búsqueda por fecha/franja/filtros habilitados", "Excluye estados no disponibles según flags"],
    ["Hardcodear estado Actividad", "Edición de malla"],
    ["HU54 absorbida: la no asignabilidad a casos es un flag del estado.",
     "Solo muestra frentes de su alcance."],
    [("Búsqueda", "hay personas en turno en la franja", "consulta", "lista resultados"),
     ("Flag", "estado no disponible/no asignable", "consulta disponibilidad operativa", "no las incluye"),
     ("Filtros", "capacidades off", "UI", "no muestra filtros fantasma"),
     ("Tenant/alcance", "OK", "OK", "OK")],
    "MT-EP01-HU09, MT-EP00-HU70", "Malla", None)

add(ep06, "MT-EP06-HU53", "Consultar cobertura del día por dimensiones habilitadas", "MVP", AM,
    "ver cobertura del día agrupada por las dimensiones activas del frente",
    "verificar dotación operativa",
    ["Vista de cobertura del día", "Comparación vs min/max"],
    [],
    ["Dimensiones dinámicas según HU65/HU19."],
    [("Vista", "día con reglas", "abre cobertura", "muestra actual vs min/max"),
     ("Dimensión", "territorio off", "vista", "sin agrupación territorio"),
     ("Permisos", "LEER consulta", "OK", "OK"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU19, MT-EP03-HU32", "Malla", None)

ep07 = []
add(ep07, "MT-EP07-HU55", "Ver programación del grupo", "MVP", AE,
    "consultar la programación publicada del grupo según la política de visibilidad del frente",
    "conocer turnos del equipo",
    ["Vista de grupo", "Solo lectura"],
    ["Editar malla ajena"],
    ["Default: visible dentro del grupo del frente (D3).",
     "Si config restringe a solo-propia, no ve compañeros."],
    [("Grupo visible", "política pública en grupo", "abre", "ve compañeros del grupo"),
     ("Restringida", "política solo propia", "abre", "solo su fila"),
     ("Borrador", "malla no publicada", "consulta empleado", "no ve borradores ajenos"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP04-HU43, MT-EP01-HU65", "Malla", None)

add(ep07, "MT-EP07-HU56", "Ver mi programación", "MVP", AE,
    "ver mi programación en vistas de día, semana y mes",
    "organizar mi trabajo",
    ["Vistas temporales", "Turnos/estados/atributos visibles permitidos", "Solo lectura salvo intercambio si está on"],
    [],
    ["No edita celdas salvo iniciar solicitud EP-09 si está habilitado."],
    [("Día/semana/mes", "tiene celdas publicadas", "cambia vista", "ve su información"),
     ("Atributos", "frente sin campaña", "vista", "no muestra campaña"),
     ("Borrador", "solo borrador", "consulta", "no lo ve como oficial"),
     ("Permisos", "usuario sin vínculo empleado", "abre", "mensaje claro")],
    "MT-EP04-HU43", "Malla; employee vínculo userId", None)

add(ep07, "MT-EP07-HU57", "Ver historial de mis turnos y cambios recientes", "MVP", AE,
    "consultar el historial de mis turnos y cambios recientes que me afectaron",
    "entender modificaciones de mi programación",
    ["Historial propio", "Cambios recientes"],
    ["Historial de otros empleados"],
    ["Solo sus eventos; inmutable."],
    [("Historial", "hubo cambios", "abre", "lista antes/después relevantes"),
     ("Recientes", "filtro recientes", "aplica", "acota ventana"),
     ("Privacidad", "otro empleado", "intenta", "niega"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP05-HU48", "Malla", None)

ep08 = []
add(ep08, "MT-EP08-HU58", "Calcular horas del periodo por tipos configurados", "MVP", AR,
    "calcular horas del periodo clasificadas por tipos de hora y afectadas por flags de estado",
    "entregar información de horas a nómina sin liquidar dinero",
    ["Cálculo por persona/periodo/corte", "Clasificación HU17", "Respeto flags HU09"],
    ["Cálculo de pesos", "Constante 42h"],
    ["Los topes de horas son reglas HU66, no constantes.",
     "Salida = cantidades de hora por tipo, nunca montos."],
    [("Cálculo", "malla con turnos", "ejecuta", "obtiene horas por tipo"),
     ("Estado no suma", "flag off", "calcula", "excluye esas celdas del tipo afectado"),
     ("Festivo", "día festivo y regla festiva", "clasifica", "según HU17"),
     ("Sin dinero", "salida", "inspecciona", "sin campos monetarios"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU17, MT-EP01-HU09, MT-EP01-HU16, MT-EP01-HU15", "Malla", None)

add(ep08, "MT-EP08-HU59", "Exportar malla a Excel o PDF", "MVP", AR,
    "exportar la malla (ventana o periodo) a Excel y/o PDF según capacidad",
    "compartir la programación fuera de la grilla",
    ["Export Excel/PDF", "Respeta alcance y tenant"],
    ["Export = fuente de verdad editable que reimporta sin control"],
    ["Export incluye solo atributos habilitados.",
     "No incluye datos de otras empresas."],
    [("Excel", "malla publicada o autorizada", "exporta", "archivo con filas/columnas coherentes"),
     ("PDF", "capacidad PDF on", "exporta", "documento legible"),
     ("Alcance", "usuario frente A", "exporta", "solo A"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP02-HU28", "Malla", None)

add(ep08, "MT-EP08-HU60", "Reportar horas de novedad versus operativas", "Fase 2", AR,
    "distinguir horas asociadas a estados de novedad frente a horas operativas según flags",
    "analizar no disponibilidad vs operación",
    ["Desglose por flags de estado"],
    [],
    ["No asume lista fija de novedades; usa flags del catálogo."],
    [("Desglose", "hay estados novedad y operativos", "reporte", "separa totales"),
     ("Flag", "estado marca no operativa", "clasifica", "va a novedad"),
     ("Permisos", "reportes", "OK", "OK"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP08-HU58, MT-EP01-HU09", "Malla", None)

add(ep08, "MT-EP08-HU61", "Exportar cobertura para terceros", "Fase 2", AR,
    "generar exportación de cobertura consumible por terceros sin obligar altas de usuario GRH",
    "compartir dotación con proveedores o clientes internos",
    ["Export específico de cobertura", "Entrega archivo/link controlado"],
    ["Crear usuarios GRH para cada tercero como único medio"],
    ["La habilitación y formato son configuración.",
     "Sigue siendo tenant-scoped."],
    [("Export", "capacidad on", "genera", "archivo de cobertura del alcance"),
     ("Sin usuario tercero", "no existe usuario GRH del tercero", "un autorizado genera el archivo", "el tercero consume el archivo sin usuario GRH obligatorio"),
     ("Permisos", "solo roles autorizados", "OK", "OK"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP06-HU53, MT-EP01-HU65", "Malla", None)

add(ep08, "MT-EP08-HU84", "Parametrizar plantilla de importación de novedades TH", "Fase 2", AP,
    "definir el mapeo de columnas de un archivo de novedades TH a estados y personas",
    "cruzar información externa sin rigidizar un formato único en código",
    ["Plantilla de importación por empresa", "Mapeo columnas→campos", "Validación"],
    ["Asumir formato fijo nacional"],
    ["Plantilla parametrizable; seeds de ejemplo opcionales."],
    [("Mapeo", "define columnas", "guarda plantilla", "queda activa para la empresa"),
     ("Validación", "archivo sin columna obligatoria", "importa", "rechaza con error claro"),
     ("Tenant", "plantilla", "propia", "OK"),
     ("Extensible", "nueva columna", "se agrega al mapeo", "sin deploy de regla fija")],
    "MT-EP05-HU83, MT-EP01-HU09", "Malla", None)

add(ep08, "MT-EP08-HU62", "Cruzar programación con novedades TH importadas", "Fase 2", AR,
    "cruzar la malla con un archivo de novedades importado según la plantilla y producir diferencias",
    "detectar inconsistencias entre operación y TH",
    ["Import + cruce + reporte de diferencias", "Opción de aplicar estados con confirmación"],
    ["Sobrescribir silenciosa masiva"],
    ["Cruce no borra historial.",
     "Aplicar cambios exige permiso y deja origen=import."],
    [("Cruce", "archivo válido y malla", "ejecuta", "lista coincidencias/diferencias"),
     ("Aplicar", "confirma diferencias", "aplica", "celdas actualizadas + historial"),
     ("Error formato", "archivo inválido", "rechaza", "sin cambios"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP08-HU84, MT-EP05-HU47, MT-EP05-HU48", "Malla", None)

add(ep08, "MT-EP08-HU63", "Aplicar reglas de compensatorio en reporte", "Fase 2", AR,
    "evaluar las reglas de compensatorio configuradas y mostrar sugerencias o marcas en el reporte de horas",
    "soportar políticas distintas sin umbrales fijos en código",
    ["Evaluación HU18 sobre periodo", "Salida en reporte"],
    ["Regla fija de tres domingos"],
    ["Umbrales y tipos de día salen de HU18."],
    [("Eval", "regla activa cumplida", "reporte", "marca/sugiere según acción"),
     ("No cumple", "umbral no alcanzado", "sin marca", "OK"),
     ("Por frente", "reglas distintas", "cada frente", "su resultado"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU18, MT-EP08-HU58", "Malla", None)

ep09 = []
add(ep09, "MT-EP09-HU76", "Habilitar y configurar solicitudes de intercambio", "Fase 2", AP,
    "activar o desactivar solicitudes de intercambio por empresa/frente y definir anticipación, quién solicita, quién aprueba, límites y notificaciones",
    "gobernar el intercambio sin imponerlo a todos los frentes",
    ["Config on/off", "Anticipación mínima", "Roles/permisos lógicos de solicitud y aprobación", "Límites de cantidad", "Motivos"],
    ["Flujo de solicitud en sí (HU77+)"],
    ["Default: deshabilitado.",
     "Toda regla numérica es parámetro.",
     "No cruza empresas."],
    [("Off", "deshabilitado", "empleado ve su malla", "sin acción de intercambio"),
     ("On", "habilitado", "aparece acción", "según quién puede solicitar"),
     ("Anticipación", "parámetro N días", "solicitud fuera de N", "rechazada por regla"),
     ("Auditoría config", "cambia config", "historial config", "OK"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU65, MT-EP00-HU02", "Malla", None)

add(ep09, "MT-EP09-HU77", "Solicitar intercambio de celda o turno", "Fase 2", AE,
    "iniciar una solicitud de intercambio eligiendo mi celda y un compañero candidato con su celda",
    "resolver cambios de turno dentro de la plataforma",
    ["Creación de solicitud pendiente", "Selección de contraparte misma empresa/frente según config"],
    ["Autoaprobar"],
    ["Solo si HU76 enabled.",
     "Ambos empleados misma empresa; frente según config.",
     "No modifica malla hasta aprobación+aplicación."],
    [("Solicitud", "intercambio on y celdas elegibles", "envía", "queda pendiente"),
     ("Misma empresa", "candidato otra empresa", "selección", "imposible"),
     ("Off", "config off", "acción", "ausente"),
     ("Límite", "supera cantidad configurada", "envía", "rechaza"),
     ("Permisos", "no habilitado a solicitar", "niega", "OK")],
    "MT-EP09-HU76, MT-EP07-HU56", "Malla", None)

add(ep09, "MT-EP09-HU78", "Validar solicitud con motor de reglas", "Fase 2", AE,
    "que el sistema valide anticipación, solape, cobertura, horas, restricciones y demás reglas al crear o aprobar",
    "evitar intercambios que rompan la operación",
    ["Validación en creación y en aprobación"],
    [],
    ["Solape real = bloqueo.",
     "Resto según HU66 + config HU76."],
    [("Creación inválida", "viola bloqueo", "crea", "rechaza con motivos"),
     ("Advertencia", "severidad advertencia", "crea", "queda pendiente con warnings visibles al aprobador"),
     ("Revalidar", "entre creación y aprobación cambió malla", "aprueba", "revalida y puede fallar"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP01-HU66, MT-EP09-HU77", "Malla", None)

add(ep09, "MT-EP09-HU79", "Aprobar o rechazar solicitud de intercambio", "Fase 2", AC,
    "aprobar o rechazar solicitudes pendientes según la configuración de aprobadores",
    "gobernar el cambio con responsabilidad clara",
    ["Bandeja de solicitudes", "Aprobar/rechazar con motivo", "N niveles si config lo define (mínimo 1)"],
    ["Aplicar sin pasar por este paso"],
    ["Quién aprueba lo define HU76 + permisos, no un rol quemado.",
     "Rechazo no cambia malla."],
    [("Aprobar", "solicitud válida y usuario aprobador", "aprueba", "pasa a aprobada pendiente de aplicación o aplica según diseño"),
     ("Rechazar", "con motivo", "rechaza", "malla intacta + notificación"),
     ("No aprobador", "usuario sin permiso", "intenta", "niega"),
     ("Revalidación", "ya no es válida", "aprueba", "falla con motivos"),
     ("Tenant", "OK", "OK", "OK")],
    "MT-EP09-HU76, MT-EP09-HU78, MT-EP00-HU71", "Malla; notification", None)

add(ep09, "MT-EP09-HU80", "Aplicar intercambio, auditar y notificar", "Fase 2", AC,
    "aplicar el intercambio aprobado sobre las celdas, registrar historial con origen intercambio y notificar a afectados",
    "cerrar el ciclo de forma trazable",
    ["Swap atómico de atributos configurados", "Historial", "Notificaciones", "Idempotencia"],
    [],
    ["Aplicación atómica: ambas celdas o ninguna.",
     "Historial referencia id de solicitud.",
     "Origen=intercambio."],
    [("Aplicar", "aprobada y válida", "aplica", "celdas intercambiadas"),
     ("Historial", "consulta", "ambas celdas", "eventos con solicitud"),
     ("Notificar", "ambos empleados", "reciben aviso", "sin aceptación adicional"),
     ("Falla parcial", "segunda celda conflicto versión", "rollback", "nada aplicado + error"),
     ("Idempotencia", "reintenta misma solicitud aplicada", "no duplica swap", "OK")],
    "MT-EP09-HU79, MT-EP05-HU48, MT-EP00-HU71, MT-EP02-HU81", "Malla; notification", None)

write_epic("EP-03", "Validación, cobertura y rotación", ep03, OUT / "EP-03-Validacion-Rotacion.md")
write_epic("EP-04", "Publicación", ep04, OUT / "EP-04-Publicacion.md")
write_epic("EP-05", "Novedades, historial y notificaciones", ep05, OUT / "EP-05-Novedades-Historial.md")
write_epic("EP-06", "Consulta operativa", ep06, OUT / "EP-06-Consulta-Operativa.md")
write_epic("EP-07", "Vista del empleado", ep07, OUT / "EP-07-Vista-Empleado.md")
write_epic("EP-08", "Reportes y horas", ep08, OUT / "EP-08-Reportes-Horas.md")
write_epic("EP-09", "Intercambio de turnos", ep09, OUT / "EP-09-Intercambio.md")
print("OK part2")
