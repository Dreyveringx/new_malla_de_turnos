# Backlog de sprints DETALLADO — Malla de Turnos

> Propuesta nueva. **No reemplaza** `BACKLOG-SPRINTS-MALLA-TURNOS.xlsx`.

| Campo | Valor |
| ----- | ----- |
| Archivo Excel | `docs/BACKLOG-SPRINTS-MALLA-TURNOS-DETALLADO.xlsx` |
| Versión | 1.2 — cada actividad con HU; BD solo Sprint 1; Backend sin Flyway |
| Sprints | 9 (Sprint 1 … Sprint 9) |
| Capacidad | 80 h / rol / sprint |

- **Diseño de BD (modelo):** solo Sprint 1, rol Fullstack.
- **Flyway:** siempre Fullstack.
- **Backend:** JPA/repos/adapters/use cases/tests; no Flyway.
- **HU en actividades:** cada fila indica entre paréntesis la(s) HU que cubre.

---

## Sprint 1 — Integración GRH y catálogos núcleo (EP-00 / EP-01 inicio)

Objetivo: Dejar el módulo usable en menú/permisos/tenant y parametrizar frentes, turnos, estados, campañas, territorio, modalidades y sitios.

Alcance HU: **HU01–HU08 (integración) + HU09–HU18 (catálogos núcleo)**

ACTIVIDADES	HORAS PLANEADAS	ROL
Diseño BD del módulo: modelo lógico ms_malla_turnos (frentes, capacidades, turnos, estados, campañas, territorio, modalidades, sitios) + convenciones tenant (HU01, HU04, HU09–HU18)	14	Fullstack
Migraciones de base de datos (Flyway) iniciales + carga inicial de módulo/submódulos en company-admin (HU01)	10	Fullstack
Arquitectura integración GRH (auth/employee/parametrization) + núcleo frentes/turnos/estados (HU04–HU06, HU09–HU14)	16	Fullstack
Patrón Frontend reutilizable de alta/edición/consulta para parametrización listado/formulario (HU09–HU18)	12	Fullstack
Revisión de código + sesión conjunta adapters/tenant y pantallas Super Admin / Parametrización (HU01–HU03, HU09–HU18)	12	Fullstack
Pruebas de integración menú-permisos-frente-tenant + ajuste con QA (HU01–HU08)	10	Fullstack
Endurecimiento índices/UNIQUE(company_id, code) + deuda técnica (HU04, HU09–HU18)	6	Fullstack
Entidades JPA/repos/adapters: frentes, capacidades, plantillas turno, horarios por día, breaks (HU09–HU13)	18	Backend
Entidades JPA/repos/adapters: estados, campañas, territorio, modalidades, sitios + vínculos (HU14–HU18)	14	Backend
Casos de uso de alta/edición/consulta catálogos núcleo + validaciones activo/unicidad/vigencia (HU09–HU18)	18	Backend
Adapters consumo empleados/áreas/festivos GRH + pruebas automatizadas de aislamiento por empresa (HU04, HU05, HU08)	14	Backend
Colección de pruebas de API / datos de prueba empresa-frente-catálogos (HU08–HU18)	10	Backend
Sesión conjunta de arquitectura Backend + ajustes con QA / corrección de código (HU01–HU18)	6	Backend
Pantallas Super Admin / permisos / alcance de frentes (HU01–HU03)	12	Frontend
Pantallas de alta/edición/consulta Angular frentes + capacidades del frente (HU09–HU10)	14	Frontend
Pantallas de alta/edición/consulta Angular turnos, horarios por día, breaks (HU11–HU13)	14	Frontend
Pantallas de alta/edición/consulta Angular estados, campañas, territorio, modalidades, sitios (HU14–HU18)	16	Frontend
Textos de interfaz GRH, vacíos, validaciones y permisos de sección (HU01–HU03, HU09–HU18)	10	Frontend
Sesión conjunta de interfaz + ajustes de experiencia de usuario por QA + regresión visual (HU01–HU18)	14	Frontend
Matriz de trazabilidad y casos felices/negativos de catálogos (HU01–HU18)	16	QA
Pruebas funcionales integración: menú, permisos, tenant, listado empleados (HU01–HU08)	14	QA
Pruebas funcionales de alta/edición/consulta catálogos núcleo y unicidad por empresa (HU09–HU18)	16	QA
Datos de prueba multi-empresa/frente + escenarios negativos (HU04, HU08–HU10)	12	QA
Volver a probar defectos + evidencia/checklist de cierre + revisión conjunta de criterios de aceptación (HU01–HU18)	22	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 2 — Catálogos avanzados y motor de reglas (EP-01 cierre)

