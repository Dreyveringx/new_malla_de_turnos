# EP-00 — Integración con GRH

## Índice

- MT-EP00-HU01 — Completar módulo y submódulos de Malla de Turnos en la plataforma
- MT-EP00-HU02 — Configurar permisos RBAC por sección de menú
- MT-EP00-HU03 — Asignar alcance de frentes operativos a usuarios o roles
- MT-EP00-HU04 — Aislar información por empresa
- MT-EP00-HU05 — Reutilizar empleados, áreas, cargos y calendario de festivos de GRH
- MT-EP00-HU06 — Distinguir jornada contractual de malla operativa
- MT-EP00-HU07 — Registrar event types de notificación y timeline para Malla
- MT-EP00-HU08 — Consumir listado de empleados con filtro por área o vínculo a frente

---
## MT-EP00-HU01 — Completar módulo y submódulos de Malla de Turnos en la plataforma

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Super-administrador de la plataforma GRH

**Quiero:** completar el módulo Malla de Turnos (ya existente en catálogo) con sus submódulos, rutas de menú y asociación a planes

**Para:** que las empresas con el módulo en su plan vean las secciones en el menú sin crear un módulo duplicado

### Alcance

**Cubre**

- Completar submódulos del módulo existente (Parametrización, Construcción, Consulta, Mi programación, Reportes)
- Asociar el módulo a planes de servicio
- Habilitar visibilidad en menú cuando el plan activo de la empresa lo incluye y hay permiso LEER

**No cubre**

- Parametrizar frentes, turnos o mallas
- Crear un segundo módulo con otro nombre o id

### Reglas de negocio

1. El módulo de plataforma se identifica en el catálogo existente; no se crea un módulo paralelo.
2. Los submódulos son secciones de menú con permisos CREAR/LEER/ACTUALIZAR/ELIMINAR.
3. La empresa solo ve el módulo si su plan activo lo incluye.
4. Los nombres de frentes operativos no son ítems del menú de plataforma.

### Criterios de aceptación

**CA01 — Completar sin duplicar**

Dado que existe el módulo Malla de Turnos en el catálogo de plataforma

Cuando el Super-administrador registra o completa los submódulos y los asocia a un plan

Entonces no se crea un segundo módulo y el plan queda asociado al módulo existente

**CA02 — Visibilidad por plan**

Dado que una empresa tiene plan activo con el módulo y un usuario con LEER en un submódulo

Cuando el usuario inicia sesión

Entonces ve las secciones habilitadas en el menú lateral

**CA03 — Sin plan**

Dado que una empresa no tiene el módulo en su plan

Cuando un usuario de esa empresa inicia sesión

Entonces no ve Malla de Turnos en el menú

**CA04 — Permisos**

Dado que solo el Super-administrador puede modificar el catálogo de módulos de plataforma

Cuando un administrador de empresa intenta crear un módulo de plataforma

Entonces la acción no está disponible

### Dependencias

- HUs: Ninguna previa de Malla
- Microservicios / GRH: company-admin (módulos, submódulos, plan_modulos); auth (permission_submodules); frontend menú

### Consideraciones técnicas

Anclar al módulo id=13 en DEV si aplica. Checklist: company-admin + seeds permisos + rutas FE.

---

## MT-EP00-HU02 — Configurar permisos RBAC por sección de menú

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Administrador de empresa

**Quiero:** asignar a roles de mi empresa los permisos CREAR, LEER, ACTUALIZAR y ELIMINAR sobre las secciones de Malla de Turnos

**Para:** controlar quién parametriza, construye, publica, consulta o reporta sin inventar un sistema de seguridad paralelo

### Alcance

**Cubre**

- Asignación de permisos por rol y submódulo usando el modelo de seguridad GRH
- Validación de acceso en cada sección

**No cubre**

- Alcance por frente operativo (ver HU03)
- Roles hardcodeados tipo Contact Center

### Reglas de negocio

