# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-02 — Construcción de la malla
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Seleccionar grupo de funcionarios de la malla. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Seleccionar grupo de funcionarios de la malla |
| Id. Requerimiento | MT-EP02-HU29 |
| Id asociado | REQ-MT-29 / EP-02 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol), quiero definir el conjunto de funcionarios que participan en la malla, para delimitar el universo de filas de la grilla.

---

## Actores

- Inicia: Usuario de la empresa con permiso de construcción de malla (coordinador/supervisora según rol)
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP02-HU28 |
| 2 | MT-EP00-HU08 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de seleccionar grupo de funcionarios de la malla.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando agrega funcionarios.
   - Sistema: Entonces aparecen como filas.

Resultado esperado: Seleccionar grupo de funcionarios de la malla queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Seleccionar grupo de funcionarios de la malla» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Agregar: dado que malla borrador, cuando agrega funcionarios, entonces aparecen como filas.
2. Quitar: dado que miembro sin celdas críticas o con política permitida, cuando se quita, entonces deja de listarse; historial de celdas previas se conserva.
3. Tenant: dado que empleado otra empresa, cuando agregar, entonces imposible.
4. Permisos: dado que sin ACTUALIZAR, cuando modifica grupo, entonces niega.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Solo empleados de la misma empresa.
- RN-02: Respetar filtros y paginación.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Malla | N/A | Selección | SI | SI | SI | Malla en construcción |
| Área / filtro de empleados | N/A | Selección | NO | SI | SI | Filtro para ubicar funcionarios |
| Funcionarios | N/A | Selección | SI | SI | SI | Personas incluidas en la malla |
| Orden de presentación | 5 | Número | NO | NO | SI | Orden de filas en la grilla |


---

*Documento para cliente y diseño.*
