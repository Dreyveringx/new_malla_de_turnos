# Propuesta de épicas e historias — Malla de Turnos

| Campo | Valor |
| ----- | ----- |
| Producto | Plataforma GRH (gestionrrhh) |
| Módulo | Malla de turnos (dominio operativo integrado a GRH) |
| Versión | 2.4 — Orden lógico continuo HU01…HU81 (05/09/2026) |
| Tipo | Listado ejecutivo de épicas y HU. Detalle en `docs/Backlog definitivo/` |
| Principio | Máxima parametrización por empresa y frente. Cero hardcoding de reglas de negocio. |
| Alcance | Módulo de cero: todas las HU del listado están incluidas. No hay recorte por “fase 2 / fase 3”. |
| Rotación | Híbrida: ninguna / manual / asistida / automática (config del frente), con simulación y ajuste manual. |
| Intercambio | EP-09 incluida; habilitada o no por configuración del frente (default: deshabilitado). |
| Construcción | Incluye copia masiva (HU41) y fijar atributo por periodo (HU42). |
| Numeración | Orden lógico HU01…HU81 (EP-00→EP-09). Sin huecos. Absorbidas = ex-HU46/50/54 (histórico). |

---

## 1. Qué cambia vs la propuesta anterior (v1 / PDF)

1. Frente operativo = catálogo (HU09/HU10), no lista fija de operaciones.
2. Permisos vs alcance: HU02 = permisos de menú; HU03 = alcance por frente.
3. Motor de reglas (HU25) centraliza validaciones sin constantes de negocio en el producto.
4. Estados con flags (HU14): absorben ex-HU50 y ex-HU54.
5. Constructor/publicador en config del frente (HU10) + publicación (HU57); se elimina ex-HU46.
6. Rotación genérica: patrón → vínculo → simulación → exclusiones → aplicación.
7. EP-09 Intercambio entra al backlog (configurable; default off por frente).
8. Sitios = catálogo Malla; novedades = estado de celda + importación de archivo (HU61/HU74).
9. Concurrencia (HU39), carga parcial de grilla (HU40), event types (HU07).
10. Módulo de plataforma: completar el existente (DEV id=13), no duplicar.
11. Se elimina la priorización por fases de alcance: el módulo se documenta completo.

---

## 2. Decisión de solución

La malla operativa no se mete dentro de la jornada contractual. Es un dominio nuevo que:

- reutiliza empleados, áreas, cargos, calendario/festivos, autenticación, notificaciones y timeline de GRH;
- parametriza por empresa + frente turnos, estados, campañas, territorio, modalidades, sitios y reglas;
- estructura cada celda como persona × fecha × (turno/estado) × atributos opcionales según config del frente;
- publica, modifica, audita y notifica de forma informativa sin aceptación del empleado;
- entrega horas a nómina, no valores a pagar.

---

## 3. Épicas e historias (listado ejecutivo)

Leyenda: [N] Nueva · [~] Reescrita/ajustada · [A] Absorbida (no viva)

### EP-00 — Integración del módulo a GRH

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP00-HU01 | Completar módulo y submódulos de Malla de Turnos en la plataforma (sin duplicar) | ~ |
| MT-EP00-HU02 | Configurar permisos por sección de menú (CREAR/LEER/ACTUALIZAR/ELIMINAR) | ~ |
| MT-EP00-HU03 | Asignar alcance de frentes operativos a usuarios o roles | N |
| MT-EP00-HU04 | Aislar mallas, catálogos y reportes por empresa (multi-tenant) | ~ |
| MT-EP00-HU05 | Reutilizar empleados, áreas, cargos y calendario de festivos (sitios = catálogo Malla) | ~ |
| MT-EP00-HU06 | Distinguir jornada contractual de malla operativa | ~ |
| MT-EP00-HU07 | Registrar event types de notificación y timeline para Malla | N |
| MT-EP00-HU08 | Consumir listado de empleados con filtro/paginación por área o vínculo a frente | N |

