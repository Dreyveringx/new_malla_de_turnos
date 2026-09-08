# EP-02 — Construcción de malla

## Índice

- MT-EP02-HU28 — Crear malla por periodo y frente
- MT-EP02-HU29 — Seleccionar grupo de funcionarios de la malla
- MT-EP02-HU30 — Asignar turno o estado a una celda
- MT-EP02-HU31 — Asignar segundo turno o turno extra el mismo día
- MT-EP02-HU32 — Asignar territorio a la celda
- MT-EP02-HU33 — Asignar modalidad y sitio a la celda
- MT-EP02-HU34 — Registrar observación en la celda
- MT-EP02-HU35 — Visualizar grilla operativa
- MT-EP02-HU36 — Asignar campaña o tarea a la celda
- MT-EP02-HU37 — Cubrir recurso de otro frente o área el mismo día
- MT-EP02-HU38 — Filtrar y buscar en la grilla por atributos habilitados
- MT-EP02-HU39 — Control de concurrencia en edición de celdas
- MT-EP02-HU40 — Carga parcial de grilla por ventana temporal y paginación de personas

---
## MT-EP02-HU28 — Crear malla por periodo y frente

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** crear una malla asociada a un frente, con rango de fechas según el periodo configurado, en estado borrador

**Para:** iniciar la programación operativa del periodo

### Alcance

**Cubre**

- Alta de malla
- Estado inicial borrador
- Validación de frente y alcance

**No cubre**

- Asignación de celdas
- Publicación

### Reglas de negocio

1. La malla pertenece a la empresa del usuario y a un frente de su alcance.
2. El periodo por defecto proviene de la config del frente; el usuario puede ajustar dentro de lo permitido.

### Criterios de aceptación

**CA01 — Alta**

Dado que frente activo y alcance OK

Cuando crea malla con fechas

Entonces queda en borrador

**CA02 — Sin alcance**

Dado que frente fuera de alcance

Cuando intenta crear

Entonces rechazo

**CA03 — Tenant**

Dado que frente de otra empresa

Cuando crear

Entonces imposible

**CA04 — Duplicidad**

Dado que ya existe malla solapada si la regla del frente lo prohíbe

Cuando crea

Entonces aplica severidad de la regla

### Dependencias

- HUs: MT-EP01-HU10, MT-EP00-HU03
- Microservicios / GRH: Malla

---

## MT-EP02-HU29 — Seleccionar grupo de funcionarios de la malla

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** definir el conjunto de funcionarios que participan en la malla

**Para:** delimitar el universo de filas de la grilla

### Alcance

**Cubre**

- Alta/baja de miembros
- Filtros HU08

**No cubre**

- Asignar turnos

### Reglas de negocio

1. Solo empleados de la misma empresa.
2. Respetar filtros y paginación.

### Criterios de aceptación

**CA01 — Agregar**

Dado que malla borrador

Cuando agrega funcionarios

Entonces aparecen como filas

**CA02 — Quitar**

Dado que miembro sin celdas críticas o con política permitida

Cuando se quita

Entonces deja de listarse; historial de celdas previas se conserva

**CA03 — Tenant**

Dado que empleado otra empresa

Cuando agregar

Entonces imposible

**CA04 — Permisos**

Dado que sin ACTUALIZAR

Cuando modifica grupo

Entonces niega

### Dependencias

- HUs: MT-EP02-HU28, MT-EP00-HU08
- Microservicios / GRH: employee; Malla

---

## MT-EP02-HU30 — Asignar turno o estado a una celda

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** asignar a una persona y fecha un turno y/o estado operativo según catálogos y reglas

**Para:** construir la programación celda a celda

### Alcance

**Cubre**

- Upsert de celda
- Validación motor reglas
- Origen manual

**No cubre**

- Publicación

### Reglas de negocio

1. Celda = persona × fecha (+ turnos/estado + atributos habilitados).
2. Se evalúa el motor de reglas al guardar.
3. No se modifica jornada contractual.

### Criterios de aceptación

**CA01 — Asignar turno**

Dado que malla editable

Cuando asigna plantilla activa

Entonces celda queda con turno y origen manual

**CA02 — Estado**

Dado que asigna estado del catálogo

Cuando guarda

Entonces aplica flags del estado

**CA03 — Bloqueo regla**

Dado que violación con severidad bloqueo

Cuando guarda

Entonces rechaza y muestra motivo

**CA04 — Advertencia**

Dado que severidad advertencia

Cuando guarda con confirmación si aplica

Entonces persiste y registra hallazgo

**CA05 — Tenant/alcance**

Dado que malla fuera de empresa o frente

Cuando edita

Entonces niega

### Dependencias

