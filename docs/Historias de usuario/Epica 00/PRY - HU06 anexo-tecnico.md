# Anexo técnico — MT-EP00-HU06 (solo desarrollo)

No incluir en presentaciones a cliente ni en Word GST-FM-04 para diseño.

La HU de negocio está en `GST-FM-04-MT-EP00-HU06-Distinguir-jornada-contractual-malla-operativa.md`.

## Decisión de arquitectura

| Dominio | MS / tablas | Propósito |
| ------- | ----------- | --------- |
| Jornada contractual | `employee` — `work_schedule`, `schedule_assignment` | Contrato laboral, tipo de jornada |
| Malla operativa | MS Malla (nuevo) — entidades propias | Grilla persona × día × turno/estado |

No persistir malla operativa en `work_schedule` ni `schedule_assignment`.

## Dependencias

| HU | Relación |
| -- | -------- |
| MT-EP00-HU05 | Mismo `employee_id`; sin duplicar maestros |
| EP-01 / EP-02 | Catálogo turno plantilla y entidad malla |

## Implementación

| Regla | Acción |
| ----- | ------ |
| Sin escritura cruzada | Use cases de Malla no llaman APIs de update de `work_schedule` |
| Lectura opcional | Puede mostrarse jornada contractual como referencia (solo lectura) vía employee |
| Nomenclatura código | Evitar `WorkSchedule` para entidades de malla; usar `ShiftTemplate`, `ScheduleGrid`, etc. |
| Reportes horas | Fuente = celdas malla publicadas, no `schedule_assignment` |

## Referencias

- `malla-turnos-context.md` — Malla ≠ work_schedule
- `LEVANTAMIENTO-MALLA-TURNOS-FASE1.md` — §10 fila jornada vs malla
- `Propuesta-HU-Malla-Turnos.md` — decisión dominio nuevo

## Pendientes técnicos

- Si en UI se muestra jornada contractual junto a la grilla (panel lateral)
- Validaciones de negocio que comparen malla vs jornada (advertencia, no bloqueo en EP-00)
