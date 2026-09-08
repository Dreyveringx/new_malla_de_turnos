# EP-01 — Parametrización y catálogos

## Índice

- MT-EP01-HU09 — Parametrizar frentes operativos de la empresa
- MT-EP01-HU10 — Configurar capacidades, estrategia de armado y publicación del frente
- MT-EP01-HU11 — Parametrizar plantillas de turno
- MT-EP01-HU12 — Configurar horarios distintos por día en un turno
- MT-EP01-HU13 — Parametrizar break y almuerzo del turno
- MT-EP01-HU14 — Parametrizar estados de celda con flags de comportamiento
- MT-EP01-HU15 — Parametrizar campañas o tareas de celda
- MT-EP01-HU16 — Parametrizar territorio con niveles configurables
- MT-EP01-HU17 — Parametrizar modalidades de trabajo
- MT-EP01-HU18 — Parametrizar sitios de asistencia
- MT-EP01-HU19 — Parametrizar tipos y restricciones de persona
- MT-EP01-HU20 — Usar festivos del calendario de empresa
- MT-EP01-HU21 — Parametrizar cortes de nómina
- MT-EP01-HU22 — Parametrizar tipos de hora y reglas de clasificación
- MT-EP01-HU23 — Parametrizar reglas de compensatorio
- MT-EP01-HU24 — Parametrizar reglas de cobertura
- MT-EP01-HU25 — Motor de reglas de validación parametrizable
- MT-EP01-HU26 — Configurar flags de atributos de celda del frente
- MT-EP01-HU27 — Importación asistida desde Excel de operación

---
## MT-EP01-HU09 — Parametrizar frentes operativos de la empresa

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** registrar frentes operativos con código, nombre, descripción y estado pertenecientes a mi empresa

**Para:** configurar operaciones distintas sin depender de una lista fija de nombres de negocio

### Alcance

**Cubre**

- CRUD de frentes por empresa
- Código único por empresa
- Activar/inactivar

**No cubre**

- Enum de producto Contact Center/Sitio/Mesa/Lab
- Ítems de menú de plataforma por frente

### Reglas de negocio

1. El frente es un catálogo tenant-scoped, no un enum de aplicación.
2. Un frente inactivo no se ofrece para nuevas mallas.
3. Los nombres de operaciones actuales son solo datos de configuración o seeds de ejemplo.

### Criterios de aceptación

**CA01 — Alta**

Dado que el usuario tiene permiso de parametrización

Cuando crea un frente con código único en su empresa

Entonces el frente queda disponible solo para esa empresa

**CA02 — Unicidad**

Dado que ya existe el código en la empresa

Cuando intenta crear otro con el mismo código

Entonces el sistema rechaza por duplicado

**CA03 — Sin defaults de producto**

Dado que una empresa nueva sin seeds

Cuando abre el catálogo de frentes

Entonces no asume frentes predefinidos de otras operaciones

**CA04 — Multiempresa**

Dado que empresa A tiene frentes

Cuando usuario de empresa B lista frentes

Entonces no ve los de A

**CA05 — Inactivo**

Dado que un frente está inactivo

Cuando se crea una malla

Entonces ese frente no aparece en el selector

### Dependencias

- HUs: MT-EP00-HU02, MT-EP00-HU04
- Microservicios / GRH: Malla (nuevo dominio)

---

## MT-EP01-HU10 — Configurar capacidades, estrategia de armado y publicación del frente

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir para cada frente el periodo de planificación por defecto, la estrategia de armado, la separación constructor/publicador, la editabilidad post-publicación y las capacidades disponibles

**Para:** que el mismo producto se adapte a cada operación sin redesplegar código

### Alcance

**Cubre**

- Periodo por defecto (valores configurables: semanal, quincenal, mensual u otros definidos en catálogo de periodos)
- Estrategia de armado: ninguna, manual, asistida, automática
- Flags de publicación y roles lógicos constructor/publicador
- Vínculo opcional a una o más áreas GRH
- Habilitación de solicitudes de intercambio (default deshabilitado)

**No cubre**

- Implementar el algoritmo de rotación (EP-03)
- Hardcodear periodos por nombre de frente

### Reglas de negocio

