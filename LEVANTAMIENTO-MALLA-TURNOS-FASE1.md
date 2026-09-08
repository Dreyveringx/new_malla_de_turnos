# Levantamiento de requisitos — Módulo Malla de turnos

| Campo | Valor |
| ----- | ----- |
| **Fase** | 1 — Elicitación / análisis de requisitos |
| **Producto** | Plataforma GRH (`gestionrrhh`) |
| **Módulo** | Malla de turnos |
| **Fuente** | Reunión 27-ago-2026 (1 h 29 min) + notas de sesión |
| **Elaborado por** | Jair Uribe |
| **Estado** | Borrador para validación de negocio — **no es diseño ni alcance cerrado** |
| **Próxima sesión** | Semana del 7–11 sep 2026 (jueves, ciclo quincenal) |

> Este documento convierte la reunión en proceso actual, actores, reglas, requisitos y pendientes.  
> Debe validarse con Contact Center, Soporte técnico / Mesa y Mesa de segundo nivel **antes** de historias de usuario y mockups.

---

## 1. Propósito de esta fase

Entender cómo se programa hoy, qué reglas aplican, qué duele y qué se espera del módulo.  
No se compromete automatización de malla óptima ni diseño de pantallas: se fija el problema.

**Entregable de esta fase:** requisitos funcionales + no funcionales + reglas + actores + excepciones + vacíos a cerrar.

---

## 2. Hallazgo principal

No hay **una** malla de turnos. Hay **varios frentes operativos** con la misma necesidad (asignar persona + día + turno + estado) y reglas distintas.

| Frente | Quién construye | Quién revisa / aprueba | Horizonte | Ritmo de cambio |
| ------ | --------------- | ---------------------- | --------- | --------------- |
| Contact Center | Supervisoras | Coordinador (Oscar) | Mensual, enviada ~1 semana antes | Ajustes puntuales por novedad |
| Soporte en sitio | Coordinadores (Freddy / Luis) | Coordinadores | Semanal (viernes) | Cambios **diarios** |
| Mesa de soporte técnico | Coordinadores / William | Coordinadores | Mensual posible | Cambios **diarios** |
| Laboratorio | Coordinador laboratorio | Coordinador | Apoyo a cobertura (sábados Bogotá) | Según novedad |
| Mesa de segundo nivel | *(pendiente Andrés / Ricardo)* | *(pendiente)* | *(pendiente)* | Intercambio entre compañeros |

**Implicación de producto:** un módulo parametrizable por **área / frente**, no un Excel único copiado a pantalla.

---

## 3. Proceso actual (AS-IS)

### 3.1 Contact Center

1. Supervisoras arman la malla en Excel (plantilla de Oscar).
2. Coordinador revisa y envía ~1 semana antes del mes.
3. Operadores reciben la malla **completa del grupo** (pública para el equipo).
4. Colores y letras marcan: vacaciones, domingo, festivo, Data Service, pagos de gobierno, línea de soporte, “canguro”, compensatorio, capacitación, incapacidad, etc.
5. Breaks (franja 18:00–22:00) y almuerzos se programan **una vez al mes** para no afectar operación.
6. Hay contadores: cuántas personas por turno, mañana / intermedio / tarde, total.
7. Rotación: no repetir el mismo tipo de turno semana tras semana; equilibrar cargas del mes.
8. Día a día las supervisoras registran novedades (otro formato de nómina de TH) y **actualizan la celda** de la malla (ej. turno 5 → incapacidad).
9. Al corte, Oscar cruza malla vs novedades de nómina (validación OK / mal).
10. Se envían a nómina: horas extras festivas diurnas/nocturnas y recargo nocturno.
11. Asistencia a sede **Elemento**: rotación semanal/mensual; excepción: una persona puede ir **todo el mes** por reforzamiento (sin pantalla de indicadores).

### 3.2 Soporte técnico (sitio, mesa, laboratorio)

