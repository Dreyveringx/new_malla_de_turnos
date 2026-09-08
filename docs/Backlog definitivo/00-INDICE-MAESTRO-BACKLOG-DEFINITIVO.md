# BACKLOG DEFINITIVO — Malla de Turnos / GRH

| Campo | Valor |
| ----- | ----- |
| Fecha | 05/09/2026 |
| Estado | Definitivo para refinamiento PO → UX → Arquitectura → Dev → QA |
| Fuentes | Auditoría integral, HU01–HU76, levantamiento Fase 1, código GRH, Excel de descubrimiento |
| Principio | Máxima parametrización por empresa y frente. Cero hardcoding de reglas de negocio. |

Este documento es el **índice maestro**. Las HUs completas están en:

| Archivo | Épica |
| ------- | ----- |
| [EP-00-Integracion-GRH.md](./EP-00-Integracion-GRH.md) | Integración con GRH |
| [EP-01-Parametrizacion.md](./EP-01-Parametrizacion.md) | Parametrización y catálogos |
| [EP-02-Construccion.md](./EP-02-Construccion.md) | Construcción de malla |
| [EP-03-Validacion-Rotacion.md](./EP-03-Validacion-Rotacion.md) | Validación, cobertura y rotación |
| [EP-04-Publicacion.md](./EP-04-Publicacion.md) | Publicación |
| [EP-05-Novedades-Historial.md](./EP-05-Novedades-Historial.md) | Novedades, historial y notificaciones |
| [EP-06-Consulta-Operativa.md](./EP-06-Consulta-Operativa.md) | Consulta operativa |
| [EP-07-Vista-Empleado.md](./EP-07-Vista-Empleado.md) | Vista del empleado |
| [EP-08-Reportes-Horas.md](./EP-08-Reportes-Horas.md) | Reportes y horas |
| [EP-09-Intercambio.md](./EP-09-Intercambio.md) | Intercambio de turnos |

Los GST-FM-04 en `docs/Historias de usuario/` están **regenerados al 10/10** (markdown + Word) alineados a este backlog (05/09/2026).

---

## 1. Principios cerrados (ya decididos en análisis)

1. Frente operativo = **catálogo**, nunca enum de producto.
2. `companyId` solo del **contexto autenticado**.
3. Malla operativa **no escribe** jornada contractual.
4. Sitios de asistencia = catálogo **Malla** (GRH no tiene sedes hoy).
5. Estados de celda = catálogo + **flags** (no HU por vacaciones/incapacidad/actividad…).
6. Motor de reglas central (info / advertencia / bloqueo). Solape horario real = **invariante bloqueante**.
7. Rotación = **patrón genérico** (secuencia + duraciones). Sin enums 15/15.
8. Intercambio = **EP-09** incluida; puede nacer deshabilitada por configuración del frente.
9. Novedades = **estado de celda** + importación opcional de archivo (no hay módulo TH nativo en GRH hoy).
10. Historial de celda append-only + timeline GRH solo para hechos de alto nivel.
11. Horas ≠ dinero.
12. Módulo plataforma: **completar el existente** (DEV id=13), no duplicar.

---

## 2. Épicas finales

| Épica | Nombre | Objetivo |
| ----- | ------ | -------- |
| EP-00 | Integración GRH | Menú, RBAC, alcance frente, tenant, maestros, eventos |
| EP-01 | Parametrización | Frentes, catálogos, reglas, config |
| EP-02 | Construcción | Malla, grilla, celdas, concurrencia, performance |
| EP-03 | Validación y rotación | Conflictos, cobertura, patrones, simulación, asistida |
| EP-04 | Publicación | Ciclo de vida oficial |
| EP-05 | Novedades y auditoría | Estados novedad, historial, notificaciones |
| EP-06 | Consulta operativa | Quién está / cobertura del día |
| EP-07 | Vista empleado | Mi programación y grupo |
| EP-08 | Reportes y horas | Horas, export, cruce TH, compensatorio |
| EP-09 | Intercambio | Solicitud → validación → aprobación → aplicación |

---

## 3. Backlog final (ID · Título · Prioridad · Dependencia clave)

