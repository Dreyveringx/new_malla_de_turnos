# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-03 — Validación, cobertura y rotación
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Vincular patrón de rotación a grupo y periodo. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Vincular patrón de rotación a grupo y periodo |
| Id. Requerimiento | MT-EP03-HU47 |
| Id asociado | REQ-MT-47 / EP-03 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla, quiero asociar un patrón a una malla o subconjunto de personas y un rango de fechas, para preparar la simulación/aplicación controlada.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP03-HU46 |
| 2 | MT-EP01-HU10 |
| 3 | MT-EP02-HU29 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de vincular patrón de rotación a grupo y periodo.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando asocia a grupo/fechas.
   - Sistema: Entonces queda listo para simular.

Resultado esperado: Vincular patrón de rotación a grupo y periodo queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Vincular patrón de rotación a grupo y periodo» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Vínculo: dado que patrón activo y estrategia permite, cuando asocia a grupo/fechas, entonces queda listo para simular.
2. Estrategia manual: dado que frente manual, cuando intenta vincular auto, entonces acción no disponible.
3. Alcance: dado que personas fuera de malla, cuando asocia, entonces rechaza.
4. Tenant: dado que patrón otra empresa, cuando rechaza, entonces OK.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Solo si la estrategia del frente es asistida o automática.
- RN-02: El vínculo no modifica celdas hasta aplicar (HU50) tras simulación (HU48).
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Patrón de rotación | N/A | Selección | SI | SI | SI | Patrón a vincular |
| Malla / periodo | N/A | Selección | SI | SI | SI | Periodo destino |
| Grupo de funcionarios | N/A | Selección | SI | SI | SI | Personas incluidas en la rotación |
| Fecha de anclaje | 10 | Fecha | SI | NO | SI | Fecha desde la cual inicia el patrón |


---

*Documento para cliente y diseño.*