- HUs: MT-EP01-HU11, MT-EP01-HU14, MT-EP01-HU25, MT-EP02-HU39
- Microservicios / GRH: Malla

---

## MT-EP02-HU31 — Asignar segundo turno o turno extra el mismo día

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** agregar un segundo turno el mismo día cuando la capacidad del frente lo permite

**Para:** cubrir jornadas partidas o extras operativas

### Alcance

**Cubre**

- Multi-turno por celda/día según flag

**No cubre**

- Si capacidad doble turno off

### Reglas de negocio

1. Solo si HU26 habilita doble turno.
2. Solape real sigue siendo bloqueo.
3. Marca de extra si el catálogo/regla lo define.

### Criterios de aceptación

**CA01 — Alta segundo**

Dado que capacidad on y sin solape

Cuando agrega segundo turno

Entonces ambos quedan registrados

**CA02 — Solape**

Dado que horarios se cruzan

Cuando guarda

Entonces bloquea

**CA03 — Capacidad off**

Dado que flag off

Cuando intenta segundo turno

Entonces no disponible

**CA04 — Reglas horas**

Dado que supera max_hours_period

Cuando guarda

Entonces aplica severidad regla

### Dependencias

- HUs: MT-EP02-HU30, MT-EP01-HU26, MT-EP01-HU25
- Microservicios / GRH: Malla

---

## MT-EP02-HU32 — Asignar territorio a la celda

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** asignar nodo territorial a la celda cuando el frente tiene la capacidad habilitada

**Para:** ubicar operativamente a la persona ese día

### Alcance

**Cubre**

- Set territorio

**No cubre**

- Frentes sin territorio

### Reglas de negocio

1. Solo nodos activos del árbol del frente/empresa.

### Criterios de aceptación

**CA01 — Asignar**

Dado que capacidad on

Cuando elige nodo

Entonces queda en celda

**CA02 — Off**

Dado que capacidad off

Cuando edita

Entonces campo ausente

**CA03 — Nodo inválido**

Dado que nodo de otro frente/empresa

Cuando asigna

Entonces rechaza

**CA04 — Cobertura**

Dado que existen reglas por territorio

Cuando guarda

Entonces revalúa cobertura

### Dependencias

- HUs: MT-EP01-HU16, MT-EP02-HU30
- Microservicios / GRH: Malla

---

## MT-EP02-HU33 — Asignar modalidad y sitio a la celda

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** definir modalidad y sitio de asistencia en la celda según flags y catálogos

**Para:** reflejar dónde y cómo asiste la persona

### Alcance

**Cubre**

- Set modalidad/sitio

**No cubre**


### Reglas de negocio

1. Si modalidad requiere sitio y capacidad sitio on, el sitio es obligatorio según severidad configurada.

### Criterios de aceptación

**CA01 — OK**

Dado que capacidades on

Cuando asigna modalidad y sitio válidos

Entonces persiste

**CA02 — Requiere sitio**

Dado que modalidad con requiereSitio y sin sitio

Cuando guarda

Entonces bloquea o advierte según regla

**CA03 — Off**

Dado que capacidades off

Cuando edita

Entonces campos ausentes

**CA04 — Tenant**

Dado que sitio ajeno

Cuando asigna

Entonces rechaza

### Dependencias

- HUs: MT-EP01-HU17, MT-EP01-HU18, MT-EP02-HU30
- Microservicios / GRH: Malla

---

## MT-EP02-HU34 — Registrar observación en la celda

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** agregar una nota u observación a la celda cuando la capacidad está habilitada

**Para:** dejar contexto operativo sin abusos de campos

### Alcance

**Cubre**

- Texto de observación
- Límite de longitud configurable

**No cubre**


### Reglas de negocio

1. Si el estado requiere motivo, el motivo puede mapearse a este campo o a campo motivo dedicado según diseño.

### Criterios de aceptación

**CA01 — Alta**

Dado que capacidad nota on

Cuando guarda texto

Entonces visible en celda e historial si cambia

**CA02 — Off**

Dado que capacidad off

Cuando intenta

Entonces no disponible

**CA03 — Límite**

Dado que excede longitud

Cuando guarda

Entonces rechaza

**CA04 — Permisos**

Dado que solo LEER

Cuando edita nota

Entonces niega

### Dependencias

- HUs: MT-EP01-HU26, MT-EP02-HU30
- Microservicios / GRH: Malla

---

## MT-EP02-HU35 — Visualizar grilla operativa

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** ver la grilla personas × fechas con turnos, estados, colores, leyenda, atributos habilitados y hallazgos

**Para:** operar la malla de forma visual

### Alcance

**Cubre**