1. Si una capacidad está deshabilitada, la UI y las API no exigen ni persisten ese atributo en celdas nuevas.
2. Si la estrategia es manual, las acciones de rotación automática permanecen deshabilitadas.
3. Si constructor/publicador está separado, quien solo construye no publica; envía a revisión según flujo HU57.
4. Publicar con advertencias solo si el flag del frente lo permite.
5. El vínculo a áreas GRH es opcional; el frente sigue siendo entidad propia.

### Criterios de aceptación

**CA01 — Capacidad off**

Dado que el frente tiene deshabilitado territorio

Cuando se edita una celda

Entonces no se solicita ni muestra territorio

**CA02 — Estrategia**

Dado que estrategia = manual

Cuando el usuario abre rotación automática

Entonces la acción no está disponible e indica que la configuración del frente no la habilita

**CA03 — Constructor**

Dado que separación constructor/publicador activa

Cuando el constructor intenta publicar

Entonces solo puede enviar a revisión o se le niega publicar según config

**CA04 — Intercambio off**

Dado que solicitudes deshabilitadas en el frente

Cuando un empleado abre su programación

Entonces no ve la acción de solicitar intercambio

**CA05 — Auditoría config**

Dado que se cambia la estrategia de armado

Cuando se guarda

Entonces queda trazabilidad de antes/después, usuario y fecha

**CA06 — Tenant**

Dado que se edita config de un frente

Cuando persiste

Entonces solo afecta a la empresa dueña del frente

### Dependencias

- HUs: MT-EP01-HU09, MT-EP00-HU03
- Microservicios / GRH: Malla; parametrization áreas (vínculo opcional)

---

## MT-EP01-HU11 — Parametrizar plantillas de turno

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** registrar plantillas de turno con código, nombre, horarios, color, cruce de medianoche y aplicabilidad por frente

**Para:** reutilizar definiciones horarias al armar mallas sin quemar turnos en código

### Alcance

**Cubre**

- CRUD plantillas por empresa y aplicabilidad a frentes
- Duración calculada, color, nocturnidad, activo/inactivo

**No cubre**

- Asignar turnos a celdas (HU30)
- Listas fijas 1–12

### Reglas de negocio

1. Las plantillas son catálogo tenant-scoped.
2. Un turno inactivo no se ofrece en nuevas asignaciones.
3. Los códigos de ejemplo de Excel son seeds, no enums.

### Criterios de aceptación

**CA01 — Alta**

Dado que existe al menos un frente

Cuando crea plantilla con código único en el alcance definido

Entonces queda disponible para asignar en frentes autorizados

**CA02 — Medianoche**

Dado que hora fin es menor que hora inicio y se marca cruce de medianoche

Cuando se guarda

Entonces la duración se calcula cruzando día

**CA03 — Inactivo**

Dado que plantilla inactiva

Cuando se asigna celda nueva

Entonces no aparece en el selector

**CA04 — Tenant**

Dado que otra empresa

Cuando lista plantillas

Entonces no ve las ajenas

### Dependencias

- HUs: MT-EP01-HU09
- Microservicios / GRH: Malla

---

## MT-EP01-HU12 — Configurar horarios distintos por día en un turno

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir para una plantilla horarios diferentes según día de la semana u otros criterios de día configurables

**Para:** representar turnos que no tienen el mismo horario todos los días

### Alcance

**Cubre**

- Variantes de horario por día asociadas a la plantilla

**No cubre**

- Reglas de cobertura

### Reglas de negocio

1. Si no hay variante para un día, aplica el horario base de la plantilla.
2. Las variantes pertenecen a la misma empresa que la plantilla.

### Criterios de aceptación

**CA01 — Variante**

Dado que existe una plantilla

Cuando se define horario distinto para un día de la semana

Entonces al asignar ese día se usa la variante

**CA02 — Default**

Dado que no hay variante para el día

Cuando se asigna la plantilla

Entonces usa horario base

**CA03 — Permisos**

Dado que usuario sin ACTUALIZAR en Parametrización

Cuando intenta editar variantes

Entonces se niega

**CA04 — Tenant**

Dado que plantilla de otra empresa

Cuando intenta editar

Entonces no accesible

### Dependencias