Objetivo: Cerrar parametrización avanzada: restricciones, cortes, tipos de hora, cobertura, compensatorio, motor de validación, flags de celda e import Excel asistida.

Alcance HU: **HU19, HU20, HU21, HU22, HU23, HU24, HU25, HU26, HU27**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura motor de reglas (info/advertencia/bloqueo) + contrato de evaluación (HU25)	12	Fullstack
Migraciones de base de datos (Flyway) del sprint: reglas, tipos hora, cortes, restricciones, flags (HU19–HU26)	10	Fullstack
Implementación núcleo motor de reglas + evaluación sobre datos de prueba de celda (HU23–HU25)	16	Fullstack
Diseño/implementación import Excel asistida mapeo columnas a catálogos (HU27)	14	Fullstack
Revisión de código + sesión conjunta Backend/Frontend sobre reglas, flags e import (HU19–HU27)	12	Fullstack
Pruebas integración motor + import con QA (HU25, HU27)	10	Fullstack
Endurecimiento parámetros/umbrales sin valores fijos en código + deuda técnica (HU23–HU26)	6	Fullstack
Entidades JPA/repos/adapters: tipos hora, cortes, compensatorio, cobertura, restricciones (HU19–HU24)	18	Backend
Casos de uso motor de reglas CRUD+evaluate y flags de atributos de celda del frente (HU25–HU26)	20	Backend
Casos de uso import asistida (validación previa + commit) + pruebas automatizadas (HU27)	18	Backend
Colección de pruebas de API reglas/import + datos de prueba (HU19–HU27)	12	Backend
Sesión conjunta de arquitectura Backend + ajustes con QA (HU19–HU27)	12	Backend
Pantallas de alta/edición/consulta restricciones, cortes, tipos hora, compensatorio, cobertura (HU19–HU24)	20	Frontend
Pantalla motor de reglas (lista, severidad, parámetros) + flags de celda del frente (HU25–HU26)	18	Frontend
Pantalla import Excel asistida: carga, mapeo, vista previa de errores, confirmar (HU27)	16	Frontend
Textos de interfaz GRH / validaciones + sesión conjunta de interfaz + ajustes con QA + regresión visual (HU19–HU27)	26	Frontend
Casos y matriz de trazabilidad reglas/severidades/import (HU19–HU27)	16	QA
Ejecución pruebas motor info/advertencia/bloqueo y cobertura/compensatorio (HU23–HU25)	18	QA
Pruebas import Excel: válido, columnas faltantes, duplicados (HU27)	14	QA
Datos de prueba + volver a probar + evidencia/cierre + revisión conjunta de criterios de aceptación (HU19–HU27)	32	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 3 — Construcción de malla core (EP-02)

Objetivo: Crear malla por periodo/frente, seleccionar personas y asignar turno/estado/extra/territorio/modalidad-sitio/nota sobre grilla operativa.

