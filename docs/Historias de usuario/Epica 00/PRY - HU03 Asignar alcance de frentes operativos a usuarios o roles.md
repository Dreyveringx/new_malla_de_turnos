# GST-FM-04 — Malla de Turnos

Nombre del proyecto: Malla de Turnos
Épica: EP-00 — Integración del módulo a la plataforma GRH
Audiencia: Cliente, diseño, negocio y pruebas funcionales

---

## Control de cambios

| Fecha | Versión | Descripción | Autor |
| ----- | ------- | ----------- | ----- |
| 05/09/2026 | 1.0 | Asignar alcance de frentes operativos a usuarios o roles. | Jair Uribe |

| Elaborado por | Fecha de elaboración | Fecha de entrega |
| ------------- | -------------------- | ---------------- |
| Jair Uribe | 05/09/2026 | Pendiente validación con negocio |

---

## Información general

| Campo | Valor |
| ----- | ----- |
| Nombre historia de usuario | Asignar alcance de frentes operativos a usuarios o roles |
| Id. Requerimiento | MT-EP00-HU03 |
| Id asociado | REQ-MT-03 / EP-00 |

### Descripción de historia de usuario

Como Administrador de empresa o usuario con permiso de parametrización, quiero definir qué frentes operativos puede ver u operar cada usuario o rol dentro de Malla, para aislar operaciones por frente sin modificar el modelo permisos de plataforma.

---

## Actores

- Inicia: Administrador de empresa o usuario con permiso de parametrización
- Participa: Otros roles según la historia
- No participa: Quienes no tienen permiso sobre la sección

---

## Historias de usuario asociadas

| Ítem | Nombre |
| ---- | ------ |
| 1 | MT-EP00-HU02 |
| 2 | MT-EP01-HU09 |

---

## Flujo básico

### Precondiciones

1. El módulo Malla de Turnos está habilitado para la empresa según su plan.
2. El usuario tiene el permiso de la sección correspondiente.
3. Cuando aplica, el frente operativo está configurado y dentro del alcance del usuario.

### Pasos

1. El usuario entra a la función de asignar alcance de frentes operativos a usuarios o roles.
   - Sistema: Muestra la información de su empresa y frentes autorizados.
2. Completa o confirma la acción descrita en la historia.
   - Sistema: Valida permisos, empresa y reglas aplicables.
3. Guarda o confirma el resultado.
   - Sistema: Persiste el cambio o muestra el resultado; deja trazabilidad cuando aplica.
4. Cuando se autoriza al usuario solo el frente A.
   - Sistema: Entonces en selectores y listados solo aparece A.

Resultado esperado: Asignar alcance de frentes operativos a usuarios o roles queda operativa, aislada por empresa y gobernada por configuración.

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

Pantalla o flujo de «Asignar alcance de frentes operativos a usuarios o roles» dentro del módulo Malla de Turnos.

1. Acceso desde el menú o acción contextual correspondiente
2. Solo datos de la empresa del usuario y frentes de su alcance
3. Mensajes de validación y confirmación claros

---

## Criterios de aceptación

1. Asignación: dado que existen frentes A y B en la empresa, cuando se autoriza al usuario solo el frente A, entonces en selectores y listados solo aparece A.
2. Intento fuera de alcance: dado que el usuario solo tiene frente A, cuando intenta abrir una malla del frente B por identificador, entonces el sistema rechaza por autorización.
3. Tenant: dado que el frente pertenece a otra empresa, cuando se intenta asignar alcance, entonces no aparece ni se puede asignar.
4. Auditoría: dado que se modifica el alcance de un usuario, cuando se guarda el cambio, entonces queda registro de quién cambió qué y cuándo.
5. Solo se muestran o modifican datos de la empresa del usuario autenticado.
6. El comportamiento que puede variar entre empresas o frentes depende de configuración, no de nombres fijos en el producto.

---

## Reglas de negocio

- RN-01: El alcance de frente es configuración del dominio Malla, no un permiso permisos de sección nuevo.
- RN-02: Un usuario solo opera frentes de su empresa y dentro de su alcance.
- RN-03: Si no tiene alcance asignado, no ve frentes (fail-closed) salvo rol con alcance total configurado explícitamente.
- RN-04: No se hardcodean frentes, turnos, estados, sitios, campañas, umbrales de horas ni reglas de compensatorio en el producto.
- RN-05: La empresa del usuario proviene del contexto autenticado; no se confía en un valor libre enviado solo desde pantalla.

---

## Datos de entrada

| Campo | Longitud | Tipo | Obligatorio | Sistema | Interfaz | Descripción |
| ----- | -------- | ---- | ----------- | ------- | -------- | ----------- |
| Usuario o rol | N/A | Selección | SI | SI | SI | Destinatario del alcance de frentes |
| Frente operativo | N/A | Selección | SI | SI | SI | Frente incluido en el alcance |
| Incluir en alcance | 1 | Booleano | SI | NO | SI | Asocia o retira el frente del alcance |


---

*Documento para cliente y diseño.*