1. Los únicos permisos de plataforma son CREAR, LEER, ACTUALIZAR y ELIMINAR por submódulo.
2. Los roles operativos (coordinador, supervisora, analista, etc.) son roles de la empresa, no enums del producto.
3. Sin LEER en la sección, el usuario no ve la opción de menú ni puede invocar la API correspondiente.

### Criterios de aceptación

**CA01 — Asignar permisos**

Dado que existe un rol de empresa y submódulos de Malla

Cuando el administrador asigna LEER y ACTUALIZAR en Construcción

Entonces los usuarios con ese rol pueden abrir Construcción y modificar según ACTUALIZAR

**CA02 — Denegación**

Dado que un usuario no tiene LEER en Reportes

Cuando intenta acceder a Reportes

Entonces el sistema niega el acceso

**CA03 — Multiempresa**

Dado que dos empresas tienen roles con el mismo nombre

Cuando se consultan permisos

Entonces cada empresa solo ve y administra sus propios roles

**CA04 — Sin inventar permisos**

Dado que se configura seguridad

Cuando se listan permisos disponibles

Entonces solo aparecen CREAR/LEER/ACTUALIZAR/ELIMINAR (no permisos inventados de frente)

### Dependencias

- HUs: MT-EP00-HU01
- Microservicios / GRH: auth (roles, permission_submodules); company-admin submódulos

### Consideraciones técnicas

Alcance por frente = HU03 (dominio Malla).

---

## MT-EP00-HU03 — Asignar alcance de frentes operativos a usuarios o roles

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Administrador de empresa o usuario con permiso de parametrización

**Quiero:** definir qué frentes operativos puede ver u operar cada usuario o rol dentro de Malla

**Para:** aislar operaciones por frente sin modificar el modelo RBAC de plataforma

### Alcance

**Cubre**

- Matriz usuario/rol ↔ frentes autorizados
- Filtrado de selectores y mallas según alcance

**No cubre**

- Permisos CREAR/LEER de menú (HU02)
- Crear frentes (HU09)

### Reglas de negocio

1. El alcance de frente es configuración del dominio Malla, no un permiso SM_* nuevo.
2. Un usuario solo opera frentes de su empresa y dentro de su alcance.
3. Si no tiene alcance asignado, no ve frentes (fail-closed) salvo rol con alcance total configurado explícitamente.

### Criterios de aceptación

**CA01 — Asignación**

Dado que existen frentes A y B en la empresa

Cuando se autoriza al usuario solo el frente A

Entonces en selectores y listados solo aparece A

**CA02 — Intento fuera de alcance**

Dado que el usuario solo tiene frente A

Cuando intenta abrir una malla del frente B por identificador

Entonces el sistema rechaza por autorización

**CA03 — Tenant**

Dado que el frente pertenece a otra empresa

Cuando se intenta asignar alcance

Entonces no aparece ni se puede asignar

**CA04 — Auditoría**

Dado que se modifica el alcance de un usuario

Cuando se guarda el cambio

Entonces queda registro de quién cambió qué y cuándo

### Dependencias

- HUs: MT-EP00-HU02, MT-EP01-HU09
- Microservicios / GRH: Malla (nuevo); auth solo para identidad del usuario

---

## MT-EP00-HU04 — Aislar información por empresa

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Administrador de empresa / Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** que toda la información de Malla de Turnos pertenezca únicamente a mi empresa

**Para:** impedir fugas de datos entre tenants

### Alcance

**Cubre**

- Aislamiento de catálogos, mallas, reglas, solicitudes, reportes e historial
- companyId desde contexto autenticado

**No cubre**

- Lógica de negocio de turnos

### Reglas de negocio

1. El identificador de empresa proviene del contexto autenticado; no se confía en el valor enviado por el cliente como fuente de verdad.
2. Todas las consultas y escrituras están filtradas por empresa.
3. Catálogos, mallas, reglas, solicitudes de intercambio y exportaciones son tenant-scoped.

### Criterios de aceptación

**CA01 — Lectura aislada**

Dado que la empresa A tiene frentes y mallas

Cuando un usuario de la empresa B lista frentes o mallas

Entonces no ve datos de A

**CA02 — Escritura aislada**

Dado que un usuario autenticado en empresa A