### EP-01 — Parametrización de catálogos y reglas

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP01-HU09 | Parametrizar frentes operativos de la empresa (catálogo) | N |
| MT-EP01-HU10 | Configurar capacidades, estrategia de armado y publicación del frente | N |
| MT-EP01-HU11 | Parametrizar plantillas de turno | ~ |
| MT-EP01-HU12 | Configurar horarios distintos por día en un turno | ~ |
| MT-EP01-HU13 | Parametrizar break y almuerzo del turno | ~ |
| MT-EP01-HU14 | Parametrizar estados de celda con flags de comportamiento | ~ |
| MT-EP01-HU15 | Parametrizar campañas o tareas de celda | ~ |
| MT-EP01-HU16 | Parametrizar territorio con niveles configurables | ~ |
| MT-EP01-HU17 | Parametrizar modalidades (catálogo + requiere sitio) | ~ |
| MT-EP01-HU18 | Parametrizar sitios de asistencia | ~ |
| MT-EP01-HU19 | Parametrizar tipos y restricciones de persona | ~ |
| MT-EP01-HU20 | Usar festivos del calendario de empresa | ~ |
| MT-EP01-HU21 | Parametrizar cortes de nómina (sin liquidar dinero) | ~ |
| MT-EP01-HU22 | Parametrizar tipos de hora y reglas de clasificación | ~ |
| MT-EP01-HU23 | Parametrizar reglas de compensatorio (umbrales configurables) | ~ |
| MT-EP01-HU24 | Parametrizar reglas de cobertura (dimensiones + min/max + severidad) | ~ |
| MT-EP01-HU25 | Motor de reglas de validación (info / advertencia / bloqueo) | N |
| MT-EP01-HU26 | Configurar flags de atributos de celda del frente | ~ |
| MT-EP01-HU27 | Importación asistida desde Excel de operación (descubrimiento → catálogos) | N |

### EP-02 — Construcción de la malla

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP02-HU28 | Crear malla por periodo y frente | ~ |
| MT-EP02-HU29 | Seleccionar grupo de funcionarios de la malla | ~ |
| MT-EP02-HU30 | Asignar turno o estado a una celda | ~ |
| MT-EP02-HU31 | Asignar segundo turno o turno extra el mismo día | ~ |
| MT-EP02-HU32 | Asignar territorio a la celda (si capacidad habilitada) | ~ |
| MT-EP02-HU33 | Asignar modalidad y sitio a la celda | ~ |
| MT-EP02-HU34 | Registrar observación en la celda | ~ |
| MT-EP02-HU35 | Visualizar grilla operativa | ~ |
| MT-EP02-HU36 | Asignar campaña o tarea a la celda | ~ |
| MT-EP02-HU37 | Cubrir recurso de otro frente o área el mismo día | ~ |
| MT-EP02-HU38 | Filtrar y buscar en la grilla por atributos habilitados | ~ |
| MT-EP02-HU39 | Control de concurrencia en edición de celdas | N |
| MT-EP02-HU40 | Carga parcial de grilla (ventana temporal + paginación) | N |
| MT-EP02-HU41 | Copiar semana o aplicar asignación masiva | N |
| MT-EP02-HU42 | Fijar atributo de celda por periodo | N |

### EP-03 — Validación, cobertura y rotación

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP03-HU43 | Visualizar indicadores de cobertura y contadores | ~ |
| MT-EP03-HU44 | Visualizar equilibrio de turnos por persona | ~ |
| MT-EP03-HU45 | Evaluar y mostrar conflictos de validación en grilla | ~ |
| MT-EP03-HU46 | Definir patrón de rotación genérico (secuencia + duraciones) | N |
| MT-EP03-HU47 | Vincular patrón de rotación a grupo y periodo | ~ |
| MT-EP03-HU48 | Simular patrón de rotación antes de aplicar | N |
| MT-EP03-HU49 | Excluir personas o celdas de la rotación | N |
| MT-EP03-HU50 | Aplicar resultado de rotación a la malla | ~ |
| MT-EP03-HU51 | Construcción asistida de asignaciones | ~ |
| MT-EP03-HU52 | Distribuir breaks y almuerzos según plantillas y reglas | ~ |
| MT-EP03-HU53 | Rotar sitios de asistencia según configuración | ~ |
| MT-EP03-HU54 | Reequilibrar cargas tras una novedad | ~ |
| MT-EP03-HU55 | Aplicar restricciones y motor de reglas al rotar o asignar | ~ |
| MT-EP03-HU56 | Ajustar manualmente tras rotación o sugerencia | ~ |

