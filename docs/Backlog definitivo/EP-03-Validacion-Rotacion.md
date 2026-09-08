# EP-03 — Validación, cobertura y rotación

## Índice

- MT-EP03-HU43 — Visualizar indicadores de cobertura y contadores
- MT-EP03-HU44 — Visualizar equilibrio de turnos por persona
- MT-EP03-HU45 — Evaluar y mostrar conflictos de validación en grilla
- MT-EP03-HU46 — Definir patrón de rotación genérico
- MT-EP03-HU47 — Vincular patrón de rotación a grupo y periodo
- MT-EP03-HU48 — Simular patrón de rotación antes de aplicar
- MT-EP03-HU49 — Excluir personas o celdas de la rotación
- MT-EP03-HU50 — Aplicar resultado de rotación a la malla
- MT-EP03-HU51 — Construcción asistida de asignaciones
- MT-EP03-HU52 — Distribuir breaks y almuerzos según plantillas y reglas
- MT-EP03-HU53 — Rotar sitios de asistencia según configuración
- MT-EP03-HU54 — Reequilibrar cargas tras una novedad
- MT-EP03-HU55 — Aplicar restricciones y motor de reglas al rotar o asignar
- MT-EP03-HU56 — Ajustar manualmente tras rotación o sugerencia

---
## MT-EP03-HU43 — Visualizar indicadores de cobertura y contadores

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** ver indicadores de cobertura y contadores calculados según las reglas y plantillas del frente

**Para:** detectar faltantes o excesos sin fórmulas fijas por operación

### Alcance

**Cubre**

- Contadores por dimensiones habilitadas
- Actualización al cambiar celdas de la ventana

**No cubre**

- Definir reglas de cobertura (HU24)

### Reglas de negocio

1. Los contadores se derivan de reglas HU24 y turnos/estados del catálogo, no de fórmulas Excel de un frente.
2. Personas con estado que no afecta cobertura no cuentan.

### Criterios de aceptación

**CA01 — Vista**

Dado que existen reglas de cobertura

Cuando abre indicadores

Entonces muestra min/max/actual por dimensión configurada

**CA02 — Recalc**

Dado que cambia una celda relevante

Cuando guarda

Entonces actualiza indicadores afectados

**CA03 — Capacidad**

Dado que dimensión no habilitada

Cuando abre indicadores

Entonces no muestra esa dimensión

**CA04 — Tenant**

Dado que consulta

Cuando datos

Entonces solo su empresa

### Dependencias

- HUs: MT-EP01-HU24, MT-EP02-HU35
- Microservicios / GRH: Malla

---

## MT-EP03-HU44 — Visualizar equilibrio de turnos por persona

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** ver distribución de plantillas/estados por persona en el periodo según métricas configurables

**Para:** apoyar decisiones de equidad sin umbrales quemados

### Alcance

**Cubre**

- Métricas de distribución configurables

**No cubre**

- Forzar equilibrio automático

### Reglas de negocio

1. Los umbrales de desequilibrio son reglas parametrizables (advertencia/bloqueo).
2. No existe una métrica única hardcodeada por frente.

### Criterios de aceptación

**CA01 — Vista**

Dado que malla con asignaciones

Cuando abre equilibrio

Entonces lista métricas por persona

**CA02 — Regla**

Dado que se supera umbral configurado

Cuando evalúa

Entonces marca hallazgo con severidad

**CA03 — Permisos**

Dado que LEER

Cuando consulta

Entonces permitido

**CA04 — Tenant**

Dado que datos

Cuando aislados

Entonces OK

### Dependencias

- HUs: MT-EP01-HU25, MT-EP02-HU35
- Microservicios / GRH: Malla

---

## MT-EP03-HU45 — Evaluar y mostrar conflictos de validación en grilla

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** ejecutar el motor de reglas y mostrar hallazgos en la grilla y un panel de conflictos

**Para:** corregir problemas antes de publicar

### Alcance

**Cubre**

- Listado de hallazgos
- Navegación a celda
- Filtro por severidad

**No cubre**

- Administrar reglas (HU25)
- Usar constantes numéricas de negocio en UI

### Reglas de negocio

1. Los mensajes muestran el nombre de la regla y sus parámetros, no constantes de producto.
2. Bloqueos impiden publicar si la config de publicación exige cero bloqueos.

### Criterios de aceptación

**CA01 — Eval**

Dado que hay violaciones

Cuando ejecuta validación

Entonces lista hallazgos con severidad

**CA02 — Navegar**

Dado que selecciona un hallazgo