- HUs: MT-EP01-HU11
- Microservicios / GRH: Malla

---

## MT-EP01-HU13 — Parametrizar break y almuerzo del turno

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir pausas (break, almuerzo u otros tipos de pausa del catálogo) asociadas a una plantilla

**Para:** que la operación programe pausas según configuración y no según reglas fijas por frente

### Alcance

**Cubre**

- Tipos de pausa configurables
- Horario o duración de pausa por plantilla

**No cubre**

- Distribución automática en grilla (HU52)

### Reglas de negocio

1. Las pausas son datos de plantilla; su obligatoriedad y efecto en cobertura lo definen reglas (HU25/HU24).
2. No se asume que todos los frentes usan break y almuerzo.

### Criterios de aceptación

**CA01 — Alta pausa**

Dado que plantilla activa

Cuando se agregan una o más pausas con tipo e intervalo

Entonces quedan asociadas a la plantilla

**CA02 — Sin pausas**

Dado que frente/plantilla sin pausas

Cuando se asigna el turno

Entonces no se exigen pausas

**CA03 — Validación**

Dado que pausa fuera del horario del turno

Cuando se guarda

Entonces el sistema rechaza o advierte según regla configurada

**CA04 — Tenant**

Dado que otra empresa

Cuando consulta pausas

Entonces no ve datos ajenos

### Dependencias

- HUs: MT-EP01-HU11
- Microservicios / GRH: Malla

---

## MT-EP01-HU14 — Parametrizar estados de celda con flags de comportamiento

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** registrar estados operativos de celda con código, nombre, color y flags que definen su comportamiento

**Para:** representar novedades y situaciones operativas sin HUs ni enums por cada estado de negocio

### Alcance

**Cubre**

- CRUD estados tenant-scoped
- Flags: cuenta horas ordinarias/extra/recargo/festivo; afecta cobertura; disponible para asignación de casos; requiere motivo; permite turno; permite ubicación; notifica empleado; requiere soporte; permite modificación

**No cubre**

- HUs separadas por vacaciones, incapacidad, actividad, etc.
- Cálculo monetario

### Reglas de negocio

1. Los estados son catálogo; vacaciones/incapacidad/actividad/descanso son ítems de datos, no tipos de sistema.
2. El efecto en horas lo determinan los flags + motor de horas (HU70).
3. Si un estado no es asignable a casos, la consulta operativa lo excluye de disponibilidad operativa según flag.
4. ex-HU50 y ex-HU54 originales quedan absorbidas por estos flags.

### Criterios de aceptación

**CA01 — Alta estado**

Dado que usuario con permiso

Cuando crea estado con flags

Entonces queda disponible en celdas de la empresa (y frentes según aplicabilidad)

**CA02 — No suma horas**

Dado que estado con flag cuenta horas ordinarias = no

Cuando se calcula el periodo

Entonces esa celda no aporta horas ordinarias

**CA03 — Afecta cobertura**

Dado que estado con afecta cobertura = no

Cuando se evalúa cobertura

Entonces la persona no cuenta para el mínimo de esa dimensión

**CA04 — Motivo**

Dado que estado requiere motivo = sí

Cuando se aplica a celda sin motivo

Entonces el sistema bloquea o advierte según severidad configurada

**CA05 — Tenant**

Dado que estados de empresa A

Cuando empresa B lista

Entonces no los ve

### Dependencias

- HUs: MT-EP01-HU09
- Microservicios / GRH: Malla

### Consideraciones técnicas

Absorbe comportamiento de ex-HU50 y ex-HU54.

---

## MT-EP01-HU15 — Parametrizar campañas o tareas de celda

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** registrar campañas o tareas con código, nombre, color, vigencia y aplicabilidad a frentes

**Para:** etiquetar celdas sin hardcodear nombres de campaña

### Alcance

**Cubre**

- CRUD campañas/tareas
- Vigencia y activo

**No cubre**

- Asignación en celda (HU36)

### Reglas de negocio

1. Solo aplica si el frente tiene la capacidad habilitada (HU10/HU26).
2. Ejemplos de operación son seeds.

### Criterios de aceptación

**CA01 — Alta**

Dado que capacidad campañas habilitada en un frente

