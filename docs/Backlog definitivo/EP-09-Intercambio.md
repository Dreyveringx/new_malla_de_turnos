# EP-09 — Intercambio de turnos

## Índice

- MT-EP09-HU77 — Habilitar y configurar solicitudes de intercambio
- MT-EP09-HU78 — Solicitar intercambio de celda o turno
- MT-EP09-HU79 — Validar solicitud con motor de reglas
- MT-EP09-HU80 — Aprobar o rechazar solicitud de intercambio
- MT-EP09-HU81 — Aplicar intercambio, auditar y notificar

---
## MT-EP09-HU77 — Habilitar y configurar solicitudes de intercambio

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización

**Quiero:** activar o desactivar solicitudes de intercambio por empresa/frente y definir anticipación, quién solicita, quién aprueba, límites y notificaciones

**Para:** gobernar el intercambio sin imponerlo a todos los frentes

### Alcance

**Cubre**

- Config on/off
- Anticipación mínima
- Roles/permisos lógicos de solicitud y aprobación
- Límites de cantidad
- Motivos

**No cubre**

- Flujo de solicitud en sí (HU78+)

### Reglas de negocio

1. Default: deshabilitado.
2. Toda regla numérica es parámetro.
3. No cruza empresas.

### Criterios de aceptación

**CA01 — Off**

Dado que deshabilitado

Cuando empleado ve su malla

Entonces sin acción de intercambio

**CA02 — On**

Dado que habilitado

Cuando aparece acción

Entonces según quién puede solicitar

**CA03 — Anticipación**

Dado que parámetro N días

Cuando solicitud fuera de N

Entonces rechazada por regla

**CA04 — Auditoría config**

Dado que cambia config

Cuando historial config

Entonces OK

**CA05 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU10, MT-EP00-HU02
- Microservicios / GRH: Malla

---

## MT-EP09-HU78 — Solicitar intercambio de celda o turno

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa vinculado a un funcionario

**Quiero:** iniciar una solicitud de intercambio eligiendo mi celda y un compañero candidato con su celda

**Para:** resolver cambios de turno dentro de la plataforma

### Alcance

**Cubre**

- Creación de solicitud pendiente
- Selección de contraparte misma empresa/frente según config

**No cubre**

- Autoaprobar

### Reglas de negocio

1. Solo si HU77 enabled.
2. Ambos empleados misma empresa; frente según config.
3. No modifica malla hasta aprobación+aplicación.

### Criterios de aceptación

**CA01 — Solicitud**

Dado que intercambio on y celdas elegibles

Cuando envía

Entonces queda pendiente

**CA02 — Misma empresa**

Dado que candidato otra empresa

Cuando selección

Entonces imposible

**CA03 — Off**

Dado que config off

Cuando acción

Entonces ausente

**CA04 — Límite**

Dado que supera cantidad configurada

Cuando envía

Entonces rechaza

**CA05 — Permisos**

Dado que no habilitado a solicitar

Cuando niega

Entonces OK

### Dependencias

- HUs: MT-EP09-HU77, MT-EP07-HU68
- Microservicios / GRH: Malla

---

## MT-EP09-HU79 — Validar solicitud con motor de reglas

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa vinculado a un funcionario

**Quiero:** que el sistema valide anticipación, solape, cobertura, horas, restricciones y demás reglas al crear o aprobar

**Para:** evitar intercambios que rompan la operación

### Alcance

**Cubre**

- Validación en creación y en aprobación

**No cubre**

- —

### Reglas de negocio

1. Solape real = bloqueo.
2. Resto según HU25 + config HU77.

### Criterios de aceptación

**CA01 — Creación inválida**

Dado que viola bloqueo

Cuando crea

Entonces rechaza con motivos

**CA02 — Advertencia**

Dado que severidad advertencia

Cuando crea

Entonces queda pendiente con warnings visibles al aprobador

**CA03 — Revalidar**

Dado que entre creación y aprobación cambió malla

Cuando aprueba

Entonces revalida y puede fallar

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU25, MT-EP09-HU78
- Microservicios / GRH: Malla

---

## MT-EP09-HU80 — Aprobar o rechazar solicitud de intercambio

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** aprobar o rechazar solicitudes pendientes según la configuración de aprobadores

**Para:** gobernar el cambio con responsabilidad clara

### Alcance

**Cubre**

- Bandeja de solicitudes
- Aprobar/rechazar con motivo
- N niveles si config lo define (mínimo 1)

**No cubre**

- Aplicar sin pasar por este paso

### Reglas de negocio

1. Quién aprueba lo define HU77 + permisos, no un rol quemado.
2. Rechazo no cambia malla.

### Criterios de aceptación

**CA01 — Aprobar**

Dado que solicitud válida y usuario aprobador

Cuando aprueba

Entonces pasa a aprobada pendiente de aplicación o aplica según diseño

**CA02 — Rechazar**

Dado que con motivo

Cuando rechaza

Entonces malla intacta + notificación

**CA03 — No aprobador**

Dado que usuario sin permiso

Cuando intenta

Entonces niega

**CA04 — Revalidación**

Dado que ya no es válida

Cuando aprueba

Entonces falla con motivos

**CA05 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP09-HU77, MT-EP09-HU79, MT-EP00-HU07
- Microservicios / GRH: Malla; notification

---

## MT-EP09-HU81 — Aplicar intercambio, auditar y notificar

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** aplicar el intercambio aprobado sobre las celdas, registrar historial con origen intercambio y notificar a afectados

**Para:** cerrar el ciclo de forma trazable

### Alcance

**Cubre**

- Swap atómico de atributos configurados
- Historial
- Notificaciones
- Idempotencia

**No cubre**

- —

### Reglas de negocio

1. Aplicación atómica: ambas celdas o ninguna.
2. Historial referencia id de solicitud.
3. Origen=intercambio.

### Criterios de aceptación

**CA01 — Aplicar**

Dado que aprobada y válida

Cuando aplica

Entonces celdas intercambiadas

**CA02 — Historial**

Dado que consulta

Cuando ambas celdas

Entonces eventos con solicitud

**CA03 — Notificar**

Dado que ambos empleados

Cuando reciben aviso

Entonces sin aceptación adicional

**CA04 — Falla parcial**

Dado que segunda celda conflicto versión

Cuando rollback

Entonces nada aplicado + error

**CA05 — Idempotencia**

Dado que reintenta misma solicitud aplicada

Cuando no duplica swap

Entonces OK

### Dependencias

- HUs: MT-EP09-HU80, MT-EP05-HU62, MT-EP00-HU07, MT-EP02-HU39
- Microservicios / GRH: Malla; notification

---