### EP-00

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU01 | Completar módulo y submódulos | Incluida | — |
| HU02 | Permisos RBAC por sección | Incluida | HU01 |
| HU03 | Alcance de frentes a usuarios/roles | Incluida | HU02, HU09 |
| HU04 | Aislar por empresa | Incluida | HU01 |
| HU05 | Reutilizar maestros GRH | Incluida | HU04, HU08 |
| HU06 | Jornada contractual vs malla | Incluida | HU05 |
| HU07 | Event types notification + timeline | Incluida | HU01 |
| HU08 | Listado empleados filtrado/paginado | Incluida | HU05 |

### EP-01

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU09 | Frentes operativos (catálogo) | Incluida | HU04 |
| HU10 | Capacidades / estrategia / publicación del frente | Incluida | HU09 |
| HU11 | Plantillas de turno | Incluida | HU09 |
| HU12 | Horarios por día | Incluida | HU11 |
| HU13 | Break / almuerzo | Incluida | HU11 |
| HU14 | Estados + flags | Incluida | HU09 |
| HU15 | Campañas / tareas | Incluida | HU10 |
| HU16 | Territorio niveles configurables | Incluida | HU10 |
| HU17 | Modalidades | Incluida | HU10 |
| HU18 | Sitios de asistencia | Incluida | HU10 |
| HU19 | Tipos y restricciones de persona | Incluida | HU05 |
| HU20 | Festivos calendario empresa | Incluida | HU05 |
| HU21 | Cortes de nómina | Incluida | — |
| HU22 | Tipos de hora | Incluida | HU21 |
| HU23 | Reglas compensatorio | Incluida | HU25 |
| HU24 | Reglas cobertura | Incluida | HU25 |
| HU25 | Motor de reglas | Incluida | HU10 |
| HU26 | Flags de atributos de celda | Incluida | HU10 |
| HU27 | Import asistida desde Excel | Incluida | catálogos |

### EP-02

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU28 | Crear malla | Incluida | HU10 |
| HU29 | Grupo de funcionarios | Incluida | HU28, HU08 |
| HU30 | Asignar turno/estado | Incluida | HU11, HU14, HU25 |
| HU31 | Segundo turno / extra | Incluida | HU26, HU30 |
| HU32 | Territorio en celda | Incluida | HU16 |
| HU33 | Modalidad y sitio | Incluida | HU17, HU18 |
| HU34 | Observación | Incluida | HU26 |
| HU35 | Visualizar grilla | Incluida | HU30, HU40 |
| HU36 | Campaña en celda | Incluida | HU15 |
| HU37 | Cobertura cruzada entre frentes | Incluida | HU25 |
| HU38 | Filtros de grilla | Incluida | HU35 |
| HU39 | Concurrencia (optimistic lock) | Incluida | HU30 |
| HU40 | Carga parcial grilla | Incluida | HU35 |
| HU41 | Copiar semana / asignación masiva | Incluida | HU30, HU25 |
| HU42 | Fijar atributo de celda por periodo | Incluida | HU26, HU30 |

### EP-03

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU43 | Indicadores cobertura | Incluida | HU24 |
| HU44 | Equilibrio por persona | Incluida | HU25 |
| HU45 | Panel de conflictos | Incluida | HU25 |
| HU46 | Patrón rotación genérico | Incluida | HU11 |
| HU47 | Vincular patrón a grupo/periodo | Incluida | HU46, HU10 |
| HU48 | Simular rotación (dry-run) | Incluida | HU47 |
| HU49 | Exclusiones de rotación | Incluida | HU47 |
| HU50 | Aplicar rotación | Incluida | HU48 |
| HU51 | Construcción asistida | Incluida | HU10 |
| HU52 | Distribuir breaks | Incluida | HU13 |
| HU53 | Rotar sitios | Incluida | HU18 |
| HU54 | Reequilibrar tras novedad | Incluida | HU60 |
| HU55 | Restricciones + reglas en asignación/rotación | Incluida | HU19, HU25 |
| HU56 | Ajuste manual post-rotación | Incluida | HU50/HU30 |

### EP-04

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU57 | Ciclo publicación | Incluida | HU10, HU45 |
| HU58 | Rechazar en revisión | Incluida | HU57 |
| HU59 | Editar publicada | Incluida | HU10, HU62 |