Cuando crea campaña vigente

Entonces aparece al asignar celdas de ese frente

**CA02 — Vigencia**

Dado que campaña fuera de vigencia

Cuando se asigna celda

Entonces no se ofrece

**CA03 — Capacidad off**

Dado que frente sin campañas

Cuando se edita celda

Entonces no pide campaña

**CA04 — Tenant**

Dado que otra empresa

Cuando lista

Entonces no ve campañas ajenas

### Dependencias

- HUs: MT-EP01-HU10
- Microservicios / GRH: Malla

---

## MT-EP01-HU16 — Parametrizar territorio con niveles configurables

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir la estructura territorial del frente con N niveles nombrados por configuración

**Para:** soportar jerarquías distintas sin fijar Regional/Zona/SPT en código

### Alcance

**Cubre**

- Definición de niveles por frente o empresa
- Árbol de nodos territoriales
- Activo/inactivo

**No cubre**

- Hardcodear 3 niveles con nombres fijos

### Reglas de negocio

1. Los nombres de nivel son configuración, no enums de producto.
2. Solo visible si el frente habilita territorio.

### Criterios de aceptación

**CA01 — Niveles**

Dado que el frente habilita territorio con K niveles nombrados

Cuando se crean nodos

Entonces la UI respeta esa jerarquía

**CA02 — Sin territorio**

Dado que capacidad deshabilitada

Cuando se opera la malla

Entonces no se exige territorio

**CA03 — Tenant**

Dado que nodos de otra empresa

Cuando lista

Entonces no visibles

**CA04 — Inactivo**

Dado que nodo inactivo

Cuando asigna celda

Entonces no se ofrece

### Dependencias

- HUs: MT-EP01-HU10
- Microservicios / GRH: Malla

---

## MT-EP01-HU17 — Parametrizar modalidades de trabajo

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** registrar modalidades (presencial, virtual u otras) con flag que indique si requieren sitio

**Para:** extender modalidades sin enums fijos

### Alcance

**Cubre**

- CRUD modalidades
- Flag requiereSitio

**No cubre**

- if (virtual) en código

### Reglas de negocio

1. Presencial/virtual/híbrido son ejemplos de datos, no tipos de sistema.
2. La obligatoriedad de sitio la define el flag + capacidad del frente.

### Criterios de aceptación

**CA01 — Alta**

Dado que permiso de parametrización

Cuando crea modalidad con requiereSitio

Entonces al asignar, si requiereSitio y capacidad sitio on, exige sitio

**CA02 — Nueva modalidad**

Dado que se necesita una modalidad nueva

Cuando se crea en catálogo

Entonces no requiere despliegue de código

**CA03 — Tenant**

Dado que otra empresa

Cuando lista

Entonces aislada

**CA04 — Capacidad off**

Dado que frente sin modalidad

Cuando edita celda

Entonces no pide modalidad

### Dependencias

- HUs: MT-EP01-HU10
- Microservicios / GRH: Malla

---

## MT-EP01-HU18 — Parametrizar sitios de asistencia

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** registrar sitios de asistencia de la empresa aplicables a frentes

**Para:** ubicar la operación sin inventar maestro de sedes en GRH ni especializar un sitio por nombre

### Alcance

**Cubre**

- CRUD sitios
- Aplicabilidad a frentes
- Activo

**No cubre**

- Tratar un nombre de sitio como caso especial de producto

### Reglas de negocio

1. Sitios son catálogo Malla; GRH no provee sedes hoy.
2. Cualquier nombre operativo es un ítem de catálogo.

### Criterios de aceptación

**CA01 — Alta**

Dado que capacidad sitio habilitada

Cuando crea sitio

Entonces disponible en celdas del frente

**CA02 — Inactivo**

Dado que sitio inactivo

Cuando asigna

Entonces no aparece

**CA03 — Tenant**

Dado que otra empresa

Cuando lista

Entonces no ve sitios ajenos

**CA04 — Sin hardcoding**

Dado que se documentan ejemplos

Cuando se implementa

Entonces ningún sitio aparece como condición en código

### Dependencias

- HUs: MT-EP01-HU10
- Microservicios / GRH: Malla

---

