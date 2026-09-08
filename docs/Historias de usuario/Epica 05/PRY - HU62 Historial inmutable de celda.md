# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-05 — Novedades, cambios y auditoría
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Historial inmutable de celda. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Historial inmutable de celda |
| Id. Requerimiento | MT-EP05-HU62 |
| Id asociado | REQ-MT-62 / EP-05 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero registrar de forma append-only cada cambio de celda con antes, después, usuario, fecha, motivo y origen, para auditar la operación sin versionar toda la malla.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP02-HU30 |
| 2 | MT-EP00-HU07 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de historial inmutable de celda.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando guarda OK.
   - Sistema: Entonces existe evento con antes/después/usuario/origen.

Resultado esperado: Historial inmutable de celda queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Historial inmutable de celda» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Registro: dado que cambia celda, cuando guarda OK, entonces existe evento con antes/después/usuario/origen.
2. Inmutable: dado que intenta borrar historial, cuando acción, entonces no existe o se niega.
3. Origen intercambio: dado que cambio por HU81, cuando historial, entonces referencia solicitud.
4. Consulta: dado que usuario autorizado, cuando abre historial celda, entonces lista cronológica.
5. Tenant: dado que historial ajeno, cuando invisible, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: El historial de dominio es la fuente del detalle de celda.
- RN-02: Timeline GRH guarda hechos de alto nivel (HU07).
- RN-03: Inmutable: no update/delete de eventos de historial.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

Esta historia no captura datos propios de formulario. El alcance y la empresa provienen del contexto autenticado.


---

*Documento para cliente y diseño.*
