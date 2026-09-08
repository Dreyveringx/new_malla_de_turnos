# Anexo técnico — MT-EP00-HU04 (solo desarrollo)

No incluir en presentaciones a cliente ni en Word GST-FM-04 para diseño.

La HU de negocio está en `GST-FM-04-MT-EP00-HU04-Aislar-informacion-por-empresa.md`.

## Dependencias

| HU | Qué aporta |
| -- | ---------- |
| MT-EP00-HU01 | Módulo habilitado por empresa |
| MT-EP00-HU02 | Permisos por sección y frente (complementa, no reemplaza tenant) |

## Regla técnica

- Tenant = `companyId` (UUID) en JWT y en toda persistencia del dominio Malla.
- Toda tabla/entidad del MS de malla lleva `company_id` NOT NULL.
- Todo query/repository filtra por `company_id` del contexto de seguridad.
- Prohibido `unique` global en identidad operativa sin incluir `company_id`.

## Capas

| Capa | Responsabilidad |
| ---- | ---------------- |
| API Gateway / JWT | Propagar `companyId` |
| Controller | No aceptar `companyId` del body como fuente de verdad |
| Use case | Validar que el recurso pertenece al tenant de sesión |
| Repository | `WHERE company_id = :companyId` en todas las lecturas y escrituras |
| Reportes / export | Mismo filtro antes de generar archivo |

## Pruebas sugeridas

1. Usuario empresa A crea registro; usuario empresa B no lo lista ni lo obtiene por ID.
2. Seed con dos `company_id` distintos; asserts cruzados negativos.
3. Export Excel: cero filas de tenant ajeno.
4. Intento S2S o API con `companyId` manipulado: rechazado.

## Referencias

- Skill `tenant-identity` / `reference.md` (grh-hu-documentation)
- `LEVANTAMIENTO-MALLA-TURNOS-FASE1.md` — RNF-01 Multi-tenant

## Pendientes técnicos

- MS nuevo vs extensión: mismo criterio `company_id` en ambos casos
- Auditoría: eventos con `company_id` para trazabilidad