Cuando intenta crear un recurso indicando empresa B en el cuerpo

Entonces el sistema ignora ese valor y persiste solo bajo A, o rechaza la petición

**CA03 — Empleados**

Dado que se seleccionan funcionarios para una malla

Cuando se listan candidatos

Entonces solo aparecen empleados de la misma empresa

**CA04 — Reportes**

Dado que se exporta un reporte

Cuando se genera el archivo

Entonces solo incluye datos de la empresa del usuario

### Dependencias

- HUs: MT-EP00-HU01
- Microservicios / GRH: Todos los MS involucrados; JWT companyId

### Consideraciones técnicas

Invariante de dominio: toda entidad operativa lleva company_id.

---

## MT-EP00-HU05 — Reutilizar empleados, áreas, cargos y calendario de festivos de GRH

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** usar los funcionarios, áreas, cargos y festivos ya existentes en GRH al armar mallas

**Para:** no duplicar padrones ni calendarios

### Alcance

**Cubre**

- Consumo de empleados, áreas, cargos y festivos del calendario de empresa
- Referencia de solo lectura a jornada contractual cuando se consulte

**No cubre**

- Crear empleados en Malla
- Inventar sedes GRH (no existen): sitios = catálogo Malla HU18
- Escribir jornada contractual desde Malla

### Reglas de negocio

1. Malla no mantiene un padrón paralelo de empleados.
2. Áreas y cargos se leen de parametrización GRH.
3. Festivos se leen del calendario de empresa.
4. Sitios de asistencia son catálogo propio de Malla.

### Criterios de aceptación

**CA01 — Empleados**

Dado que existen empleados activos en la empresa

Cuando el coordinador arma el grupo de la malla

Entonces selecciona desde el padrón GRH de su empresa

**CA02 — Áreas y cargos**

Dado que se filtra por área o cargo

Cuando se aplican filtros

Entonces los valores vienen de maestros GRH

**CA03 — Festivos**

Dado que el calendario de empresa tiene un festivo

Cuando se consulta el día en malla

Entonces el sistema reconoce el festivo sin catálogo paralelo de festivos en Malla

**CA04 — Sin sedes GRH**

Dado que se necesita un sitio de asistencia

Cuando el usuario busca sedes en GRH

Entonces usa el catálogo de sitios de Malla (HU18), no un maestro inexistente de sedes

### Dependencias

- HUs: MT-EP00-HU04, MT-EP00-HU08, MT-EP01-HU18, MT-EP01-HU20
- Microservicios / GRH: employee; parametrization (areas, positions, company-calendars); Malla para sitios

### Consideraciones técnicas

Si employee no filtra por área: HU08.

---

## MT-EP00-HU06 — Distinguir jornada contractual de malla operativa

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** consultar la jornada contractual como referencia sin modificarla al programar la malla

**Para:** separar condición laboral de la programación operativa diaria

### Alcance

**Cubre**

- Lectura de jornada contractual como referencia
- Programación operativa independiente (persona × fecha × turno/estado × atributos)

**No cubre**

- Actualizar work_schedule / schedule_assignment desde Malla
- Tratar la malla como fuente de jornada contractual

### Reglas de negocio

1. La jornada contractual define condiciones laborales; la malla define la operación por fecha.
2. Guardar una celda no altera la jornada contractual.
3. Las diferencias entre jornada y malla pueden advertirse si existe una regla configurada; no se corrigen escribiendo la jornada.

### Criterios de aceptación

**CA01 — No escritura**

Dado que un funcionario tiene jornada contractual definida

Cuando se le asigna un turno en malla distinto al habitual

Entonces la jornada contractual permanece igual

**CA02 — Referencia**

Dado que el coordinador consulta la ficha del funcionario en contexto de malla

Cuando abre la referencia de jornada

Entonces ve la jornada contractual en modo lectura

**CA03 — Independencia**

Dado que no hay jornada contractual cargada

Cuando se crea una celda operativa

Entonces la malla permite programar según reglas del frente (sin bloquear por ausencia de jornada, salvo regla explícita)

**CA04 — Permisos**

