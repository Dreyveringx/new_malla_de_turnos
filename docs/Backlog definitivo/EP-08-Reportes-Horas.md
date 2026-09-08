# EP-08 — Reportes y horas

## Índice

- MT-EP08-HU70 — Calcular horas del periodo por tipos configurados
- MT-EP08-HU71 — Exportar malla a Excel o PDF
- MT-EP08-HU72 — Reportar horas de novedad versus operativas
- MT-EP08-HU73 — Exportar cobertura para terceros
- MT-EP08-HU74 — Parametrizar plantilla de importación de novedades TH
- MT-EP08-HU75 — Cruzar programación con novedades TH importadas
- MT-EP08-HU76 — Aplicar reglas de compensatorio en reporte

---
## MT-EP08-HU70 — Calcular horas del periodo por tipos configurados

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de reportes

**Quiero:** calcular horas del periodo clasificadas por tipos de hora y afectadas por flags de estado

**Para:** entregar información de horas a nómina sin liquidar dinero

### Alcance

**Cubre**

- Cálculo por persona/periodo/corte
- Clasificación HU22
- Respeto flags HU14

**No cubre**

- Cálculo de pesos
- Constante 42h

### Reglas de negocio

1. Los topes de horas son reglas HU25, no constantes.
2. Salida = cantidades de hora por tipo, nunca montos.

### Criterios de aceptación

**CA01 — Cálculo**

Dado que malla con turnos

Cuando ejecuta

Entonces obtiene horas por tipo

**CA02 — Estado no suma**

Dado que flag off

Cuando calcula

Entonces excluye esas celdas del tipo afectado

**CA03 — Festivo**

Dado que día festivo y regla festiva

Cuando clasifica

Entonces según HU22

**CA04 — Sin dinero**

Dado que salida

Cuando inspecciona

Entonces sin campos monetarios

**CA05 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU22, MT-EP01-HU14, MT-EP01-HU21, MT-EP01-HU20
- Microservicios / GRH: Malla

---

## MT-EP08-HU71 — Exportar malla a Excel o PDF

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de reportes

**Quiero:** exportar la malla (ventana o periodo) a Excel y/o PDF según capacidad

**Para:** compartir la programación fuera de la grilla

### Alcance

**Cubre**

- Export Excel/PDF
- Respeta alcance y tenant

**No cubre**

- Export = fuente de verdad editable que reimporta sin control

### Reglas de negocio

1. Export incluye solo atributos habilitados.
2. No incluye datos de otras empresas.

### Criterios de aceptación

**CA01 — Excel**

Dado que malla publicada o autorizada

Cuando exporta

Entonces archivo con filas/columnas coherentes

**CA02 — PDF**

Dado que capacidad PDF on

Cuando exporta

Entonces documento legible

**CA03 — Alcance**

Dado que usuario frente A

Cuando exporta

Entonces solo A

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP02-HU35
- Microservicios / GRH: Malla

---

## MT-EP08-HU72 — Reportar horas de novedad versus operativas

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de reportes

**Quiero:** distinguir horas asociadas a estados de novedad frente a horas operativas según flags

**Para:** analizar no disponibilidad vs operación

### Alcance

**Cubre**

- Desglose por flags de estado

**No cubre**

- —

### Reglas de negocio

1. No asume lista fija de novedades; usa flags del catálogo.

### Criterios de aceptación

**CA01 — Desglose**

Dado que hay estados novedad y operativos

Cuando reporte

Entonces separa totales

**CA02 — Flag**

Dado que estado marca no operativa

Cuando clasifica

Entonces va a novedad

**CA03 — Permisos**

Dado que reportes

Cuando OK

Entonces OK

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP08-HU70, MT-EP01-HU14
- Microservicios / GRH: Malla

---

## MT-EP08-HU73 — Exportar cobertura para terceros

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de reportes

**Quiero:** generar exportación de cobertura consumible por terceros sin obligar altas de usuario GRH

**Para:** compartir dotación con proveedores o clientes internos

### Alcance

**Cubre**

