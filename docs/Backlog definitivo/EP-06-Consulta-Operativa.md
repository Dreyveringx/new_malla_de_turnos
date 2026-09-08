# EP-06 — Consulta operativa

## Índice

- MT-EP06-HU65 — Buscar quién está en turno o disponible
- MT-EP06-HU66 — Consultar cobertura del día por dimensiones habilitadas

---
## MT-EP06-HU65 — Buscar quién está en turno o disponible

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de consulta operativa

**Quiero:** consultar qué personas están en turno o disponibles en una fecha/franja según filtros del frente

**Para:** atender operación en tiempo real

### Alcance

**Cubre**

- Búsqueda por fecha/franja/filtros habilitados
- Excluye estados no disponibles según flags

**No cubre**

- Hardcodear estado Actividad
- Edición de malla

### Reglas de negocio

1. ex-HU54 absorbida: la no asignabilidad a casos es un flag del estado.
2. Solo muestra frentes de su alcance.

### Criterios de aceptación

**CA01 — Búsqueda**

Dado que hay personas en turno en la franja

Cuando consulta

Entonces lista resultados

**CA02 — Flag**

Dado que estado no disponible/no asignable

Cuando consulta disponibilidad operativa

Entonces no las incluye

**CA03 — Filtros**

Dado que capacidades off

Cuando UI

Entonces no muestra filtros fantasma

**CA04 — Tenant/alcance**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU14, MT-EP00-HU03
- Microservicios / GRH: Malla

---

## MT-EP06-HU66 — Consultar cobertura del día por dimensiones habilitadas

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de consulta operativa

**Quiero:** ver cobertura del día agrupada por las dimensiones activas del frente

**Para:** verificar dotación operativa

### Alcance

**Cubre**

- Vista de cobertura del día
- Comparación vs min/max

**No cubre**

- —

### Reglas de negocio

1. Dimensiones dinámicas según HU10/HU24.

### Criterios de aceptación

**CA01 — Vista**

Dado que día con reglas

Cuando abre cobertura

Entonces muestra actual vs min/max

**CA02 — Dimensión**

Dado que territorio off

Cuando vista

Entonces sin agrupación territorio

**CA03 — Permisos**

Dado que LEER consulta

Cuando OK

Entonces OK

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU24, MT-EP03-HU43
- Microservicios / GRH: Malla

---