Alcance HU: **HU28, HU29, HU30, HU31, HU32, HU33, HU34, HU35**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura grilla: API de ventana, modelo de celda, bloqueo optimista básico para evitar sobrescritura (HU28, HU35)	12	Fullstack
Migraciones de base de datos (Flyway): schedule_grid, schedule_grid_person, schedule_cell (HU28–HU35)	10	Fullstack
Implementación núcleo crear malla + asignar turno/estado/slot extra (HU28, HU30–HU31)	18	Fullstack
Patrón Frontend de grilla operativa: selección de celda y paginación inicial (HU35)	14	Fullstack
Revisión de código + sesión conjunta Backend/Frontend grilla y asignación (HU28–HU35)	10	Fullstack
Pruebas integración asignación y grilla con QA (HU30–HU35)	10	Fullstack
Endurecimiento performance consultas de celda + deuda técnica (HU35)	6	Fullstack
Entidades JPA/repos/adapters: malla, personas de malla y celdas (HU28–HU31)	18	Backend
Casos de uso crear malla, alta/baja personas, asignar turno/estado/extra (HU28–HU31)	20	Backend
Casos de uso atributos celda territorio/modalidad/sitio/observación + pruebas automatizadas (HU32–HU34)	18	Backend
Datos de prueba API malla semanal + colección de pruebas de API (HU28–HU35)	12	Backend
Sesión conjunta + ajustes con QA (HU28–HU35)	12	Backend
Pantalla crear malla + selección de grupo de funcionarios (HU28–HU29)	16	Frontend
Grilla operativa: render filas/columnas, asignar turno/estado, slot extra (HU30–HU31, HU35)	22	Frontend
Asignación territorio/modalidad/sitio/nota desde celda o panel (HU32–HU34)	16	Frontend
Estados de interfaz/servicios + textos de interfaz GRH + sesión conjunta + ajustes con QA + regresión (HU28–HU35)	26	Frontend
Casos de prueba crear/asignar/atributos/grilla (HU28–HU35)	16	QA
Ejecución funcional grilla y asignaciones incluyendo segundo turno (HU30–HU31, HU35)	20	QA
Datos multi-persona/periodo + negativos sin permiso/frente inactivo (HU28–HU29)	14	QA
Volver a probar + evidencia/cierre + revisión conjunta de criterios de aceptación (HU28–HU35)	30	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 4 — Construcción avanzada (EP-02 cierre)

Objetivo: Campaña en celda, cobertura cruzada, filtros, concurrencia, carga parcial, copia masiva y fijar atributos por periodo.

Alcance HU: **HU36, HU37, HU38, HU39, HU40, HU41, HU42**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura concurrencia optimista + API ventana temporal/paginación personas (HU39–HU40)	14	Fullstack
Migraciones de base de datos (Flyway): version/locked_attrs u otros del alcance (HU39, HU42)	8	Fullstack
Implementación núcleo copia masiva / fijar atributo por periodo (HU41–HU42)	18	Fullstack
Patrón Frontend filtros avanzados + manejo de conflicto de versión en la interfaz (HU38–HU39)	14	Fullstack
Revisión de código + sesión conjunta Backend/Frontend (HU36–HU42)	10	Fullstack
Pruebas integración concurrencia/copia con QA (HU39, HU41)	10	Fullstack
Endurecimiento carga parcial y deuda técnica (HU40)	6	Fullstack
Casos de uso campaña en celda, cobertura cruzada y filtros en el servidor (HU36–HU38)	18	Backend
Casos de uso concurrencia version/conflict, carga parcial y paginación + adapters (HU39–HU40)	20	Backend
Casos de uso copiar semana/masivo y fijar atributo por rango + pruebas automatizadas (HU41–HU42)	18	Backend
Datos de prueba escenarios de conflicto + colección de pruebas de API (HU39–HU42)	12	Backend
Sesión conjunta + ajustes con QA (HU36–HU42)	12	Backend
Pantalla asignar campaña + cobertura cruzada otro frente/área (HU36–HU37)	14	Frontend
Pantalla filtros/búsqueda grilla + carga parcial ventana/paginación (HU38, HU40)	18	Frontend
Pantalla conflicto de edición, copia masiva y fijar atributo por periodo (HU39, HU41–HU42)	20	Frontend
Servicios/textos + sesión conjunta + ajustes con QA + regresión visual (HU36–HU42)	28	Frontend
Casos filtros, conflicto, copia y fix atributo (HU36–HU42)	16	QA
Ejecución concurrencia A guarda / B falla y copia masiva (HU39, HU41)	18	QA
Pruebas performance básica carga parcial + datos de prueba (HU40)	14	QA
Volver a probar + evidencia/cierre + revisión conjunta de criterios de aceptación (HU36–HU42)	32	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 5 — Validación y rotación base (EP-03)

Objetivo: Indicadores de cobertura/equilibrio, conflictos en grilla, patrones de rotación, simulación, exclusiones y aplicación a la malla.