### EP-04 — Publicación y ciclo de vida

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP04-HU57 | Ciclo de vida de publicación (borrador / revisión / publicada / rechazada) | ~ |
| MT-EP04-HU58 | Rechazar malla en revisión | ~ |
| MT-EP04-HU59 | Editar malla publicada (según config del frente) | ~ |
| MT-EP04-ex-HU46 | Separar constructor y publicador | A → HU10 + HU57 |

### EP-05 — Novedades, cambios y auditoría

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP05-HU60 | Aplicar estado de novedad operativa a la celda (catálogo) | ~ |
| MT-EP05-HU61 | Criterio operativo de novedades (estado de celda + importación opcional) | N |
| MT-EP05-HU62 | Historial inmutable de celda | ~ |
| MT-EP05-HU63 | Notificar cambio relevante al empleado (sin aceptación) | ~ |
| MT-EP05-ex-HU50 | Dejar de sumar horas en novedad | A → HU14 + HU70 |
| MT-EP05-HU64 | Consultar historial de cambios por funcionario | ~ |

### EP-06 — Consulta operativa

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP06-HU65 | Buscar quién está en turno o disponible | ~ |
| MT-EP06-HU66 | Consultar cobertura del día por dimensiones habilitadas | ~ |
| MT-EP06-ex-HU54 | Actividad no asignable a casos | A → HU14 + HU65 |

### EP-07 — Vista del empleado

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP07-HU67 | Ver programación del grupo (según política de visibilidad) | ~ |
| MT-EP07-HU68 | Ver mi programación (día, semana, mes) | ~ |
| MT-EP07-HU69 | Ver historial de mis turnos y cambios recientes | ~ |

### EP-08 — Reportes y horas para nómina

El módulo entrega horas, no liquidación monetaria.

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP08-HU70 | Calcular horas del periodo por tipos configurados | ~ |
| MT-EP08-HU71 | Exportar malla a Excel o PDF | ~ |
| MT-EP08-HU72 | Reportar horas de novedad versus operativas | ~ |
| MT-EP08-HU73 | Exportar cobertura para terceros | ~ |
| MT-EP08-HU74 | Parametrizar plantilla de importación de novedades TH | N |
| MT-EP08-HU75 | Cruzar programación con novedades TH importadas | ~ |
| MT-EP08-HU76 | Aplicar reglas de compensatorio en reporte | ~ |

### EP-09 — Intercambio de turnos

Incluida. Por configuración del frente puede nacer deshabilitada.

| ID | Título | Nota |
| -- | ------ | ---- |
| MT-EP09-HU77 | Habilitar y configurar solicitudes de intercambio | N |
| MT-EP09-HU78 | Solicitar intercambio de celda o turno | N |
| MT-EP09-HU79 | Validar solicitud con motor de reglas | N |
| MT-EP09-HU80 | Aprobar o rechazar solicitud | N |
| MT-EP09-HU81 | Aplicar intercambio, auditar y notificar | N |

---

## 4. Absorbidas (no generan Word activo)

| ID | Absorber en |
| -- | ----------- |
| ex-HU46 | HU10 + HU57 |
| ex-HU50 | HU14 + HU70 |
| ex-HU54 | HU14 + HU65 |

---

## 5. Fuera de alcance (explícito)

- Liquidación de nómina en pesos (solo horas).
- Módulo completo de vacaciones/incapacidades nativo en GRH (en Malla: estado de celda + importación de archivo; conector nativo futuro si negocio lo define).
- Pantalla de indicadores de desempeño.
- Personal de fábrica (sesión propia).
- Reportería gráfica avanzada corporativa.

---

## 6. Orden de construcción (solo dependencias)

Todas las HU están incluidas. El orden refleja dependencias para construir el módulo de cero:

1. EP-00 — integración.
2. EP-01 — parametrización y motor de reglas.
3. EP-02 — construcción / grilla.
4. EP-03 — validación y rotación.
5. EP-04 — publicación.
6. EP-05 — novedades, historial y notificaciones.
7. EP-06 — consulta operativa.
8. EP-07 — vista empleado.
9. EP-08 — reportes y horas.
10. EP-09 — intercambio (capacidad en el producto; on/off por frente).

Detalle completo: `docs/Backlog definitivo/`.  
Tabla para corrección Word: `docs/Backlog definitivo/TABLA-CORRECCION-WORD.md`.
