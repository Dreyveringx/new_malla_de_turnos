# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-06 — Consulta operativa
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Buscar quién está en turno o disponible. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Buscar quién está en turno o disponible |
| Id. Requerimiento | MT-EP06-HU65 |
| Id asociado | REQ-MT-65 / EP-06 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de consulta operativa, quiero consultar qué personas están en turno o disponibles en una fecha/franja según filtros del frente, para atender operación en tiempo real.

---

## Actores

- Inicia: Usuario de la empresa con permiso de consulta operativa
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU14 |
| 2 | MT-EP00-HU03 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de buscar quién está en turno o disponible.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando consulta.
   - Sistema: Entonces lista resultados.

Resultado esperado: Buscar quién está en turno o disponible queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Buscar quién está en turno o disponible» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Búsqueda: dado que hay personas en turno en la franja, cuando consulta, entonces lista resultados.
2. Flag: dado que estado no disponible/no asignable, cuando consulta disponibilidad operativa, entonces no las incluye.
3. Filtros: dado que capacidades off, cuando UI, entonces no muestra filtros fantasma.
4. Tenant/alcance: dado que OK, cuando OK, entonces OK.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: ex-HU54 absorbida: la no asignabilidad a casos es un flag del estado.
- RN-02: Solo muestra frentes de su alcance.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Fecha | 10 | Fecha | SI | NO | SI | Día de la consulta |
| Hora (opcional) | 8 | Hora | NO | NO | SI | Momento puntual a consultar |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente de la búsqueda |
| Criterio (en turno / disponible) | 20 | Selección | SI | NO | SI | Tipo de búsqueda |
| Texto de búsqueda | 120 | Alfanumérico | NO | NO | SI | Nombre u otro filtro |


---

*Documento para cliente y diseño.*