1. Soporte en sitio: Excel con **9 turnos** (lun–vie, lun–sáb, domingo/festivo).
2. Programación por **regional / zona** (Bogotá, Cundinamarca) y **SPT**.
3. Bogotá: ~3 técnicos por regional, ~40 técnicos. Más complejo que Cundinamarca (3–4 turnos).
4. Si un técnico descansa sábado en Bogotá, se cubre con laboratorio o mesa (coordinación entre coordinadores).
5. El viernes se **envía** el horario semanal; el archivo se mantiene **en línea** porque hay novedades todos los días.
6. Los técnicos se contratan para una zona, pero en Bogotá **rotan entre zonas** según necesidad.
7. Mesa consulta **en tiempo real** quién está en turno / zona / SPT para asignar casos.
8. Un técnico puede cubrir **dos turnos el mismo día** → se contabiliza como horas extra (ej. 07:00–20:00).
9. Solo coordinadores modifican. Analistas y técnicos no.
10. Estados: descanso (DES), incapacidad, capacitación, permiso, **actividad** (está ocupado, no recibe casos aunque no esté en la malla de turno).
11. Jornada de referencia: **42 h semanales**. Quien descansa sábado incrementa horas lun–vie; quien trabaja sábado reduce lun–vie.
12. Domingos/festivos: un técnico por regional y uno en municipios; horario típico Bogotá 07:00–20:00.
13. Mesa: 06:00–21:00. Patrón de descansos soporte técnico: **2 trabajan / 1 descansa**.
14. Rotación deseada: 15 días mañana + 15 días tarde, excepto quien estudia (se deja en día).
15. Directores y analistas de SPT necesitan ver qué recurso técnico hay en cada punto.

### 3.3 Mesa de segundo nivel

Mencionado, **no levantado**. Tienen malla visible porque intercambian turnos entre compañeros. Requiere sesión propia.

---

## 4. Qué es una “malla” para el negocio

Una malla **no** es solo Empleado → Día → Turno.

Para ellos incluye:

```
Empresa → Área / frente operativo → (Regional / Zona / SPT)* → Grupo de personas
        → Periodo (semana | mes)
        → Por cada persona y día: turno | estado | (sede / modalidad)* | (campaña / tarea)*
        → Cobertura (cuántos por franja)
        → Novedades y horas para nómina
```

\* Aplica según el frente (sitio vs Contact Center).

**Definición de trabajo (a validar):**

> Malla = programación de un **grupo de empleados de un área** para un **periodo**, donde cada celda (persona × día) tiene un **turno plantilla** o un **estado**, y puede llevar atributos extra (zona, SPT, sede física, campaña, break, almuerzo).

---

## 5. Actores y permisos (borrador)

| Actor | Qué hace hoy | Qué debería poder (propuesto) |
| ----- | ------------ | ----------------------------- |
| Supervisora Contact Center | Crea y ajusta celdas; registra novedades diarias | Crear/editar borrador; aplicar cambios puntuales; registrar novedad |
| Coordinador Contact Center | Revisa, aprueba, envía, cruza nómina | Revisar/aprobar/publicar; ver conflictos; generar reporte nómina |
| Coordinador soporte / mesa / lab | Construye, cambia en línea, cubre zonas | Crear/editar/publicar; cambio inmediato; buscar disponibilidad |
| Analista de mesa | Consulta quién está en turno/zona/SPT | **Solo consulta en tiempo real** (no editar) |
| Director / analista SPT | Recibe Excel de recursos | Consultar o recibir exportación de cobertura |
| Operador / técnico | Recibe malla del grupo | Ver malla del grupo + la propia; recibir notificación de cambio |
| Talento humano / nómina | Recibe horas y novedades | Recibir/exportar reporte de horas (no opera la malla) |
| Empleado con permiso de estudio | Restricción de turno diurno | El sistema debe respetar restricción (regla, no pantalla aparte) |

**Confirmado:** el empleado **no acepta** el cambio. Queda registro + notificación informativa.

**Confirmado:** no hace falta versionar la malla completa. El cambio es **puntual** con historial (valor anterior, valor nuevo, quién, cuándo, motivo).

---

## 6. Alcance

### 6.1 Dentro (MVP de negocio, no de sprint)

- Parametrizar turnos reutilizables por área/empresa (código, horario, color, cruce de medianoche, break, almuerzo).
- Construir malla por área/grupo y periodo (semana y mes).
- Asignar turno o estado por persona y día.
- Rotación y cobertura como **apoyo al armado** (contadores, equilibrio), no como motor de optimización automática.
- Novedades: vacaciones, incapacidad, permiso, descanso, capacitación, actividad, compensatorio, día libre.
- Cambio posterior a publicar: inmediato, auditado, notificado.
- Consulta en tiempo real: persona / zona / SPT / quién está disponible ahora.
- Vista pública de la malla del grupo + vista personal.
- Exportar (Excel como mínimo).
- Reporte de horas para nómina (festivas, recargo nocturno, extras).
- Asignar asistencia física a sede (Elemento) por semana o mes completo, con rotación y excepciones.

