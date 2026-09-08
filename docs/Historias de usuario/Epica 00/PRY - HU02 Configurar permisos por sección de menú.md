# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-00 — Integración del módulo a la plataforma GRH
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Configurar permisos por sección de menú. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Configurar permisos por sección de menú |
| Id. Requerimiento | MT-EP00-HU02 |
| Id asociado | REQ-MT-02 / EP-00 |

### Descripción de historia de usuario

Como Administrador de empresa, quiero asignar a roles de mi empresa los permisos CREAR, LEER, ACTUALIZAR y ELIMINAR sobre las secciones de Malla de Turnos, para controlar quién parametriza, construye, publica, consulta o reporta sin inventar un sistema de seguridad paralelo.

---

## Actores

- Inicia: Administrador de empresa
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU01 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de configurar permisos por sección de menú.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando el administrador asigna LEER y ACTUALIZAR en Construcción.
   - Sistema: Entonces los usuarios con ese rol pueden abrir Construcción y modificar según ACTUALIZAR.

Resultado esperado: Configurar permisos por sección de menú queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Configurar permisos por sección de menú» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Asignar permisos: dado que existe un rol de empresa y submódulos de Malla, cuando el administrador asigna LEER y ACTUALIZAR en Construcción, entonces los usuarios con ese rol pueden abrir Construcción y modificar según ACTUALIZAR.
2. Denegación: dado que un usuario no tiene LEER en Reportes, cuando intenta acceder a Reportes, entonces el sistema niega el acceso.
3. Multiempresa: dado que dos empresas tienen roles con el mismo nombre, cuando se consultan permisos, entonces cada empresa solo ve y administra sus propios roles.
4. Sin inventar permisos: dado que se configura seguridad, cuando se listan permisos disponibles, entonces solo aparecen CREAR/LEER/ACTUALIZAR/ELIMINAR (no permisos inventados de frente).
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: Los únicos permisos de plataforma son CREAR, LEER, ACTUALIZAR y ELIMINAR por submódulo.
- RN-02: Los roles operativos (coordinador, supervisora, analista, etc.) son roles de la empresa, no enums del producto.
- RN-03: Sin LEER en la sección, el usuario no ve la opción de menú ni puede usar la función del sistema correspondiente.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Rol | N/A | Selección | SI | SI | SI | Rol de la empresa al que se asignan permisos |
| Sección de menú | N/A | Selección | SI | SI | SI | Sección de Malla de Turnos |
| Permiso crear | 1 | Booleano | SI | NO | SI | Habilita crear en la sección |
| Permiso leer | 1 | Booleano | SI | NO | SI | Habilita consultar en la sección |
| Permiso actualizar | 1 | Booleano | SI | NO | SI | Habilita actualizar en la sección |
| Permiso eliminar | 1 | Booleano | SI | NO | SI | Habilita eliminar en la sección |


---

*Documento para cliente y diseño.*
