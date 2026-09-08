# Anexo técnico — MT-EP01-HU11 (solo desarrollo)

No incluir en presentaciones a cliente ni en Word GST-FM-04 para diseño.

## Entidad sugerida

`shift_template` (o equivalente en MS Malla):

| Columna | Tipo | Notas |
| ------- | ---- | ----- |
| id | UUID | PK |
| company_id | UUID | NOT NULL, tenant |
| operational_front | enum/string | CC, SITE, DESK, LAB |
| code | varchar(20) | UNIQUE (company_id, operational_front, code) |
| name | varchar(120) | |
| start_time | time | Horario base HU11 |
| end_time | time | |
| crosses_midnight | boolean | |
| is_night_shift | boolean | |
| application_days | jsonb o tabla hija | bitmask o filas por tipo de día |
| color | varchar(7) | hex |
| active | boolean | |

Horarios por día (HU12) y break/almuerzo (HU13) en tablas hijas `shift_template_day_schedule`, `shift_template_break`.

## API (borrador)

- `GET /v1/shift-templates?front=&active=`
- `POST /v1/shift-templates`
- `PUT /v1/shift-templates/{id}`
- Validar `company_id` desde JWT, no desde body

## UI

- Ruta: `malla-turnos/main/parametrizacion` → subruta plantillas (S01)
- Scope RBAC: submódulo Parametrización, permiso CREAR/ACTUALIZAR

## Referencias

- RF-01, RF-02 levantamiento
- `PROMPT-FIGMA-MALLA-TURNOS.md` — S01
