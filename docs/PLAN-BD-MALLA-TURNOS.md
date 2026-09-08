# Plan de base de datos — Malla de Turnos

| Campo | Valor |
| ----- | ----- |
| Fecha | 2026-09-07 |
| Alcance | Diseño lógico previo a Flyway del MS nuevo |
| BD objetivo | PostgreSQL `ms_malla_turnos` |
| Tenant | `company_id` (UUID) en toda tabla de negocio |

---

## 1. Decisión de almacenamiento

| Pieza | Dónde | Notas |
| ----- | ----- | ----- |
| Dominio Malla (catálogos, grilla, reglas, intercambio, staging TH) | **Nueva BD** `ms_malla_turnos` | MS hexagonal nuevo |
| Módulo / submódulos / plan | `ms_company_admin` | Solo seed/config (HU01) |
| Roles / `permission_submodules` | `ms_auth` | Solo seed/config (HU02) |
| Empleados | `ms_employee` | Lectura por API; UUID lógico |
| Áreas, cargos, festivos | `ms_parametrization` | Lectura por API; UUID lógico |
| Notificaciones | `ms_notification` | Event types nuevos |

**No** usar `work_schedule` / `schedule_assignment` (jornada contractual).  
**No** FK cross-database: solo UUID lógicos + validación en use case.

---

## 2. Convenciones de tipos

| Tipo | Uso | Por qué |
| ---- | --- | ------- |
| `UUID` | PK y FKs lógicas | Estándar GRH |
| `UUID company_id` | Todas las tablas de negocio | Tenant; UNIQUE siempre compuesto |
| `VARCHAR(n)` | Códigos, nombres, status | Indexable; status string evita enums PG rígidos |
| `TEXT` | Notas / motivos | Longitud variable |
| `DATE` | Días / periodos de malla | Día calendario sin TZ |
| `TIME` | Horas de plantilla | Independiente de fecha; medianoche = flag |
| `TIMESTAMPTZ` | Auditoría / publicación | Instantes con zona |
| `BOOLEAN` | Flags | Capacidades, activo, asignable |
| `SMALLINT` / `INT` | Orden, slot, minutos, dow | Enteros pequeños |
| `NUMERIC` | Umbrales de reglas | Precisión decimal si hace falta |
| `JSONB` | Historial, warnings, config | Evoluciona sin migración por atributo |

---

## 3. Inventario de tablas

### 3.1 Catálogo

#### `operational_front`

| Columna | Tipo | Motivo |
| ------- | ---- | ------ |
| `id` | UUID PK | Identidad estable |
| `company_id` | UUID NOT NULL | Tenant |
| `code` | VARCHAR(20) | UNIQUE(`company_id`, `code`) |
| `name` | VARCHAR(120) | Visible |
| `description` | TEXT NULL | Ayuda |
| `build_mode` | VARCHAR(20) | `manual` \| `asistido` \| `automatico` |
| `period_type` | VARCHAR(10) | `semana` \| `mes` |
| `published_editable` | BOOLEAN | Edición post-publicación |
| `swap_enabled` | BOOLEAN DEFAULT false | EP-09 OFF por defecto |
| `active` | BOOLEAN | Inactivo no entra a nuevas mallas |
| `created_at` / `updated_at` | TIMESTAMPTZ | Auditoría |

#### `front_capability`

| Columna | Tipo | Motivo |
| ------- | ---- | ------ |
| `id` | UUID PK | |
| `company_id` | UUID | Tenant |
| `front_id` | UUID FK → `operational_front` | |
| `capability_code` | VARCHAR(40) | `usa_territorio`, `usa_campanas`, … |
| `enabled` | BOOLEAN | |
| `config_json` | JSONB NULL | Parámetros flexibles del flag |

#### `front_area_link`

| Columna | Tipo | Motivo |
| ------- | ---- | ------ |
| `id` | UUID PK | |
| `company_id` | UUID | |
| `front_id` | UUID FK | |
| `area_id` | UUID | ID lógico en `ms_parametrization` |

#### Alcance usuarios/roles (HU03)

- `front_user_scope` (`user_id`, `front_id`, `company_id`)
- `front_role_scope` (`role_id`, `front_id`, `company_id`)

#### Turnos

- `shift_template` — plantilla (`code`, `name`, `start_time`/`end_time` TIME, `crosses_midnight`, `color_hex`, `active`)
- `shift_template_front` — N:M plantilla ↔ frentes
- `shift_template_day_schedule` — `dow` SMALLINT 0–6 + horario
- `shift_template_break` — `duration_minutes` INT, `paid` BOOLEAN