### 6.2 Fuera de esta fase / no comprometido

- Generación automática de “malla óptima” para N personas (rotación + vacaciones + máximos + disponibilidad).
- Pantalla de indicadores de desempeño (Ricardo: **no**).
- Flujo empleado → solicitud de cambio → aprobación (mencionado, no pedido como necesidad actual).
- Cálculo de valor a pagar (nómina solo recibe **horas**, no liquidación).
- Personal de fábrica (otro frente; sesión con Coronado).
- Mesa de segundo nivel (sesión pendiente).
- Reportería gráfica avanzada (Ricardo pidió espacio aparte).
- Integración bidireccional automática con el formato Excel de novedades de TH (hoy es cruce manual; se toma como requerimiento a evaluar).

---

## 7. Requisitos funcionales

Convención: **RF** = debe; **RF-D** = deseable / segunda ola; **Pend** = no cerrado.

Prioridad: **P0** imprescindible para reemplazar Excel del frente; **P1** necesario para operación diaria; **P2** valor; **P3** posterior.

### 7.1 Parametrización

| ID | Requisito | Prioridad | Fuente |
| -- | --------- | --------- | ------ |
| RF-01 | El sistema permite crear **plantillas de turno** reutilizables (no se inventan solo dentro de cada malla): código/número, nombre, hora inicio/fin, duración, color, si cruza medianoche, si es nocturno, días de aplicación (lun–vie, lun–sáb, domingo/festivo). | P0 | Sitio (9 turnos), CC (1–12) |
| RF-02 | Los turnos se parametrizan **por empresa y por área/frente**. No se asume un catálogo único para toda la plataforma. | P0 | Multi-frente + fábrica pendiente |
| RF-03 | Un turno puede tener **horas distintas según el día** (ej. lun–jue 07:00–15:30, vie hasta las 16:00, sáb 8 h). | P0 | Turno 8 / 6 / 5 / 4 de sitio |
| RF-04 | El turno puede incluir **break** (inicio/fin) y/o **almuerzo** (inicio/fin). | P0 | CC breaks 18–22; mesa almuerzo por turno |
| RF-05 | Deben existir **estados de celda** distintos de un horario: DES/descanso, incapacidad, permiso, capacitación, vacaciones, actividad, día libre, compensatorio, compensatorio no remunerado, inactividad, reemplazo por incapacidad, otros. | P0 | Sitio + CC |
| RF-06 | Los estados son parametrizables (código letra, color, si suma horas, si la persona está asignable a casos). | P0 | Letras de Oscar; “actividad” no recibe casos |
| RF-07 | Festivos se toman del **calendario de empresa** ya existente en parametrización. | P1 | Plataforma actual + colores CC |
| RF-08 | Deben poder parametrizarse **campañas / tareas** que colorean o etiquetan la celda (Data Service, pagos de gobierno, línea de soporte, canguro) **sin** ser un turno distinto. | P1 | CC |
| RF-09 | Deben poder parametrizarse **regionales, zonas y SPT** para soporte en sitio. | P0 | Sitio / mesa |

### 7.2 Construcción de la malla

