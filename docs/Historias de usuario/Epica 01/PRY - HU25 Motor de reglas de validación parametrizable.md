# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Motor de reglas de validación parametrizable. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Motor de reglas de validación parametrizable |
| Id. Requerimiento | MT-EP01-HU25 |
| Id asociado | REQ-MT-25 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero administrar reglas de validación con código, alcance, parámetros, prioridad, severidad y estado, y evaluarlas al asignar o publicar, para centralizar solape, horas, cobertura, descanso, repetición, restricciones, anticipación e intercambio sin constantes en código.

---

## Actores

- Inicia: Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU10 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de motor de reglas de validación parametrizable.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando la malla supera N.
   - Sistema: Entonces se genera hallazgo con la severidad de la regla.

Resultado esperado: Motor de reglas de validación parametrizable queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Motor de reglas de validación parametrizable» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Horas máximas: dado que regla max_hours_period = N para el frente, cuando la malla supera N, entonces se genera hallazgo con la severidad de la regla.
2. Solape: dado que dos asignaciones se solapan en el tiempo para la misma persona, cuando se intenta guardar, entonces se bloquea.
3. Inactiva: dado que regla inactiva, cuando validación, entonces no aparece.
4. Alcance frente: dado que regla solo del frente A, cuando se valida malla del frente B, entonces no aplica.
5. Tenant: dado que reglas empresa A, cuando empresa B, entonces aisladas.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Invariante de dominio: solape horario real de la misma persona en el mismo instante es siempre bloqueo.
- RN-02: Horas máximas/mínimas, cobertura, repetición, celda vacía, anticipación, etc. son reglas parametrizables.
- RN-03: Regla inactiva no se evalúa.
- RN-04: Parámetros numéricos viven en la regla, nunca en el título de una HU ni en constantes de negocio en código.
- RN-05: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-06: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Código regla | 40 | Alfanumérico | SI | NO | SI | Identificador de la regla de validación |
| Nombre | 120 | Alfanumérico | SI | NO | SI | Nombre de la regla |
| Alcance | 20 | Selección | SI | NO | SI | Empresa o frente |
| Frente operativo | N/A | Selección | NO | SI | SI | Obligatorio si el alcance es frente |
| Valor del parámetro | 40 | Alfanumérico | NO | NO | SI | Parámetro editable (ej. máximo de horas) |
| Unidad del parámetro | 40 | Selección | NO | NO | SI | Unidad del parámetro |
| Severidad | 20 | Selección | SI | NO | SI | Info, advertencia o bloqueo |
| Prioridad | 5 | Número | NO | NO | SI | Orden de evaluación |
| Activo | 1 | Booleano | SI | NO | SI | Indica si la regla está activa |


---

*Documento para cliente y diseño.*
