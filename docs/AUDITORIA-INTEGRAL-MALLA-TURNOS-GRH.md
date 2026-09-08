# AUDITORÍA INTEGRAL — Malla de Turnos / GRH

| Campo | Valor |
| ----- | ----- |
| Fecha | 05/09/2026 |
| Alcance | EP-00 a EP-08 (HU01–HU76) + Propuesta-HU + Levantamiento Fase 1 |
| Fuentes código | gestionrrhh (auth, company-admin, employee, parametrization, notification, audit, FE) |
| Fuentes negocio | LEVANTAMIENTO-MALLA-TURNOS-FASE1.md, Propuesta-HU-Malla-Turnos.md, GST-FM-04 markdown, Excel insumos |
| Principio rector | Máxima parametrización por empresa y frente. Cero hardcoding de reglas de negocio. |

Clasificación de hallazgos:

- REQUERIMIENTO EVIDENCIADO — nace de levantamiento, Excel o HU explícita.
- RECOMENDACIÓN TÉCNICA/FUNCIONAL — propuesta del análisis para cumplir el principio de parametrización / integración GRH.

---

## 1. VEREDICTO GENERAL

### Estado actual

Las HU actuales están en **madurez media-alta como backlog de producto**: cubren el ciclo completo (integración → catálogos → grilla → publicación → novedades → consulta → empleado → reportes) y ya articulan la idea correcta de “configuración por frente” (HU26) y “malla ≠ jornada contractual” (HU06).

No están listas para diseño/implementación sin refinamiento: hay **acoplamiento narrativo a frentes de ejemplo**, reglas citadas como constantes (42 h, 3 domingos, Elemento, estudio/salud), épicas que mezclan capacidades, y **huecos críticos** (motor de reglas genérico, intercambio de turno, novedades TH como dominio, sedes, alcance por frente vs área GRH, concurrencia de grilla).

### Nivel de madurez

| Dimensión | Nota | Comentario |
| --------- | ---- | ---------- |
| Correctitud funcional del dominio | 7/10 | El modelo celda = persona × día × turno/estado + atributos es sólido. |
| Parametrización real | 5/10 | Intención correcta; muchos ejemplos se leen como reglas fijas. |
| Integración GRH | 6/10 | EP-00 acertado; subestima auth RBAC real, timeline, working-profile, falta de sedes. |
| Arquitectura / escalabilidad | 4/10 | Casi no hay HU de performance, paginación de grilla, motor de reglas, agregados. |
| Completitud vs levantamiento | 6/10 | Falta intercambio de turno (explícito en “fuera de listado”); rotación bien encaminada pero incompleta como DSL. |

### Qué está bien

1. EP-00: nacer dentro de GRH (menú, plan, permisos, tenant, maestros).
2. Separación jornada contractual vs malla operativa (HU06) — alineada con `work_schedule` / `schedule_assignment` en parametrization.
3. HU26 como “interruptor de capacidades” del frente (periodo, publicar, editable, modo armado, flags).
4. Estados con banderas de comportamiento (suma horas, asignable) — dirección correcta.
5. Notificación informativa sin aceptación (HU63) — confirmado en levantamiento.
6. Historial puntual de celda en lugar de versionar malla completa.
7. Entrega de horas, no liquidación en pesos.

### Qué debe corregirse (top riesgos)

1. **Frente operativo no es un enum de 4 valores.** Hoy las HU listan CC/Sitio/Mesa/Lab como si fueran el catálogo. Debe ser entidad parametrizable (o área GRH + perfil de configuración).
2. **Hardcoding narrativo** en RN/FA: Elemento, 42 h, 3 domingos, estudio/salud, presencial/virtual/híbrido como si fueran el modelo.
3. **HU45 mete “42 h” como regla fija** en el título — viola el principio.
4. **ex-HU54 “actividad”** como caso especial — debe ser flag del estado (`asignableACasos`), no HU de estado concreto.
5. **Alcance por frente vs permiso RBAC:** GRH solo tiene CREAR/LEER/ACTUALIZAR/ELIMINAR por submódulo. El alcance por frente/área es dominio Malla, no auth nuevo.
6. **No existen sedes en parametrization** — sitios de asistencia son catálogo nuevo de Malla (correcto en espíritu; no decir “reutilizar sedes GRH”).
7. **No existen vacaciones/incapacidades TH en GRH** — HU60/HU72/HU75 no pueden “reutilizar” un módulo inexistente; hay que decidir ownership (catálogo de estados en malla vs integración futura).
8. **Intercambio de turno** quedó fuera; el usuario pide reconsiderarlo como épica parametrizable.
9. **DEV ya tiene módulo id=13 `MALLA DE TURNOS`** sin submódulos ni plan — HU01 debe anclarse a ese hecho, no asumir “módulo nuevo desde cero”.
10. **Rotación:** HU47–HU56 van en la dirección correcta, pero falta un modelo de patrón genérico (secuencia, ciclo, exclusiones, estrategia) sin ejemplos quemados.