Cuando hace clic

Entonces enfoca la celda

**CA03 — Filtro**

Dado que filtra solo bloqueos

Cuando aplica

Entonces oculta info/advertencias

**CA04 — Sin hardcode**

Dado que regla max_hours_period=N

Cuando muestra mensaje

Entonces incluye N desde la regla

**CA05 — Tenant**

Dado que validación

Cuando solo malla propia

Entonces OK

### Dependencias

- HUs: MT-EP01-HU25, MT-EP02-HU35
- Microservicios / GRH: Malla

---

## MT-EP03-HU46 — Definir patrón de rotación genérico

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización

**Quiero:** crear patrones como secuencia ordenada de elementos (turno/estado), cada uno con duración, formando un ciclo

**Para:** representar cualquier rotación (incluidos ejemplos 15/15 o 2×1) sin tipos enum de patrón

### Alcance

**Cubre**

- CRUD patrón
- Secuencia + duraciones + ciclo
- Fecha inicio de anclaje
- Respeto opcional de restricciones

**No cubre**

- Enums FIFTEEN_FIFTEEN / TWO_ONE
- Aplicar a malla (HU50)

### Reglas de negocio

1. Un patrón es solo datos: secuencia, duraciones, ciclo, prioridad, vigencia.
2. No existen tipos de patrón de producto.
3. Ejemplos de negocio son seeds o instancias.

### Criterios de aceptación

**CA01 — Alta**

Dado que define secuencia de plantillas con duraciones

Cuando guarda

Entonces patrón reutilizable en la empresa

**CA02 — Ciclo**

Dado que secuencia completa

Cuando se consulta longitud de ciclo

Entonces es la suma de duraciones

**CA03 — Sin enum**

Dado que lista tipos de patrón del sistema

Cuando consulta

Entonces no hay tipos especiales; solo patrones creados

**CA04 — Tenant**

Dado que patrón ajeno

Cuando invisible

Entonces OK

**CA05 — Inactivo**

Dado que patrón inactivo

Cuando aplicar

Entonces no ofrecido

### Dependencias

- HUs: MT-EP01-HU11, MT-EP01-HU14
- Microservicios / GRH: Malla

---

## MT-EP03-HU47 — Vincular patrón de rotación a grupo y periodo

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** asociar un patrón a una malla o subconjunto de personas y un rango de fechas

**Para:** preparar la simulación/aplicación controlada

### Alcance

**Cubre**

- Vínculo patrón↔malla/grupo/fechas

**No cubre**

- Aplicar sin simular

### Reglas de negocio

1. Solo si la estrategia del frente es asistida o automática.
2. El vínculo no modifica celdas hasta aplicar (HU50) tras simulación (HU48).

### Criterios de aceptación

**CA01 — Vínculo**

Dado que patrón activo y estrategia permite

Cuando asocia a grupo/fechas

Entonces queda listo para simular

**CA02 — Estrategia manual**

Dado que frente manual

Cuando intenta vincular auto

Entonces acción no disponible

**CA03 — Alcance**

Dado que personas fuera de malla

Cuando asocia

Entonces rechaza

**CA04 — Tenant**

Dado que patrón otra empresa

Cuando rechaza

Entonces OK

### Dependencias

- HUs: MT-EP03-HU46, MT-EP01-HU10, MT-EP02-HU29
- Microservicios / GRH: Malla

---

## MT-EP03-HU48 — Simular patrón de rotación antes de aplicar

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** ejecutar un dry-run del patrón que muestre asignaciones propuestas y conflictos sin alterar la malla

**Para:** revisar el impacto antes de escribir

### Alcance

**Cubre**

- Resultado simulado
- Lista de conflictos
- Diff propuesto

**No cubre**

- Persistir simulación como malla real sin confirmación

### Reglas de negocio

1. La simulación no escribe celdas.
2. Debe mostrar qué sería automático y qué queda excluido (HU49).

### Criterios de aceptación

**CA01 — Dry-run**

Dado que vínculo válido

Cuando simula

Entonces muestra propuesta sin cambiar malla

**CA02 — Conflictos**

Dado que hay violaciones

Cuando simula

Entonces lista conflictos detectados

**CA03 — Exclusiones**

Dado que personas excluidas

Cuando simula

Entonces no propone cambios para ellas

**CA04 — Reintentar**

Dado que ajusta parámetros

Cuando vuelve a simular

Entonces actualiza propuesta

**CA05 — Permisos**

Dado que sin ACTUALIZAR

Cuando simula si LEER+política lo permite o niega escritura posterior