Alcance HU: **HU43, HU44, HU45, HU46, HU47, HU48, HU49, HU50**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura flujo de rotación: definir, vincular, simular, excluir, aplicar (HU46–HU50)	12	Fullstack
Migraciones de base de datos (Flyway): patrones/pasos/vínculos/exclusiones (HU46–HU49)	10	Fullstack
Implementación núcleo simulación/aplicación de patrón + contadores cobertura (HU43, HU48, HU50)	18	Fullstack
Patrón Frontend visualización conflictos/indicadores sobre grilla (HU43–HU45)	14	Fullstack
Revisión de código + sesión conjunta Backend/Frontend rotación (HU43–HU50)	10	Fullstack
Pruebas integración simulación vs aplicación con QA (HU48, HU50)	10	Fullstack
Endurecimiento consistencia simulación/aplicar + deuda (HU48–HU50)	6	Fullstack
Entidades JPA/repos/adapters: patrones y pasos de rotación + vínculos (HU46–HU47)	16	Backend
Casos de uso indicadores cobertura/equilibrio + evaluate conflictos en grilla (HU43–HU45)	20	Backend
Casos de uso simular/excluir/aplicar rotación transaccional + pruebas automatizadas (HU48–HU50)	20	Backend
Datos de prueba patrones + colección de pruebas de API (HU46–HU50)	12	Backend
Sesión conjunta + ajustes con QA (HU43–HU50)	12	Backend
Pantalla indicadores cobertura/equilibrio y panel de conflictos (HU43–HU45)	18	Frontend
Pantalla de alta/edición/consulta patrón + vincular a grupo/periodo (HU46–HU47)	16	Frontend
Pantalla simulación con vista previa, exclusiones y confirmar aplicación (HU48–HU50)	18	Frontend
Textos/estados + sesión conjunta + ajustes con QA + regresión (HU43–HU50)	28	Frontend
Casos indicadores, conflictos y simulación (HU43–HU50)	16	QA
Ejecución rotación: simular no persiste; aplicar sí persiste (HU48, HU50)	18	QA
Negativos exclusiones/patrón incompleto + datos de prueba (HU46, HU49)	14	QA
Volver a probar + evidencia/cierre + revisión conjunta de criterios de aceptación (HU43–HU50)	32	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 6 — Rotación avanzada y publicación (EP-03 / EP-04)

Objetivo: Construcción asistida, distribución de pausas, rotación de sitios, reequilibrio, ajuste manual y ciclo de publicación (revisión/rechazo/edición publicada).

Alcance HU: **HU51, HU52, HU53, HU54, HU55, HU56, HU57, HU58, HU59**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura ciclo de vida publicación borrador/revisión/publicada/rechazada + política post-pub (HU57–HU59)	12	Fullstack
Migraciones de base de datos (Flyway): status, rejection_reason, published_at y relacionados (HU57–HU59)	8	Fullstack
Implementación núcleo publicación/rechazo + reequilibrio post-novedad (HU54, HU57–HU58)	18	Fullstack
Patrón Frontend asistente de armado + estados de publicación (HU51, HU57)	14	Fullstack
Revisión de código + sesión conjunta Backend/Frontend (HU51–HU59)	12	Fullstack
Pruebas integración publicación y asistida con QA (HU51, HU57–HU59)	10	Fullstack
Endurecimiento reglas al rotar/asignar + deuda (HU55–HU56)	6	Fullstack
Casos de uso construcción asistida, distribución breaks/almuerzos, rotación sitios (HU51–HU53)	20	Backend
Casos de uso reequilibrio, aplicar motor al rotar, ajuste manual post-sugerencia (HU54–HU56)	18	Backend
Casos de uso ciclo publicación/rechazo/editar publicada + pruebas automatizadas (HU57–HU59)	18	Backend
Datos de prueba estados de malla + colección de pruebas de API (HU57–HU59)	12	Backend
Sesión conjunta + ajustes con QA (HU51–HU59)	12	Backend
Pantalla asistida + distribución pausas + rotación sitios + reequilibrio (HU51–HU54)	20	Frontend
Pantalla ajuste manual post-rotación y feedback de reglas (HU55–HU56)	14	Frontend
Pantalla ciclo publicación: revisión, publicar, rechazar con motivo, editar publicada (HU57–HU59)	18	Frontend
Textos/estados + sesión conjunta + ajustes con QA + regresión (HU51–HU59)	28	Frontend
Casos asistida, publicación y rechazo (HU51–HU59)	16	QA
Ejecución ciclo de vida completo + edición post-publicación según config (HU57–HU59)	18	QA
Negativos rechazo sin motivo / publicar sin permiso + datos (HU57–HU58)	14	QA
Volver a probar + evidencia/cierre + revisión conjunta de criterios de aceptación (HU51–HU59)	32	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 7 — Novedades, consulta y empleado (EP-05 / EP-06 / EP-07)