| ID | Requisito | Prioridad | Fuente |
| -- | --------- | --------- | ------ |
| RF-10 | Crear malla con: nombre, empresa, área/frente, periodo (inicio–fin), responsable (usuario en sesión). | P0 | Prototipo + proceso |
| RF-11 | El periodo puede ser **semanal o mensual** según el frente. | P0 | Sitio semanal; CC mensual |
| RF-12 | Seleccionar el grupo de empleados que entran a la malla (ya existen en la plataforma; no se dan de alta aquí). | P0 | Empleados actuales |
| RF-13 | Asignar por celda (empleado × día): un turno, un estado, o turno + etiqueta de campaña/tarea. | P0 | Excel actual |
| RF-14 | Permitir **más de un turno el mismo día** para un empleado, marcándolo como extra. | P0 | Sitio: turno 1 + 3 |
| RF-15 | Asignar zona / SPT / regional a la celda o a la persona en el periodo (un técnico puede cambiar de zona día a día). | P0 | “Hoy Jennifer en norte, mañana otra zona” |
| RF-16 | Asignar **modalidad / sede del día**: presencial (Elemento u otra), virtual, híbrido. | P1 | CC Elemento; mixto virtual/presencial |
| RF-17 | Fijar a una o varias personas **asistencia física un mes completo** (reforzamiento), sin módulo de indicadores. | P1 | Ricardo |
| RF-18 | Vista tipo grilla (persona × días) con colores por turno, estado, festivo, domingo, campaña. | P0 | Excel Oscar / Freddy |
| RF-19 | Contadores en vivo al armar: personas por turno, por franja (mañana / intermedio / tarde), total del día. | P0 | Fórmulas de Oscar |
| RF-20 | Resumen de **cuántas veces** cada persona tuvo cada turno en el periodo (equilibrio de carga). | P1 | Rotación CC |
| RF-21 | Detectar y mostrar **conflictos** (solape, sin turno, cobertura insuficiente, breaks pegados). | P1 | Prototipo + CC breaks |
| RF-22 | Copiar semana, copiar patrón de rotación, asignación masiva. | P2 | Dolor de Excel; no detallado aún |
| RF-23 | Respetar restricciones de persona: estudia (solo diurno), restricción de salud (no va a oficina). | P1 | Sitio + Elemento |

### 7.3 Flujo de estados de la malla

| ID | Requisito | Prioridad | Fuente |
| -- | --------- | --------- | ------ |
| RF-24 | Estados de malla: **Borrador → En revisión → Publicada**. Rechazo devuelve a borrador. | P1 | CC: supervisora crea, coordinador aprueba |
| RF-25 | En soporte, la malla publicada **sigue editable** por coordinadores (operación en línea). | P0 | “No es fijo lo enviado el viernes” |
| RF-26 | Quien publica no tiene que ser quien construye (CC: sí hay separación; sitio: coordinadores hacen ambos). Configurable por área. | P1 | Dos modelos |

### 7.4 Cambios, novedades y auditoría

| ID | Requisito | Prioridad | Fuente |
| -- | --------- | --------- | ------ |
| RF-27 | Tras publicar, un coordinador/supervisora puede cambiar **una celda** sin generar una malla nueva. | P0 | William / Freddy |
| RF-28 | Todo cambio guarda historial: empleado, fecha, valor anterior, valor nuevo, usuario, fecha/hora, motivo. | P0 | Pedido explícito |
| RF-29 | Notificar al empleado (plataforma + correo) de forma **informativa**; no requiere aceptación. | P0 | William |
| RF-30 | Incapacidad / permiso / vacaciones: la celda se reemplaza por el estado y **deja de sumar** horas, extras y recargos. | P0 | Oscar |
| RF-31 | Si la novedad es el mismo día, el cambio es **inmediato** (cobertura de zona, no asignar casos). | P0 | Sitio / mesa |
| RF-32 | Nota / observación en la celda (qué pasó con el operador). | P1 | Oscar |
| RF-33 | Novedades diarias registradas por supervisoras, alineadas a cortes de nómina. | P0 | CC |
| RF-34 | Al corte, poder **cruzar** programación vs novedades reportadas a TH y señalar inconsistencias. | P2 | Validación OK/mal de Oscar |

### 7.5 Consulta operativa (tiempo real)

| ID | Requisito | Prioridad | Fuente |
| -- | --------- | --------- | ------ |
| RF-35 | Buscar por técnico, zona o SPT y ver **ahora**: horario, zona, si está en turno, si está disponible (no DES / no actividad / no incapacidad). | P0 | William / Freddy — analistas de mesa |
| RF-36 | Listar cobertura del día: “quién está en SPT Restrepo en este momento”. | P0 | ~40 técnicos |
| RF-37 | Estado **actividad** = persona ocupada (mantenimiento u otra) y **no asignable** a casos, aunque no tenga turno de operación. | P0 | Freddy |

### 7.6 Vista del empleado