Entonces según permisos

### Dependencias

- HUs: MT-EP03-HU47, MT-EP03-HU49, MT-EP01-HU25
- Microservicios / GRH: Malla

---

## MT-EP03-HU49 — Excluir personas o celdas de la rotación

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** marcar personas o celdas concretas para que la rotación asistida/automática no las modifique

**Para:** proteger excepciones operativas

### Alcance

**Cubre**

- Exclusiones por persona, rango o celda

**No cubre**

- —

### Reglas de negocio

1. Las exclusiones son tenant-scoped y auditables.
2. Celdas excluidas conservan su valor actual al aplicar.

### Criterios de aceptación

**CA01 — Excluir persona**

Dado que grupo vinculado

Cuando marca exclusión

Entonces simulación no la altera

**CA02 — Excluir celda**

Dado que día específico

Cuando excluye

Entonces propuesta la omite

**CA03 — Quitar exclusión**

Dado que había exclusión

Cuando quita

Entonces vuelve a participar

**CA04 — Tenant**

Dado que exclusión

Cuando propia empresa

Entonces OK

### Dependencias

- HUs: MT-EP03-HU47
- Microservicios / GRH: Malla

---

## MT-EP03-HU50 — Aplicar resultado de rotación a la malla

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** aplicar la propuesta simulada aceptada, marcando origen automático y dejando historial

**Para:** materializar la rotación de forma trazable

### Alcance

**Cubre**

- Aplicación atómica o por lote con reporte
- Origen=automático
- Historial

**No cubre**

- Aplicar sin simulación previa si la config exige dry-run

### Reglas de negocio

1. Toda celda escrita por rotación registra origen automático.
2. Ajustes posteriores manuales cambian origen a manual (HU56).
3. Se revalidan reglas; bloqueos impiden aplicar esas celdas.

### Criterios de aceptación

**CA01 — Aplicar**

Dado que simulación aceptada sin bloqueos críticos

Cuando aplica

Entonces celdas actualizadas con origen automático

**CA02 — Parcial**

Dado que algunas celdas bloqueadas

Cuando aplica

Entonces omite bloqueadas y reporta

**CA03 — Historial**

Dado que celda cambia

Cuando consulta historial

Entonces antes/después + origen automático

**CA04 — Sin simulación**

Dado que config exige dry-run

Cuando aplica directo

Entonces rechaza

**CA05 — Notificación**

Dado que si flags de estado/config lo requieren

Cuando aplica

Entonces despacha eventos HU07

### Dependencias

- HUs: MT-EP03-HU48, MT-EP05-HU62, MT-EP00-HU07
- Microservicios / GRH: Malla; notification

---

## MT-EP03-HU51 — Construcción asistida de asignaciones

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** obtener sugerencias de asignación según la estrategia asistida del frente y aceptarlas o modificarlas

**Para:** acelerar el armado sin perder control humano

### Alcance

**Cubre**

- Sugerencias de turnos/cobertura/descansos/sitios según config
- Aceptar/rechazar por celda o lote

**No cubre**

- Estrategia automática plena sin revisión

### Reglas de negocio

1. Solo si estrategia=asistida (o automática con paso de revisión).
2. Sugerir ≠ aplicar; aplicar genera origen asistido/automático.

### Criterios de aceptación

**CA01 — Sugerir**

Dado que estrategia asistida

Cuando solicita sugerencias

Entonces recibe propuesta

**CA02 — Aceptar**

Dado que selecciona subconjunto

Cuando acepta

Entonces escribe celdas elegidas

**CA03 — Modificar**

Dado que ajusta una sugerencia

Cuando guarda

Entonces origen manual o asistido según diseño

**CA04 — Estrategia**

Dado que manual

Cuando sugerir

Entonces no disponible

### Dependencias

- HUs: MT-EP01-HU10, MT-EP01-HU25, MT-EP03-HU46
- Microservicios / GRH: Malla

---

## MT-EP03-HU52 — Distribuir breaks y almuerzos según plantillas y reglas

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** proponer o aplicar distribución de pausas cuando el frente y las plantillas lo definen

**Para:** evitar solapes de pausas que rompan cobertura si hay reglas

### Alcance

**Cubre**

- Distribución asistida de pausas

**No cubre**

- Pausas hardcodeadas por frente

### Reglas de negocio

1. Depende de HU13 y reglas de cobertura en franja de pausa.

### Criterios de aceptación

**CA01 — Distribuir**

Dado que plantillas con pausas y capacidad on

Cuando ejecuta

