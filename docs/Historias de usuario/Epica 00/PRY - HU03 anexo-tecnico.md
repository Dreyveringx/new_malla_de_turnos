# Anexo técnico — MT-EP00-HU03

Audiencia: desarrollo / arquitectura. No presentar al cliente.

## Implementación

- Tabla/dominio Malla: user_id o role_id × front_id × company_id.
- No crear permission_submodules nuevos por frente.
- Enforcement en use cases de malla/catálogos: filtrar por alcance + companyId JWT.

## Dependencias

- auth: identidad usuario/roles
- Malla: frentes (HU09)


---
*Generado 05/09/2026 con backlog definitivo v2.0.*
