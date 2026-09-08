# Backlog de sprints — Malla de Turnos

| Campo | Valor |
| ----- | ----- |
| Versión | 4.0 — Sprint 1…9 (EP-00 dentro de Sprint 1) |
| Integrantes | 1 Fullstack · 1 Backend (aprendiz) · 1 Frontend (aprendiz) · 1 QA (aprendiz) |
| Duración sprint | 2 semanas |
| Capacidad por integrante | **80 h / sprint** (4 × 80 = **320 h** equipo) |
| Total sprints | **9** (Sprint 1 … Sprint 9) |
| Duración orientativa | 9 × 2 semanas ≈ **18 semanas** |
| Orden | HU01→HU81 (EP-00→EP-09) |
| Excel | `docs/BACKLOG-SPRINTS-MALLA-TURNOS.xlsx` (una hoja por sprint) |

Verificación: en cada sprint Fullstack = 80, Backend = 80, Frontend = 80, QA = 80.

Fullstack hace **diseño de BD solo en Sprint 1**; en sprints siguientes solo migraciones Flyway si el esquema crece. Backend **no** hace Flyway.

---

## Resumen

| Sprint | Alcance HU | Enfoque | Horas/integrante |
| ------ | ---------- | ------- | ---------------- |
| 1 | HU01–HU18 | Integración GRH y catálogos núcleo (EP-00 / EP-01 inicio) | 80 |
| 2 | HU19–HU27 | Catálogos avanzados y motor de reglas (EP-01 cierre) | 80 |
| 3 | HU28–HU35 | Construcción de malla core (EP-02) | 80 |
| 4 | HU36–HU42 | Construcción avanzada (EP-02 cierre) | 80 |
| 5 | HU43–HU50 | Validación y rotación base (EP-03) | 80 |
| 6 | HU51–HU59 | Rotación avanzada y publicación (EP-03 / EP-04) | 80 |
| 7 | HU60–HU69 | Novedades, consulta y empleado (EP-05 / EP-06 / EP-07) | 80 |
| 8 | HU70–HU76 | Reportes y horas (EP-08) | 80 |
| 9 | HU77–HU81 | Intercambio y estabilización (EP-09) | 80 |

---

## Sprint 1 — Integración GRH y catálogos núcleo (EP-00 / EP-01 inicio)

Objetivo: Habilitar el módulo en la plataforma (menú/submódulos Super Admin, permisos, alcance por frente, tenant, maestros GRH) y parametrizar catálogos núcleo: frentes, capacidades, turnos, horarios, pausas, estados, campañas, territorio, modalidades y sitios. La alta de módulo/submódulos en Super Admin es una actividad corta dentro de este sprint.

Alcance HU: **HU01, HU02, HU03, HU04, HU05, HU06, HU07, HU08, HU09, HU10, HU11, HU12, HU13, HU14, HU15, HU16, HU17, HU18**

ACTIVIDADES	HORAS PLANEADAS	ROL
Diseño de la base de datos del módulo (modelo lógico, tablas iniciales, índices, constraints tenant) + primeras migraciones Flyway	16	Fullstack
Arquitectura/diseño técnico del alcance HU01–HU18 y contratos de API	10	Fullstack
Implementación núcleo backend de Integración GRH + Catálogos núcleo (HU01–HU18)	18	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU01–HU18)	14	Fullstack
Revisión PR aprendices + pair BE/FE	10	Fullstack
Pruebas de integración y ajuste de criterios con QA	8	Fullstack
Hardening / deuda técnica del sprint	4	Fullstack
Entidades JPA, repositorios y adapters del alcance HU01–HU18 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU01–HU18)	20	Backend
Tests H2/tenant del alcance HU01–HU18	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU01–HU18	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU01–HU18	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 2 — Catálogos avanzados y motor de reglas (EP-01 cierre)

Objetivo: Restricciones, festivos, cortes, tipos de hora, compensatorio, cobertura, motor de reglas, flags de atributos e importación asistida desde Excel.

