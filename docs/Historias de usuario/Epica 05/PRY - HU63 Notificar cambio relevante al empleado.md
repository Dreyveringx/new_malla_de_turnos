# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-05 — Novedades, cambios y auditoría
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Notificar cambio relevante al empleado. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Notificar cambio relevante al empleado |
| Id. Requerimiento | MT-EP05-HU63 |
| Id asociado | REQ-MT-63 / EP-05 |

### Descripción de historia de usuario

Como Usuario de la empresa vinculado a un funcionario, quiero recibir notificación informativa cuando cambia su programación publicada según flags y event types, para enterarse del cambio sin tener que aceptar en la plataforma.

---

## Actores

- Inicia: Usuario de la empresa vinculado a un funcionario
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU07 |
| 2 | MT-EP01-HU14 |
| 3 | MT-EP04-HU59 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de notificar cambio relevante al empleado.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando guarda.
   - Sistema: Entonces empleado recibe notificación.

Resultado esperado: Notificar cambio relevante al empleado queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Notificar cambio relevante al empleado» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Cambio: dado que celda publicada cambia y notifica=sí, cuando guarda, entonces empleado recibe notificación.
2. Sin aceptación: dado que recibe aviso, cuando abre app, entonces no se le pide aceptar el turno.
3. No notifica: dado que flag notifica=no, cuando cambia, entonces no despacha a empleado.
4. Falla canal: dado que email falla, cuando reintento idempotente, entonces no duplica popup si ya entregado según diseño del MS.
5. Tenant: dado que destinatario, cuando misma empresa, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Si el estado/config indica notifica=sí y la malla está en alcance de notificación, se despacha.
- RN-02: Idempotencia por clave de evento.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Evento de cambio | N/A | Selección | SI | SI | SI | Cambio relevante que dispara aviso |
| Destinatario empleado | N/A | Selección | N/A | SI | NO | Empleado vinculado a la celda |
| Plantilla / canal de notificación | N/A | Selección | SI | SI | SI | Medio configurado de aviso |


---

*Documento para cliente y diseño.*