Objetivo: Novedades en celda, responsable de novedad (MVP), historial inmutable, notificaciones; consulta quién está disponible; vistas de empleado (grupo/propia/historial).

Alcance HU: **HU60, HU61, HU62, HU63, HU64, HU65, HU66, HU67, HU68, HU69**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura historial inmutable + disparo de notificaciones relevantes (HU62–HU63)	12	Fullstack
Migraciones de base de datos (Flyway): historial solo-agregar / responsable de novedades (HU60–HU62)	8	Fullstack
Implementación núcleo novedad en celda + historial + consulta operativa (HU60, HU62, HU65–HU66)	18	Fullstack
Patrón Frontend vistas empleado día/semana/mes y política de visibilidad de grupo (HU67–HU69)	14	Fullstack
Revisión de código + sesión conjunta Backend/Frontend (HU60–HU69)	12	Fullstack
Pruebas integración notificación/historial con QA (HU62–HU64)	10	Fullstack
Endurecimiento políticas de visibilidad + deuda (HU67)	6	Fullstack
Casos de uso aplicar novedad, responsable de la novedad (MVP), historial por celda/funcionario (HU60–HU62, HU64)	20	Backend
Casos de uso notificar cambio relevante sin aceptación + adapter notification (HU63)	16	Backend
Casos de uso consulta turno/disponible/cobertura + vistas empleado + pruebas automatizadas (HU65–HU69)	20	Backend
Datos de prueba novedades/historial + colección de pruebas de API (HU60–HU69)	12	Backend
Sesión conjunta + ajustes con QA (HU60–HU69)	12	Backend
Pantalla aplicar novedad + responsable de novedad + consulta historial funcionario (HU60–HU61, HU64)	16	Frontend
Pantalla consulta operativa quién está / cobertura del día (HU65–HU66)	16	Frontend
Pantalla empleado: mi programación, grupo según política, historial reciente (HU67–HU69)	20	Frontend
Textos/estados + sesión conjunta + ajustes con QA + regresión (HU60–HU69)	28	Frontend
Casos novedad, historial, empleado y consulta (HU60–HU69)	16	QA
Ejecución notificaciones y políticas de visibilidad de grupo (HU63, HU67)	16	QA
Consulta operativa + vistas empleado + datos de prueba (HU65–HU69)	16	QA
Volver a probar + evidencia/cierre + revisión conjunta de criterios de aceptación (HU60–HU69)	32	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 8 — Reportes y horas (EP-08)

Objetivo: Calcular horas por tipo, exportar malla/cobertura, cruzar novedades TH y aplicar compensatorio en reporte (sin liquidar pesos).

