# Anexo técnico — MT-EP00-HU08

Audiencia: desarrollo / arquitectura. No presentar al cliente.

## Gap conocido

- Employee list puede no filtrar por areaId hoy.
- Opciones: extender EmployeeFilterRequest o filtrar/paginar en BFF/use case Malla.

## Regla

- companyId siempre desde JWT; nunca del body como fuente de verdad.


---
*Generado 05/09/2026 con backlog definitivo v2.0.*
