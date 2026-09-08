# EP-04 — Publicación

## Índice

- MT-EP04-HU57 — Ciclo de vida de publicación de la malla
- MT-EP04-HU58 — Rechazar malla en revisión
- MT-EP04-HU59 — Editar malla publicada

---
## MT-EP04-HU57 — Ciclo de vida de publicación de la malla

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de publicación según configuración del frente

**Quiero:** mover la malla entre borrador, en revisión, publicada y rechazada según la configuración del frente

**Para:** controlar cuándo la programación es oficial

### Alcance

**Cubre**

- Transiciones de estado
- Validación previa
- Publicar con advertencias si el flag lo permite
- Notificación de publicación

**No cubre**

- Versionado completo de malla (no requerido)
- Aceptación del empleado

### Reglas de negocio

1. Estados: Borrador, En revisión (si aplica), Publicada, Rechazada.
2. Si constructor/publicador está separado (HU10), el constructor solo envía a revisión.
3. No se publica con bloqueos; advertencias requieren confirmación solo si el frente lo permite.
4. ex-HU46 absorbida aquí + HU10.

### Criterios de aceptación

**CA01 — Publicar**

Dado que borrador sin bloqueos y usuario publicador

Cuando publica

Entonces estado=Publicada y se notifica según HU07

**CA02 — Revisión**

Dado que separación activa

Cuando constructor envía

Entonces pasa a En revisión

**CA03 — Advertencias**

Dado que flag permite y hay advertencias

Cuando confirma

Entonces publica registrando aceptación de advertencias

**CA04 — Bloqueos**

Dado que hay bloqueos

Cuando publica

Entonces rechaza

**CA05 — Permisos**

Dado que no publicador

Cuando publica

Entonces niega

**CA06 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU10, MT-EP03-HU45, MT-EP00-HU07, MT-EP05-HU63
- Microservicios / GRH: Malla; notification

---

## MT-EP04-HU58 — Rechazar malla en revisión

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de publicación según configuración del frente

**Quiero:** rechazar una malla en revisión con motivo y devolverla a borrador

**Para:** permitir correcciones antes de publicar

### Alcance

**Cubre**

- Rechazo con motivo
- Vuelta a borrador
- Notificación al constructor si aplica

**No cubre**

- —

### Reglas de negocio

1. Solo desde En revisión.
2. Motivo obligatorio.

### Criterios de aceptación

**CA01 — Rechazo**

Dado que malla en revisión

Cuando rechaza con motivo

Entonces queda borrador y motivo visible

**CA02 — Sin motivo**

Dado que rechaza vacío

Cuando valida

Entonces bloquea

**CA03 — Estado inválido**

Dado que ya publicada

Cuando rechaza

Entonces niega

**CA04 — Permisos**

Dado que no autorizado

Cuando niega

Entonces OK

### Dependencias

- HUs: MT-EP04-HU57
- Microservicios / GRH: Malla; notification

---

## MT-EP04-HU59 — Editar malla publicada

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** modificar celdas de una malla publicada cuando la configuración lo permite, con motivo e historial

**Para:** atender cambios reales sin perder trazabilidad

### Alcance

**Cubre**

- Edición post-publicación gobernada
- Motivo según config
- Historial + notificación

**No cubre**

- Crear nueva versión completa de malla

### Reglas de negocio

1. Si editabilidad post-publicación = no, solo novedades vía flujo permitido o nada.
2. Cada cambio deja historial inmutable.
3. Estado puede marcarse como modificada después de publicar a nivel de celda/malla según diseño.

### Criterios de aceptación

**CA01 — Edición permitida**

Dado que flag on

Cuando cambia celda con motivo

Entonces persiste, historial y notifica si corresponde

**CA02 — Flag off**

Dado que no editable

Cuando intenta

Entonces niega

**CA03 — Motivo**

Dado que config exige motivo

Cuando guarda sin motivo

Entonces bloquea

**CA04 — Concurrencia**

Dado que versión vieja

Cuando guarda

Entonces conflicto HU39

**CA05 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU10, MT-EP05-HU62, MT-EP05-HU63, MT-EP02-HU39
- Microservicios / GRH: Malla; notification

---
