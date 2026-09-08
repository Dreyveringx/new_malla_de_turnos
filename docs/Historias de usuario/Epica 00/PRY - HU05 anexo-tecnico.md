# Anexo técnico — MT-EP00-HU05 (solo desarrollo)

No incluir en presentaciones a cliente ni en Word GST-FM-04 para diseño.

La HU de negocio está en `GST-FM-04-MT-EP00-HU05-Reutilizar-maestros-grh.md`.

## Dependencias

| HU | Qué aporta |
| -- | ---------- |
| MT-EP00-HU04 | Filtro `company_id` en consultas |
| MT-EP02-HU29 | Selección formal del grupo de la malla |

## Fuentes GRH (no duplicar)

| Maestro | Microservicio | Uso en Malla |
| ------- | ------------- | ------------ |
| Funcionarios | `employee` | `employee_id` en filas de malla; búsqueda paginada |
| Áreas | `parametrization` | Filtros, frente ↔ `area_id` |
| Cargos | `parametrization` | Filtros y etiquetas |
| Calendario / festivos | `parametrization` (`company_calendar`) | Marcación en grilla y reglas de día festivo |

## Implementación

| Paso | Qué |
| ---- | --- |
| 1 | API Malla expone selector que delega en employee-service (por `companyId`) |
| 2 | Áreas/cargos: lectura parametrization; sin tabla local duplicada |
| 3 | Festivos: consulta calendario empresa; sin tabla `holidays` propia en MVP |
| 4 | Persistencia malla: guardar `employee_id`, no snapshot de PII salvo auditoría histórica acordada |
| 5 | Funcionario inactivo: validar en use case antes de nueva asignación |

## Frente ↔ área

Tabla o catálogo en Malla: `operational_front` con `area_id` opcional FK lógica a parametrization. Complementa MT-EP00-HU02.

## Prohibido

- Alta de empleado desde MS Malla
- CRUD de áreas/cargos/calendario desde MS Malla
- `unique` global en documento sin `company_id`

## Referencias

- `LEVANTAMIENTO-MALLA-TURNOS-FASE1.md` — §10 Matriz de información, RNF-02
- `PROMPT-FIGMA-MALLA-TURNOS.md` — selector no crea empleados

## Pendientes técnicos

- API exacta de búsqueda employee (filtros areaId, positionId, active)
- Cache vs tiempo real al cambiar área en GHV
- Vacaciones/incapacidades: otro MS o solo celda en malla (fuera de HU05)