## MT-EP01-HU19 — Parametrizar tipos y restricciones de persona

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir tipos de restricción y registrar restricciones por persona con alcance, vigencia y efecto

**Para:** respetar limitaciones individuales sin categorías quemadas

### Alcance

**Cubre**

- Catálogo de tipos de restricción
- Restricción: persona, vigencia, días/franjas, turnos/sitios/modalidades permitidos o no, efecto bloquear/advertir

**No cubre**

- Tipos estudio/salud como enums

### Reglas de negocio

1. Los tipos son catálogo tenant-scoped.
2. El motor de asignación/rotación consume restricciones (HU55).
3. Efecto bloquear impide guardar; advertir permite con confirmación según severidad.

### Criterios de aceptación

**CA01 — Tipo**

Dado que parametrizador

Cuando crea un tipo de restricción

Entonces queda disponible para usar en restricciones

**CA02 — Restricción**

Dado que persona con restricción vigente que bloquea un turno

Cuando se intenta asignar ese turno

Entonces se aplica el efecto configurado

**CA03 — Vigencia**

Dado que restricción vencida

Cuando se asigna

Entonces no aplica

**CA04 — Tenant**

Dado que persona de otra empresa

Cuando alta restricción

Entonces imposible

### Dependencias

- HUs: MT-EP00-HU05, MT-EP01-HU25
- Microservicios / GRH: Malla; employee (identidad)

---

## MT-EP01-HU20 — Usar festivos del calendario de empresa

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** considerar los festivos definidos en el calendario GRH de la empresa al programar y calcular horas

**Para:** no duplicar calendarios

### Alcance

**Cubre**

- Lectura de festivos company calendar
- Uso en reglas de hora festiva si están configuradas

**No cubre**

- CRUD de festivos dentro de Malla

### Reglas de negocio

1. Fuente de verdad de festivos = calendario de empresa GRH.
2. Malla no mantiene un calendario paralelo de festivos.

### Criterios de aceptación

**CA01 — Lectura**

Dado que hay festivo en calendario empresa

Cuando se visualiza el día en malla

Entonces se identifica como festivo

**CA02 — Horas**

Dado que existen reglas de tipo hora festiva

Cuando se calcula el día festivo

Entonces se clasifica según reglas HU22/HU70

**CA03 — Tenant**

Dado que festivos de otra empresa

Cuando consulta

Entonces no aplican

**CA04 — Sin calendario**

Dado que empresa sin festivos cargados

Cuando opera malla

Entonces no inventa festivos

### Dependencias

- HUs: MT-EP00-HU05, MT-EP01-HU22
- Microservicios / GRH: parametrization company-calendars / holidays

---

## MT-EP01-HU21 — Parametrizar cortes de nómina

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir la frecuencia y fechas de corte usadas para agrupar horas a entregar

**Para:** alinear reportes de horas con el ciclo de la empresa sin liquidar dinero

### Alcance

**Cubre**

- Config de corte por empresa (y override por frente si se habilita)
- Periodos de corte

**No cubre**

- Cálculo de pesos
- Integración contable

### Reglas de negocio

1. Malla entrega horas por corte; no calcula valores monetarios.
2. La frecuencia y días de corte son configuración.

### Criterios de aceptación

**CA01 — Config**

Dado que se define frecuencia y anclas de corte

Cuando se consulta un periodo

Entonces el sistema determina el rango de corte aplicable

**CA02 — Reporte**

Dado que existe malla en el rango

Cuando se pide horas del corte

Entonces agrupa según la config (HU70)

**CA03 — Tenant**

Dado que cortes de otra empresa

Cuando consulta

Entonces no visibles

**CA04 — Sin dinero**

Dado que se genera salida de corte

Cuando se inspecciona

Entonces no incluye campos de liquidación monetaria

### Dependencias

- HUs: MT-EP01-HU22, MT-EP08-HU70
- Microservicios / GRH: Malla

---

## MT-EP01-HU22 — Parametrizar tipos de hora y reglas de clasificación

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir tipos de hora (ordinaria, extra, festiva, nocturna, recargo u otros) con condiciones, prioridad y aplicabilidad

**Para:** clasificar horas sin fórmulas quemadas por frente

### Alcance