Alcance HU: **HU70, HU71, HU72, HU73, HU74, HU75, HU76**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura cálculo de horas por tipos configurados + flujo de importación TH (HU70, HU74–HU75)	12	Fullstack
Migraciones de base de datos (Flyway): tabla temporal TH / params de reporte si aplica (HU74–HU75)	8	Fullstack
Implementación núcleo cálculo horas + export Excel/PDF (HU70–HU71)	18	Fullstack
Patrón Frontend reportes/filtros de periodo + vista previa cruce TH (HU70, HU75)	14	Fullstack
Revisión de código + sesión conjunta Backend/Frontend (HU70–HU76)	12	Fullstack
Pruebas integración cálculo/export/import con QA (HU70–HU76)	10	Fullstack
Endurecimiento performance reportes + deuda (HU70–HU73)	6	Fullstack
Casos de uso calcular horas por tipo y novedad vs operativa (HU70, HU72)	18	Backend
Casos de uso export malla Excel/PDF y cobertura para terceros (HU71, HU73)	18	Backend
Casos de uso plantilla import TH, cruce con programación, compensatorio + pruebas automatizadas (HU74–HU76)	20	Backend
Datos de prueba periodos/novedades TH + colección de pruebas de API (HU70–HU76)	12	Backend
Sesión conjunta + ajustes con QA (HU70–HU76)	12	Backend
Pantalla reporte horas: filtros, tipos, desglose novedad vs operativa (HU70, HU72)	18	Frontend
Pantalla export malla/cobertura + descarga archivos (HU71, HU73)	14	Frontend
Pantalla plantilla import TH + cruce/resultados + compensatorio en reporte (HU74–HU76)	20	Frontend
Textos/estados + sesión conjunta + ajustes con QA + regresión (HU70–HU76)	28	Frontend
Casos cálculo, export, import TH y compensatorio (HU70–HU76)	16	QA
Ejecución cálculo horas y contrastes con flags de estado (HU70, HU72)	18	QA
Pruebas import/cruce TH + exports + datos (HU71, HU73–HU75)	14	QA
Volver a probar + evidencia/cierre + revisión conjunta de criterios de aceptación (HU70–HU76)	32	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

## Sprint 9 — Intercambio y estabilización (EP-09)

Objetivo: Configurar intercambio por frente, solicitar, validar con reglas, aprobar/rechazar, aplicar con auditoría/notificación; estabilizar para piloto.

Alcance HU: **HU77, HU78, HU79, HU80, HU81**

ACTIVIDADES	HORAS PLANEADAS	ROL
Arquitectura flujo intercambio: config, solicitud, validación, aprobación, apply atómico (HU77–HU81)	12	Fullstack
Migraciones de base de datos (Flyway): shift_swap_request y relacionados (HU77–HU81)	8	Fullstack
Implementación núcleo aplicación del intercambio todo-o-nada + notificaciones (HU81)	14	Fullstack
Hardening/estabilización piloto: regresión transversal, performance, deuda crítica (HU77–HU81)	16	Fullstack
Revisión de código + sesión conjunta Backend/Frontend intercambio (HU77–HU81)	12	Fullstack
Pruebas integración flujo completo con QA + prueba rápida de punta a punta del piloto (HU77–HU81)	12	Fullstack
Ajustes finales de salida a piloto (HU77–HU81)	6	Fullstack
Entidades JPA/repos/adapters: solicitudes de intercambio + config por frente (HU77–HU78)	16	Backend
Casos de uso habilitar/configurar, solicitar, validar con motor (HU77–HU79)	20	Backend
Casos de uso aprobar/rechazar, aplicar + auditar + notificar + pruebas automatizadas con reversión de cambios (HU80–HU81)	20	Backend
Datos de prueba solicitudes + colección de pruebas de API (HU77–HU81)	12	Backend
Sesión conjunta + estabilización de defectos del piloto + ajustes con QA (HU77–HU81)	12	Backend
Pantalla config intercambio del frente (HU77)	12	Frontend
Pantalla solicitar intercambio mi celda / contraparte + warnings de reglas (HU78–HU79)	18	Frontend
Pantalla bandeja aprobar/rechazar + confirmación de aplicación (HU80–HU81)	18	Frontend
Ajustes UX piloto + sesión conjunta + regresión visual amplia (HU77–HU81)	32	Frontend
Casos + matriz de punta a punta intercambio (HU77–HU81)	14	QA
Ejecución flujo completo on/off por frente, rechazo y apply (HU77–HU81)	18	QA
Regresión humo transversal sprints 1–8 + datos piloto (HU01–HU76)	20	QA
Volver a probar + evidencia/cierre piloto + revisión conjunta de criterios de aceptación (HU77–HU81)	28	QA

Subtotal: Fullstack 80 · Backend 80 · Frontend 80 · QA 80

---