- Render grilla
- Leyenda
- Indicadores de conflicto

**No cubre**

- Export (HU71)
- Carga total sin ventana (prohibido: ver HU40)

### Reglas de negocio

1. La grilla consume ventana temporal y página de personas (HU40).
2. Colores vienen de catálogos, no de constantes de frente.

### Criterios de aceptación

**CA01 — Vista**

Dado que malla con celdas

Cuando abre grilla

Entonces ve filas/columnas de la ventana cargada

**CA02 — Leyenda**

Dado que existen turnos/estados con color

Cuando abre leyenda

Entonces lista códigos y colores del frente

**CA03 — Conflictos**

Dado que hay hallazgos

Cuando visualiza

Entonces se destacan celdas/reglas

**CA04 — Permisos**

Dado que sin LEER construcción

Cuando abre

Entonces niega

### Dependencias

- HUs: MT-EP02-HU30, MT-EP02-HU40, MT-EP03-HU45
- Microservicios / GRH: Malla FE

---

## MT-EP02-HU36 — Asignar campaña o tarea a la celda

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** etiquetar la celda con campaña/tarea si la capacidad está activa

**Para:** reflejar la actividad operativa del día

### Alcance

**Cubre**

- Set campaña

**No cubre**


### Reglas de negocio

1. Solo campañas vigentes y del frente/empresa.

### Criterios de aceptación

**CA01 — OK**

Dado que capacidad on

Cuando asigna campaña vigente

Entonces persiste

**CA02 — Off**

Dado que capacidad off

Cuando campo ausente

Entonces OK

**CA03 — No vigente**

Dado que campaña vencida

Cuando asigna

Entonces rechaza

**CA04 — Tenant**

Dado que campaña ajena

Cuando rechaza

Entonces OK

### Dependencias

- HUs: MT-EP01-HU15, MT-EP02-HU30
- Microservicios / GRH: Malla

---

## MT-EP02-HU37 — Cubrir recurso de otro frente o área el mismo día

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** asignar a una persona en una malla distinta el mismo día cuando las reglas de solape y horas lo permitan

**Para:** soportar coberturas cruzadas sin hardcodear frentes

### Alcance

**Cubre**

- Asignación cruzada gobernada por reglas

**No cubre**

- Permitir solape real

### Reglas de negocio

1. La contabilización de horas en cruce sigue la configuración (cuenta en malla destino por defecto).
2. Solape horario real siempre bloquea.

### Criterios de aceptación

**CA01 — Permitido**

Dado que sin solape y reglas OK

Cuando asigna en segunda malla

Entonces ambas celdas existen

**CA02 — Solape**

Dado que horarios cruzan

Cuando bloquea

Entonces OK

**CA03 — Horas**

Dado que supera tope

Cuando aplica severidad

Entonces OK

**CA04 — Tenant**

Dado que malla otra empresa

Cuando imposible

Entonces OK

### Dependencias

- HUs: MT-EP02-HU30, MT-EP01-HU25
- Microservicios / GRH: Malla

### Consideraciones técnicas

Default recomendado: cuenta horas donde se asigna + regla solape.

---

## MT-EP02-HU38 — Filtrar y buscar en la grilla por atributos habilitados

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** filtrar la grilla por texto, turno, estado y atributos habilitados del frente

**Para:** encontrar rápido personas o situaciones

### Alcance

**Cubre**

- Filtros dinámicos según flags

**No cubre**


### Reglas de negocio

1. No mostrar filtros de capacidades deshabilitadas.

### Criterios de aceptación

**CA01 — Filtro estado**

Dado que hay varios estados

Cuando filtra uno

Entonces solo filas/celdas coincidentes en la ventana

**CA02 — Sin filtro fantasma**

Dado que territorio off

Cuando abre filtros

Entonces no aparece filtro territorio

**CA03 — Permisos**

Dado que LEER

Cuando filtra

Entonces permitido

**CA04 — Tenant**

Dado que datos

Cuando filtro

Entonces solo propia empresa

### Dependencias

- HUs: MT-EP02-HU35, MT-EP01-HU26
- Microservicios / GRH: Malla

---

## MT-EP02-HU39 — Control de concurrencia en edición de celdas

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** evitar que dos ediciones concurrentes sobrescriban en silencio la misma celda

**Para:** proteger integridad operativa

### Alcance

**Cubre**

- Versionado/optimistic locking por celda
- Conflicto visible al usuario

**No cubre**

- Bloqueo pesimista de malla completa (no requerido)

### Reglas de negocio

1. Cada celda tiene versión; escribir con versión obsoleta falla con conflicto.
2. El usuario debe poder recargar y reintentar.

### Criterios de aceptación

**CA01 — Conflicto**

