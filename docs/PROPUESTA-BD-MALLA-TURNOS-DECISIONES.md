# Decisiones BD Malla de Turnos v2

Revision post feedback: transversalidad, reuso GRH, quitar reglas de cobertura/compensatorio/restricciones/normas.

## Que ya existe en GRH y como se reutiliza

| Concepto | Donde esta | Como lo usa Malla |
|---|---|---|
| Empresa (tenant) | `ms_company_admin` / JWT | `company_id` UUID logico en todas las tablas |
| Empleado | `ms_employee` | `employee_id` UUID; datos por API |
| Areas / cargos | `organizational_areas`, `positions` | `front_area_link.area_id`; no duplicar |
| Usuarios / roles / permisos | `ms_auth` RBAC | Permisos de modulo; **sin** `front_role_scope` |
| Estados configurables | `entity_status` | `entity_type='malla_cell_state'` → estados de celda |
| Festivos / calendario | `company_calendar`, `national_holidays` | Lectura API para clasificacion de horas |
| Jornada contractual | `work_schedule`, `work_schedule_day`, `work_schedule_shift`, `schedule_assignment` | **No** reutilizar como plantilla de malla (otro dominio) |
| Modalidad de estudio | `study_modalities` | **No** sirve para modalidad laboral |
| Tipos de zona | `zone_types` | **No** es arbol operativo de cobertura |
| Auditoria | `ms_audit` (`audit_log` / timeline) | Reemplaza `schedule_cell_history` |
| Notificaciones | `ms_notification` | Eventos de publicacion/cambios |

## Catalogos NUEVOS en `ms_parametrization` (transversales)

- `catalog_code_sequence`
- `shift_template` + `break_type` + `shift_template_break`
- `work_modality`
- `attendance_site`
- `operational_label` (antes campaign)
- `territory` (arbol `parent_id`)
- `hour_classification_band`

## Dominio en `ms_malla_turnos`

Frente, capacidades, vinculos, rotacion, grilla, celdas, breaks de celda, swap, novedades, import Excel.

## Eliminado

`front_role_scope`, `attendance_site_front`, `shift_template_day_schedule`, `territory_level`, `territory_node`, `campaign` (→ label), `cell_state` (→ entity_status), `validation_rule` y toda cobertura/compensatorio/restricciones/normas, `schedule_cell_history` (→ audit), secuencia local de malla.
