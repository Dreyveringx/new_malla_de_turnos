# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar reglas de compensatorio. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar reglas de compensatorio |
| Id. Requerimiento | MT-EP01-HU23 |
| Id asociado | REQ-MT-23 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero definir reglas que, ante umbrales y tipos de día configurables, sugieran o apliquen estados/acciones de compensatorio, para representar políticas distintas sin fijar cantidades de domingos u otros días en código.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU25 |
| 2 | MT-EP01-HU14 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de parametrizar reglas de compensatorio.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se evalúa.
   - Sistema: Entonces si se cumple, aplica la acción configurada.

Resultado esperado: Parametrizar reglas de compensatorio queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Parametrizar reglas de compensatorio» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Alta regla: dado que se configura umbral N sobre tipo de día D en ventana V, cuando se evalúa, entonces si se cumple, aplica la acción configurada.
2. Inactiva: dado que regla inactiva, cuando evaluación, entonces no se considera.
3. Por frente: dado que dos frentes con umbrales distintos, cuando se evalúa cada uno, entonces usa su propia regla.
4. Tenant: dado que otra empresa, cuando no ve reglas ajenas, entonces aislamiento OK.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Cualquier umbral numérico es parámetro de la regla.
- RN-02: La aplicación en reporte consume estas reglas (HU76).
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código regla | 40 | Alfanumérico | SI | NO | SI | Identificador de la regla de compensatorio |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre de la regla |
| Umbral / parámetro | 40 | Alfanumérico | SI | NO | SI | Valor configurable de la regla |
| Unidad | 40 | Selección | SI | NO | SI | Horas, días u otra unidad |
| Activo | 1 | Booleano | SI | NO | SI | Indica si la regla está activa |


---

*Documento para cliente y diseño.*
