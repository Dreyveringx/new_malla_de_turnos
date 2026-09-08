# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-02 — Construcción de la malla
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Fijar atributo de celda por periodo. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Fijar atributo de celda por periodo |
| Id. Requerimiento | MT-EP02-HU42 |
| Id asociado | REQ-MT-42 / EP-02 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero fijar un atributo habilitado del frente para un funcionario en todo el periodo, para no repetir el mismo valor celda por celda.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU26 |
| 2 | MT-EP02-HU30 |
| 3 | MT-EP02-HU33 |
| 4 | MT-EP05-HU62 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de fijar atributo de celda por periodo.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.

Resultado esperado: Fijar atributo de celda por periodo queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Fijar atributo de celda por periodo» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. La acción solo está disponible con el permiso correspondiente.
2. Solo afecta datos de la empresa del usuario.
3. El comportamiento variable depende de configuración, no de nombres fijos de frente o turno.
4. Solo se muestran o modifican datos de la empresa del usuario autenticado.
5. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Solo atributos habilitados en la configuración del frente.
- RN-02: Los valores vienen de catálogos de la empresa.
- RN-03: Una edición puntual posterior puede diferir y queda auditada.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Celda o rango | N/A | Selección | SI | SI | SI | Celdas a fijar |
| Atributo a fijar | 40 | Selección | SI | NO | SI | Turno, sitio, modalidad u otro atributo |
| Valor fijado | N/A | Selección | SI | SI | SI | Valor que queda bloqueado |
| Fecha desde | 10 | Fecha | SI | NO | SI | Inicio del periodo fijado |
| Fecha hasta | 10 | Fecha | SI | NO | SI | Fin del periodo fijado |


---

*Documento para cliente y diseño.*