#### `cell_state`

Flags: `assignable`, `counts_hours`, `deducts_productive`, `requires_support`, `active` + `code`/`name`/`color_hex`.

#### Catálogos opcionales (según capacidad del frente)

- `work_modality`
- `attendance_site` (+ aplicabilidad por frente)
- `campaign`
- `territory_level`, `territory_node` (`parent_id` NULL = raíz)

Patrón: `id`, `company_id`, `code`, `name`, `active`.

---

### 3.2 Motor de reglas y patrones

#### `validation_rule`

| Columna | Tipo | Motivo |
| ------- | ---- | ------ |
| `code` | VARCHAR(40) | `NO_SOLAPE`, `MAX_HORAS`, … |
| `scope` | VARCHAR(20) | `empresa` \| `frente` |
| `front_id` | UUID NULL | Si scope = frente |
| `param_value` | VARCHAR(40) | Editable (ej. `46`) |
| `param_unit` | VARCHAR(40) | `horas`, `dias`, … |
| `severity` | VARCHAR(20) | `info` \| `advertencia` \| `bloqueo` |
| `priority` | INT | Orden |
| `active` | BOOLEAN | |

También: `coverage_rule`, `compensatory_rule`, `hour_type`, `payroll_cutoff`, `person_restriction`, `rotation_pattern` + `rotation_pattern_step`.

---

### 3.3 Operación

#### `schedule_grid`

Cabecera: `front_id`, `period_start`/`period_end` DATE, `status`, `build_mode`, `owner_user_id`, `rejection_reason`, `published_at`, `version` (optimistic lock).

#### `schedule_grid_person`

PK lógica (`grid_id`, `employee_id`); `sort_order`; `employee_id` = UUID lógico `ms_employee`.

#### `schedule_cell` (núcleo)

| Columna | Tipo | Motivo |
| ------- | ---- | ------ |
| `work_date` | DATE | Día calendario |
| `slot` | SMALLINT DEFAULT 0 | 0 = principal; 1+ = extra mismo día |
| `shift_template_id` | UUID NULL | Turno |
| `cell_state_id` | UUID NULL | Estado (XOR lógico con turno) |
| `modality_id` / `site_id` / `campaign_id` / `territory_node_id` | UUID NULL | Según flags del frente |
| `note` | TEXT NULL | |
| `locked_attrs` | JSONB NULL | Atributos fijados (HU42) |
| `updated_at` / `updated_by` | TIMESTAMPTZ / UUID | Concurrencia |

**UNIQUE**(`grid_id`, `employee_id`, `work_date`, `slot`).

#### `schedule_cell_history`

Append-only: `before_json` / `after_json` JSONB, `origin`, `reason`, `changed_by`, `changed_at`. Sin `ON DELETE CASCADE` destructivo.

---

### 3.4 Intercambio y staging TH

- `shift_swap_request` — requester/counterpart, celdas, `status`, `rule_warnings` JSONB
- `th_import_batch` / `th_import_row` — staging cruce novedades TH

---

## 4. Índices mínimos

| Constraint / índice | Motivo |
| ------------------- | ------ |
| `UNIQUE(company_id, code)` en catálogos | Código por empresa |
| `UNIQUE(grid_id, employee_id, work_date, slot)` | Celda lógica |
| `INDEX(company_id, front_id, period_start)` | Listar mallas |
| `INDEX(company_id, employee_id, work_date)` | Quién está / mi programación |
| `INDEX(cell_id, changed_at)` en history | Timeline |
| Nunca `UNIQUE(code)` sin `company_id` | Multiempresa |

---

## 5. Orden sugerido de Flyway

1. Catálogos EP-01 (`operational_front` → capacidades → turnos/estados → atributos).
2. Reglas (`validation_rule` + coverage/hour/compensatory).
3. Operación (`schedule_grid` → person → cell → history).
4. Intercambio + staging TH (pueden ir en sprint posterior; EP-09 OFF).

Semillas de menú/RBAC **no** van en esta BD: van en `ms_company_admin` / `ms_auth`.

---

## 6. Nota sobre anexos técnicos viejos

Si algún anexo aún dice `operational_front` como enum `CC|SITE|DESK|LAB`, está **obsoleto**. El modelo vigente es catálogo UUID por `company_id`.
