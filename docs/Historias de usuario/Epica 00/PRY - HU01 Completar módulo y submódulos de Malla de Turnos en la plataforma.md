# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-00 — Integración del módulo a la plataforma GRH
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Completar módulo y submódulos de Malla de Turnos en la plataforma. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Completar módulo y submódulos de Malla de Turnos en la plataforma |
| Id. Requerimiento | MT-EP00-HU01 |
| Id asociado | REQ-MT-01 / EP-00 |

### Descripción de historia de usuario

Como Super-administrador de la plataforma GRH, quiero completar el módulo Malla de Turnos (ya existente en catálogo) con sus submódulos, rutas de menú y asociación a planes, para que las empresas con el módulo en su plan vean las secciones en el menú sin crear un módulo duplicado.

---

## Actores

- Inicia: Super-administrador de la plataforma GRH
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | Ver dependencias en el backlog definitivo del módulo |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de completar módulo y submódulos de malla de turnos en la plataforma.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando el Super-administrador registra o completa los submódulos y los asocia a un plan.
   - Sistema: Entonces no se crea un segundo módulo y el plan queda asociado al módulo existente.

Resultado esperado: Completar módulo y submódulos de Malla de Turnos en la plataforma queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Completar módulo y submódulos de Malla de Turnos en la plataforma» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Completar sin duplicar: dado que existe el módulo Malla de Turnos en el catálogo de plataforma, cuando el Super-administrador registra o completa los submódulos y los asocia a un plan, entonces no se crea un segundo módulo y el plan queda asociado al módulo existente.
2. Visibilidad por plan: dado que una empresa tiene plan activo con el módulo y un usuario con LEER en un submódulo, cuando el usuario inicia sesión, entonces ve las secciones habilitadas en el menú lateral.
3. Sin plan: dado que una empresa no tiene el módulo en su plan, cuando un usuario de esa empresa inicia sesión, entonces no ve Malla de Turnos en el menú.
4. Permisos: dado que solo el Super-administrador puede modificar el catálogo de módulos de plataforma, cuando un administrador de empresa intenta crear un módulo de plataforma, entonces la acción no está disponible.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: El módulo de plataforma se identifica en el catálogo existente; no se crea un módulo paralelo.
- RN-02: Los submódulos son secciones de menú con permisos CREAR/LEER/ACTUALIZAR/ELIMINAR.
- RN-03: La empresa solo ve el módulo si su plan activo lo incluye.
- RN-04: Los nombres de frentes operativos no son ítems del menú de plataforma.
- RN-05: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-06: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Nombre del módulo | 120 | Alfanumérico | SI | NO | SI | Nombre en catálogo de plataforma (Malla de Turnos) |
| Descripción del módulo | N/A | Texto | NO | NO | SI | Descripción del módulo en catálogo |
| Icono del módulo | 80 | Alfanumérico | NO | NO | SI | Clase de icono visible en menú |
| Nombre del submódulo / sección | 120 | Alfanumérico | SI | NO | SI | Nombre de la sección de menú |
| Descripción del submódulo | N/A | Texto | NO | NO | SI | Ayuda o tooltip de la sección |
| Icono del submódulo | 80 | Alfanumérico | NO | NO | SI | Clase de icono de la sección |
| Ruta de la sección | 200 | Alfanumérico | SI | NO | SI | Ruta de navegación asociada a la sección |
| Activo | 1 | Booleano | SI | NO | SI | Indica si el ítem está activo en catálogo |
| Plan de servicio | N/A | Selección | SI | SI | SI | Plan al que se asocia el módulo |


---

*Documento para cliente y diseño.*