---

## 2. HUs CORRECTAS (mantener con ajustes menores de redacción)

| ID | Título | Nota |
| -- | ------ | ---- |
| HU01 | Registrar módulo/submódulos | Mantener; anclar a módulo 13 DEV y checklist company-admin + auth + FE. |
| HU04 | Aislar por empresa | Mantener; reforzar companyId desde JWT, no del body. |
| HU06 | Jornada vs malla | Mantener; referenciar working-profile solo lectura. |
| HU11–HU13 | Plantillas + horario día + break | Mantener; quitar listas fijas de frentes. |
| HU14 | Estados con flags | Mantener y **ampliar flags** (ver §7). |
| HU15 | Campañas/tareas | Mantener; ejemplos solo en datos de prueba. |
| HU17–HU18 | Modalidades y sitios | Mantener; “requiere sitio” es flag, no if(virtual). |
| HU20 | Festivos calendario empresa | Mantener; consumir company_calendar. |
| HU21–HU22 | Cortes y tipos de hora | Mantener; tipos como catálogo + motor de cálculo configurable. |
| HU26 | Config frente | Mantener como HU clave; ampliar capacidades (ver §6). |
| HU28–HU30 | Crear malla, grupo, asignar celda | Mantener núcleo. |
| HU31 | Segundo turno / extra | Mantener; flag extra + validación solape parametrizable. |
| HU34–HU35 | Nota + grilla | Mantener. |
| HU57–ex-HU46 | Ciclo publicación | Mantener; ligado a flags HU26. |
| HU62–HU63 | Historial + notificación | Mantener; timeline + notification event types. |
| HU64 | Historial por funcionario | Mantener. |
| HU67–HU69 | Vistas empleado | Mantener; solo lectura + scopes. |
| HU70–HU71 | Horas + export | Mantener; sin pesos. |

---

## 3. HUs A CORREGIR

### HU02 — Permisos por rol y por área/frente

- Problema: mezcla RBAC de plataforma (submódulo × CREAR/LEER/…) con alcance operativo por frente.
- Por qué: auth GRH no modela “frente”; solo `permission_submodules`.
- Modificación: dividir en (a) permisos por sección de menú vía Seguridad GRH; (b) alcance de frentes autorizados como configuración de Malla (rol/usuario ↔ frente).

### HU05 — Reutilizar maestros

- Problema: asume sedes/áreas listas; employee no filtra por `areaId` en listado.
- Modificación: reutilizar employee + areas + positions + calendars; **sitios = catálogo Malla**; pedir extensión de filtro área en employee o filtrar en Malla con paginación consciente.
- Trazabilidad: RECOMENDACIÓN TÉCNICA + código employee `EmployeeFilterRequest`.

### HU16 — Regionales/zonas/SPT

- Problema: jerarquía fija “Regional → Zona → SPT” puede no aplicar a todos.
- Modificación: catálogo territorial **parametrizable en niveles** (árbol N niveles o niveles habilitados por frente). No hardcodear 3 niveles con nombres fijos.
- REQUERIMIENTO EVIDENCIADO (sitio/mesa) + RECOMENDACIÓN (genericidad).

### HU19 — Restricciones estudio/salud

- Problema: tipos citados como si fueran el catálogo.
- Modificación: catálogo genérico de tipos de restricción + efectos (bloquear/advertir) + alcance (turnos, sitios, franjas, días). “Estudio/salud” solo ejemplos de seed.

### HU23 — Compensatorio “3 domingos”

- Problema: la condición del ejemplo se filtra como la regla.
- Modificación: motor de reglas de compensatorio (umbral, tipo de día, ventana temporal, acción sugerir/advertir). Seed opcional con regla de 3 domingos.

