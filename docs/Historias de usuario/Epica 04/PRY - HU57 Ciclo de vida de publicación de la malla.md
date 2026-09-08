# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-04 — Publicación y ciclo de vida
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Ciclo de vida de publicación de la malla. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Ciclo de vida de publicación de la malla |
| Id. Requerimiento | MT-EP04-HU57 |
| Id asociado | REQ-MT-57 / EP-04 |

### Descripción de historia de usuario

Como Usuario de la empresa con permiso de publicación según configuración del frente, quiero mover la malla entre borrador, en revisión, publicada y rechazada según la configuración del frente, para controlar cuándo la programación es oficial.

---

## Actores

- Inicia: Usuario de la empresa con permiso de publicación según configuración del frente
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP01-HU10 |
| 2 | MT-EP03-HU45 |
| 3 | MT-EP00-HU07 |
| 4 | MT-EP05-HU63 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de ciclo de vida de publicación de la malla.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando publica.
   - Sistema: Entonces estado=Publicada y se notifica según HU07.

Resultado esperado: Ciclo de vida de publicación de la malla queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Ciclo de vida de publicación de la malla» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Publicar: dado que borrador sin bloqueos y usuario publicador, cuando publica, entonces estado=Publicada y se notifica según HU07.
2. Revisión: dado que separación activa, cuando constructor envía, entonces pasa a En revisión.
3. Advertencias: dado que flag permite y hay advertencias, cuando confirma, entonces publica registrando aceptación de advertencias.
4. Bloqueos: dado que hay bloqueos, cuando publica, entonces rechaza.
5. Permisos: dado que no publicador, cuando publica, entonces niega.
6. Tenant: dado que OK, cuando OK, entonces OK.
7. Solo se muestran o modifican datos de la empresa del usuario autenticado.
8. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Estados: Borrador, En revisión (si aplica), Publicada, Rechazada.
- RN-02: Si constructor/publicador está separado (HU10), el constructor solo envía a revisión.
- RN-03: No se publica con bloqueos; advertencias requieren confirmación solo si el frente lo permite.
- RN-04: ex-HU46 absorbida aquí + HU10.
- RN-05: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-06: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Malla | N/A | Selección | SI | SI | SI | Malla a cambiar de estado |
| Acción del ciclo | 20 | Selección | SI | NO | SI | Enviar a revisión, publicar, etc. |
| Comentario | N/A | Texto | NO | NO | SI | Nota del cambio de estado |


---

*Documento para cliente y diseño.*