| ID | Requisito | Prioridad | Fuente |
| -- | --------- | --------- | ------ |
| RF-38 | Ver **la malla del grupo** (pública para integrantes del frente). | P0 | Ricardo: debe ser pública |
| RF-39 | Ver su programación: día, semana, mes, próximo turno, horario, sede, descansos. | P0 | Pregunta 10 + prototipo |
| RF-40 | Ver historial de cambios de **sus** turnos. | P1 | “Que le quede registro” |
| RF-D-41 | Solicitar cambio / intercambio de turno. | P3 | Segundo nivel; no pedido como actual |

### 7.7 Nómina y reportes

| ID | Requisito | Prioridad | Fuente |
| -- | --------- | --------- | ------ |
| RF-42 | Calcular, a partir del turno asignado, horas: ordinarias, extra, festiva diurna, festiva nocturna, recargo nocturno. | P0 | Oscar: “solo enviamos horas” |
| RF-43 | Respetar **cortes de nómina** (rangos de fechas configurables, ej. 7–21). | P0 | Hoja “pago de nómina” |
| RF-44 | Compensatorios: regla de 3 domingos trabajados en el mes; otros (voto, familia) parametrizables. **Pendiente** impacto de reducción de jornada. | P1 | Oscar |
| RF-45 | Exportar malla y reportes a **Excel**. PDF/impresión: P2. | P0 / P2 | Uso actual |
| RF-46 | Reporte de horas de incapacidad vs horas operativas del periodo (total e individual). | P1 | Ricardo CC |
| RF-47 | Reporte de horas no cubiertas por vacaciones (impacto de capacidad). | P1 | Ricardo CC |
| RF-48 | Reporte de horas extra desde el horario (soporte). | P1 | William sobre el proceso de Luis |
| RF-49 | Compartir / exportar cobertura para directores y analistas SPT. | P1 | Freddy cierre |
| RF-D-50 | Gráficos de reportería. | P3 | Sesión aparte de informes |

### 7.8 Rotación y cobertura (sin optimizar automáticamente)

| ID | Requisito | Prioridad | Fuente |
| -- | --------- | --------- | ------ |
| RF-51 | Apoyar rotación: avisar si una persona repite el mismo tipo de turno semana a semana. | P1 | CC |
| RF-52 | Apoyar patrón 15 días mañana / 15 tarde (sitio), con excepción por estudio. | P2 | Luis |
| RF-53 | Apoyar patrón 2×1 de descansos (soporte técnico). | P2 | Freddy |
| RF-54 | Cubrir sábado: poder asignar recurso de **otra área** (laboratorio o mesa) a la malla de sitio. | P0 | Bogotá |
| RF-55 | Distribuir breaks para que no coincidan entre compañeros en la misma franja. | P1 | CC 18:00–22:00 |
| RF-56 | Rotar quién asiste a sede física, salvo restricciones. | P1 | Elemento |
| RF-D-57 | Generar automáticamente la malla completa. | Fuera | No comprometer |

---

## 8. Reglas de negocio

Clave: **bloquea** vs **advierte**. En la reunión **no se cerró** el criterio. Propuesta para validar:

| ID | Regla | Propuesta | Frente |
| -- | ----- | --------- | ------ |
| RN-01 | Un empleado puede tener dos turnos el mismo día. | Permitir + marcar extra | Sitio |
| RN-02 | Solape horario real (misma hora, dos turnos). | **Bloquear** | Todos |
| RN-03 | Semana de referencia 42 h. Descanso sábado ⇒ más horas lun–vie; trabajo sábado ⇒ menos lun–vie. | Advertir si no cierra 42 h | Sitio |
| RN-04 | Domingos/festivos: cobertura mínima (1 técnico/regional + 1 municipios). | Advertir si falta | Sitio |
| RN-05 | Persona en DES / incapacidad / permiso / vacaciones **no** es asignable a casos. | Bloquear asignación operativa | Mesa |
| RN-06 | Persona en **actividad** no recibe casos. | Igual que RN-05 | Mesa |
| RN-07 | Breaks de un mismo tramo no deben solaparse entre operadores. | Advertir | CC |
| RN-08 | Almuerzos no pueden dejar la operación sin cobertura. | Advertir | CC / mesa |
| RN-09 | No repetir el mismo turno semana tras semana (rotación). | Advertir | CC |
| RN-10 | Estudiante: no turno que impida estudio. | Bloquear o advertir (validar) | Sitio |
| RN-11 | Restricción de salud: no forzar asistencia a oficina. | Bloquear | CC |
| RN-12 | Solo roles de coordinación/supervisión editan malla publicada. | Bloquear | Todos |
| RN-13 | Cambio de celda con estado de novedad deja de sumar horas/extras/recargos. | Sistema | CC |
| RN-14 | Si cumplió la mayoría del turno y salió temprano, se puede dejar el turno completo en malla y ajustar en novedad de nómina. | Permitir + advertir descuadre | CC |
| RN-15 | Festivo usa catálogo de turnos de domingo/festivo (CC: 6–12; sitio: turnos 7/festivo). | Sistema | CC / sitio |
| RN-16 | Un empleado puede aparecer en más de una malla del mismo periodo (cobertura sábado lab → sitio). | Permitir + **advertir** doble programación | Sitio/lab |
| RN-17 | Compensatorio por 3 domingos trabajados en el mes. | Advertir / sugerir | CC |