### HU24 — Cobertura mínima

- Problema: ejemplos “1 técnico/regional” en criterios.
- Modificación: regla genérica dimensión (franja/día/territorio/turno/…) + umbral min/max + severidad.

### HU45 — Conflictos “42 h”

- Problema: **hardcoding explícito en el título de la HU**.
- Modificación: “Evaluar reglas de validación parametrizadas (solape, cobertura, horas del periodo, repetición, restricciones…)”. 42 h = regla configurable de horas máximas del periodo.

### HU55 — “estudio, salud, no repetir turno”

- Problema: mezcla restricciones de persona con reglas de rotación.
- Modificación: “Aplicar motor de reglas y restricciones al asignar/rotar” (sin listar tipos).

### HU60 / ex-HU50 / ex-HU54

- Problema: ex-HU54 especializa “actividad”; ex-HU50 es consecuencia del flag del estado.
- Modificación: fusionar comportamiento en HU14 + motor de cálculo; HU60 queda como “aplicar estado de novedad a celda”; eliminar ex-HU54 como HU independiente o convertirla en criterio de HU65/HU14.

### HU01 (detalle)

- Problema: reference.md decía “módulo nuevo”; DEV ya tiene id 13.
- Modificación: completar submódulos del 13, asociar a plan, seeds permisos, rutas FE. No crear segundo módulo.

---

## 4. HUs A DIVIDIR

| HU | Por qué dividir | Propuesta |
| -- | --------------- | --------- |
| HU02 | RBAC plataforma ≠ alcance frente | HU02a permisos submódulo; HU02b alcance frente usuario/rol |
| HU26 | Demasiadas capacidades en una | Mantener HU26 como “perfil de frente”; sacar “habilitar capacidades de celda” y “estrategia de armado” si el GST-FM-04 queda ilegible — o dejar una con secciones claras |
| HU45 | Motor de validación + UI de conflictos | HU34a catálogo/motor de reglas; HU34b panel de conflictos en grilla |
| HU47–HU50 | Definición de patrón vs aplicación | OK separados; falta HU de “estrategia de rotación” (manual/asistida/automática/ninguna) si no queda solo en HU26 |
| HU70 | Cálculo + clasificación de tipos | HU58a motor; opcional HU de “prioridad de tipos de hora” |

---

## 5. HUs A FUSIONAR

| Fusionar | En | Motivo |
| -------- | -- | ------ |
| ex-HU50 | HU14 + HU70 | “No suma horas” es flag de estado + efecto en cálculo |
| ex-HU54 | HU14 + HU65 | “No asignable” es flag; consulta solo lo lee |
| ex-HU46 | HU10 + HU57 | Separar constructor/publicador es configuración del frente + flujo |
| HU12–HU13 | Opcional bajo HU11 como subtareas | Mismo agregado plantilla de turno (OK dejar separadas para GST-FM-04 cliente) |

---

## 6. HUs FALTANTES (crítico)

### A. Configuración y catálogos transversales

| ID propuesto | Título | Origen |
| ------------ | ------ | ------ |
| HU-NEW-01 | Parametrizar frentes operativos de la empresa (catálogo, no enum) | RECOMENDACIÓN + riesgo hardcoding |
| HU-NEW-02 | Vincular frente a área(s) GRH y a capacidades habilitadas | RECOMENDACIÓN (área ya existe) |
| HU-NEW-03 | Catálogo genérico de severidad de reglas (info/advertir/bloquear) | RECOMENDACIÓN |
| HU-NEW-04 | Motor de reglas de validación por empresa/frente (condiciones + acción) | RECOMENDACIÓN + HU45 mal formulada |
| HU-NEW-05 | Ampliar flags de estado de celda (extras, recargos, cobertura, motivo, notificación, soporte) | Levantamiento + RECOMENDACIÓN |
| HU-NEW-06 | Tipo de restricción como catálogo + matriz de efectos | Corrección HU19 |

### B. Rotación (completar DSL)

| ID | Título | Origen |
| -- | ------ | ------ |
| HU-NEW-07 | Parametrizar estrategia de armado: ninguna / manual / asistida / automática | HU26 + levantamiento |
| HU-NEW-08 | Modelo de patrón: secuencia, duración ciclo, exclusiones, prioridad, respeto restricciones | HU47 insuficiente |
| HU-NEW-09 | Simular patrón (dry-run) antes de aplicar | RECOMENDACIÓN UX/riesgo |
| HU-NEW-10 | Exclusión de empleados/celdas de rotación automática | Levantamiento excepciones |

