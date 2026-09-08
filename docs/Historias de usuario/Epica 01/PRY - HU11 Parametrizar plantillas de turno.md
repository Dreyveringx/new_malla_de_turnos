# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar plantillas de turno. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar plantillas de turno |
| Id. Requerimiento | MT-EP01-HU11 |
| Id asociado | REQ-MT-11 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero registrar plantillas de turno con código, nombre, horarios, color, cruce de medianoche y aplicabilidad por frente, para reutilizar definiciones horarias al armar mallas sin quemar turnos en código.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU09 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de parametrizar plantillas de turno.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando crea plantilla con código único en el alcance definido.
   - Sistema: Entonces queda disponible para asignar en frentes autorizados.

Resultado esperado: Parametrizar plantillas de turno queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Parametrizar plantillas de turno» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta: dado que existe al menos un frente, cuando crea plantilla con código único en el alcance definido, entonces queda disponible para asignar en frentes autorizados.
2. Medianoche: dado que hora fin es menor que hora inicio y se marca cruce de medianoche, cuando se guarda, entonces la duración se calcula cruzando día.
3. Inactivo: dado que plantilla inactiva, cuando se asigna celda nueva, entonces no aparece en el selector.
4. Tenant: dado que otra empresa, cuando lista plantillas, entonces no ve las ajenas.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Las plantillas son catálogo tenant-scoped.
- RN-02: Un turno inactivo no se ofrece en nuevas asignaciones.
- RN-03: Los códigos de ejemplo de Excel son seeds, no enums.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código | 20 | Alfanumérico | SI | NO | SI | Identificador único del plantilla de turno en la empresa |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre visible del plantilla de turno |
| Descripción | N/A | Texto | NO | NO | SI | Texto de ayuda o detalle |
| Hora inicio | 8 | Hora | SI | NO | SI | Hora de inicio del turno |
| Hora fin | 8 | Hora | SI | NO | SI | Hora de fin del turno |
| Cruza medianoche | 1 | Booleano | SI | NO | SI | Indica si el turno pasa de un día a otro |
| Color | 7 | Color | NO | NO | SI | Color de visualización (ej. #RRGGBB) |
| Frentes aplicables | N/A | Selección | SI | SI | SI | Frentes donde aplica la plantilla |
| Activo | 1 | Booleano | SI | NO | SI | Indica si la plantilla está disponible |


---

*Documento para cliente y diseño.*