- Export específico de cobertura
- Entrega archivo/link controlado

**No cubre**

- Crear usuarios GRH para cada tercero como único medio

### Reglas de negocio

1. La habilitación y formato son configuración.
2. Sigue siendo tenant-scoped.

### Criterios de aceptación

**CA01 — Export**

Dado que capacidad on

Cuando genera

Entonces archivo de cobertura del alcance

**CA02 — Sin usuario tercero**

Dado que no existe usuario GRH del tercero

Cuando un autorizado genera el archivo

Entonces el tercero consume el archivo sin usuario GRH obligatorio

**CA03 — Permisos**

Dado que solo roles autorizados

Cuando OK

Entonces OK

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP06-HU66, MT-EP01-HU10
- Microservicios / GRH: Malla

---

## MT-EP08-HU74 — Parametrizar plantilla de importación de novedades TH

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de parametrización

**Quiero:** definir el mapeo de columnas de un archivo de novedades TH a estados y personas

**Para:** cruzar información externa sin rigidizar un formato único en código

### Alcance

**Cubre**

- Plantilla de importación por empresa
- Mapeo columnas→campos
- Validación

**No cubre**

- Asumir formato fijo nacional

### Reglas de negocio

1. Plantilla parametrizable; seeds de ejemplo opcionales.

### Criterios de aceptación

**CA01 — Mapeo**

Dado que define columnas

Cuando guarda plantilla

Entonces queda activa para la empresa

**CA02 — Validación**

Dado que archivo sin columna obligatoria

Cuando importa

Entonces rechaza con error claro

**CA03 — Tenant**

Dado que plantilla

Cuando propia

Entonces OK

**CA04 — Extensible**

Dado que nueva columna

Cuando se agrega al mapeo

Entonces sin deploy de regla fija

### Dependencias

- HUs: MT-EP05-HU61, MT-EP01-HU14
- Microservicios / GRH: Malla

---

## MT-EP08-HU75 — Cruzar programación con novedades TH importadas

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de reportes

**Quiero:** cruzar la malla con un archivo de novedades importado según la plantilla y producir diferencias

**Para:** detectar inconsistencias entre operación y TH

### Alcance

**Cubre**

- Import + cruce + reporte de diferencias
- Opción de aplicar estados con confirmación

**No cubre**

- Sobrescribir silenciosa masiva

### Reglas de negocio

1. Cruce no borra historial.
2. Aplicar cambios exige permiso y deja origen=import.

### Criterios de aceptación

**CA01 — Cruce**

Dado que archivo válido y malla

Cuando ejecuta

Entonces lista coincidencias/diferencias

**CA02 — Aplicar**

Dado que confirma diferencias

Cuando aplica

Entonces celdas actualizadas + historial

**CA03 — Error formato**

Dado que archivo inválido

Cuando rechaza

Entonces sin cambios

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP08-HU74, MT-EP05-HU60, MT-EP05-HU62
- Microservicios / GRH: Malla

---

## MT-EP08-HU76 — Aplicar reglas de compensatorio en reporte

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de reportes

**Quiero:** evaluar las reglas de compensatorio configuradas y mostrar sugerencias o marcas en el reporte de horas

**Para:** soportar políticas distintas sin umbrales fijos en código

### Alcance

**Cubre**

- Evaluación HU23 sobre periodo
- Salida en reporte

**No cubre**

- Regla fija de tres domingos

### Reglas de negocio

1. Umbrales y tipos de día salen de HU23.

### Criterios de aceptación

**CA01 — Eval**

Dado que regla activa cumplida

Cuando reporte

Entonces marca/sugiere según acción

**CA02 — No cumple**

Dado que umbral no alcanzado

Cuando sin marca

Entonces OK

**CA03 — Por frente**

Dado que reglas distintas

Cuando cada frente

Entonces su resultado

**CA04 — Tenant**

Dado que OK

Cuando OK

Entonces OK

### Dependencias

- HUs: MT-EP01-HU23, MT-EP08-HU70
- Microservicios / GRH: Malla

---
