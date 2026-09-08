# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-09 — Intercambio de turnos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Aplicar intercambio, auditar y notificar. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Aplicar intercambio, auditar y notificar |
| Id. Requerimiento | MT-EP09-HU81 |
| Id asociado | REQ-MT-81 / EP-09 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero aplicar el intercambio aprobado sobre las celdas, registrar historial con origen intercambio y notificar a afectados, para cerrar el ciclo de forma trazable.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP09-HU80 |
| 2 | MT-EP05-HU62 |
| 3 | MT-EP00-HU07 |
| 4 | MT-EP02-HU39 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de aplicar intercambio, auditar y notificar.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando aplica.
   - Sistema: Entonces celdas intercambiadas.

Resultado esperado: Aplicar intercambio, auditar y notificar queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Aplicar intercambio, auditar y notificar» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Aplicar: dado que aprobada y válida, cuando aplica, entonces celdas intercambiadas.
2. Historial: dado que consulta, cuando ambas celdas, entonces eventos con solicitud.
3. Notificar: dado que ambos empleados, cuando reciben aviso, entonces sin aceptación adicional.
4. Falla parcial: dado que segunda celda conflicto versión, cuando rollback, entonces nada aplicado + error.
5. Idempotencia: dado que reintenta misma solicitud aplicada, cuando no duplica swap, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Aplicación atómica: ambas celdas o ninguna.
- RN-02: Historial referencia id de solicitud.
- RN-03: Origen=intercambio.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Solicitud aprobada | N/A | Selección | SI | SI | SI | Solicitud lista para aplicar |
| Confirmar aplicación | 1 | Booleano | SI | NO | SI | Aplica el intercambio y dispara auditoría/aviso |


---

*Documento para cliente y diseño.*
