# Anexo técnico — MT-EP00-HU01 (solo desarrollo)

**No incluir en presentaciones a cliente ni en Word GST-FM-04 para diseño.**

La HU de negocio está en `GST-FM-04-MT-EP00-HU01-Registrar-modulo-submodulos-plataforma.md`.

## Perfiles GRH (anexo)

| Perfil negocio | Auth | company_id |
| -------------- | ---- | ------------ |
| Super-administrador | SUPER_ADMIN | null |
| Administrador de empresa | ADMIN | UUID empresa |
| Usuario colaborador | EMPLOYEE / roles custom | UUID empresa |

| Paso | Dónde | Qué |
| ---- | ----- | --- |
| 1 | `company-admin` — `modulos` | INSERT módulo Malla de turnos |
| 2 | `company-admin` — `submodules` | 5 filas con `route` alineada a Angular |
| 3 | `company-admin` — `plan_modulos` | Asociar módulo al plan piloto |
| 4 | `gestion-empresarial-frontend-web` | Lazy `malla-turnos` + `RbacConstant.SCOPES` |
| 5 | `auth` — `permission_submodules` | **MT-EP00-HU02**, no esta HU |

## Rutas propuestas (validar con arquitectura)

- `malla-turnos/main/parametrizacion`
- `malla-turnos/main/construccion`
- `malla-turnos/main/consulta-operativa`
- `malla-turnos/main/mi-programacion`
- `malla-turnos/main/reportes`

## Referencias código

- `candidate_migration_modulos_submodulos.sql`
- `docs/GST-AN-Parametrizacion-Categorias-Documentales-Super-Admin.md`
- `rbac.constant.ts`, `app-routing.module.ts`

## Pendientes técnicos

- IDs en BD DEV/QA
- `plan_id` piloto
- MS nuevo vs extensión
