# Anexo técnico — MT-EP00-HU02 (solo desarrollo)

**No incluir en presentaciones a cliente ni en Word GST-FM-04 para diseño.**

La HU de negocio está en `GST-FM-04-MT-EP00-HU02-Configurar-permisos-rol-area-frente.md`.

## Dependencias

| HU | Qué aporta |
| -- | ---------- |
| MT-EP00-HU01 | Módulo y 5 submódulos en `company-admin`; rutas Angular; plan activo |
| MT-EP00-HU04 | Filtro `company_id` en datos de malla (complementa alcance de rol) |
| MT-EP00-HU05 | Vinculación frente ↔ `area_id` de parametrization |

## Perfiles GRH (anexo)

| Perfil negocio | Auth | Configura permisos Malla |
| -------------- | ---- | ------------------------ |
| Super-administrador | SUPER_ADMIN | No (catálogo en HU01) |
| Administrador de empresa | ADMIN | Sí — UI Seguridad |
| Usuario colaborador | EMPLOYEE + roles custom | Recibe `permission_submodules` |

## Implementación auth (referencia)

| Paso | Dónde | Qué |
| ---- | ----- | --- |
| 1 | `auth` — `roles` | INSERT roles por `company_id` (ej. COORDINADOR_CC) |
| 2 | `auth` — `permission_submodules` | `(role_id, permission_id, sub_module_id)` por cada celda de la matriz |
| 3 | `auth` — `user_roles` | Asignar usuarios a roles |
| 4 | JWT | Claims `scopedAuthorities`: `SM_{subModuleId}_{CREAR\|LEER\|ACTUALIZAR\|ELIMINAR}` |
| 5 | FE | `RbacConstant.SCOPES` + `data.routeAuthz` en rutas `malla-turnos/main/*` |
| 6 | FE | Deshabilitar acciones según scope; tooltip "Sin permiso" |

### Permisos base (`BasePermissions`)

| Negocio (GST-FM-04) | Código auth |
| ------------------- | ----------- |
| Consultar | LEER |
| Crear | CREAR |
| Modificar | ACTUALIZAR |
| Eliminar | ELIMINAR |

### Submódulos Malla (IDs post HU01 — verificar en BD)

| Sección | `route` propuesta |
| ------- | ----------------- |
| Parametrización | `malla-turnos/main/parametrizacion` |
| Construcción | `malla-turnos/main/construccion` |
| Consulta operativa | `malla-turnos/main/consulta-operativa` |
| Mi programación | `malla-turnos/main/mi-programacion` |
| Reportes | `malla-turnos/main/reportes` |

## Alcance por frente operativo

**Requisito negocio:** además del RBAC por submódulo, filtrar datos por frente (CC, Sitio, Mesa, Lab).

Opciones de diseño (elegir en arquitectura):

| Opción | Descripción |
| ------ | ----------- |
| A | Tabla `role_operational_front` (`role_id`, `front_code`, `company_id`) |
| B | Claim o atributo en JWT `allowedFronts[]` derivado del rol |
| C | Relación rol ↔ `area_id` (parametrization) cuando HU05 vincule frente–área |

El menú lateral sigue gobernado por `permission_submodules`; el filtro de frente aplica en APIs y consultas del MS de malla.

## UI empresa

- **Roles:** `form-roles` / Seguridad en parametrización (patrón existente GP, GHV).
- **No** usar mock super-admin `assing-permission-role` para empresas cliente.
- Matriz permisos: reutilizar componente de checkboxes CRUD por submódulo.

## Seed sugerido (DEV/QA)

Tras HU01, script o migración de datos que cree roles piloto y `permission_submodules` alineados a la tabla de plantillas del GST-FM-04. IDs de `submodules` deben leerse de BD tras HU01.

## Referencias código

- `business-management-backend-auth` — `PermissionSubModuleController`, `BasePermissions`
- `gestion-empresarial-frontend-web` — `rbac.constant.ts`, módulo seguridad/roles
- `reference.md` (skill grh-hu-documentation) — menú = plan ∩ LEER

## Pendientes técnicos

- Modelo definitivo frente ↔ rol ↔ `area_id`
- Unión de permisos con múltiples roles (ya usado en auth; validar en Malla)
- Refresh de menú sin relogin (hoy suele requerir nuevo login para JWT)
- Tests de integración: usuario rol Analista mesa sin ACTUALIZAR en construcción