**Pregunta a cerrar en validación:** ¿publicar con advertencias es válido, o hay bloqueos mínimos (solape, celda vacía, 0 cobertura en un SPT)?

---

## 9. Requisitos no funcionales

| ID | Categoría | Requisito |
| -- | --------- | --------- |
| RNF-01 | Multi-tenant | Toda malla, turno y reporte va por `companyId`. Catálogos de turno **por empresa** (y por área). |
| RNF-02 | Reutilización | Empleados, áreas, cargos, calendarios/festivos, notificaciones y auditoría de la plataforma; no duplicar maestros. |
| RNF-03 | Seguridad | Autorización por rol y por área/frente. Analista de mesa: lectura. Técnico/operador: lectura de su grupo. |
| RNF-04 | Auditoría | Cambios de celda inmutables en historial (quién, cuándo, antes, después, motivo). |
| RNF-05 | Tiempo real | Consulta de “quién está en turno ahora” con datos consistentes tras un cambio (mesa asigna casos en vivo). Objetivo a acordar: visibilidad en segundos, no en el siguiente envío semanal. |
| RNF-06 | Usabilidad | Grilla comparable a Excel (color, filtros, conteos). El Excel actual es el estándar de usabilidad. |
| RNF-07 | Volumen | Contact Center: plantilla mensual de todo el grupo. Sitio: ~40 técnicos, varias regionales/SPT. |
| RNF-08 | Notificaciones | Campana de plataforma + correo en cambios de turno (módulo notification existente). |
| RNF-09 | Exportación | Excel como canal actual hacia directores, SPT y nómina. |
| RNF-10 | Trazabilidad de cortes | Cálculos de horas anclados a rangos de corte de nómina, no solo a mes calendario. |
| RNF-11 | Integridad | No borrar historial al corregir una celda; el valor vigente es uno, el histórico se acumula. |
| RNF-12 | Disponibilidad | Horario operativo amplio (sitio ~07:00–20:00; mesa 06:00–21:00; CC 06:00–22:00). La consulta de cobertura no puede “esperar al viernes”. |
| RNF-13 | Privacidad | Malla **pública dentro del grupo**; no se pidió ocultar compañeros. Validar si aplica a toda la empresa o solo al frente. |
| RNF-14 | Evolución | Parametría de turnos/estados/reglas por área para no hardcodear Contact Center vs Sitio. |
| RNF-15 | Accesibilidad de color | El color es semántica operativa; debe haber código/leyenda, no solo color. |
| RNF-16 | Desempeño de grilla | Una malla mensual de decenas de personas × ~31 días debe ser usable (filtros, scroll, edición de celda). |

---

## 10. Matriz de información (datos que necesitan para construir)

| Dato | ¿Ya existe en GRH? | Uso |
| ---- | ------------------- | --- |
| Empleado, cargo, área | Sí | Filas de la malla |
| Empresa / sede / centro de trabajo | Sí (parcial) | Filtros; Elemento |
| Calendario y festivos | Sí (`company_calendar`) | Colores y turnos festivos |
| Jornada / `work_schedule` | Sí, pero es jornada tipo, no malla operativa | **No sustituye** este módulo; se puede reutilizar concepto de turno plantilla |
| Catálogo de turnos operativos (1–12, 9 turnos sitio) | No | Parametría nueva |
| Regional / zona / SPT | No (o no al nivel que usan) | Sitio / mesa |
| Modalidad (virtual, híbrido, presencial) | Revisar catálogo empleado | Elemento / rotación |
| Vacaciones / incapacidades / permisos | Parcial / otros procesos | Integrar o registrar en malla |
| Cortes de nómina | No | Parametría nueva |
| Campañas (Data Service, gobierno, canguro) | No | Etiquetas de celda |
| Restricciones (estudio, salud) | No como regla de malla | Atributo de persona |

