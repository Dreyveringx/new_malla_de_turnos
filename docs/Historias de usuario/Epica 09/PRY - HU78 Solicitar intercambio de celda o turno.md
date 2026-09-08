# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-09 — Intercambio de turnos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Solicitar intercambio de celda o turno. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Solicitar intercambio de celda o turno |
| Id. Requerimiento | MT-EP09-HU78 |
| Id asociado | REQ-MT-78 / EP-09 |

### Descripción de historia de usuario

Como Usuario de la empresa vinculado a un funcionario, quiero iniciar una solicitud de intercambio eligiendo mi celda y un compañero candidato con su celda, para resolver cambios de turno dentro de la plataforma.

---

## Actores

- Inicia: Usuario de la empresa vinculado a un funcionario
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP09-HU77 |
| 2 | MT-EP07-HU68 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de solicitar intercambio de celda o turno.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando envía.
   - Sistema: Entonces queda pendiente.

Resultado esperado: Solicitar intercambio de celda o turno queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Solicitar intercambio de celda o turno» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Solicitud: dado que intercambio on y celdas elegibles, cuando envía, entonces queda pendiente.
2. Misma empresa: dado que candidato otra empresa, cuando selección, entonces imposible.
3. Off: dado que config off, cuando acción, entonces ausente.
4. Límite: dado que supera cantidad configurada, cuando envía, entonces rechaza.
5. Permisos: dado que no habilitado a solicitar, cuando niega, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Solo si HU77 enabled.
- RN-02: Ambos empleados misma empresa; frente según config.
- RN-03: No modifica malla hasta aprobación+aplicación.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Mi celda / turno | N/A | Selección | SI | SI | SI | Celda propia a intercambiar |
| Celda / turno de contraparte | N/A | Selección | SI | SI | SI | Celda objetivo del intercambio |
| Motivo | N/A | Texto | NO | NO | SI | Justificación de la solicitud |


---

*Documento para cliente y diseño.*