Alcance HU: **HU19, HU20, HU21, HU22, HU23, HU24, HU25, HU26, HU27**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura/diseño técnico del alcance HU19–HU27, contratos de API y migraciones Flyway del sprint (si el esquema crece)	12	Fullstack
Implementación núcleo backend de Catálogos avanzados + motor (HU19–HU27)	22	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU19–HU27)	16	Fullstack
Revisión PR aprendices + pair BE/FE	14	Fullstack
Pruebas de integración y ajuste de criterios con QA	10	Fullstack
Hardening / deuda técnica del sprint	6	Fullstack
Entidades JPA, repositorios y adapters del alcance HU19–HU27 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU19–HU27)	20	Backend
Tests H2/tenant del alcance HU19–HU27	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU19–HU27	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU19–HU27	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 3 — Construcción de malla core (EP-02)

Objetivo: Crear malla, grupo, asignar turno/estado/extra/territorio/modalidad-sitio/nota y visualizar la grilla operativa.

Alcance HU: **HU28, HU29, HU30, HU31, HU32, HU33, HU34, HU35**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura/diseño técnico del alcance HU28–HU35, contratos de API y migraciones Flyway del sprint (si el esquema crece)	12	Fullstack
Implementación núcleo backend de Construcción de malla core (HU28–HU35)	22	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU28–HU35)	16	Fullstack
Revisión PR aprendices + pair BE/FE	14	Fullstack
Pruebas de integración y ajuste de criterios con QA	10	Fullstack
Hardening / deuda técnica del sprint	6	Fullstack
Entidades JPA, repositorios y adapters del alcance HU28–HU35 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU28–HU35)	20	Backend
Tests H2/tenant del alcance HU28–HU35	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU28–HU35	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU28–HU35	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 4 — Construcción avanzada (EP-02 cierre)

Objetivo: Campaña en celda, cobertura cruzada, filtros, concurrencia, carga parcial, copia masiva y fijar atributo por periodo.

Alcance HU: **HU36, HU37, HU38, HU39, HU40, HU41, HU42**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura/diseño técnico del alcance HU36–HU42, contratos de API y migraciones Flyway del sprint (si el esquema crece)	12	Fullstack
Implementación núcleo backend de Construcción avanzada (HU36–HU42)	22	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU36–HU42)	16	Fullstack
Revisión PR aprendices + pair BE/FE	14	Fullstack
Pruebas de integración y ajuste de criterios con QA	10	Fullstack
Hardening / deuda técnica del sprint	6	Fullstack
Entidades JPA, repositorios y adapters del alcance HU36–HU42 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU36–HU42)	20	Backend
Tests H2/tenant del alcance HU36–HU42	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU36–HU42	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU36–HU42	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 5 — Validación y rotación base (EP-03)

Objetivo: Contadores, equilibrio, conflictos, patrón, vínculo, simulación, exclusiones y aplicar rotación.

Alcance HU: **HU43, HU44, HU45, HU46, HU47, HU48, HU49, HU50**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura/diseño técnico del alcance HU43–HU50, contratos de API y migraciones Flyway del sprint (si el esquema crece)	12	Fullstack
Implementación núcleo backend de Validación y rotación base (HU43–HU50)	22	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU43–HU50)	16	Fullstack
Revisión PR aprendices + pair BE/FE	14	Fullstack
Pruebas de integración y ajuste de criterios con QA	10	Fullstack
Hardening / deuda técnica del sprint	6	Fullstack
Entidades JPA, repositorios y adapters del alcance HU43–HU50 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU43–HU50)	20	Backend
Tests H2/tenant del alcance HU43–HU50	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU43–HU50	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU43–HU50	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 6 — Rotación avanzada y publicación (EP-03 / EP-04)

Objetivo: Asistida, breaks, sitios, reequilibrio, restricciones al rotar, ajuste manual y ciclo de publicación.

Alcance HU: **HU51, HU52, HU53, HU54, HU55, HU56, HU57, HU58, HU59**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura/diseño técnico del alcance HU51–HU59, contratos de API y migraciones Flyway del sprint (si el esquema crece)	12	Fullstack
Implementación núcleo backend de Rotación avanzada + publicación (HU51–HU59)	22	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU51–HU59)	16	Fullstack
Revisión PR aprendices + pair BE/FE	14	Fullstack
Pruebas de integración y ajuste de criterios con QA	10	Fullstack
Hardening / deuda técnica del sprint	6	Fullstack
Entidades JPA, repositorios y adapters del alcance HU51–HU59 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU51–HU59)	20	Backend
Tests H2/tenant del alcance HU51–HU59	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU51–HU59	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU51–HU59	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 7 — Novedades, consulta y empleado (EP-05 / EP-06 / EP-07)

