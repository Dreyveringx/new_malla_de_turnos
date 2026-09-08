# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-09 — Intercambio de turnos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Habilitar y configurar solicitudes de intercambio. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Habilitar y configurar solicitudes de intercambio |
| Id. Requerimiento | MT-EP09-HU77 |
| Id asociado | REQ-MT-77 / EP-09 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización, quiero activar o desactivar solicitudes de intercambio por empresa/frente y definir anticipación, quién solicita, quién aprueba, límites y notificaciones, para gobernar el intercambio sin imponerlo a todos los frentes.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU10 |
| 2 | MT-EP00-HU02 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de habilitar y configurar solicitudes de intercambio.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando empleado ve su malla.
   - Sistema: Entonces sin acción de intercambio.

Resultado esperado: Habilitar y configurar solicitudes de intercambio queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Habilitar y configurar solicitudes de intercambio» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Off: dado que deshabilitado, cuando empleado ve su malla, entonces sin acción de intercambio.
2. On: dado que habilitado, cuando aparece acción, entonces según quién puede solicitar.
3. Anticipación: dado que parámetro N días, cuando solicitud fuera de N, entonces rechazada por regla.
4. Auditoría config: dado que cambia config, cuando historial config, entonces OK.
5. Tenant: dado que OK, cuando OK, entonces OK.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Default: deshabilitado.
- RN-02: Toda regla numérica es parámetro.
- RN-03: No cruza empresas.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente a configurar |
| Intercambio habilitado | 1 | Booleano | SI | NO | SI | Activa o desactiva solicitudes |
| Plazo máximo (horas) | 5 | Número | NO | NO | SI | Ventana para solicitar/aprobar |
| Requiere aprobación | 1 | Booleano | SI | NO | SI | Define si hay flujo de aprobación |
| Restricciones adicionales | N/A | Texto | NO | NO | SI | Condiciones configurables del frente |


---

*Documento para cliente y diseño.*
