# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar campañas o tareas de celda. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar campañas o tareas de celda |
| Id. Requerimiento | MT-EP01-HU15 |
| Id asociado | REQ-MT-15 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero registrar campañas o tareas con código, nombre, color, vigencia y aplicabilidad a frentes, para etiquetar celdas sin hardcodear nombres de campaña.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU10 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de parametrizar campañas o tareas de celda.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando crea campaña vigente.
   - Sistema: Entonces aparece al asignar celdas de ese frente.

Resultado esperado: Parametrizar campañas o tareas de celda queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Parametrizar campañas o tareas de celda» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta: dado que capacidad campañas habilitada en un frente, cuando crea campaña vigente, entonces aparece al asignar celdas de ese frente.
2. Vigencia: dado que campaña fuera de vigencia, cuando se asigna celda, entonces no se ofrece.
3. Capacidad off: dado que frente sin campañas, cuando se edita celda, entonces no pide campaña.
4. Tenant: dado que otra empresa, cuando lista, entonces no ve campañas ajenas.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Solo aplica si el frente tiene la capacidad habilitada (HU10/HU26).
- RN-02: Ejemplos de operación son seeds.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código | 20 | Alfanumérico | SI | NO | SI | Identificador único del campaña o tarea en la empresa |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre visible del campaña o tarea |
| Descripción | N/A | Texto | NO | NO | SI | Texto de ayuda o detalle |
| Color | 7 | Color | NO | NO | SI | Color de visualización |
| Vigencia desde | 10 | Fecha | NO | NO | SI | Inicio de vigencia |
| Vigencia hasta | 10 | Fecha | NO | NO | SI | Fin de vigencia |
| Frentes aplicables | N/A | Selección | SI | SI | SI | Frentes donde aplica |
| Activo | 1 | Booleano | SI | NO | SI | Indica si está disponible |


---

*Documento para cliente y diseño.*