---

## 11. Excepciones (qué pasa cuando algo sale mal)

| Situación | Qué hacen hoy | Qué debería hacer el sistema |
| --------- | ------------- | ---------------------------- |
| Incapacidad el mismo día | Cambian la celda en el Excel en línea; cubren con otra zona/lab | Cambio inmediato + historial + notificación + persona no asignable |
| No hay recurso para un turno | Un técnico hace dos turnos (extras) | Permitir doble turno + extras; avisar cobertura |
| Descanso sábado Bogotá | Piden técnico a lab o mesa | Asignar persona de otra malla/área |
| Salida temprana con mayoría del turno | Dejan turno completo; ajustan en formato TH | Permitir descuadre controlado vs novedad |
| Olvido de actualizar malla vs novedad TH | El cruce de Oscar marca “mal” | Reporte de inconsistencias (P2) |
| Persona nueva (“canguro”) | Color/etiqueta en la malla | Etiqueta de campaña/tarea |
| Reforzamiento en Elemento | Cambian el número de turno (el de oficina) | Asignar sede mes completo; el resto de rotación sigue |
| Malla enviada el viernes ya no vale el sábado | Viven en el archivo en línea | Publicada + editable; la consulta siempre lee el vigente |

---

## 12. Respuestas a las 7 preguntas de apertura

| Pregunta | Respuesta consolidada |
| -------- | --------------------- |
| ¿Quién crea la malla? | CC: supervisoras. Sitio/mesa: coordinadores. |
| ¿Para quién? | Operadores CC; técnicos de sitio; analistas de mesa (consulta); lab (cobertura); segundo nivel (pendiente). |
| ¿Cómo la hacen hoy? | Excel (plantilla Oscar muy formulada; Excel de 9 turnos + archivo en línea). Envío semanal o mensual + cambios diarios. |
| ¿Qué información necesitan? | Personas, turnos plantilla, periodo, festivos, zonas/SPT, estados, campañas, cortes de nómina, restricciones, sede. |
| ¿Qué reglas deben cumplirse? | 42 h, cobertura mínima, rotación, breaks/almuerzos sin dejar operación, extras si doble turno, novedades no suman horas. |
| ¿Cambios y excepciones? | Edición puntual post-publicación, historial, notificación sin aceptación, cobertura cruzada entre áreas. |
| ¿Cuándo está “correcta” y lista? | CC: cobertura por franja ok, rotación equilibrada, breaks/almuerzos ok, coordinador revisó, se puede enviar 1 semana antes. Sitio: viernes enviable **y** actualizable en línea; mesa puede ver quién está ahora. Nómina: al corte, horas y novedades cuadran. |

---

## 13. Dependencias con la plataforma actual

| Módulo | Relación |
| ------ | -------- |
| Employee | Maestro de personas de la malla |
| Parameterization | Áreas, cargos, calendarios, festivos, sedes; posible extensión zona/SPT |
| Auth / roles | Permisos por frente (crear, aprobar, consultar, exportar) |
| Notification | Cambio de turno y publicación |
| Audit | Complemento al historial de celda |
| Horario laboral (`work_schedule`) | Jornada contractual ≠ programación operativa. Decisión: **nuevo dominio de malla**, reutilizando ideas de turno, sin forzar la malla dentro de `schedule_assignment` |

---

## 14. Riesgos de esta fase

1. **Unificar en exceso** Contact Center y Soporte: mismas pantallas rígidas. Mitigación: núcleo común (celda, turno, estado, historial) + parametría por frente.
2. **Prometer generación automática** de rotación óptima. El Excel de Oscar ya es un motor semimanual; automatizarlo es un proyecto aparte.
3. **Nómina** como liquidación. El alcance confirmado es **horas**, no pesos.
4. **Segundo nivel y fábrica** fuera de la reunión: el diseño prematuro los deja por fuera.
5. **“Tiempo real”** de mesa puede empujar a consulta operativa tipo tablero de despacho, más que a un Excel mensual. Hay que acotar UX.
6. **Integración con novedades TH**: hoy son dos Excel que se cruzan. Integrar de verdad implica al dueño de ese formato.