Dado que usuario A y B cargan misma celda

Cuando A guarda y luego B guarda con versión vieja

Entonces B recibe error de conflicto y no pisa a A

**CA02 — OK**

Dado que versión actual

Cuando guarda

Entonces incrementa versión

**CA03 — Historial**

Dado que guarda OK

Cuando consulta historial

Entonces incluye el cambio de A

**CA04 — Permisos**

Dado que sin ACTUALIZAR

Cuando guarda

Entonces niega antes del versionado

### Dependencias

- HUs: MT-EP02-HU30, MT-EP05-HU62
- Microservicios / GRH: Malla

### Consideraciones técnicas

Optimistic locking / ETag por celda.

---

## MT-EP02-HU40 — Carga parcial de grilla por ventana temporal y paginación de personas

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** cargar solo la ventana de fechas y la página de personas necesarias

**Para:** operar mallas grandes sin payloads inmanejables

### Alcance

**Cubre**

- API de grilla con from/to + page/size
- Virtualización en UI

**No cubre**

- Descargar 1000×31 siempre

### Reglas de negocio

1. El backend no debe exigir devolver toda la malla para editar una ventana.
2. Los contadores globales pueden ser proyecciones/agregados aparte.

### Criterios de aceptación

**CA01 — Ventana**

Dado que malla de un mes

Cuando pide 7 días

Entonces solo recibe esos días

**CA02 — Página**

Dado que 200 personas

Cuando pide página 1 size 50

Entonces recibe 50 filas

**CA03 — Edición**

Dado que celda de la ventana

Cuando guarda

Entonces no requiere recargar toda la malla

**CA04 — Permisos/tenant**

Dado que consulta

Cuando datos

Entonces solo empresa y alcance

### Dependencias

- HUs: MT-EP02-HU35
- Microservicios / GRH: Malla

### Consideraciones técnicas

Requisito no funcional de performance.

---

## MT-EP02-HU41 — Copiar semana o aplicar asignación masiva

**Alcance:** Incluida en el módulo  
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla  
**Quiero:** copiar un rango de fechas o aplicar la misma asignación a varias celdas  
**Para:** armar el periodo más rápido sin saltarme validaciones

### Alcance

**Cubre**

- Copia de rango origen → destino
- Asignación masiva a selección de celdas
- Validación con motor de reglas e historial

**No cubre**

- Bypass de reglas
- Copia entre empresas

### Reglas de negocio

1. Origen y destino pertenecen a la misma empresa y malla/frente autorizados.
2. Los bloqueos del motor de reglas no se aplican; se reportan.
3. Queda historial en celdas modificadas.

### Criterios de aceptación

**CA01 — Copia de rango**

Dado que hay un rango origen con asignaciones  
Cuando se copia a un rango destino válido  
Entonces las celdas destino se actualizan respetando reglas

**CA02 — Masiva**

Dado que hay celdas seleccionadas  
Cuando se aplica una asignación  
Entonces solo se escriben las que pasan validación

**CA03 — Tenant**

Dado que el usuario opera su empresa  
Cuando intenta destino de otra empresa  
Entonces la acción es imposible

### Dependencias

- HUs: MT-EP02-HU30, MT-EP01-HU25, MT-EP05-HU62, MT-EP02-HU39
- Microservicios / GRH: Malla

---

## MT-EP02-HU42 — Fijar atributo de celda por periodo

**Alcance:** Incluida en el módulo  
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla  
**Quiero:** fijar un atributo habilitado del frente para un funcionario en todo el periodo  
**Para:** no repetir el mismo valor celda por celda

### Alcance

**Cubre**

- Fijación de atributos habilitados (sitio, modalidad, territorio, campaña u otros según config)
- Aplicación a periodo o subrango

**No cubre**

- Casos especiales por nombre de sitio o frente en el producto

### Reglas de negocio

1. Solo atributos habilitados en la configuración del frente.
2. Los valores vienen de catálogos de la empresa.
3. Una edición puntual posterior puede diferir y queda auditada.

### Criterios de aceptación

**CA01 — Fijar**

Dado que el frente habilita el atributo  
Cuando se fija un valor para un funcionario en el periodo  
Entonces las celdas del rango reciben ese valor

**CA02 — Capacidad off**

Dado que el atributo está deshabilitado  
Cuando se busca la acción  
Entonces no está disponible

**CA03 — Sin hardcoding**

Dado que el producto  
Cuando se implementa  
Entonces no existe un sitio o frente tratado como caso especial en código

### Dependencias

- HUs: MT-EP01-HU26, MT-EP02-HU30, MT-EP02-HU33, MT-EP05-HU62
- Microservicios / GRH: Malla

---
