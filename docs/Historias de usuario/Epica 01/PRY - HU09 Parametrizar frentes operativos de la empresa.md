# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar frentes operativos de la empresa. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar frentes operativos de la empresa |
| Id. Requerimiento | MT-EP01-HU09 |
| Id asociado | REQ-MT-09 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero registrar frentes operativos con código, nombre, descripción y estado pertenecientes a mi empresa, para configurar operaciones distintas sin depender de una lista fija de nombres de negocio.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU02 |
| 2 | MT-EP00-HU04 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de parametrizar frentes operativos de la empresa.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando crea un frente con código único en su empresa.
   - Sistema: Entonces el frente queda disponible solo para esa empresa.

Resultado esperado: Parametrizar frentes operativos de la empresa queda operativa, aislada por empresa y gobernada por configuración.

---

## Flujos alternos

- FA-01: Si falta configuración previa requerida, el sistema indica qué falta y no continúa.
- FA-02: Si el frente o la capacidad están deshabilitados, la acción no aparece o se informa.
- FA-03: Si hay advertencias de reglas, el usuario puede confirmar solo cuando la configuración lo permita.

---

## Errores

- E-01: Datos incompletos o inválidos.
  - Comportamiento esperado: No guarda; indica el problema.
- E-02: Sin permiso o fuera de alcance de frente.
  - Comportamiento esperado: Acceso no permitido.
- E-03: Intento de operar datos de otra empresa.
  - Comportamiento esperado: No visible / rechazado.
- E-04: Fallo al guardar.
  - Comportamiento esperado: Mensaje claro; no deja información inconsistente.

---

## Prototipo de interfaz de usuario y/o reportes

Pantalla o flujo de «Parametrizar frentes operativos de la empresa» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta: dado que el usuario tiene permiso de parametrización, cuando crea un frente con código único en su empresa, entonces el frente queda disponible solo para esa empresa.
2. Unicidad: dado que ya existe el código en la empresa, cuando intenta crear otro con el mismo código, entonces el sistema rechaza por duplicado.
3. Sin defaults de producto: dado que una empresa nueva sin seeds, cuando abre el catálogo de frentes, entonces no asume frentes predefinidos de otras operaciones.
4. Multiempresa: dado que empresa A tiene frentes, cuando usuario de empresa B lista frentes, entonces no ve los de A.
5. Inactivo: dado que un frente está inactivo, cuando se crea una malla, entonces ese frente no aparece en el selector.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: El frente es un catálogo tenant-scoped, no un enum de aplicación.
- RN-02: Un frente inactivo no se ofrece para nuevas mallas.
- RN-03: Los nombres de operaciones actuales son solo datos de configuración o seeds de ejemplo.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código | 20 | Alfanumérico | SI | NO | SI | Identificador único del frente operativo en la empresa |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre visible del frente operativo |
| Descripción | N/A | Texto | NO | NO | SI | Texto de ayuda o detalle |
| Activo | 1 | Booleano | SI | NO | SI | Indica si está disponible para uso |


---

*Documento para cliente y diseño.*