### EP-05

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU60 | Aplicar novedad (estado catálogo) | Incluida | HU14, HU61 |
| HU61 | Ownership MVP novedades | Incluida | HU14 |
| HU62 | Historial inmutable celda | Incluida | HU30 |
| HU63 | Notificar cambio empleado | Incluida | HU07 |
| HU64 | Historial por funcionario | Incluida | HU62 |

### EP-06

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU65 | Quién está en turno / disponible | Incluida | HU14 |
| HU66 | Cobertura del día | Incluida | HU24 |

### EP-07

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU67 | Programación del grupo | Incluida | HU57 |
| HU68 | Mi programación | Incluida | HU57 |
| HU69 | Historial de mis turnos | Incluida | HU62 |

### EP-08

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU70 | Calcular horas | Incluida | HU22, HU14 |
| HU71 | Export Excel/PDF | Incluida | HU35 |
| HU72 | Horas novedad vs operativas | Incluida | HU70 |
| HU73 | Export cobertura terceros | Incluida | HU66 |
| HU74 | Plantilla import novedades TH | Incluida | HU61 |
| HU75 | Cruzar con novedades TH | Incluida | HU74 |
| HU76 | Compensatorio en reporte | Incluida | HU23 |

### EP-09

| ID | Título | Alcance | Dep. |
| -- | ------ | --------- | ---- |
| HU77 | Configurar intercambio | Incluida | HU10 |
| HU78 | Solicitar intercambio | Incluida | HU77 |
| HU79 | Validar solicitud | Incluida | HU25 |
| HU80 | Aprobar/rechazar | Incluida | HU79 |
| HU81 | Aplicar, auditar, notificar | Incluida | HU80, HU62 |

---

## 4. Matriz de trazabilidad HU01–HU76

