# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-02 — Construcción de la malla
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Asignar turno o estado a una celda. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Asignar turno o estado a una celda |
| Id. Requerimiento | MT-EP02-HU30 |
| Id asociado | REQ-MT-30 / EP-02 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol), quiero asignar a una persona y fecha un turno y/o estado operativo según catálogos y reglas, para construir la programación celda a celda.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU11 |
| 2 | MT-EP01-HU14 |
| 3 | MT-EP01-HU25 |
| 4 | MT-EP02-HU39 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de asignar turno o estado a una celda.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando asigna plantilla activa.
   - Sistema: Entonces celda queda con turno y origen manual.

Resultado esperado: Asignar turno o estado a una celda queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Asignar turno o estado a una celda» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Asignar turno: dado que malla editable, cuando asigna plantilla activa, entonces celda queda con turno y origen manual.
2. Estado: dado que asigna estado del catálogo, cuando guarda, entonces aplica flags del estado.
3. Bloqueo regla: dado que violación con severidad bloqueo, cuando guarda, entonces rechaza y muestra motivo.
4. Advertencia: dado que severidad advertencia, cuando guarda con confirmación si aplica, entonces persiste y registra hallazgo.
5. Tenant/alcance: dado que malla fuera de empresa o frente, cuando edita, entonces niega.
6. Solo se muestran o modifican datos de la empresa del usuario autenticado.
7. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Celda = persona × fecha (+ turnos/estado + atributos habilitados).
- RN-02: Se evalúa el motor de reglas al guardar.
- RN-03: No se modifica jornada contractual.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Celda (persona y fecha) | N/A | Selección | SI | SI | SI | Celda de la grilla a editar |
| Plantilla de turno | N/A | Selección | NO | SI | SI | Turno a asignar (alternativa a estado) |
| Estado de celda | N/A | Selección | NO | SI | SI | Estado a asignar (alternativa a turno) |
| Motivo | N/A | Texto | NO | NO | SI | Obligatorio si el estado lo exige |


---

*Documento para cliente y diseño.*