### C. Intercambio / solicitud de turno (nueva épica)

| ID | Título | Origen |
| -- | ------ | ------ |
| EP-09 / HU-NEW-11 | Habilitar/deshabilitar solicitudes de intercambio por empresa y frente | Usuario + levantamiento “fuera de listado” |
| HU-NEW-12 | Empleado solicita intercambio de celda/turno | Idem |
| HU-NEW-13 | Validar solicitud con motor de reglas (cobertura, solape, horas, anticipación) | RECOMENDACIÓN |
| HU-NEW-14 | Aprobar/rechazar solicitud por rol configurado | Idem |
| HU-NEW-15 | Aplicar cambio, auditar y notificar | Idem |

### D. Integración, concurrencia, operación

| ID | Título | Origen |
| -- | ------ | ------ |
| HU-NEW-16 | Concurrencia: bloqueo optimista / versionado de celda o malla | Riesgo arquitectura |
| HU-NEW-17 | Carga parcial de grilla (ventana de fechas, paginación de personas) | Escalabilidad |
| HU-NEW-18 | Registrar event types de notificación Malla en notification-service | Código notification |
| HU-NEW-19 | Publicar eventos de timeline (audit) para cambios de celda/publicación | Código audit |
| HU-NEW-20 | Extender listado de empleados con filtro por área (o BFF paginado) | Código employee |
| HU-NEW-21 | Idempotencia y reintento de notificaciones | RECOMENDACIÓN |
| HU-NEW-22 | Importación asistida desde Excel (descubrimiento → catálogos, no Excel=BD) | Excel insumos + prompt §21 |

### E. Novedades TH

| ID | Título | Origen |
| -- | ------ | ------ |
| HU-NEW-23 | Definir ownership de novedades: estado de celda vs registro TH externo | Código: no hay módulo TH |
| HU-NEW-24 | Formato de importación de novedades TH parametrizable por empresa | HU75 |

---

## 7. PARAMETRIZACIONES FALTANTES

| Elemento | Actualmente en HU | Debe parametrizarse como | Nivel |
| -------- | ----------------- | ------------------------ | ----- |
| Frentes CC/Sitio/Mesa/Lab | Lista fija en RN/datos | Catálogo `operational_front` | Empresa |
| Periodo semana/mes | Flag HU26 | Enum en config frente (+ futuros) | Frente |
| Modo armado | manual/asistido/automático | Estrategia + patrón asociado | Frente |
| Constructor vs publicador | Flag HU26 | Roles/permisos + flag | Frente |
| Malla publicada editable | Flag HU26 | Boolean + políticas de motivo | Frente |
| Capacidades celda (zona, campaña, modalidad, sitio, nota, doble turno) | Flags parciales HU26 | Feature flags por frente | Frente |
| Turnos 1–12 / 1–9 | Ejemplos Excel | Catálogo plantillas | Empresa+Frente |
| Colores | En plantilla/estado | Campo del catálogo | Empresa |
| Estados DES/INC/ACT… | Ejemplos | Catálogo + flags comportamiento | Empresa (+filtro frente) |
| 42 horas | HU45 título | Regla `max_hours_period` | Frente |
| 3 domingos → compensatorio | HU23 ejemplo | Regla compensatorio genérica | Empresa/Frente |
| Cobertura 1 técnico/regional | Ejemplos RN | Regla cobertura min/max | Frente |
| Estudio / salud | HU19 | Tipos de restricción | Empresa |
| Presencial/virtual/híbrido | HU17 ejemplos | Catálogo modalidades + `requiresSite` | Empresa |
| Elemento | HU18/HU38 | Ítem de catálogo sitios | Empresa |
| Data Service / Canguro | HU15 | Catálogo campañas | Empresa+Frente |
| Tipos hora ORD/EXT/FES… | HU22 lista | Catálogo + reglas de clasificación | Empresa |
| Severidad advertir/bloquear | Parcial | Catálogo severidad en cada regla | Frente |
| Anticipación intercambio | Fuera | Config solicitud | Frente |
| Quién aprueba intercambio | Fuera | Config + permisos | Frente |
| Niveles territoriales | Regional/Zona/SPT fijos | Árbol o niveles configurables | Frente |
| Breaks obligatorios | Implícito CC | Flag en plantilla + regla cobertura en pausa | Frente |

