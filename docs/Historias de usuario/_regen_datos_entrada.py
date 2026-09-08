"""Regenera la sección Datos de entrada (formato oficial GST-FM-04) en todas las HU .md."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

HEADER = (
    "| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |\n"
    "| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |\n"
)

NO_CAPTURE = (
    "Esta historia no captura datos propios de formulario. "
    "El alcance y la empresa provienen del contexto autenticado."
)


def R(
    campo: str,
    longitud: str,
    tipo: str,
    obligatorio: str,
    sistema: str,
    interfaz: str,
    desc: str,
) -> tuple[str, ...]:
    return (campo, longitud, tipo, obligatorio, sistema, interfaz, desc)


def table(rows: list[tuple[str, ...]]) -> str:
    lines = [HEADER.rstrip()]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def catalog_base(entity: str) -> list[tuple[str, ...]]:
    return [
        R("Código", "20", "Alfanumérico", "SI", "NO", "SI", f"Identificador único del {entity} en la empresa"),
        R("Nombre", "120", "Alfanumérico", "SI", "NO", "SI", f"Nombre visible del {entity}"),
        R("Descripción", "N/A", "Texto", "NO", "NO", "SI", "Texto de ayuda o detalle"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si está disponible para uso"),
    ]


def period_filters() -> list[tuple[str, ...]]:
    return [
        R("Fecha desde", "10", "Fecha", "SI", "NO", "SI", "Inicio del periodo a consultar"),
        R("Fecha hasta", "10", "Fecha", "SI", "NO", "SI", "Fin del periodo a consultar"),
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente autorizado del usuario"),
    ]


# --- Definiciones por HU (MT-EPxx-HUyy) ---

FIELDS: dict[str, list[tuple[str, ...]] | None] = {
    # EP-00
    "MT-EP00-HU01": [
        R("Nombre del módulo", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre en catálogo de plataforma (Malla de Turnos)"),
        R("Descripción del módulo", "N/A", "Texto", "NO", "NO", "SI", "Descripción del módulo en catálogo"),
        R("Icono del módulo", "80", "Alfanumérico", "NO", "NO", "SI", "Clase de icono visible en menú"),
        R("Nombre del submódulo / sección", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre de la sección de menú"),
        R("Descripción del submódulo", "N/A", "Texto", "NO", "NO", "SI", "Ayuda o tooltip de la sección"),
        R("Icono del submódulo", "80", "Alfanumérico", "NO", "NO", "SI", "Clase de icono de la sección"),
        R("Ruta de la sección", "200", "Alfanumérico", "SI", "NO", "SI", "Ruta de navegación asociada a la sección"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si el ítem está activo en catálogo"),
        R("Plan de servicio", "N/A", "Selección", "SI", "SI", "SI", "Plan al que se asocia el módulo"),
    ],
    "MT-EP00-HU02": [
        R("Rol", "N/A", "Selección", "SI", "SI", "SI", "Rol de la empresa al que se asignan permisos"),
        R("Sección de menú", "N/A", "Selección", "SI", "SI", "SI", "Sección de Malla de Turnos"),
        R("Permiso crear", "1", "Booleano", "SI", "NO", "SI", "Habilita crear en la sección"),
        R("Permiso leer", "1", "Booleano", "SI", "NO", "SI", "Habilita consultar en la sección"),
        R("Permiso actualizar", "1", "Booleano", "SI", "NO", "SI", "Habilita actualizar en la sección"),
        R("Permiso eliminar", "1", "Booleano", "SI", "NO", "SI", "Habilita eliminar en la sección"),
    ],
    "MT-EP00-HU03": [
        R("Usuario o rol", "N/A", "Selección", "SI", "SI", "SI", "Destinatario del alcance de frentes"),
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente incluido en el alcance"),
        R("Incluir en alcance", "1", "Booleano", "SI", "NO", "SI", "Asocia o retira el frente del alcance"),
    ],
    "MT-EP00-HU04": None,
    "MT-EP00-HU05": None,
    "MT-EP00-HU06": None,
    "MT-EP00-HU07": [
        R("Código de evento de notificación", "40", "Alfanumérico", "SI", "NO", "SI", "Identificador del tipo de evento"),
        R("Nombre del evento", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre visible del evento"),
        R("Descripción del evento", "N/A", "Texto", "NO", "NO", "SI", "Detalle del evento de notificación"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si el evento está habilitado"),
    ],
    "MT-EP00-HU08": [
        R("Área organizacional", "N/A", "Selección", "NO", "SI", "SI", "Filtro de empleados por área"),
        R("Texto de búsqueda", "120", "Alfanumérico", "NO", "NO", "SI", "Nombre o documento a buscar"),
        R("Solo activos", "1", "Booleano", "NO", "NO", "SI", "Limita el listado a empleados activos"),
    ],
    # EP-01
    "MT-EP01-HU09": catalog_base("frente operativo"),
    "MT-EP01-HU10": [
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente a configurar"),
        R("Periodo de planificación por defecto", "20", "Selección", "SI", "NO", "SI", "Semana, mes u otro valor del catálogo"),
        R("Estrategia de armado", "20", "Selección", "SI", "NO", "SI", "Ninguna, manual, asistida o automática"),
        R("Separar constructor y publicador", "1", "Booleano", "SI", "NO", "SI", "Exige roles distintos en el ciclo de publicación"),
        R("Editable tras publicación", "1", "Booleano", "SI", "NO", "SI", "Permite editar malla publicada"),
        R("Solicitudes de intercambio habilitadas", "1", "Booleano", "SI", "NO", "SI", "Activa EP-09 en el frente"),
        R("Áreas vinculadas", "N/A", "Selección", "NO", "SI", "SI", "Áreas GRH asociadas al frente"),
        R("Capacidad / atributo", "40", "Selección", "SI", "NO", "SI", "Capacidad del frente a habilitar o deshabilitar"),
        R("Capacidad habilitada", "1", "Booleano", "SI", "NO", "SI", "Estado de la capacidad seleccionada"),
    ],
    "MT-EP01-HU11": [
        *catalog_base("plantilla de turno")[:3],
        R("Hora inicio", "8", "Hora", "SI", "NO", "SI", "Hora de inicio del turno"),
        R("Hora fin", "8", "Hora", "SI", "NO", "SI", "Hora de fin del turno"),
        R("Cruza medianoche", "1", "Booleano", "SI", "NO", "SI", "Indica si el turno pasa de un día a otro"),
        R("Color", "7", "Color", "NO", "NO", "SI", "Color de visualización (ej. #RRGGBB)"),
        R("Frentes aplicables", "N/A", "Selección", "SI", "SI", "SI", "Frentes donde aplica la plantilla"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si la plantilla está disponible"),
    ],
    "MT-EP01-HU12": [
        R("Plantilla de turno", "N/A", "Selección", "SI", "SI", "SI", "Plantilla a la que aplica el horario"),
        R("Día de la semana", "1", "Selección", "SI", "NO", "SI", "Día (0–6) con horario distinto"),
        R("Hora inicio", "8", "Hora", "SI", "NO", "SI", "Inicio para ese día"),
        R("Hora fin", "8", "Hora", "SI", "NO", "SI", "Fin para ese día"),
        R("Cruza medianoche", "1", "Booleano", "SI", "NO", "SI", "Indica cruce de medianoche ese día"),
    ],
    "MT-EP01-HU13": [
        R("Plantilla de turno", "N/A", "Selección", "SI", "SI", "SI", "Plantilla asociada a la pausa"),
        R("Tipo de pausa", "40", "Selección", "SI", "NO", "SI", "Break, almuerzo u otro tipo del catálogo"),
        R("Duración (minutos)", "5", "Número", "SI", "NO", "SI", "Duración de la pausa"),
        R("Remunerada", "1", "Booleano", "SI", "NO", "SI", "Indica si la pausa es remunerada"),
        R("Hora inicio sugerida", "8", "Hora", "NO", "NO", "SI", "Inicio orientativo de la pausa"),
    ],
    "MT-EP01-HU14": [
        *catalog_base("estado de celda")[:3],
        R("Color", "7", "Color", "NO", "NO", "SI", "Color de visualización del estado"),
        R("Cuenta horas", "1", "Booleano", "SI", "NO", "SI", "El estado aporta horas al cálculo"),
        R("Afecta cobertura", "1", "Booleano", "SI", "NO", "SI", "Impacta indicadores de cobertura"),
        R("Asignable a casos", "1", "Booleano", "SI", "NO", "SI", "Persona disponible para asignación"),
        R("Requiere motivo", "1", "Booleano", "SI", "NO", "SI", "Obliga a registrar motivo al aplicar"),
        R("Permite turno", "1", "Booleano", "SI", "NO", "SI", "Permite coexistir con plantilla de turno"),
        R("Permite ubicación", "1", "Booleano", "SI", "NO", "SI", "Permite sitio/modalidad en la celda"),
        R("Notifica empleado", "1", "Booleano", "SI", "NO", "SI", "Dispara notificación al aplicar"),
        R("Requiere soporte", "1", "Booleano", "SI", "NO", "SI", "Marca necesidad de cobertura de soporte"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si el estado está disponible"),
    ],
    "MT-EP01-HU15": [
        *catalog_base("campaña o tarea")[:3],
        R("Color", "7", "Color", "NO", "NO", "SI", "Color de visualización"),
        R("Vigencia desde", "10", "Fecha", "NO", "NO", "SI", "Inicio de vigencia"),
        R("Vigencia hasta", "10", "Fecha", "NO", "NO", "SI", "Fin de vigencia"),
        R("Frentes aplicables", "N/A", "Selección", "SI", "SI", "SI", "Frentes donde aplica"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si está disponible"),
    ],
    "MT-EP01-HU16": [
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente dueño de la estructura territorial"),
        R("Nombre del nivel", "80", "Alfanumérico", "SI", "NO", "SI", "Nombre configurable del nivel (ej. Zona)"),
        R("Orden del nivel", "3", "Número", "SI", "NO", "SI", "Posición jerárquica del nivel"),
        R("Código del nodo", "20", "Alfanumérico", "SI", "NO", "SI", "Código del nodo territorial"),
        R("Nombre del nodo", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre del nodo territorial"),
        R("Nodo padre", "N/A", "Selección", "NO", "SI", "SI", "Padre en la jerarquía; vacío si es raíz"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si el nodo/nivel está activo"),
    ],
    "MT-EP01-HU17": catalog_base("modalidad de trabajo"),
    "MT-EP01-HU18": [
        *catalog_base("sitio de asistencia"),
        R("Frentes aplicables", "N/A", "Selección", "SI", "SI", "SI", "Frentes donde aplica el sitio"),
    ],
    "MT-EP01-HU19": [
        R("Código del tipo de restricción", "40", "Alfanumérico", "SI", "NO", "SI", "Identificador del tipo"),
        R("Nombre del tipo", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre visible"),
        R("Funcionario", "N/A", "Selección", "SI", "SI", "SI", "Persona a la que aplica la restricción"),
        R("Tipo de restricción", "N/A", "Selección", "SI", "SI", "SI", "Tipo parametrizado"),
        R("Fecha desde", "10", "Fecha", "SI", "NO", "SI", "Inicio de la restricción"),
        R("Fecha hasta", "10", "Fecha", "NO", "NO", "SI", "Fin de la restricción"),
        R("Observación", "N/A", "Texto", "NO", "NO", "SI", "Detalle de la restricción"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si la restricción está vigente"),
    ],
    "MT-EP01-HU20": [
        R("Año", "4", "Número", "SI", "NO", "SI", "Año del calendario de festivos a consultar"),
        R("Fecha festivo", "10", "Fecha", "N/A", "SI", "SI", "Fecha aportada por el calendario de empresa"),
        R("Nombre festivo", "120", "Alfanumérico", "N/A", "SI", "SI", "Nombre del festivo consultado"),
    ],
    "MT-EP01-HU21": [
        R("Código", "20", "Alfanumérico", "SI", "NO", "SI", "Identificador del corte de nómina"),
        R("Nombre", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre del corte"),
        R("Día de corte", "2", "Número", "SI", "NO", "SI", "Día del mes o regla de corte"),
        R("Periodicidad", "20", "Selección", "SI", "NO", "SI", "Mensual, quincenal u otra"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si el corte está activo"),
    ],
    "MT-EP01-HU22": [
        R("Código tipo de hora", "40", "Alfanumérico", "SI", "NO", "SI", "Identificador del tipo de hora"),
        R("Nombre", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre del tipo de hora"),
        R("Orden", "3", "Número", "NO", "NO", "SI", "Orden de presentación"),
        R("Regla de clasificación", "N/A", "Texto", "NO", "NO", "SI", "Criterio de clasificación del tipo"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si el tipo está disponible"),
    ],
    "MT-EP01-HU23": [
        R("Código regla", "40", "Alfanumérico", "SI", "NO", "SI", "Identificador de la regla de compensatorio"),
        R("Nombre", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre de la regla"),
        R("Umbral / parámetro", "40", "Alfanumérico", "SI", "NO", "SI", "Valor configurable de la regla"),
        R("Unidad", "40", "Selección", "SI", "NO", "SI", "Horas, días u otra unidad"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si la regla está activa"),
    ],
    "MT-EP01-HU24": [
        R("Código regla", "40", "Alfanumérico", "SI", "NO", "SI", "Identificador de la regla de cobertura"),
        R("Nombre", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre de la regla"),
        R("Frente operativo", "N/A", "Selección", "NO", "SI", "SI", "Alcance por frente; vacío = empresa"),
        R("Dimensión", "40", "Selección", "SI", "NO", "SI", "Dimensión de cobertura (turno, sitio, etc.)"),
        R("Mínimo requerido", "5", "Número", "SI", "NO", "SI", "Cantidad mínima a cubrir"),
        R("Severidad", "20", "Selección", "SI", "NO", "SI", "Info, advertencia o bloqueo"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si la regla está activa"),
    ],
    "MT-EP01-HU25": [
        R("Código regla", "40", "Alfanumérico", "SI", "NO", "SI", "Identificador de la regla de validación"),
        R("Nombre", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre de la regla"),
        R("Alcance", "20", "Selección", "SI", "NO", "SI", "Empresa o frente"),
        R("Frente operativo", "N/A", "Selección", "NO", "SI", "SI", "Obligatorio si el alcance es frente"),
        R("Valor del parámetro", "40", "Alfanumérico", "NO", "NO", "SI", "Parámetro editable (ej. máximo de horas)"),
        R("Unidad del parámetro", "40", "Selección", "NO", "NO", "SI", "Unidad del parámetro"),
        R("Severidad", "20", "Selección", "SI", "NO", "SI", "Info, advertencia o bloqueo"),
        R("Prioridad", "5", "Número", "NO", "NO", "SI", "Orden de evaluación"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si la regla está activa"),
    ],
    "MT-EP01-HU26": [
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente a configurar"),
        R("Atributo de celda", "40", "Selección", "SI", "NO", "SI", "Territorio, campaña, modalidad, sitio, etc."),
        R("Habilitado", "1", "Booleano", "SI", "NO", "SI", "Muestra el atributo en la grilla del frente"),
        R("Obligatorio al asignar", "1", "Booleano", "NO", "NO", "SI", "Exige el atributo al guardar la celda"),
    ],
    "MT-EP01-HU27": [
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente destino de la importación"),
        R("Archivo Excel", "N/A", "Archivo", "SI", "NO", "SI", "Archivo de operación a importar"),
        R("Hoja / mapeo de columnas", "N/A", "Selección", "SI", "NO", "SI", "Correspondencia de columnas del archivo"),
        R("Confirmar importación", "1", "Booleano", "SI", "NO", "SI", "Confirmación tras la validación previa"),
    ],
    # EP-02
    "MT-EP02-HU28": [
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente de la malla"),
        R("Fecha inicio del periodo", "10", "Fecha", "SI", "NO", "SI", "Inicio del periodo de la malla"),
        R("Fecha fin del periodo", "10", "Fecha", "SI", "NO", "SI", "Fin del periodo de la malla"),
        R("Modo de armado", "20", "Selección", "SI", "SI", "SI", "Según estrategia configurada del frente"),
        R("Nombre o etiqueta", "120", "Alfanumérico", "NO", "NO", "SI", "Referencia opcional de la malla"),
    ],
    "MT-EP02-HU29": [
        R("Malla", "N/A", "Selección", "SI", "SI", "SI", "Malla en construcción"),
        R("Área / filtro de empleados", "N/A", "Selección", "NO", "SI", "SI", "Filtro para ubicar funcionarios"),
        R("Funcionarios", "N/A", "Selección", "SI", "SI", "SI", "Personas incluidas en la malla"),
        R("Orden de presentación", "5", "Número", "NO", "NO", "SI", "Orden de filas en la grilla"),
    ],
    "MT-EP02-HU30": [
        R("Celda (persona y fecha)", "N/A", "Selección", "SI", "SI", "SI", "Celda de la grilla a editar"),
        R("Plantilla de turno", "N/A", "Selección", "NO", "SI", "SI", "Turno a asignar (alternativa a estado)"),
        R("Estado de celda", "N/A", "Selección", "NO", "SI", "SI", "Estado a asignar (alternativa a turno)"),
        R("Motivo", "N/A", "Texto", "NO", "NO", "SI", "Obligatorio si el estado lo exige"),
    ],
    "MT-EP02-HU31": [
        R("Celda (persona y fecha)", "N/A", "Selección", "SI", "SI", "SI", "Día donde se agrega el segundo turno"),
        R("Slot / turno adicional", "2", "Número", "SI", "NO", "SI", "Número de slot (>0) del turno extra"),
        R("Plantilla de turno", "N/A", "Selección", "SI", "SI", "SI", "Turno del slot adicional"),
    ],
    "MT-EP02-HU32": [
        R("Celda (persona y fecha)", "N/A", "Selección", "SI", "SI", "SI", "Celda a actualizar"),
        R("Nodo territorial", "N/A", "Selección", "SI", "SI", "SI", "Territorio asignado a la celda"),
    ],
    "MT-EP02-HU33": [
        R("Celda (persona y fecha)", "N/A", "Selección", "SI", "SI", "SI", "Celda a actualizar"),
        R("Modalidad de trabajo", "N/A", "Selección", "NO", "SI", "SI", "Modalidad de la celda"),
        R("Sitio de asistencia", "N/A", "Selección", "NO", "SI", "SI", "Sitio de la celda"),
    ],
    "MT-EP02-HU34": [
        R("Celda (persona y fecha)", "N/A", "Selección", "SI", "SI", "SI", "Celda a anotar"),
        R("Observación", "N/A", "Texto", "SI", "NO", "SI", "Nota libre de la celda"),
    ],
    "MT-EP02-HU35": period_filters()
    + [
        R("Vista temporal", "20", "Selección", "NO", "NO", "SI", "Día, semana o mes"),
    ],
    "MT-EP02-HU36": [
        R("Celda (persona y fecha)", "N/A", "Selección", "SI", "SI", "SI", "Celda a actualizar"),
        R("Campaña o tarea", "N/A", "Selección", "SI", "SI", "SI", "Campaña/tarea asignada"),
    ],
    "MT-EP02-HU37": [
        R("Celda origen", "N/A", "Selección", "SI", "SI", "SI", "Recurso/persona a cubrir"),
        R("Frente o área de cobertura", "N/A", "Selección", "SI", "SI", "SI", "Origen del recurso de otro frente/área"),
        R("Fecha", "10", "Fecha", "SI", "NO", "SI", "Día de la cobertura cruzada"),
        R("Turno o estado", "N/A", "Selección", "SI", "SI", "SI", "Asignación del día de cobertura"),
    ],
    "MT-EP02-HU38": [
        R("Texto de búsqueda", "120", "Alfanumérico", "NO", "NO", "SI", "Nombre u otro criterio de búsqueda"),
        R("Filtro por turno", "N/A", "Selección", "NO", "SI", "SI", "Filtra celdas por plantilla"),
        R("Filtro por estado", "N/A", "Selección", "NO", "SI", "SI", "Filtra celdas por estado"),
        R("Filtro por atributo habilitado", "N/A", "Selección", "NO", "SI", "SI", "Sitio, modalidad, territorio, campaña, etc."),
    ],
    "MT-EP02-HU39": None,
    "MT-EP02-HU40": [
        R("Ventana desde", "10", "Fecha", "SI", "NO", "SI", "Inicio de la ventana temporal cargada"),
        R("Ventana hasta", "10", "Fecha", "SI", "NO", "SI", "Fin de la ventana temporal cargada"),
        R("Página de personas", "5", "Número", "SI", "NO", "SI", "Página del listado de filas"),
        R("Tamaño de página", "5", "Número", "SI", "NO", "SI", "Cantidad de personas por página"),
    ],
    "MT-EP02-HU41": [
        R("Malla destino", "N/A", "Selección", "SI", "SI", "SI", "Malla donde se aplica la copia"),
        R("Semana / rango origen", "N/A", "Selección", "SI", "NO", "SI", "Periodo origen a copiar"),
        R("Semana / rango destino", "N/A", "Selección", "SI", "NO", "SI", "Periodo destino"),
        R("Personas incluidas", "N/A", "Selección", "NO", "SI", "SI", "Subset opcional de filas"),
        R("Confirmar sobrescritura", "1", "Booleano", "SI", "NO", "SI", "Confirma reemplazo de celdas existentes"),
    ],
    "MT-EP02-HU42": [
        R("Celda o rango", "N/A", "Selección", "SI", "SI", "SI", "Celdas a fijar"),
        R("Atributo a fijar", "40", "Selección", "SI", "NO", "SI", "Turno, sitio, modalidad u otro atributo"),
        R("Valor fijado", "N/A", "Selección", "SI", "SI", "SI", "Valor que queda bloqueado"),
        R("Fecha desde", "10", "Fecha", "SI", "NO", "SI", "Inicio del periodo fijado"),
        R("Fecha hasta", "10", "Fecha", "SI", "NO", "SI", "Fin del periodo fijado"),
    ],
    # EP-03
    "MT-EP03-HU43": period_filters(),
    "MT-EP03-HU44": period_filters()
    + [
        R("Funcionario", "N/A", "Selección", "NO", "SI", "SI", "Filtro opcional por persona"),
    ],
    "MT-EP03-HU45": [
        R("Malla", "N/A", "Selección", "SI", "SI", "SI", "Malla a validar"),
        R("Severidad mínima a mostrar", "20", "Selección", "NO", "NO", "SI", "Info, advertencia o bloqueo"),
    ],
    "MT-EP03-HU46": [
        R("Código del patrón", "40", "Alfanumérico", "SI", "NO", "SI", "Identificador del patrón de rotación"),
        R("Nombre", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre del patrón"),
        R("Paso / día relativo", "5", "Número", "SI", "NO", "SI", "Orden del paso en el patrón"),
        R("Turno o estado del paso", "N/A", "Selección", "SI", "SI", "SI", "Asignación del paso"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si el patrón está disponible"),
    ],
    "MT-EP03-HU47": [
        R("Patrón de rotación", "N/A", "Selección", "SI", "SI", "SI", "Patrón a vincular"),
        R("Malla / periodo", "N/A", "Selección", "SI", "SI", "SI", "Periodo destino"),
        R("Grupo de funcionarios", "N/A", "Selección", "SI", "SI", "SI", "Personas incluidas en la rotación"),
        R("Fecha de anclaje", "10", "Fecha", "SI", "NO", "SI", "Fecha desde la cual inicia el patrón"),
    ],
    "MT-EP03-HU48": [
        R("Vinculación patrón-grupo", "N/A", "Selección", "SI", "SI", "SI", "Configuración a simular"),
        R("Confirmar simulación", "1", "Booleano", "SI", "NO", "SI", "Ejecuta la simulación sin persistir"),
    ],
    "MT-EP03-HU49": [
        R("Vinculación patrón-grupo", "N/A", "Selección", "SI", "SI", "SI", "Rotación en curso"),
        R("Funcionario excluido", "N/A", "Selección", "NO", "SI", "SI", "Persona fuera de la rotación"),
        R("Celda excluida", "N/A", "Selección", "NO", "SI", "SI", "Celda concreta fuera de la rotación"),
        R("Motivo de exclusión", "N/A", "Texto", "NO", "NO", "SI", "Justificación opcional"),
    ],
    "MT-EP03-HU50": [
        R("Resultado de simulación", "N/A", "Selección", "SI", "SI", "SI", "Simulación a aplicar"),
        R("Confirmar aplicación", "1", "Booleano", "SI", "NO", "SI", "Persiste el resultado en la malla"),
    ],
    "MT-EP03-HU51": [
        R("Malla", "N/A", "Selección", "SI", "SI", "SI", "Malla a armar de forma asistida"),
        R("Parámetros de sugerencia", "N/A", "Texto", "NO", "NO", "SI", "Criterios configurables de armado"),
        R("Confirmar sugerencias", "1", "Booleano", "SI", "NO", "SI", "Acepta el lote sugerido"),
    ],
    "MT-EP03-HU52": [
        R("Malla", "N/A", "Selección", "SI", "SI", "SI", "Malla donde se distribuyen pausas"),
        R("Rango de fechas", "N/A", "Selección", "SI", "NO", "SI", "Días a redistribuir"),
        R("Confirmar distribución", "1", "Booleano", "SI", "NO", "SI", "Aplica la distribución de break/almuerzo"),
    ],
    "MT-EP03-HU53": [
        R("Malla", "N/A", "Selección", "SI", "SI", "SI", "Malla donde se rotan sitios"),
        R("Configuración de rotación de sitios", "N/A", "Selección", "SI", "SI", "SI", "Regla/patrón de sitios"),
        R("Confirmar rotación", "1", "Booleano", "SI", "NO", "SI", "Aplica la rotación de sitios"),
    ],
    "MT-EP03-HU54": [
        R("Malla", "N/A", "Selección", "SI", "SI", "SI", "Malla a reequilibrar"),
        R("Novedad disparadora", "N/A", "Selección", "SI", "SI", "SI", "Cambio/novedad que motiva el reequilibrio"),
        R("Confirmar reequilibrio", "1", "Booleano", "SI", "NO", "SI", "Aplica el reequilibrio sugerido"),
    ],
    "MT-EP03-HU55": [
        R("Malla o acción de rotación", "N/A", "Selección", "SI", "SI", "SI", "Contexto donde se evalúan las reglas"),
        R("Confirmar pese a advertencias", "1", "Booleano", "NO", "NO", "SI", "Solo si la severidad lo permite"),
    ],
    "MT-EP03-HU56": [
        R("Celda a ajustar", "N/A", "Selección", "SI", "SI", "SI", "Celda tras rotación o sugerencia"),
        R("Nuevo turno o estado", "N/A", "Selección", "SI", "SI", "SI", "Ajuste manual"),
        R("Motivo del ajuste", "N/A", "Texto", "NO", "NO", "SI", "Justificación del cambio manual"),
    ],
    # EP-04
    "MT-EP04-HU57": [
        R("Malla", "N/A", "Selección", "SI", "SI", "SI", "Malla a cambiar de estado"),
        R("Acción del ciclo", "20", "Selección", "SI", "NO", "SI", "Enviar a revisión, publicar, etc."),
        R("Comentario", "N/A", "Texto", "NO", "NO", "SI", "Nota del cambio de estado"),
    ],
    "MT-EP04-HU58": [
        R("Malla en revisión", "N/A", "Selección", "SI", "SI", "SI", "Malla a rechazar"),
        R("Motivo de rechazo", "N/A", "Texto", "SI", "NO", "SI", "Justificación obligatoria del rechazo"),
    ],
    "MT-EP04-HU59": [
        R("Malla publicada", "N/A", "Selección", "SI", "SI", "SI", "Malla editable post-publicación"),
        R("Celda a modificar", "N/A", "Selección", "SI", "SI", "SI", "Celda de la malla publicada"),
        R("Nuevo valor", "N/A", "Selección", "SI", "SI", "SI", "Turno, estado o atributo nuevo"),
        R("Motivo del cambio", "N/A", "Texto", "SI", "NO", "SI", "Justificación de la edición post-publicación"),
    ],
    # EP-05
    "MT-EP05-HU60": [
        R("Celda", "N/A", "Selección", "SI", "SI", "SI", "Celda donde se aplica la novedad"),
        R("Estado de novedad", "N/A", "Selección", "SI", "SI", "SI", "Estado operativo de novedad"),
        R("Fecha desde", "10", "Fecha", "SI", "NO", "SI", "Inicio de la novedad"),
        R("Fecha hasta", "10", "Fecha", "NO", "NO", "SI", "Fin de la novedad"),
        R("Motivo", "N/A", "Texto", "NO", "NO", "SI", "Obligatorio si el estado lo exige"),
    ],
    "MT-EP05-HU61": [
        R("Tipo de novedad", "N/A", "Selección", "SI", "SI", "SI", "Clase de novedad a configurar"),
        R("Responsable MVP (ownership)", "40", "Selección", "SI", "NO", "SI", "Quién captura/aprueba en el MVP"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Vigencia de la definición"),
    ],
    "MT-EP05-HU62": None,
    "MT-EP05-HU63": [
        R("Evento de cambio", "N/A", "Selección", "SI", "SI", "SI", "Cambio relevante que dispara aviso"),
        R("Destinatario empleado", "N/A", "Selección", "N/A", "SI", "NO", "Empleado vinculado a la celda"),
        R("Plantilla / canal de notificación", "N/A", "Selección", "SI", "SI", "SI", "Medio configurado de aviso"),
    ],
    "MT-EP05-HU64": period_filters()
    + [
        R("Funcionario", "N/A", "Selección", "SI", "SI", "SI", "Persona cuyo historial se consulta"),
    ],
    # EP-06
    "MT-EP06-HU65": [
        R("Fecha", "10", "Fecha", "SI", "NO", "SI", "Día de la consulta"),
        R("Hora (opcional)", "8", "Hora", "NO", "NO", "SI", "Momento puntual a consultar"),
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente de la búsqueda"),
        R("Criterio (en turno / disponible)", "20", "Selección", "SI", "NO", "SI", "Tipo de búsqueda"),
        R("Texto de búsqueda", "120", "Alfanumérico", "NO", "NO", "SI", "Nombre u otro filtro"),
    ],
    "MT-EP06-HU66": [
        R("Fecha", "10", "Fecha", "SI", "NO", "SI", "Día de cobertura"),
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente a consultar"),
        R("Dimensiones habilitadas", "N/A", "Selección", "NO", "SI", "SI", "Dimensiones activas del frente"),
    ],
    # EP-07
    "MT-EP07-HU67": period_filters()
    + [
        R("Vista", "20", "Selección", "NO", "NO", "SI", "Día, semana o mes"),
    ],
    "MT-EP07-HU68": [
        R("Fecha desde", "10", "Fecha", "SI", "NO", "SI", "Inicio del periodo a consultar"),
        R("Fecha hasta", "10", "Fecha", "SI", "NO", "SI", "Fin del periodo a consultar"),
        R("Vista", "20", "Selección", "SI", "NO", "SI", "Día, semana o mes"),
        R("Funcionario (yo)", "N/A", "Selección", "N/A", "SI", "SI", "Identidad del usuario vinculada al funcionario"),
    ],
    "MT-EP07-HU69": [
        R("Fecha desde", "10", "Fecha", "SI", "NO", "SI", "Inicio del historial a consultar"),
        R("Fecha hasta", "10", "Fecha", "SI", "NO", "SI", "Fin del historial a consultar"),
        R("Funcionario (yo)", "N/A", "Selección", "N/A", "SI", "SI", "Identidad del usuario vinculada al funcionario"),
    ],
    # EP-08
    "MT-EP08-HU70": period_filters()
    + [
        R("Tipos de hora", "N/A", "Selección", "NO", "SI", "SI", "Tipos configurados a incluir"),
        R("Funcionario", "N/A", "Selección", "NO", "SI", "SI", "Filtro opcional por persona"),
    ],
    "MT-EP08-HU71": [
        R("Malla o periodo", "N/A", "Selección", "SI", "SI", "SI", "Contenido a exportar"),
        R("Formato", "10", "Selección", "SI", "NO", "SI", "Excel o PDF"),
        R("Incluir atributos", "1", "Booleano", "NO", "NO", "SI", "Incluye columnas de atributos habilitados"),
    ],
    "MT-EP08-HU72": period_filters()
    + [
        R("Funcionario", "N/A", "Selección", "NO", "SI", "SI", "Filtro opcional por persona"),
    ],
    "MT-EP08-HU73": [
        R("Fecha / periodo", "N/A", "Selección", "SI", "NO", "SI", "Periodo de cobertura a exportar"),
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente a exportar"),
        R("Formato de salida", "10", "Selección", "SI", "NO", "SI", "Formato acordado para terceros"),
    ],
    "MT-EP08-HU74": [
        R("Nombre de plantilla", "120", "Alfanumérico", "SI", "NO", "SI", "Nombre de la plantilla de importación TH"),
        R("Columnas esperadas", "N/A", "Texto", "SI", "NO", "SI", "Definición de columnas del archivo"),
        R("Separador / formato", "20", "Selección", "SI", "NO", "SI", "Formato del archivo de entrada"),
        R("Activo", "1", "Booleano", "SI", "NO", "SI", "Indica si la plantilla está vigente"),
    ],
    "MT-EP08-HU75": [
        R("Archivo de novedades TH", "N/A", "Archivo", "SI", "NO", "SI", "Archivo según plantilla parametrizada"),
        R("Periodo a cruzar", "N/A", "Selección", "SI", "NO", "SI", "Periodo de programación a contrastar"),
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Alcance del cruce"),
    ],
    "MT-EP08-HU76": period_filters()
    + [
        R("Regla de compensatorio", "N/A", "Selección", "NO", "SI", "SI", "Regla activa a aplicar en el reporte"),
    ],
    # EP-09
    "MT-EP09-HU77": [
        R("Frente operativo", "N/A", "Selección", "SI", "SI", "SI", "Frente a configurar"),
        R("Intercambio habilitado", "1", "Booleano", "SI", "NO", "SI", "Activa o desactiva solicitudes"),
        R("Plazo máximo (horas)", "5", "Número", "NO", "NO", "SI", "Ventana para solicitar/aprobar"),
        R("Requiere aprobación", "1", "Booleano", "SI", "NO", "SI", "Define si hay flujo de aprobación"),
        R("Restricciones adicionales", "N/A", "Texto", "NO", "NO", "SI", "Condiciones configurables del frente"),
    ],
    "MT-EP09-HU78": [
        R("Mi celda / turno", "N/A", "Selección", "SI", "SI", "SI", "Celda propia a intercambiar"),
        R("Celda / turno de contraparte", "N/A", "Selección", "SI", "SI", "SI", "Celda objetivo del intercambio"),
        R("Motivo", "N/A", "Texto", "NO", "NO", "SI", "Justificación de la solicitud"),
    ],
    "MT-EP09-HU79": [
        R("Solicitud de intercambio", "N/A", "Selección", "SI", "SI", "SI", "Solicitud a validar con el motor"),
        R("Confirmar pese a advertencias", "1", "Booleano", "NO", "NO", "SI", "Solo si la severidad lo permite"),
    ],
    "MT-EP09-HU80": [
        R("Solicitud de intercambio", "N/A", "Selección", "SI", "SI", "SI", "Solicitud pendiente"),
        R("Decisión", "20", "Selección", "SI", "NO", "SI", "Aprobar o rechazar"),
        R("Motivo de rechazo", "N/A", "Texto", "NO", "NO", "SI", "Obligatorio si se rechaza"),
    ],
    "MT-EP09-HU81": [
        R("Solicitud aprobada", "N/A", "Selección", "SI", "SI", "SI", "Solicitud lista para aplicar"),
        R("Confirmar aplicación", "1", "Booleano", "SI", "NO", "SI", "Aplica el intercambio y dispara auditoría/aviso"),
    ],
}


def hu_id_from_path(path: Path) -> str | None:
    """Resuelve MT-EPxx-HUyy desde el contenido o, en su defecto, solo el número HU."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"MT-EP(\d+)-HU(\d+)", text)
    if m:
        return f"MT-EP{int(m.group(1)):02d}-HU{int(m.group(2)):02d}"
    m = re.search(r"HU(\d+)", path.name.upper())
    if m:
        # fallback: buscar en FIELDS por sufijo
        num = f"{int(m.group(1)):02d}"
        for key in FIELDS:
            if key.endswith(f"-HU{num}"):
                return key
    return None


