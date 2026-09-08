# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-01 — Parametrización de catálogos
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Parametrizar territorio con niveles configurables. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Parametrizar territorio con niveles configurables |
| Id. Requerimiento | MT-EP01-HU16 |
| Id asociado | REQ-MT-16 / EP-01 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de parametrización (o administrador de empresa con ese permiso), quiero definir la estructura territorial del frente con N niveles nombrados por configuración, para soportar jerarquías distintas sin fijar Regional/Zona/el territorio configurado en código.

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

1. El usuario entra a la función de parametrizar territorio con niveles configurables.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se crean nodos.
   - Sistema: Entonces la UI respeta esa jerarquía.

Resultado esperado: Parametrizar territorio con niveles configurables queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Parametrizar territorio con niveles configurables» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Niveles: dado que el frente habilita territorio con K niveles nombrados, cuando se crean nodos, entonces la UI respeta esa jerarquía.
2. Sin territorio: dado que capacidad deshabilitada, cuando se opera la malla, entonces no se exige territorio.
3. Tenant: dado que nodos de otra empresa, cuando lista, entonces no visibles.
4. Inactivo: dado que nodo inactivo, cuando asigna celda, entonces no se ofrece.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Los nombres de nivel son configuración, no enums de producto.
- RN-02: Solo visible si el frente habilita territorio.
- RN-03: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-04: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente dueño de la estructura territorial |
| Nombre del nivel | 80 | Alfanumérico | SI | NO | SI | Nombre configurable del nivel (ej. Zona) |
| Orden del nivel | 3 | Número | SI | NO | SI | Posición jerárquica del nivel |
| Código del nodo | 20 | Alfanumérico | SI | NO | SI | Código del nodo territorial |
| Nombre del nodo | 120 | Alfanumérico | SI | NO | SI | Nombre del nodo territorial |
| Nodo padre | N/A | Selección | NO | SI | SI | Padre en la jerarquía; vacío si es raíz |
| Activo | 1 | Booleano | SI | NO | SI | Indica si el nodo/nivel está activo |


---

*Documento para cliente y diseño.*