---

## 8. HARDCODING DETECTADO

| Dónde | Problema | Propuesta |
| ----- | -------- | --------- |
| HU01 RN-06 lista 4 frentes | Enum implícito de producto | Catálogo de frentes |
| HU11 datos entrada “CC, Sitio, Mesa, Lab” | Select fijo | Select desde catálogo |
| HU13 RN-02 “CC y mesa suelen…” | Regla de negocio en RN | Quitar; que lo diga config de plantilla |
| HU17 “presencial/virtual/híbrido” en descripción | Semántica fija | Catálogo + flag requiere sitio |
| HU19 estudio/salud en flujo y CA | Tipos quemados | Catálogo de tipos |
| HU23 / HU76 “3 domingos” | Regla quemada | Motor de reglas |
| HU26 precondiciones “frentes identificados” | Asume los 4 | “Existe al menos un frente configurado” |
| HU38 / HU18 “Elemento” | Caso especial narrativo | Ejemplo de sitio en datos de prueba, no en RN |
| HU43 RN “fórmulas Excel CC” | Acoplamiento a un frente | Contadores según turnos/franjas del catálogo |
| HU45 “42 h” | Constante | Regla parametrizable |
| HU47 FA “15/15”, “2 trabajan / 1 descansa” | OK como ejemplos de patrón, no como tipos de sistema | Modelo de secuencia genérico |
| HU55 lista estudio/salud | Idem HU19 | Motor + catálogo |
| ex-HU54 Actividad | Estado especial | Flag `caseAssignable=false` |
| Propuesta “fuera de listado” intercambio | Omite necesidad | EP-09 parametrizable |
| reference.md “sedes” en parametrization | Incorrecto en código actual | Sitios en Malla; sedes GRH no existen |

---

## 9. DEPENDENCIAS CON GRH

| HU / capacidad | Microservicio | Recurso a reutilizar |
| -------------- | ------------- | -------------------- |
| HU01 menú/plan | company-admin | `modulos` (id 13), `submodules`, `plan_modulos`, `company_planes` |
| HU02 permisos sección | auth | `roles`, `permission_submodules`, JWT `SM_{id}_{PERM}` |
| HU02b alcance frente | Malla (nuevo) | Tabla propia; no auth |
| HU04 tenant | todos | `companyId` JWT; repos `*AndCompanyId` |
| HU05 empleados | employee | `GET /v1/employees`, entity `currentAreaId`/`currentPositionId` |
| HU05 áreas/cargos | parametrization | `/v1/areas`, `/v1/positions` |
| HU05/HU20 festivos | parametrization | `company-calendars`, `company-calendar-holidays` |
| HU06 jornada contractual | parametrization | `work-schedules`, `schedule-assignments`, `working-profile` (solo lectura) |
| HU63 notificación | notification | `POST /v1/events/dispatch` + nuevos event types |
| HU62 auditoría | audit (+ catalogo parametrization timeline) | `POST /v1/internal/timeline/events` + historial de dominio Malla |
| HU67–57 usuario | auth + employee | `userId` en employee |
| Sitios / territorio / turnos operativos | **Malla nuevo** | No existen equivalentes suficientes |
| Novedades TH | **No existe** | Estados de celda MVP; import TH HU75; futuro MS TH |
| PersonDateException | parametrization | No usar como fuente TH; solo override de calendario puntual si se acuerda |

Arquitectura recomendada del MS:

- **Nuevo microservicio `malla-turnos` (o nombre alineado al monorepo)** dueño del dominio operativo.
- No meter malla en employee ni en work_schedule.
- Hexagonal como el resto: controller → use case → port → adapter.
- Agregado candidato: **Malla (ScheduleGrid)** con celdas; catálogos como aggregates separados; historial de celda append-only (no borrar con la malla).

---

## 10. RIESGOS ARQUITECTÓNICOS

