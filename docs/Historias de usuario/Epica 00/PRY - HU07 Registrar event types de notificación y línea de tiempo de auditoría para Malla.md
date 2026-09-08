# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-00 — Integración del módulo a la plataforma GRH
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Registrar event types de notificación y línea de tiempo de auditoría para Malla. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Registrar event types de notificación y línea de tiempo de auditoría para Malla |
| Id. Requerimiento | MT-EP00-HU07 |
| Id asociado | REQ-MT-07 / EP-00 |

### Descripción de historia de usuario

Como Super-administrador de la plataforma GRH  o equipo de plataforma, quiero registrar los tipos de evento de notificación y de línea de tiempo de auditoría que usará Malla, para reutilizar infraestructura de notificaciones de GRH y auditoría GRH sin mailers ni logs paralelos.

---

## Actores

- Inicia: Super-administrador de la plataforma GRH  o equipo de plataforma
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU01 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de registrar event types de notificación y línea de tiempo de auditoría para malla.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se consultan en el catálogo de notificaciones.
   - Sistema: Entonces existen los códigos definidos para publicación, cambio, novedad e intercambio.

Resultado esperado: Registrar event types de notificación y línea de tiempo de auditoría para Malla queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Registrar event types de notificación y línea de tiempo de auditoría para Malla» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Registro: dado que se despliegan los event types de Malla, cuando se consultan en el catálogo de notificaciones, entonces existen los códigos definidos para publicación, cambio, novedad e intercambio.
2. Publicación: dado que se publica una malla, cuando el flujo termina OK, entonces se despacha el evento de publicación a los destinatarios configurados.
3. Timeline: dado que ocurre un cambio relevante de celda o publicación, cuando se consulta línea de tiempo de auditoría, entonces existe el hecho de negocio correspondiente.
4. Idempotencia: dado que el mismo evento se reintenta con la misma clave, cuando se procesa el reintento, entonces no se duplica la notificación al destinatario.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Malla no envía correo directo; despacha eventos al servicio de notificaciones.
- RN-02: Los hechos de alto nivel van a línea de tiempo de auditoría; el detalle de celda vive en historial de dominio (HU62).
- RN-03: Los despachos deben ser idempotentes por clave de evento de negocio.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código de evento de notificación | 40 | Alfanumérico | SI | NO | SI | Identificador del tipo de evento |
| Nombre del evento | 120 | Alfanumérico | SI | NO | SI | Nombre visible del evento |
| Descripción del evento | N/A | Texto | NO | NO | SI | Detalle del evento de notificación |
| Activo | 1 | Booleano | SI | NO | SI | Indica si el evento está habilitado |


---

*Documento para cliente y diseño.*