**Cubre**

- Catálogo tipos de hora
- Reglas de clasificación con prioridad

**No cubre**

- Cálculo de dinero

### Reglas de negocio

1. ORD/EXT/FES etc. son códigos de catálogo/seeds, no enums rígidos de producto.
2. La prioridad resuelve solapes de clasificación.

### Criterios de aceptación

**CA01 — Alta tipo**

Dado que parametrizador

Cuando crea tipo de hora

Entonces disponible para el motor HU70

**CA02 — Prioridad**

Dado que dos reglas aplican al mismo intervalo

Cuando se clasifica

Entonces gana la de mayor prioridad según config

**CA03 — Tenant**

Dado que otra empresa

Cuando lista tipos

Entonces aislados

**CA04 — Extensibilidad**

Dado que se necesita un tipo nuevo

Cuando se crea en catálogo

Entonces sin despliegue de lógica específica

### Dependencias

- HUs: MT-EP01-HU21
- Microservicios / GRH: Malla

---

## MT-EP01-HU23 — Parametrizar reglas de compensatorio

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir reglas que, ante umbrales y tipos de día configurables, sugieran o apliquen estados/acciones de compensatorio

**Para:** representar políticas distintas sin fijar cantidades de domingos u otros días en código

### Alcance

**Cubre**

- Reglas: ventana temporal, tipo de día, umbral, acción (sugerir estado, advertir, bloquear), severidad

**No cubre**

- Regla fija de tres domingos

### Reglas de negocio

1. Cualquier umbral numérico es parámetro de la regla.
2. La aplicación en reporte consume estas reglas (HU76).

### Criterios de aceptación

**CA01 — Alta regla**

Dado que se configura umbral N sobre tipo de día D en ventana V

Cuando se evalúa

Entonces si se cumple, aplica la acción configurada

**CA02 — Inactiva**

Dado que regla inactiva

Cuando evaluación

Entonces no se considera

**CA03 — Por frente**

Dado que dos frentes con umbrales distintos

Cuando se evalúa cada uno

Entonces usa su propia regla

**CA04 — Tenant**

Dado que otra empresa

Cuando no ve reglas ajenas

Entonces aislamiento OK

### Dependencias

- HUs: MT-EP01-HU25, MT-EP01-HU14
- Microservicios / GRH: Malla

---

## MT-EP01-HU24 — Parametrizar reglas de cobertura

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** definir cobertura mínima y máxima por dimensiones configurables con severidad

**Para:** controlar dotación sin reglas del tipo mínimo fijo por región en código

### Alcance

**Cubre**

- Dimensiones: fecha, franja, turno, territorio, sitio, modalidad, campaña, frente (según capacidades)
- min/max + severidad info/advertencia/bloqueo + vigencia

**No cubre**

- mínimo N técnicos hardcodeado

### Reglas de negocio

1. La evaluación usa solo dimensiones habilitadas en el frente.
2. Personas con estado que no afecta cobertura no cuentan.

### Criterios de aceptación

**CA01 — Alta**

Dado que se crea regla min=X en dimensión configurada

Cuando la malla queda por debajo

Entonces se emite hallazgo con la severidad definida

**CA02 — Máximo**

Dado que se supera max

Cuando evaluación

Entonces aplica severidad de la regla

**CA03 — Dimensión off**

Dado que frente sin territorio

Cuando no se exigen reglas de territorio

Entonces no aparecen

**CA04 — Tenant**

Dado que reglas ajenas

Cuando no visibles

Entonces OK

### Dependencias

- HUs: MT-EP01-HU25, MT-EP01-HU14, MT-EP01-HU10
- Microservicios / GRH: Malla

---

## MT-EP01-HU25 — Motor de reglas de validación parametrizable

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** administrar reglas de validación con código, alcance, parámetros, prioridad, severidad y estado, y evaluarlas al asignar o publicar

**Para:** centralizar solape, horas, cobertura, descanso, repetición, restricciones, anticipación e intercambio sin constantes en código

### Alcance

**Cubre**

- CRUD reglas por empresa/frente
- Severidades: informativa, advertencia, bloqueo
- Evaluación en asignación, publicación, rotación e intercambio

**No cubre**