| Riesgo | Impacto | Mitigación |
| ------ | ------- | ---------- |
| Multi-tenant: companyId del body | Fuga entre empresas | Ignorar companyId del cliente; siempre JWT |
| Grilla N personas × 31 días en un payload | Timeout/FE lento | Ventana de fechas, paginar personas, virtual scroll (HU-NEW-17) |
| Recalcular toda cobertura/horas por celda | CPU | Incremental + proyección de contadores |
| Doble fuente de verdad novedades (malla vs TH) | Descuadre nómina | Ownership claro HU-NEW-23 + cruce HU75 |
| Historial en audit + historial dominio | Duplicidad/confusión | Dominio: detalle celda; Timeline: hechos de negocio de alto nivel |
| permission_submodules cross-DB | Ops frágil | Checklist EP-00; no inventar auth paralelo |
| Concurrencia dos coordinadores misma celda | Lost update | Version/ETag HU-NEW-16 |
| Rotación automática sin dry-run | Daño operativo | HU-NEW-09 |
| Filtro empleados sin areaId | Overfetch | Extender employee o proyección Malla |
| Módulo 13 sin submódulos en DEV | Doble alta | Completar 13, no crear 14 |

---

## 11. PUNTOS QUE REALMENTE REQUIEREN DECISIÓN DE NEGOCIO

Solo lo que no se resuelve solo con “poner un flag”.

| # | Decisión | Impacto | Propuesta recomendada | Default sugerido |
| - | -------- | ------- | --------------------- | ---------------- |
| D1 | ¿Novedades TH (vacaciones/incapacidad) viven solo como estado de celda o habrá sistema TH fuente de verdad? | HU60/60/62, integraciones | MVP: estado de celda + import archivo; fase 2: conector TH | Estado de celda + import |
| D2 | ¿Frente = área GRH o entidad aparte vinculada a área? | Modelo datos HU-NEW-01/02 | Entidad Frente con FK opcional a `area_id` | Frente propio + vínculo opcional |
| D3 | ¿Malla pública del grupo para todos los integrantes? | HU67 privacidad | Pública dentro del frente (levantamiento) | Pública en el grupo |
| D4 | ¿Publicar con advertencias permitido? | HU57 | Configurable por frente | Permitir con confirmación |
| D5 | ¿Intercambio de turnos en MVP o fase 2? | EP-09, alcance sprint | Fase 2; diseño parametrizable desde ya | Deshabilitado por defecto |
| D6 | ¿Rotación automática en MVP? | EP-03 | Manual + asistido en MVP; automático cuando haya patrones maduros | Manual; asistido piloto CC |
| D7 | ¿Un empleado en dos mallas el mismo día (cobertura cruzada HU37) suma horas dónde? | Nómina | Configurable: cuenta en malla destino / origen / ambas con tope | Cuenta en malla donde se asigna + regla solape |
| D8 | Formato oficial archivo novedades TH | HU75 | Definir columnas mínimas comunes | Plantilla CSV/XLSX parametrizable |

Todo lo demás del levantamiento “abierto” se convierte en **parametrización** (Caso 3 del prompt), no en pendiente eterno.

---

## 12. PROPUESTA FINAL DE BACKLOG

### Principios de reorganización

1. Conservar numeración MT-EPxx-HUyy para trazabilidad; nuevas van `MT-EP09-HU09+` o `MT-EP01-HU20b` según épica.
2. Eliminar/absorber HU que son efectos de flags (ex-HU50, ex-HU54, parte de ex-HU46).
3. Nueva EP-09 Solicitudes de intercambio (deshabilitada por config).
4. Nueva EP-10 (técnica transversal) o anexos: concurrencia, performance, event types — pueden vivir como HU no-funcionales en EP-00/EP-05.

### Épicas propuestas

| Épica | Tema | HU |
| ----- | ---- | -- |
| EP-00 | Integración GRH | HU01 (ajustada), HU02a, HU02b, HU04, HU05 (ajustada), HU06, HU-NEW-18, HU-NEW-19, HU-NEW-20 |
| EP-01 | Catálogos y config | HU11–HU26 + HU-NEW-01,02,03,05,06 + reglas HU-NEW-04 |
| EP-02 | Construcción | HU28–HU38 (HU32/26 condicionadas por flags) + HU-NEW-16,17 |
| EP-03 | Validación y rotación | HU43–HU44, HU34a/b, HU47–HU56 + HU-NEW-07..10 |
| EP-04 | Publicación | HU57–HU59 (ex-HU46 absorbida en HU26/43) |
| EP-05 | Novedades y auditoría | HU60–HU63, HU64 + HU-NEW-23 |
| EP-06 | Consulta operativa | HU65–HU66 (ex-HU54 absorbida) |
| EP-07 | Vista empleado | HU67–HU69 |
| EP-08 | Reportes/horas | HU70–HU76 + HU-NEW-24 |
| EP-09 | Solicitudes intercambio | HU-NEW-11..15 (default off) |