def section_for(hu_id: str) -> str:
    if hu_id not in FIELDS:
        raise KeyError(f"Sin definición de Datos de entrada para {hu_id}")
    rows = FIELDS[hu_id]
    if rows is None:
        return f"## Datos de entrada\n\n{NO_CAPTURE}\n"
    return f"## Datos de entrada\n\n{table(rows)}\n"


def patch_md(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    hu_id = hu_id_from_path(path)
    if not hu_id:
        print(f"SKIP (sin id): {path}")
        return False

    new_section = section_for(hu_id)
    pattern = re.compile(r"## Datos de entrada\n\n.*?(?=\n---\n|\n\*Documento|\Z)", re.S)
    if not pattern.search(text):
        print(f"SKIP (sin sección): {path.name}")
        return False
    updated = pattern.sub(new_section.rstrip() + "\n\n", text)
    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")
        return True
    return False


def iter_hu_mds():
    for p in sorted(ROOT.rglob("PRY - HU*.md")):
        if "_Obsoletas" in str(p):
            continue
        if "anexo-tecnico" in p.name.lower() or "anexo tecnico" in p.name.lower():
            continue
        yield p


def main() -> None:
    md_files = list(iter_hu_mds())
    missing = []
    for p in md_files:
        hid = hu_id_from_path(p)
        if not hid or hid not in FIELDS:
            missing.append(p.name)
    if missing:
        raise SystemExit(f"Faltan definiciones ({len(missing)}): {missing[:10]}")

    changed = 0
    for p in md_files:
        if patch_md(p):
            changed += 1
            print(f"OK {hu_id_from_path(p)}")
    print(f"Actualizados: {changed}/{len(md_files)}")


if __name__ == "__main__":
    main()