| HU ORIGINAL | ACCIÓN | HU FINAL | MOTIVO |
| ----------- | ------ | -------- | ------ |
| HU01 | Reescribir | HU01 | Anclar a módulo existente; no duplicar |
| HU02 | Dividir | HU02 + HU03 | RBAC menú ≠ alcance frente |
| HU04 | Reescribir | HU04 | Reforzar JWT / tenant |
| HU05 | Reescribir | HU05 | Sitios ≠ sedes GRH; empleados sin padrón paralelo |
| HU06 | Mantener/refinar | HU06 | Separación contractual vs operativa |
| HU11 | Reescribir | HU11 | Sin listas fijas de frentes/turnos |
| HU12 | Reescribir | HU12 | Variantes por día genéricas |
| HU13 | Reescribir | HU13 | Pausas como datos de plantilla |
| HU14 | Ampliar | HU14 | Flags completos; absorbe ex-HU50/ex-HU54 |
| HU15 | Reescribir | HU15 | Campañas catálogo |
| HU16 | Reescribir | HU16 | Niveles territoriales configurables |
| HU17 | Reescribir | HU17 | Modalidades + requiereSitio |
| HU18 | Reescribir | HU18 | Sitios catálogo; sin “Elemento” especial |
| HU19 | Reescribir | HU19 | Tipos de restricción catálogo |
| HU20 | Reescribir | HU20 | Solo lectura calendario GRH |
| HU21 | Reescribir | HU21 | Cortes sin dinero |
| HU22 | Reescribir | HU22 | Tipos de hora catálogo |
| HU23 | Reescribir | HU23 | Compensatorio parametrizable |
| HU24 | Reescribir | HU24 | Cobertura dimensional |
| HU26 | Dividir/refinar | HU10 + HU26 | Estrategia/publicación vs flags de celda |
| HU28 | Reescribir | HU28 | Malla por frente/periodo |
| HU29 | Reescribir | HU29 | Grupo + paginación |
| HU30 | Reescribir | HU30 | Celda + motor reglas |
| HU31 | Reescribir | HU31 | Multi-turno por capacidad |
| HU32 | Reescribir | HU32 | Territorio opcional |
| HU33 | Reescribir | HU33 | Modalidad/sitio opcional |
| HU34 | Reescribir | HU34 | Observación |
| HU35 | Reescribir | HU35 | Grilla + HU40 |
| HU36 | Reescribir | HU36 | Campaña opcional |
| HU37 | Reescribir | HU37 | Cruce frentes Fase 2 |
| HU38 | Reescribir | HU38 | Filtros dinámicos |
| HU43 | Reescribir | HU43 | Contadores desde reglas |
| HU44 | Reescribir | HU44 | Equilibrio parametrizable |
| HU45 | Dividir/reescribir | HU25 + HU45 | Motor vs panel UI; sin “42 h” |
| HU47 | Dividir | HU46 + HU47 | Patrón genérico + vínculo |
| HU50 | Reescribir | HU50 | Aplicar post simulación |
| HU51 | Reescribir | HU51 | Asistida según estrategia |
| HU52 | Reescribir | HU52 | Breaks desde plantillas |
| HU53 | Reescribir | HU53 | Rotación sitios genérica |
| HU54 | Reescribir | HU54 | Reequilibrio post novedad |
| HU55 | Reescribir | HU55 | Sin listar estudio/salud |
| HU56 | Reescribir | HU56 | Ajuste manual + origen |
| HU57 | Reescribir | HU57 | Ciclo vida + absorbe ex-HU46 |
| HU58 | Reescribir | HU58 | Rechazo |
| HU59 | Reescribir | HU59 | Post-publicación |
| ex-HU46 | Absorber | HU10 + HU57 | Constructor/publicador = config |
| HU60 | Reescribir | HU60 + HU61 | Estado catálogo + ownership |
| HU62 | Reescribir | HU62 | Historial dominio |
| HU63 | Reescribir | HU63 | notification-service |
| ex-HU50 | Absorber | HU14 + HU70 | Flag no suma horas |
| HU64 | Reescribir | HU64 | Historial por persona |
| HU65 | Reescribir | HU65 | Flags disponibilidad |
| HU66 | Reescribir | HU66 | Cobertura dimensional |
| ex-HU54 | Absorber | HU14 + HU65 | Flag no asignable |
| HU67 | Reescribir | HU67 | Visibilidad grupo configurable |
| HU68 | Reescribir | HU68 | Mi programación |
| HU69 | Reescribir | HU69 | Historial propio |
| HU70 | Reescribir | HU70 | Horas sin dinero ni 42h |
| HU71 | Reescribir | HU71 | Export |
| HU72 | Reescribir | HU72 | Novedad vs operativa por flags |
| HU73 | Reescribir | HU73 | Export terceros |
| HU75 | Reescribir | HU75 + HU74 | Cruce + plantilla import |
| HU76 | Reescribir | HU76 | Compensatorio desde HU23 |

### HUs nuevas (no existían en 01–63)

| ID | Título | Origen |
| -- | ------ | ------ |
| HU09 | Frentes catálogo | Anti-hardcoding |
| HU10 | Config frente (estrategia/publicación) | Split HU26 |
| HU25 | Motor de reglas | Split HU45 |
| HU46 | Patrón rotación genérico | Completar DSL |
| HU03 | Alcance frentes | Split HU02 |
| HU07 | Event types | Integración GRH |
| HU08 | Filtro/paginación empleados | Gap employee API |
| HU48 | Simulación rotación | Riesgo operativo |
| HU49 | Exclusiones rotación | Levantamiento |
| HU77–HU81 | Intercambio | EP-09 |
| HU39 | Concurrencia | Arquitectura |
| HU40 | Carga parcial grilla | Escalabilidad |
| HU61 | Ownership novedades | Gap TH |
| HU74 | Plantilla import TH | HU75 |
| HU27 | Import asistida Excel | Descubrimiento |

---

## 5. Decisiones de negocio realmente necesarias

Solo lo que **no** se cierra solo con un flag. El resto ya está convertido en parametrización con default.