### HUs nuevas redactadas (formato pedido)

#### MT-EP01-HU09 — Parametrizar frentes operativos de la empresa

**Como:** administrador de empresa / usuario con permiso de parametrización  
**Quiero:** registrar frentes operativos con código, nombre y estado  
**Para:** configurar mallas sin depender de una lista fija de áreas de negocio

**Criterios de aceptación**

- Dado una empresa, cuando creo un frente con código único, entonces queda disponible solo para esa empresa.
- Dado un frente inactivo, cuando armo una malla, entonces no aparece en el selector.
- Dado el sistema, cuando no existen frentes, entonces no se asumen Contact Center ni otros nombres por defecto.
- Multi-tenant: una empresa no ve frentes de otra.
- Permisos: solo roles con ACTUALIZAR/CREAR en Parametrización.

#### MT-EP01-HU10 — Configurar capacidades y estrategia de armado del frente

**Como:** usuario con permiso de parametrización  
**Quiero:** definir para cada frente periodo por defecto, estrategia de armado (ninguna/manual/asistida/automática), separación constructor/publicador, editabilidad post-publicación y flags de atributos de celda  
**Para:** que el mismo producto se adapte a cada operación sin desplegar código

**Criterios de aceptación**

- Dado un frente, cuando desactivo “usa territorio”, entonces la UI de celda no pide zona/SPT.
- Dado estrategia manual, cuando abro rotación automática, entonces la acción está deshabilitada con mensaje de configuración.
- Dado separación constructor/publicador activa, cuando el constructor intenta publicar, entonces solo puede enviar a revisión.
- Auditoría: cambios de configuración de frente quedan registrados (quién/cuándo/antes/después).

#### MT-EP01-HU25 — Motor de reglas de validación parametrizable

**Como:** usuario con permiso de parametrización  
**Quiero:** definir reglas con condición, alcance (frente), severidad (info/advertir/bloquear) y parámetros numéricos/categóricos  
**Para:** validar solapes, horas del periodo, cobertura, repetición y restricciones sin constantes en código

**Criterios de aceptación**

- Dado una regla de horas máximas del periodo = N, cuando la malla supera N, entonces aplica la severidad configurada.
- Dado solape horario real, cuando se guarda una celda, entonces el sistema bloquea (regla de integridad de dominio, no desactivable) **o** — si negocio permite desactivar — solo con severidad mínima bloqueo (decisión D: se recomienda solape real siempre bloqueante).
- Dado una regla inactiva, cuando valido la malla, entonces no se evalúa.
- Multi-tenant y por frente.

**Nota:** solape horario en la misma persona/día es candidato a **invariante de dominio** (siempre bloqueo). El resto (42h, cobertura, celda vacía, repetir turno) es parametrizable.

#### MT-EP03-HU46 — Definir patrón de rotación genérico

**Como:** usuario con permiso de parametrización  
**Quiero:** crear patrones con secuencia ordenada de plantillas de turno, duración de ciclo, exclusiones y opción de respetar restricciones  
**Para:** representar 15/15, mañana→tarde, 2×1 descanso u otros sin tipos especiales en código

**Criterios de aceptación**

- Dado una secuencia de plantillas y duración en días, cuando aplico el patrón en simulación, entonces produce asignaciones predecibles.
- Dado empleados excluidos, cuando aplico, entonces no se modifican.
- Dado restricciones vigentes, cuando el patrón respeta restricciones, entonces no propone turnos incompatibles.
- No existen tipos de patrón enum; solo datos.

#### MT-EP09-HU48 — Solicitud de intercambio de turno (parametrizable)

**Como:** empleado del frente con solicitudes habilitadas  
**Quiero:** solicitar intercambio de una celda con otro empleado  
**Para:** resolver cambios de turno en la plataforma con validación y aprobación

**Criterios de aceptación**