Objetivo: Novedades, ownership, historial, notificaciones, consulta operativa y vistas del empleado.

Alcance HU: **HU60, HU61, HU62, HU63, HU64, HU65, HU66, HU67, HU68, HU69**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura/diseño técnico del alcance HU60–HU69, contratos de API y migraciones Flyway del sprint (si el esquema crece)	12	Fullstack
Implementación núcleo backend de Novedades, consulta y empleado (HU60–HU69)	22	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU60–HU69)	16	Fullstack
Revisión PR aprendices + pair BE/FE	14	Fullstack
Pruebas de integración y ajuste de criterios con QA	10	Fullstack
Hardening / deuda técnica del sprint	6	Fullstack
Entidades JPA, repositorios y adapters del alcance HU60–HU69 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU60–HU69)	20	Backend
Tests H2/tenant del alcance HU60–HU69	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU60–HU69	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU60–HU69	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 8 — Reportes y horas (EP-08)

Objetivo: Cálculo de horas, export, novedad vs operativa, cobertura terceros, plantilla/import TH y compensatorio.

Alcance HU: **HU70, HU71, HU72, HU73, HU74, HU75, HU76**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura/diseño técnico del alcance HU70–HU76, contratos de API y migraciones Flyway del sprint (si el esquema crece)	12	Fullstack
Implementación núcleo backend de Reportes y horas (HU70–HU76)	22	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU70–HU76)	16	Fullstack
Revisión PR aprendices + pair BE/FE	14	Fullstack
Pruebas de integración y ajuste de criterios con QA	10	Fullstack
Hardening / deuda técnica del sprint	6	Fullstack
Entidades JPA, repositorios y adapters del alcance HU70–HU76 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU70–HU76)	20	Backend
Tests H2/tenant del alcance HU70–HU76	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU70–HU76	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU70–HU76	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 9 — Intercambio y estabilización (EP-09)

Objetivo: Configurar, solicitar, validar, aprobar y aplicar intercambio; hardening y salida a piloto.

Alcance HU: **HU77, HU78, HU79, HU80, HU81**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura/diseño técnico del alcance HU77–HU81, contratos de API y migraciones Flyway del sprint (si el esquema crece)	12	Fullstack
Implementación núcleo backend de Intercambio + estabilización (HU77–HU81)	22	Fullstack
Pieza FE compleja o patrón reutilizable del sprint (HU77–HU81)	16	Fullstack
Revisión PR aprendices + pair BE/FE	14	Fullstack
Pruebas de integración y ajuste de criterios con QA	10	Fullstack
Hardening / deuda técnica del sprint	6	Fullstack
Entidades JPA, repositorios y adapters del alcance HU77–HU81 (sobre el esquema definido y migrado por Fullstack)	18	Backend
Use cases + puertos del sprint (HU77–HU81)	20	Backend
Tests H2/tenant del alcance HU77–HU81	16	Backend
Colección API / fixtures de datos	12	Backend
Pair hexagonal con Fullstack y corrección PR	10	Backend
Ajustes por feedback QA	4	Backend
Pantallas/flujos Angular del alcance HU77–HU81	22	Frontend
Integración servicios domain/infra + estados UI	16	Frontend
GrhUiTexts, vacíos, validaciones y permisos de sección	14	Frontend
Pair UI con Fullstack	12	Frontend
Ajustes UX por feedback QA	10	Frontend
Regresión visual del sprint	6	Frontend
Diseño de casos y matriz de trazabilidad HU77–HU81	16	QA
Ejecución pruebas funcionales del sprint	18	QA
Datos de prueba (empresa/frente/roles) y escenarios negativos	12	QA
Retest defectos + regresión humo de sprints previos	14	QA
Evidencia y checklist de cierre	10	QA
Pair con Fullstack sobre criterios de aceptación	10	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Criterios de priorización si hay que cortar

1. Mantener: Sprint 1–4 y 6–8 (módulo usable: integra, parametriza, arma, publica, empleado ve, exporta horas).
2. Diferir parcial Sprint 5–6 modo automático completo (dejar manual + conflictos/contadores).
3. Diferir Sprint 9 (intercambio) si el frente piloto nace con la capacidad off y negocio lo acepta temporalmente.
4. Fullstack: diseño BD en Sprint 1; Flyway siempre a cargo de Fullstack. Backend: use cases/JPA/adapters/tests, sin Flyway.

