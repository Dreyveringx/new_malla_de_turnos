# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-04 — Publicación y ciclo de vida
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Editar malla publicada. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Editar malla publicada |
| Id. Requerimiento | MT-EP04-HU59 |
| Id asociado | REQ-MT-59 / EP-04 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero modificar celdas de una malla publicada cuando la configuración lo permite, con motivo e historial, para atender cambios reales sin perder trazabilidad.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU10 |
| 2 | MT-EP05-HU62 |
| 3 | MT-EP05-HU63 |
| 4 | MT-EP02-HU39 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de editar malla publicada.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando cambia celda con motivo.
   - Sistema: Entonces persiste, historial y notifica si corresponde.

Resultado esperado: Editar malla publicada queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Editar malla publicada» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Edición permitida: dado que flag on, cuando cambia celda con motivo, entonces persiste, historial y notifica si corresponde.
2. Flag off: dado que no editable, cuando intenta, entonces niega.
3. Motivo: dado que config exige motivo, cuando guarda sin motivo, entonces bloquea.
4. Concurrencia: dado que versión vieja, cuando guarda, entonces conflicto HU39.
5. Tenant: dado que OK, cuando OK, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Si editabilidad post-publicación = no, solo novedades vía flujo permitido o nada.
- RN-02: Cada cambio deja historial inmutable.
- RN-03: Estado puede marcarse como modificada después de publicar a nivel de celda/malla según diseño.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Malla publicada | N/A | Selección | SI | SI | SI | Malla editable post-publicación |
| Celda a modificar | N/A | Selección | SI | SI | SI | Celda de la malla publicada |
| Nuevo valor | N/A | Selección | SI | SI | SI | Turno, estado o atributo nuevo |
| Motivo del cambio | N/A | Texto | SI | NO | SI | Justificación de la edición post-publicación |


---

*Documento para cliente y diseño.*
