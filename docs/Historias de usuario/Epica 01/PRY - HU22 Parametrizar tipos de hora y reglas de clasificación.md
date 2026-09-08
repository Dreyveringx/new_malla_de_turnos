# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar tipos de hora y reglas de clasificación. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar tipos de hora y reglas de clasificación |
| Id. Requerimiento | MT-EP01-HU22 |
| Id asociado | REQ-MT-22 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero definir tipos de hora (ordinaria, extra, festiva, nocturna, recargo u otros) con condiciones, prioridad y aplicabilidad, para clasificar horas sin fórmulas quemadas por frente.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU21 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de parametrizar tipos de hora y reglas de clasificación.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando crea tipo de hora.
   - Sistema: Entonces disponible para el motor HU70.

Resultado esperado: Parametrizar tipos de hora y reglas de clasificación queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Parametrizar tipos de hora y reglas de clasificación» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta tipo: dado que parametrizador, cuando crea tipo de hora, entonces disponible para el motor HU70.
2. Prioridad: dado que dos reglas aplican al mismo intervalo, cuando se clasifica, entonces gana la de mayor prioridad según config.
3. Tenant: dado que otra empresa, cuando lista tipos, entonces aislados.
4. Extensibilidad: dado que se necesita un tipo nuevo, cuando se crea en catálogo, entonces sin despliegue de lógica específica.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: ORD/EXT/FES etc. son códigos de catálogo/seeds, no enums rígidos de producto.
- RN-02: La prioridad resuelve solapes de clasificación.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código tipo de hora | 40 | Alfanumérico | SI | NO | SI | Identificador del tipo de hora |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre del tipo de hora |
| Orden | 3 | Número | NO | NO | SI | Orden de presentación |
| Regla de clasificación | N/A | Texto | NO | NO | SI | Criterio de clasificación del tipo |
| Activo | 1 | Booleano | SI | NO | SI | Indica si el tipo está disponible |


---

*Documento para cliente y diseño.*