Entonces propone horarios de pausa

**CA02 — Conflicto cobertura**

Dado que regla de cobertura en pausa

Cuando evalúa

Entonces hallazgo con severidad

**CA03 — Off**

Dado que sin pausas en plantillas

Cuando acción

Entonces no aplica

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU13, MT-EP01-HU24, MT-EP03-HU51
- Microservicios / GRH: Malla

---

## MT-EP03-HU53 — Rotar sitios de asistencia según configuración

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** aplicar un patrón o política de rotación de sitios cuando la capacidad está habilitada

**Para:** alternar ubicaciones sin reglas fijas por nombre de sitio

### Alcance

**Cubre**

- Rotación de sitios parametrizable

**No cubre**

- —

### Reglas de negocio

1. Sitios son catálogo; la secuencia es configuración.

### Criterios de aceptación

**CA01 — Aplicar**

Dado que capacidad sitio on y patrón de sitios

Cuando simula/aplica

Entonces asigna sitios según secuencia

**CA02 — Exclusión**

Dado que persona excluida

Cuando aplica

Entonces no cambia sitio

**CA03 — Off**

Dado que capacidad off

Cuando acción ausente

Entonces OK

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU18, MT-EP03-HU46, MT-EP03-HU48
- Microservicios / GRH: Malla

---

## MT-EP03-HU54 — Reequilibrar cargas tras una novedad

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** obtener sugerencias de reasignación cuando una novedad deja huecos de cobertura

**Para:** recuperar cobertura sin rearmar toda la malla a ciegas

### Alcance

**Cubre**

- Sugerencias post-novedad

**No cubre**

- Borrar historial de la novedad

### Reglas de negocio

1. Se dispara tras HU60 según estrategia del frente.
2. No hardcodea tipos de novedad.

### Criterios de aceptación

**CA01 — Hueco**

Dado que estado no afecta cobertura deja min incumplido

Cuando solicita reequilibrio

Entonces sugiere candidatos

**CA02 — Aceptar**

Dado que elige sugerencia

Cuando aplica

Entonces historial con origen asistido

**CA03 — Estrategia**

Dado que manual sin asistida

Cuando reequilibrio auto

Entonces no disponible o solo aviso

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP05-HU60, MT-EP03-HU51, MT-EP01-HU24
- Microservicios / GRH: Malla

---

## MT-EP03-HU55 — Aplicar restricciones y motor de reglas al rotar o asignar

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** que toda asignación manual, asistida o automática pase por restricciones de persona y reglas del frente

**Para:** impedir propuestas inválidas

### Alcance

**Cubre**

- Integración restricciones HU19 + motor HU25 en todos los flujos de escritura

**No cubre**

- —

### Reglas de negocio

1. Bloqueo de restricción impide propuesta/guardado.
2. Advertencia requiere confirmación cuando la UI lo permita.

### Criterios de aceptación

**CA01 — Bloqueo**

Dado que restricción vigente incompatible

Cuando asigna o simula

Entonces no propone/guarda ese turno

**CA02 — Rotación**

Dado que patrón caería en turno prohibido

Cuando simula

Entonces marca conflicto o excluye

**CA03 — Manual**

Dado que mismo control

Cuando guarda celda

Entonces idéntica evaluación

**CA04 — Tenant**

Dado que restricción ajena

Cuando no aplica

Entonces OK

### Dependencias

- HUs: MT-EP01-HU19, MT-EP01-HU25, MT-EP02-HU30, MT-EP03-HU48
- Microservicios / GRH: Malla

---

## MT-EP03-HU56 — Ajustar manualmente tras rotación o sugerencia

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** modificar celdas después de una aplicación automática/asistida, dejando trazabilidad de origen manual

**Para:** permitir excepciones humanas controladas

### Alcance

**Cubre**

- Edición post-aplicación
- Cambio de origen a manual
- Historial

**No cubre**

- —

### Reglas de negocio

1. El ajuste manual revalida reglas.
2. Si la malla está publicada, aplican políticas HU59.

### Criterios de aceptación

**CA01 — Ajuste**

Dado que celda origen automático

Cuando cambia turno

Entonces origen pasa a manual y hay historial

**CA02 — Regla**

Dado que ajuste inválido

Cuando guarda

Entonces aplica severidad

**CA03 — Publicada**

Dado que editabilidad off

Cuando intenta

Entonces niega o exige flujo HU59

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP03-HU50, MT-EP02-HU30, MT-EP05-HU62, MT-EP04-HU59
- Microservicios / GRH: Malla

---