- UI completa de conflictos (HU45)
- DSL visual avanzado (futuro)

### Reglas de negocio

1. Invariante de dominio: solape horario real de la misma persona en el mismo instante es siempre bloqueo.
2. Horas máximas/mínimas, cobertura, repetición, celda vacía, anticipación, etc. son reglas parametrizables.
3. Regla inactiva no se evalúa.
4. Parámetros numéricos viven en la regla, nunca en el título de una HU ni en constantes de negocio en código.

### Criterios de aceptación

**CA01 — Horas máximas**

Dado que regla max_hours_period = N para el frente

Cuando la malla supera N

Entonces se genera hallazgo con la severidad de la regla

**CA02 — Solape**

Dado que dos asignaciones se solapan en el tiempo para la misma persona

Cuando se intenta guardar

Entonces se bloquea

**CA03 — Inactiva**

Dado que regla inactiva

Cuando validación

Entonces no aparece

**CA04 — Alcance frente**

Dado que regla solo del frente A

Cuando se valida malla del frente B

Entonces no aplica

**CA05 — Tenant**

Dado que reglas empresa A

Cuando empresa B

Entonces aisladas

### Dependencias

- HUs: MT-EP01-HU10; consumida por HU45, HU55, HU57, HU79
- Microservicios / GRH: Malla (domain service)

### Consideraciones técnicas

No dispersar if/else de negocio fuera del motor.

---

## MT-EP01-HU26 — Configurar flags de atributos de celda del frente

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** activar o desactivar qué atributos puede tener una celda en el frente (territorio, campaña, modalidad, sitio, nota, doble turno, etc.)

**Para:** mostrar en grilla solo lo que la operación necesita

### Alcance

**Cubre**

- Flags de atributos de celda por frente

**No cubre**

- Estrategia de armado (HU10)
- Crear los catálogos base

### Reglas de negocio

1. HU10 define estrategia/publicación/vínculos; HU26 detalla atributos de celda visibles/editables.
2. Atributo off ⇒ no se captura en UI ni se exige en API de celda.

### Criterios de aceptación

**CA01 — Flag off**

Dado que doble turno deshabilitado

Cuando se edita celda

Entonces no permite segundo turno

**CA02 — Flag on**

Dado que nota habilitada

Cuando se edita celda

Entonces permite observación

**CA03 — Consistencia**

Dado que se deshabilita campaña con celdas ya etiquetadas

Cuando se consulta histórico

Entonces se conserva dato histórico; nuevas celdas no piden campaña

**CA04 — Tenant**

Dado que config ajena

Cuando no visible

Entonces OK

### Dependencias

- HUs: MT-EP01-HU10
- Microservicios / GRH: Malla

### Consideraciones técnicas

ex-HU46 absorbida: constructor/publicador está en HU10 + flujo HU57.

---

## MT-EP01-HU27 — Importación asistida desde Excel de operación

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)

**Quiero:** cargar un Excel de operación para sugerir catálogos (turnos, estados, sitios, campañas) sin convertir el Excel en modelo de datos

**Para:** acelerar el onboarding de un frente descubriendo columnas y valores

### Alcance

**Cubre**

- Mapeo asistido columna→catálogo
- Sugerencias de alta
- Confirmación humana

**No cubre**

- Persistir filas Excel como tablas espejo
- Reemplazar la grilla por Excel

### Reglas de negocio

1. El Excel es fuente de descubrimiento, no esquema de BD.
2. Nada se crea sin confirmación del usuario autorizado.

### Criterios de aceptación

**CA01 — Sugerencia**

Dado que Excel con columnas de turnos

Cuando se procesa

Entonces sugiere plantillas candidatas

**CA02 — Confirmación**

Dado que hay sugerencias

Cuando usuario confirma un subconjunto

Entonces solo ese subconjunto se crea en catálogos

**CA03 — Tenant**

Dado que import

Cuando persiste

Entonces bajo la empresa del usuario

**CA04 — No espejo**

Dado que import termina

Cuando se inspecciona modelo

Entonces no existe tabla que replique el Excel crudo como fuente operativa

### Dependencias

- HUs: MT-EP01-HU11..HU19
- Microservicios / GRH: Malla

---