Dado que el usuario solo tiene permisos de Malla

Cuando intenta editar jornada contractual desde Malla

Entonces no existe esa acción

### Dependencias

- HUs: MT-EP00-HU05
- Microservicios / GRH: parametrization (work-schedules, schedule-assignments, working-profile) solo lectura

---

## MT-EP00-HU07 — Registrar event types de notificación y timeline para Malla

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Super-administrador de la plataforma GRH / equipo de plataforma

**Quiero:** registrar los tipos de evento de notificación y de timeline que usará Malla

**Para:** reutilizar notification-service y auditoría GRH sin mailers ni logs paralelos

### Alcance

**Cubre**

- Alta de event types: publicación, cambio de celda, novedad, intercambio (aprobación/rechazo/aplicación)
- Despacho vía infraestructura existente (correo + popup según config del evento)

**No cubre**

- Motor de plantillas de correo propio de Malla
- Auditoría paralela completa

### Reglas de negocio

1. Malla no envía correo directo; despacha eventos al servicio de notificaciones.
2. Los hechos de alto nivel van a timeline; el detalle de celda vive en historial de dominio (HU62).
3. Los despachos deben ser idempotentes por clave de evento de negocio.

### Criterios de aceptación

**CA01 — Registro**

Dado que se despliegan los event types de Malla

Cuando se consultan en el catálogo de notificaciones

Entonces existen los códigos definidos para publicación, cambio, novedad e intercambio

**CA02 — Publicación**

Dado que se publica una malla

Cuando el flujo termina OK

Entonces se despacha el evento de publicación a los destinatarios configurados

**CA03 — Timeline**

Dado que ocurre un cambio relevante de celda o publicación

Cuando se consulta timeline

Entonces existe el hecho de negocio correspondiente

**CA04 — Idempotencia**

Dado que el mismo evento se reintenta con la misma clave

Cuando se procesa el reintento

Entonces no se duplica la notificación al destinatario

### Dependencias

- HUs: MT-EP00-HU01; usada por HU63, HU57, HU81
- Microservicios / GRH: notification-service; audit/timeline; parametrization catálogo timeline si aplica

---

## MT-EP00-HU08 — Consumir listado de empleados con filtro por área o vínculo a frente

**Alcance:** Incluida en el módulo
**Estado:** Definitiva

### Historia

**Como:** Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)

**Quiero:** listar funcionarios aplicables al frente filtrando por área, cargo y estado sin traer toda la empresa de golpe

**Para:** armar grupos de malla de forma usable y tenant-safe

### Alcance

**Cubre**

- Listado paginado de empleados de la empresa
- Filtros por área, cargo, estado y texto
- Resolución de empleados del frente vía vínculo frente↔área (HU10) o selección manual

**No cubre**

- Alta de empleados
- Filtros por frentes hardcodeados

### Reglas de negocio

1. Toda consulta de empleados usa la empresa del contexto autenticado.
2. Si el servicio de empleados no expone filtro por área, Malla debe paginar y filtrar de forma explícita documentada, o solicitar la extensión del API.
3. No se cachea padrón completo de otra empresa.

### Criterios de aceptación

**CA01 — Paginación**

Dado que la empresa tiene cientos de empleados

Cuando se abre el selector de grupo

Entonces se cargan páginas o resultados filtrados, no un volcado único no paginado obligatorio

**CA02 — Filtro área**

Dado que el frente está vinculado a una o más áreas

Cuando se listan candidatos

Entonces se priorizan o filtran empleados de esas áreas según configuración

**CA03 — Tenant**

Dado que existen empleados en otra empresa

Cuando se lista

Entonces no aparecen

**CA04 — Estado**

Dado que hay empleados inactivos

Cuando se aplica filtro de activos

Entonces solo se ofrecen los que cumplen el filtro

### Dependencias

- HUs: MT-EP00-HU05, MT-EP01-HU10
- Microservicios / GRH: employee-service (extender filtro areaId si falta); Malla BFF/use case

### Consideraciones técnicas

Dependencia técnica: hoy el listado employee puede no filtrar por areaId.

---
