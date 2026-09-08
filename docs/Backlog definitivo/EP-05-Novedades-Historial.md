# EP-05 — Novedades, historial y notificaciones

## Índice

- MT-EP05-HU60 — Aplicar estado de novedad operativa a la celda
- MT-EP05-HU61 — Definir ownership MVP de novedades
- MT-EP05-HU62 — Historial inmutable de celda
- MT-EP05-HU63 — Notificar cambio relevante al empleado
- MT-EP05-HU64 — Consultar historial de cambios por funcionario

---
## MT-EP05-HU60 — Aplicar estado de novedad operativa a la celda

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** cambiar el estado de una celda a un estado de novedad del catálogo (vacaciones, incapacidad u otros ítems)

**Para:** reflejar la disponibilidad real sin inventar un módulo TH inexistente

### Alcance

**Cubre**

- Cambio de estado a ítems del catálogo HU14
- Motivo/soporte según flags
- Recálculo cobertura/horas

**No cubre**

- Módulo completo de vacaciones GRH
- HUs por cada tipo de novedad

### Reglas de negocio

1. Ownership MVP: la novedad operativa vive como estado de celda (HU61).
2. No existen estados especiales en código; solo flags.
3. ex-HU50 absorbida: si el estado no cuenta horas, HU70 no las suma.

### Criterios de aceptación

**CA01 — Aplicar**

Dado que estado novedad del catálogo

Cuando asigna a celda

Entonces flags determinan cobertura/horas/notificación

**CA02 — Motivo**

Dado que requiere motivo

Cuando sin motivo

Entonces bloquea/advierte

**CA03 — Publicada**

Dado que políticas HU59

Cuando aplica

Entonces historial + posible notificación

**CA04 — Sin hardcode**

Dado que cualquier código de estado

Cuando mismo flujo

Entonces OK

**CA05 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU14, MT-EP05-HU61, MT-EP04-HU59, MT-EP05-HU62
- Microservicios / GRH: Malla

---

## MT-EP05-HU61 — Definir ownership MVP de novedades

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización

**Quiero:** operar novedades como estado de celda con importación opcional, dejando explícito que no hay módulo TH en GRH hoy

**Para:** evitar dobles fuentes de verdad no gobernadas

### Alcance

**Cubre**

- Política MVP documentada e implementada
- Importación opcional (HU74/HU75)
- Extensibilidad a conector futuro

**No cubre**

- Afirmar que GRH ya tiene vacaciones/incapacidades

### Reglas de negocio

1. Fuente operativa MVP = estado de celda.
2. Archivo TH es complemento de cruce, no reemplaza el catálogo de estados.
3. Futuro conector TH no debe romper historial de celda.

### Criterios de aceptación

**CA01 — MVP**

Dado que se aplica novedad

Cuando persiste

Entonces como estado de celda

**CA02 — Import**

Dado que existe archivo

Cuando importa

Entonces propone/aplica estados según mapeo

**CA03 — Sin módulo TH**

Dado que documentación/producto

Cuando consulta capacidades GRH

Entonces no asume módulo TH

**CA04 — Tenant**

Dado que import

Cuando empresa del usuario

Entonces OK

### Dependencias

- HUs: MT-EP01-HU14, MT-EP08-HU74
- Microservicios / GRH: Malla

### Consideraciones técnicas

Decisión D1 cerrada por defecto: estado + import.

---

## MT-EP05-HU62 — Historial inmutable de celda

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** registrar de forma append-only cada cambio de celda con antes, después, usuario, fecha, motivo y origen

**Para:** auditar la operación sin versionar toda la malla

### Alcance

**Cubre**

- Historial por celda
- Orígenes: manual, automático, asistido, novedad, intercambio, import

**No cubre**

- Borrado de historial
- Duplicar timeline GRH con el mismo detalle

### Reglas de negocio

1. El historial de dominio es la fuente del detalle de celda.
2. Timeline GRH guarda hechos de alto nivel (HU07).
3. Inmutable: no update/delete de eventos de historial.

### Criterios de aceptación

**CA01 — Registro**

Dado que cambia celda

Cuando guarda OK

Entonces existe evento con antes/después/usuario/origen

**CA02 — Inmutable**

Dado que intenta borrar historial

Cuando acción

Entonces no existe o se niega

**CA03 — Origen intercambio**

Dado que cambio por HU81

Cuando historial

Entonces referencia solicitud

**CA04 — Consulta**

Dado que usuario autorizado

Cuando abre historial celda

Entonces lista cronológica

**CA05 — Tenant**

Dado que historial ajeno

Cuando invisible

Entonces OK

### Dependencias

- HUs: MT-EP02-HU30, MT-EP00-HU07
- Microservicios / GRH: Malla; audit timeline (alto nivel)

---

## MT-EP05-HU63 — Notificar cambio relevante al empleado

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa vinculado a un funcionario

**Quiero:** recibir notificación informativa cuando cambia su programación publicada según flags y event types

**Para:** enterarse del cambio sin tener que aceptar en la plataforma

### Alcance

**Cubre**

- Despacho notification-service
- Popup/email según event type
- Sin aceptación

**No cubre**

- Workflow de aceptación del empleado
- Mailer propio

### Reglas de negocio

1. Si el estado/config indica notifica=sí y la malla está en alcance de notificación, se despacha.
2. Idempotencia por clave de evento.

### Criterios de aceptación

**CA01 — Cambio**

Dado que celda publicada cambia y notifica=sí

Cuando guarda

Entonces empleado recibe notificación

**CA02 — Sin aceptación**

Dado que recibe aviso

Cuando abre app

Entonces no se le pide aceptar el turno

**CA03 — No notifica**

Dado que flag notifica=no

Cuando cambia

Entonces no despacha a empleado

**CA04 — Falla canal**

Dado que email falla

Cuando reintento idempotente

Entonces no duplica popup si ya entregado según diseño del MS

**CA05 — Tenant**

Dado que destinatario

Cuando misma empresa

Entonces OK

### Dependencias

- HUs: MT-EP00-HU07, MT-EP01-HU14, MT-EP04-HU59
- Microservicios / GRH: notification-service

---

## MT-EP05-HU64 — Consultar historial de cambios por funcionario

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla

**Quiero:** ver el historial de cambios de celdas de un funcionario en un rango de fechas

**Para:** investigar novedades y ajustes

### Alcance

**Cubre**

- Consulta por persona + rango
- Detalle de eventos HU62

**No cubre**

- —

### Reglas de negocio

1. Respeta alcance de frente y permisos LEER.

### Criterios de aceptación

**CA01 — Consulta**

Dado que persona de la empresa

Cuando filtra fechas

Entonces lista cambios

**CA02 — Vacío**

Dado que sin cambios

Cuando consulta

Entonces estado vacío claro

**CA03 — Permisos**

Dado que sin LEER

Cuando niega

Entonces OK

**CA04 — Tenant**

Dado que persona otra empresa

Cuando niega

Entonces OK

### Dependencias

- HUs: MT-EP05-HU62
- Microservicios / GRH: Malla

---
