# EP-07 — Vista del empleado

## Índice

- MT-EP07-HU67 — Ver programación del grupo
- MT-EP07-HU68 — Ver mi programación
- MT-EP07-HU69 — Ver historial de mis turnos y cambios recientes

---
## MT-EP07-HU67 — Ver programación del grupo

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa vinculado a un funcionario

**Quiero:** consultar la programación publicada del grupo según la política de visibilidad del frente

**Para:** conocer turnos del equipo

### Alcance

**Cubre**

- Vista de grupo
- Solo lectura

**No cubre**

- Editar malla ajena

### Reglas de negocio

1. Default: visible dentro del grupo del frente (D3).
2. Si config restringe a solo-propia, no ve compañeros.

### Criterios de aceptación

**CA01 — Grupo visible**

Dado que política pública en grupo

Cuando abre

Entonces ve compañeros del grupo

**CA02 — Restringida**

Dado que política solo propia

Cuando abre

Entonces solo su fila

**CA03 — Borrador**

Dado que malla no publicada

Cuando consulta empleado

Entonces no ve borradores ajenos

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP04-HU57, MT-EP01-HU10
- Microservicios / GRH: Malla

---

## MT-EP07-HU68 — Ver mi programación

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa vinculado a un funcionario

**Quiero:** ver mi programación en vistas de día, semana y mes

**Para:** organizar mi trabajo

### Alcance

**Cubre**

- Vistas temporales
- Turnos/estados/atributos visibles permitidos
- Solo lectura salvo intercambio si está on

**No cubre**

- —

### Reglas de negocio

1. No edita celdas salvo iniciar solicitud EP-09 si está habilitado.

### Criterios de aceptación

**CA01 — Día/semana/mes**

Dado que tiene celdas publicadas

Cuando cambia vista

Entonces ve su información

**CA02 — Atributos**

Dado que frente sin campaña

Cuando vista

Entonces no muestra campaña

**CA03 — Borrador**

Dado que solo borrador

Cuando consulta

Entonces no lo ve como oficial

**CA04 — Permisos**

Dado que usuario sin vínculo empleado

Cuando abre

Entonces mensaje claro

### Dependencias

- HUs: MT-EP04-HU57
- Microservicios / GRH: Malla; employee vínculo userId

---

## MT-EP07-HU69 — Ver historial de mis turnos y cambios recientes

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa vinculado a un funcionario

**Quiero:** consultar el historial de mis turnos y cambios recientes que me afectaron

**Para:** entender modificaciones de mi programación

### Alcance

**Cubre**

- Historial propio
- Cambios recientes

**No cubre**

- Historial de otros empleados

### Reglas de negocio

1. Solo sus eventos; inmutable.

### Criterios de aceptación

**CA01 — Historial**

Dado que hubo cambios

Cuando abre

Entonces lista antes/después relevantes

**CA02 — Recientes**

Dado que filtro recientes

Cuando aplica

Entonces acota ventana

**CA03 — Privacidad**

Dado que otro empleado

Cuando intenta

Entonces niega

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP05-HU62
- Microservicios / GRH: Malla

---