| ID | Decisión | Por qué no es solo técnica | Impacto | Recomendación | Default |
| -- | -------- | -------------------------- | ------- | -------------- | ------- |
| D1 | ¿TH será fuente de verdad futura? | Ownership organizacional de RRHH | HU75/84, integraciones | MVP estado de celda + import; conector después | Estado + import |
| D2 | ¿Frente debe igualar 1:1 un área GRH? | Gobernanza org. vs flexibilidad operativa | HU09/65 | Frente propio con vínculo opcional a área(s) | Frente propio + vínculo opcional |
| D3 | ¿El grupo ve la malla de todos? | Privacidad laboral | HU67 | Pública dentro del grupo del frente | Pública en grupo |
| D4 | ¿Se puede publicar con advertencias? | Apetito de riesgo operativo | HU57 | Configurable por frente | Permitir con confirmación |
| D5 | ¿Intercambio en el primer release usable? | Capacidad del equipo / cambio cultural | EP-09 | Fase 2; config desde ya | Off |
| D6 | ¿Rotación automática en el primer release? | Madurez de patrones | EP-03 | Manual en MVP; asistida/auto en Fase 2 con dry-run | Manual; auto Fase 2 |
| D7 | ¿Horas en cobertura cruzada (dos mallas/día)? | Criterio de nómina | HU37, HU70 | Contar donde se asigna + solape bloqueante | Cuenta en malla de asignación |
| D8 | ¿Quién firma el formato oficial del archivo TH? | Convenio con TH externo | HU74 | Columnas mínimas comunes + mapeo | Plantilla XLSX parametrizable |

---

## 6. Orden de construcción (dependencias, no recortes de alcance)

Todas las HU del backlog definitivo están incluidas. El orden siguiente solo refleja dependencias técnicas/funcionales para construir el módulo de cero:

1. EP-00 integración (módulo, RBAC, tenant, eventos, empleados).
2. EP-01 catálogos, frentes, motor de reglas y configuración.
3. EP-02 grilla/celdas + concurrencia/carga parcial.
4. EP-03 validación, cobertura, rotación (patrón, simulación, aplicación) y armado asistido.
5. EP-04 publicación.
6. EP-05 novedades, historial y notificaciones.
7. EP-06 consulta operativa.
8. EP-07 vista empleado.
9. EP-08 horas, exportes, cruce TH y compensatorio.
10. EP-09 intercambio (configurable; puede nacer deshabilitado por frente, pero la capacidad está en el módulo).


## 7. Modelo conceptual

```
Empresa (tenant)
 └── Frente operativo (catálogo)
      ├── Config (periodo, estrategia, publicación, intercambio, flags celda)
      ├── Catálogos (turnos, estados, campañas, territorio, modalidades, sitios, reglas…)
      └── Malla (periodo + grupo)
           └── Celda (persona × fecha)
                ├── turno(s) / estado + atributos opcionales
                └── historial append-only
```

Invariantes: `company_id` · solape real bloqueante · historial inmutable · no escribir jornada contractual.

---

## 8. Checklist 10/10

### Funcional

- [x] Varios frentes por empresa
- [x] Reglas distintas por frente
- [x] Turnos / estados / restricciones / cobertura / horas parametrizables
- [x] Rotación genérica
- [x] Intercambio contemplado (EP-09)
- [x] Ownership novedades claro (HU61)
- [x] Publicación con ciclo claro
- [x] Historial inmutable
- [x] Vista empleado
- [x] Horas ≠ dinero

### Multiempresa

- [x] Tenant-scoped en todas las HUs relevantes
- [x] companyId no confiable desde frontend

### Parametrización (anti-hardcoding)

- [x] Sin frentes/turnos/estados/42h/3 domingos/Elemento/estudio-salud/15-15 quemados

### Arquitectura

- [x] Reuso employee / parametrization / notification / audit
- [x] Sin write a work_schedule
- [x] Concurrencia HU39
- [x] Performance grilla HU40

### UX/QA

- [x] CA Gherkin verificables
- [x] Errores, permisos y config en cada HU

---

## 9. Orden de construcción sugerido

1. EP-00 (módulo 13, RBAC, tenant, events, empleados)
2. EP-01 (frentes → catálogos → motor reglas → config)
3. EP-02 + EP-04 + EP-05 (grilla, publicar, novedad, historial) + HU39/82
4. EP-07 + HU70/59
5. EP-06
6. EP-03 (indicadores → asistida → rotación con dry-run)
7. EP-08 restante
8. EP-09 cuando D5 lo active

---

*Fin del índice maestro. Detalle de cada HU en los archivos EP-00 … EP-09 de esta carpeta.*