- Dado frente con solicitudes deshabilitadas, cuando intento solicitar, entonces la acción no está disponible.
- Dado solicitud creada, cuando el aprobador rechaza, entonces no cambia la malla y queda auditoría.
- Dado aprobación, cuando hay conflicto de cobertura/solape según reglas, entonces no se aplica.
- Notificación a ambos empleados; sin aceptación del cambio de destino más allá del flujo de solicitud.
- Multi-tenant; permisos de solicitar/aprobar configurables.

#### MT-EP00-HU49 — Integrar notificaciones y timeline de Malla

**Como:** equipo de plataforma  
**Quiero:** registrar event types de notification y timeline para publicación y cambio de celda  
**Para:** reutilizar la infraestructura GRH sin mailers ni auditorías paralelas

**Criterios de aceptación**

- Dado publicación de malla, cuando termina OK, entonces se despacha evento EMAIL+POPUP.
- Dado cambio de celda relevante, cuando se guarda, entonces existe evento de timeline y registro de historial de dominio.
- Idempotencia de notificación por clave de evento.

### HUs a eliminar o absorber (trazabilidad)

| HU | Acción |
| -- | ------ |
| ex-HU50 | Absorber en HU14 + HU70 |
| ex-HU54 | Absorber en HU14 + HU65 |
| ex-HU46 | Absorber en HU26 + HU57 (criterios) |

### Orden de implementación revisado

1. EP-00 (incl. event types, módulo 13, tenant).
2. EP-01 catálogos + frentes + motor de reglas + config.
3. EP-02 + EP-04 + EP-05 (grilla, publicar, novedad, historial) + concurrencia/paginación.
4. EP-07 + HU70–59 (empleado + horas/export).
5. EP-06 consulta.
6. EP-03 validación/rotación (asistido → automático).
7. EP-08 resto reportes (cruce TH, compensatorio).
8. EP-09 intercambio (cuando negocio active D5).

---

## ANEXO A — Hallazgos de código GRH (resumen)

1. Tenant = `companyId` en JWT; enforcement por MS (sin filtro Hibernate global).
2. Menú = plan activo ∩ submódulos con LEER.
3. Permisos base solo CREAR/LEER/ACTUALIZAR/ELIMINAR + `SM_{subModuleId}_{PERM}`.
4. DEV: módulo **13 MALLA DE TURNOS** sin submódulos ni plan.
5. Jornada contractual = `work_schedule` + `schedule_assignment` + working-profile (parametrization).
6. No hay sedes/centros en parametrization.
7. No hay módulo de vacaciones/incapacidades TH.
8. Notification: dispatch por `eventTypeCode` (EMAIL+POPUP).
9. Audit: preferir Timeline interno + historial de dominio para celdas.
10. Employee list no filtra por `areaId` hoy.

## ANEXO B — Mapa conceptual del dominio (recomendado)

```
Empresa (tenant)
 └── Frente operativo (catálogo Malla, opcionalmente ↔ Área GRH)
      ├── Configuración (periodo, estrategia armado, flags, publicación, solicitudes)
      ├── Catálogos filtrables (turnos, estados, campañas, territorio, modalidades, sitios, reglas)
      └── Malla (periodo + grupo empleados)
           └── Celda (persona × fecha)
                ├── turno(s) / estado
                ├── atributos opcionales según flags
                └── historial append-only
```

Invariantes de dominio sugeridos (no configurables o solo con privilegio extremo):

- Toda entidad operativa lleva `company_id`.
- Solape horario real misma persona mismo instante → bloqueo.
- No borrar historial de celda.
- No escribir en `work_schedule` desde Malla.

---

## ANEXO C — Checklist anti-hardcoding (gate de diseño)

Antes de aprobar cualquier HU o ticket de desarrollo:

1. ¿Puede otra empresa necesitar otro comportamiento? → configuración.
2. ¿Cambiarlo exige deploy? → aún no está parametrizado.
3. ¿Aparece nombre de frente/turno/estado/sitio en un `if`? → rechazo.
4. ¿El ejemplo del Excel se coló como enum? → mover a seed/datos.
5. ¿Reutiliza employee/auth/notification/calendar o inventa paralelo? → justificar.

---

*Fin de la auditoría. Siguiente paso sugerido: priorizar con negocio D1–D8 y reescribir GST-FM-04 de las HU marcadas “a corregir” + nuevas HU09+.*