---

## 15. Vacío de información (no dejar pasar en la próxima sesión)

### 15.1 Obligatorio (bloquea diseño)

1. **Mesa de segundo nivel** (Andrés / Ricardo): proceso, actores, intercambio, horizonte.
2. Recibir los **Excel** prometidos (CC septiembre + sitio) para campos reales, no ASR de la acta.
3. Lista cerrada de **turnos** (sitio 1–9 y CC 1–12) con horarios por día.
4. Lista cerrada de **estados/letras** y si cada uno suma horas / es asignable.
5. ¿La malla es una por área o puede mezclar mesa + lab + sitio en la misma grilla?
6. Bloquear vs advertir: tabla RN-xx validada.
7. ¿Vacaciones e incapacidades ya viven en otro módulo o se capturan solo en la malla?

### 15.2 Importante (sesión de informes)

8. Layout exacto del archivo que recibe **nómina**.
9. Cortes vigentes y si varían por empresa.
10. Compensatorios vigentes post reducción de jornada.
11. Reportería de mesa/sitio además de extras.

### 15.3 Posterior

12. Personal de fábrica (Coronado).
13. Solicitud de intercambio entre compañeros.
14. Indicadores → Elemento (solo excepción manual, ya dicho).

---

## 16. Propuesta de trabajo hacia la próxima sesión (no desarrollo)

1. Validar este documento con Oscar, Ricardo, Freddy, Luis, William.
2. Inventariar Excel (hojas, columnas, catálogos, fórmulas que son reglas).
3. Redactar **historias de usuario** solo del núcleo común + 1 frente piloto.
4. Mockups de: parametría de turnos, grilla de malla, consulta “quién está ahora”, vista empleado, historial de celda.
5. Decidir frente piloto: **Contact Center** (mensual, rica en reglas de horas) o **Soporte en sitio** (semanal, tiempo real, zonas). Recomendación: núcleo común + piloto **Contact Center** para parametría/nómina y un **spike de consulta en vivo** para mesa, sin pretender el Excel de Oscar al 100 % en el primer incremento.

---

## 17. Historias de usuario candidatas (borrador, no comprometidas)

Solo para aterrizar el núcleo. Se detallan tras validación.

1. Como **supervisora**, quiero armar la malla del mes sobre plantillas de turno para no reconstruir horarios a mano.
2. Como **coordinador**, quiero revisar cobertura por franja antes de publicar.
3. Como **coordinador**, quiero cambiar un turno hoy por incapacidad y que quede historial y aviso al empleado.
4. Como **analista de mesa**, quiero buscar por SPT/técnico y ver si está disponible ahora.
5. Como **operador/técnico**, quiero ver la malla de mi grupo y mi horario.
6. Como **coordinador**, quiero exportar horas (extra, festiva, recargo) según corte de nómina.
7. Como **coordinador de sitio**, quiero cubrir un sábado con alguien de laboratorio.
8. Como **coordinador CC**, quiero marcar a una persona en Elemento todo el mes sin pasar por indicadores.

---

## 18. Glosario

| Término | Significado en esta operación |
| ------- | ----------------------------- |
| Malla | Programación del grupo para un periodo |
| Turno | Plantilla reutilizable (código + horario + color) |
| Estado / novedad | Celda que no es horario operativo (DES, INC, etc.) |
| SPT | Punto / sede técnica donde se cubre el recurso |
| Regional / zona | Agrupación geográfica (Bogotá norte, Cundinamarca, …) |
| Elemento | Sede física de asistencia Contact Center |
| Canguro | Acompañamiento a personal nuevo |
| Actividad | Ocupado en labor no despachable (ej. mantenimiento) |
| Publicar | Enviar/visible al grupo; en sitio **no** significa inmutable |
| Corte de nómina | Rango de fechas que agrupa horas a reportar |

---

## Control de cambios

| Versión | Fecha | Autor | Descripción |
| ------- | ----- | ----- | ----------- |
| 0.1 | 27/08/2026 | Jair Uribe | Consolidación de la primera reunión. Pendiente validación de negocio e insumos Excel. |
